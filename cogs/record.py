from discord.gateway import DiscordVoiceWebSocket
from discord import VoiceClient

MAX_SRC = 65535

class PacketQueue:
    def __init__(self):
        self.queues = defaultdict(list)

    def push(self, packet):
        self.queues[packet.ssrc].append(packet)

    def get_all_ssrc(self):
        return self.queues.keys()

    def get_packets(self, ssrc: int):
        last_seq = None
        packets = self.queues[ssrc]

        while packets:
            if last_seq is None:
                packet = packets.pop(0)
                last_seq = packet.seq
                yield packet
                continue

            if last_seq == MAX_SRC:
                last_seq = -1

            if packets[0].seq - 1 == last_seq:
                packet = packets.pop(0)
                last_seq = packet.seq
                yield packet
                continue

            # 順番がおかしかったときの場合
            for i in range(1, min(1000, len(packets))):
                if packets[i].seq - 1 == last_seq:
                    packet = packets.pop(0)
                    last_seq = packet.seq
                    yield packet
                    break
            else:
                #  該当するパケットがなかった場合、破損していたとみなす
                yield None

        # 終了
        yield -1


class BufferDecoder:
    def __init__(self):
        self.queue = PacketQueue()

    def recv_packet(self, packet):
        self.queue.push(packet)


class MyVoiceWebSocket(DiscordVoiceWebSocket):
    def __init__(self, socket, loop):
        super().__init__(socket, loop)
        self.record_ready = False

    async def received_message(self, msg):
        await super(MyVoiceWebSocket, self).received_message(msg)
        op = msg['op']

        if op == self.SESSION_DESCRIPTION:  # op 5
            self.record_ready = True


class RTCPacket:
    def __init__(self, header, decrypted):
        self.version = (header[0] & 0b11000000) >> 6
        self.padding = (header[0] & 0b00100000) >> 5
        self.extend = (header[0] & 0b00010000) >> 4
        self.cc = header[0] & 0b00001111
        self.marker = header[1] >> 7
        self.payload_type = header[1] & 0b01111111
        self.offset = 0
        self.ext_length = None
        self.ext_header = None
        self.csrcs = None
        self.profile = None
        self.real_time = None

        self.header = header
        self.decrypted = decrypted
        self.seq, self.timestamp, self.ssrc = struct.unpack_from('>HII', header, 2)
        
    def set_real_time(self):
        self.real_time = time.time()

    def calc_extension_header_length(self) -> None:
        if not (self.decrypted[0] == 0xbe and self.decrypted[1] == 0xde and len(self.decrypted) > 4):
            return
        self.ext_length = int.from_bytes(self.decrypted[2:4], "big")
        offset = 4
        for i in range(self.ext_length):
            byte_ = self.decrypted[offset]
            offset += 1
            if byte_ == 0:
                continue
            offset += 1 + (0b1111 & (byte_ >> 4))

        # Discordの仕様
        if self.decrypted[offset + 1] in [0, 2]:
            offset += 1
        self.decrypted = self.decrypted[offset + 1:]

class MyVoiceClient(VoiceClient):
    def __init__(self, client, channel):
        super().__init__(client, channel)
        self.record_task = None
        self.decoder = None

    async def recv_voice_packet(self):
        if not self.ws.record_ready:
            raise ValueError("Not Record Ready")

        while True:
            recv = await self.loop.sock_recv(self.socket, 2 ** 16)

    async def connect_websocket(self) -> MyVoiceWebSocket:
        ws = await MyVoiceWebSocket.from_client(self)
        self._connected.clear()
        while ws.secret_key is None:
            await ws.poll_event()
        self._connected.set()
        return ws

    def decrypt_xsalsa20_poly1305(self, data: bytes) -> tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted = data[:8], data[8:]
            nonce = bytearray(24)
            nonce[:8] = header
        else:
            header, encrypted = data[:12], data[12:]
            nonce = bytearray(24)
            nonce[:12] = header
        return header, box.decrypt(bytes(encrypted), bytes(nonce))

    def decrypt_xsalsa20_poly1305_suffix(self, data: bytes) -> tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted, nonce = data[:8], data[8:-24], data[-24:]
        else:
            header, encrypted, nonce = data[:12], data[12:-24], data[-24:]
        return header, box.decrypt(bytes(encrypted), bytes(nonce))

    def decrypt_xsalsa20_poly1305_lite(self, data: bytes) -> tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted, _nonce = data[:8], data[8:-4], data[-4:]
        else:
            header, encrypted, _nonce = data[:12], data[12:-4], data[-4:]
        nonce = bytearray(24)
        nonce[:4] = _nonce
        return header, box.decrypt(bytes(encrypted), bytes(nonce))

    async def recv_voice_packet(self):
        if not self.ws.record_ready:
            raise ValueError("Not Record Ready")

        while True:
            recv = await self.loop.sock_recv(self.socket, 2 ** 16)
            if 200 <= recv[1] < 205:
                continue
            decrypt_func = getattr(self, f'decrypt_{self.mode}')
            header, data = decrypt_func(recv)
            packet = RTCPacket(header, data)
            packet.set_real_time()
            packet.calc_extension_header_length()
            self.decoder.recv_packet(packet)

    async def record(self, record_time=30):
        if self.is_recording:
            raise ValueError("Already recording")

        # init
        self.decoder = None
        self.is_recording = True
        self.decoder = BufferDecoder()

        # do record
        self.record_task = self.loop.create_task(self.recv_voice_packet())
        await asyncio.sleep(record_time)

        self.record_task.cancel()

        # clear data
        self.record_task = None
        self.is_recording = False


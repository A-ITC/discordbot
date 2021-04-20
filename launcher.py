from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random
from discord.ext import tasks

class Timer:
    def __init__(self,year,month,day,hour,min,sec,span):
        self.begin_time=datetime.datetime(year,month,day,min,sec)
        self.span=span

class ITCBot(commands.Bot):
    def __init__( self,command_prefix,**options):
        self.voice_count=0
        self.timer_dat=[]#一日限り
        self.yobi_timer_dat=[]#決められた曜日で
        super().__init__(command_prefix=command_prefix,  **options)
    onAddTimer=[]
    def on_add_timer_event(self,func):
        self.onAddTimer.append(func)
    def invoke_add_timer(self):
        for eve in self.onAddTimer:
            eve()
    def add_timer(self,year,month,day,hour,min,sec,span):
    
        return
    
    
    # 任意のチャンネルで挨拶する非同期関数を定義
    async def greet(self):
        #channel = bot.get_channel(config.CHANNEL_ID)
        #if channel==None:
        #    print("error : get channel failed")
        return

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print("on_ready")

intents = discord.Intents.default()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False  # typingを受け取らないように
intents.members=True

print("build bot")
#botインスタンスの作成
bot = ITCBot(command_prefix=["!","！","/"],intents=intents)
bot.load_extension("cogs.add_role") 
bot.load_extension("cogs.client_app_info") 
bot.load_extension("cogs.count_members")
bot.load_extension("cogs.dice")
bot.load_extension("cogs.export_channel")
bot.load_extension("cogs.get_roles") 
bot.load_extension("cogs.info") 
bot.load_extension("cogs.join") 
bot.load_extension("cogs.member_list_up") 
bot.load_extension("cogs.reload") 
bot.load_extension("cogs.send") 
bot.load_extension("cogs.send2") 
bot.load_extension("cogs.set_timer") 
bot.load_extension("cogs.stop")
bot.load_extension("cogs.おみくじ")
bot.load_extension("cogs.ほめる")
bot.load_extension("cogs.メスガキ")
bot.load_extension("cogs.召喚")
bot.load_extension("cogs.天気")


@bot.event
async def on_message(message):
    try:
        if message.author.bot: # メッセージの送信者がBotなら何もしない
            return
        #print(message.reference)
        await bot.process_commands(message)
    except Exception as e:
        print(e)
    
@bot.event
async def on_disconnect():
    print("on_disconnect")

@bot.event
async def on_command_error(ctx, error):
    await ctx.reply(f"{error}")


@bot.event
async def on_voice_state_update(member,before,after):
    print("on voice update")
    count=0
    try:
        def check_channel(channel):
            #print(f"check channel {channel} {type(channel)}")
            return channel.type==discord.ChannelType.voice
        voiceChannels = list(filter(check_channel ,member.guild.channels))
        print(f"channel count : {len(voiceChannels)}")
        for channel in voiceChannels : count += len(channel.members)
        #if type(before.channel)==type(None) and type(after.channel)!=type(None):#以前にボイスチャンネルに入ってない
        #    print(f"on voice connected {count}")
        #    bot.voice_count+=1
        #if type(after.channel)==type(None):
        #    print(f"on voice disconnected {count}")
        #    bot.voice_count-=1
        #    if bot.voice_count<0:bot.voice_count=0
        if count==0:
            await bot.change_presence(activity=discord.Game(f""))
        else:
            await bot.change_presence(activity=discord.Game(f"現在{count}人が通話中"))
    except Exception as e:
        print(e)

import datetime
#https://qiita.com/higuratu/items/033e6fa655ee4b1d2ff0
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.datetime.now().strftime('%m:%d:%H:%M')
    index=0
    while index<len(bot.timer_dat):
        time= bot.timer_dat[index]
        if now == time[0]:
            channel = bot.get_channel(config.CHANNEL_ID)
            await channel.send(time[1])
            bot.timer_dat.pop(index)
            continue
        index+=1
import csv
import os

"""#中止
check_interval=60
@tasks.loop(seconds=check_interval)#30分に一回
async def check_online():
    print("check loop")
    print(f"{config.CHANNEL_ID}を探します")
    channel = bot.get_channel(config.CHANNEL_ID)
    print(channel)
    if type(channel)==type(None):
        print("error : get channel failed")
    else:
        await channel.send("30分タイマーテスト")

    now = datetime.datetime.now().strftime('%m/%d %H:%M:%S')
    print(now)
    print(bot.guilds)
    for guild in bot.guilds:
        check_online_guild(guild)
        
def check_online_guild(guild):
    filename=guild.name
    dir_path="data"
    path=dir_path+f"/{filename}.csv"
    data=read_csv(path)
    for role in guild.roles:
        if role.hoist:#そのロールが他のロールと分けて表示に設定されてたら
            if role.name not in data:
                data[role.name]=[]
            data[role.name].append(len(role.members))
    if not os.path.exists(dir_path):#
        print("ディレクトリがありません")
        os.mkdir(dir_path)
    print(f"{guild.name}について書き込みます")
    with open(path, 'w') as f:
        writer = csv.writer(f)
        headers=[]
        for i in data.keys():
            print(i)
            headers.append(i)
        writer.writerow(headers)#ヘッダーを記入
        output=[]
        for i in range(0,len(data["time"])):
            output.append([])
            output[i].append(data["time"][i])
        now=datetime.datetime.now().strftime('%m/%d %H:%M:%S')
        output.append([])
        output[-1].append(now)
        for v in data.values():
            count=0
            for i in v:
                output[count].append(i)
            count+=1
        for i in output:
            print(f"書き込む内容 {i}")
            writer.writerow(i)

def read_csv(path):
    data={"time":[]}
    headers=[]#最初の要素は時間
    if not os.path.exists(path):return data#ファイルがなかったらとばす
    with open(path, 'r') as f:
        print(f"既存のファイルが確認されました。{path}から読み込みます。")
        reader = csv.reader(f)
        is_header=False
        for row in reader:
            if not is_header:#最初の行（ヘッダー）
                is_header=True
                headers.extend(row)
                for header in headers:data[header]=[]
                continue
            if len(row)!=len(headers):
                print("フォーマットエラー")
                print(headers)
                print(row)
                break#rowのデータ数がヘッダ数とあってなかったら強制終了
            count=0
            for dat in row:
                data[headers[count]].append(dat)
                count+=1
        print(f"ヘッダー {headers}")
        return data
"""
#いったん中止
@bot.command()
async def count_cogs(ctx):
    cog_list=bot.cogs.values()
    sorted(cog_list)
        
    embed = discord.Embed(title="ロール一覧")
    # Embed の表示色を青色に設定
    embed.color = config.EMBED_COLOR
    for i in cog_list:
        embed.add_field(name=f"{i}", value=f"{bot.cogs[i].count}",inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def get_guilds(ctx):
    await ctx.send(bot.guilds)

print("start run")
#check_online.start()
bot.run(config.TOKEN)#Botのトークン
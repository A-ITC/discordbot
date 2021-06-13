from discord.ext import commands
import discord

class ITCBot(commands.Bot):
    def __init__( self,command_prefix,**options):
        super().__init__(command_prefix=command_prefix,  **options)
        self.voice_count=0
        #self.accounts=account.AccountManager()


    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print("on_ready")
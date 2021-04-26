from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 
import requests

"""
type
1 SUB_COMMAND
2 SUB_COMMAND_GROUP
3 STRING
4 INTEGER
5 BOOLEAN
6 USER
7 CHANNEL
8 ROLE
"""

json = {
    "name": "join",
    "description": "そのコマンドを実行した人と同じボイスチャンネルに入る",
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)

json = {
    "name": "banish",
    "description": "ボイスチャンネルから抜ける",
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)
#print(r.json())

class Join(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
        self.vc=None
        self.channel=None

    @commands.command()
    async def join(self, ctx ):
        self.count+=1
        voice_status=ctx.author.voice
        self.channel=voice_status.channel
        if type(voice_status)==type(None) or type(self.channel)==type(None):
            await ctx.reply("ボイスチャンネルに入っていません")
            return
        if self.channel.type!=discord.ChannelType.voice:
            await ctx.reply("ボイスチャンネルに入っていません")
            return
        self.vc = await self.channel.connect()
        await ctx.reply(f"ボイスチャンネル{self.channel.mention}に入りました")

    @commands.command()
    async def banish(self,ctx):
        await self.vc.disconnect()
        await ctx.reply(f"ボイスチャンネル{self.channel.mention}から切断します。")

def setup(bot):
    bot.add_cog(Join(bot))

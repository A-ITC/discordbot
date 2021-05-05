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

from glob import glob
import os
from discord.ext import commands
from typing import Dict


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
        voice_status=ctx.author.voice
        channel=voice_status.channel
        vc =self.get_vc(channel)
        if vc is None:
            await ctx.reply("エラー！")
            return
        await ctx.reply(f"ボイスチャンネル{channel.mention}から切断します。")
        await vc.disconnect()
        await ctx.send("切断完了しました")

    @commands.command()
    async def play_music(self, ctx: commands.Context, *, title: str = ''):
        voice_status=ctx.author.voice
        channel=voice_status.channel
        vc =self.get_vc(channel)
        if vc is None:
            await ctx.reply("error")
            return 
        music_pathes = glob('./music/**.mp3')
        music_pathes.extend( glob('./music/**.m4a'))
        music_titles = [
            os.path.basename(path).rstrip('.mp3m4a')
            for path in music_pathes
        ]
        if not title in music_titles:
            return await ctx.send('指定の曲はありません．')
        idx = music_titles.index(title)
        src = discord.FFmpegPCMAudio(music_pathes[idx],options ="-af volume=-10dB")
        vc.play(src)
        await ctx.send(f'{title}を再生します')

    @commands.command()
    async def stop_music(self, ctx: commands.Context):
        voice_status=ctx.author.voice
        channel=voice_status.channel
        vc =self.get_vc(channel)
        print("a")
        if type(vc) == type(None):
            await ctx.reply("error")
            return 
        if not vc.is_playing:
            await ctx.send('既に停止しています')
            return
        print("b")
        vc.stop()
        await ctx.send('停止しました')

    def get_vc(self,channel):
        for vc in self.bot.voice_clients:
            if vc.channel==channel:
                return vc
        return None


def setup(bot):
    bot.add_cog(Join(bot))

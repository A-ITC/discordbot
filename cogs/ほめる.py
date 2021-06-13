from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random
import requests

from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

texts=[
    "えらい！！！",
    "天才すぎ",
    "すごい！ほんとにすごい！！",
    "神じゃん…",
    "素晴らしい…もっと精進するといいでしょう。",
    "Awesome.",
    "👏👏👏👏",
    "ITCにこんなつよつよ人材いていいんですか",
    "最高だ！！！！！！！！！",
    "🎉🎉✨✨🎉🎉",
    "は～～～～～最高…",
    "よく頑張りましたね",
    "あなたは素晴らしい人材です",
    "ばなな",
    "つよつよじゃん",
    "ファミチキください",
    "GREAT WORKS!!!!!!!",
    "最強が服着てあるいてる！",
    "仕上がってるよ！",
    "チョベリグ"
    ]
class Encourage(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def ほめる(self,ctx,target:discord.Member=None):
        self.count+=1
        if target==None:
            target=ctx.author
        async with ctx.channel.typing():
            await ctx.reply(f"{target.mention} {random.choice(texts)}")
            
    @commands.command()
    async def ほめて(self,ctx,target:discord.Member=None):
        await self.ほめる(ctx,target)
    @commands.command()
    async def ほめろ(self,ctx,target:discord.Member=None):
        await self.ほめる(ctx,target)
                
    @cog_ext.cog_slash(name="ほめる",  description= "えらい！！！！！",options=[
            create_option(
                name="target",
                description="対象となるアカウント",
                option_type=6,
                required=False
            )
            ],guild_ids=config.guild_ids)
    async def _ほめる(self,ctx,target:discord.Member=None):
        self.count+=1
        if target==None:
            target=ctx.author
        async with ctx.channel.typing():
            await ctx.send(f"{target.mention} {random.choice(texts)}")
        
def setup(bot):
    bot.add_cog(Encourage(bot))
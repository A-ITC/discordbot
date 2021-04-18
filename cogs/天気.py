from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 

class Weather(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def 天気(self,ctx):
        self.count+=1
        texts=[
            "天気？分かりませんよそんなん",
            "晴か曇りか雨か雪かその他でしょう",
            "Coming soon!",
            "yahoo newsがおススメですよ！",
            "https://weathernews.jp/onebox/35.55/139.58/temp=c"
            ]
        async with ctx.channel.typing():
            await ctx.reply(random.choice(texts))

        
def setup(bot):
    bot.add_cog(Weather(bot))
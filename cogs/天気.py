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
            "烈日",
            "快晴",
            "蒼天",
            "雹",
            "霰",
            "霧",
            "疎雨",
            "晴れ",
            "曇り",
            "花曇り",
            "雨",
            "霧雨",
            "風雨",
            "晴嵐",
            "川霧",
            "台風",
            "雪",
            "凪",
            "黄砂",
            "梅雨",
            "極光",
            "ダイヤモンドダスト",
            "天気雨",
            "萃雨",
            "蜃気楼",
            "濃霧",
            "虹",
            ""
            ]
        async with ctx.channel.typing():
            await ctx.reply(f"{random.choice(texts)}かもしれません。")

        
def setup(bot):
    bot.add_cog(Weather(bot))
from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 

class Encourage(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def ほめる(self,ctx):
        self.count+=1
        texts=[
            "えらい！！！",
            "天才すぎ",
            "すごい！ほんとにすごい！！",
            "神じゃん…",
            "素晴らしい…もっと精進するといいでしょう。",
            "Awosome.",
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
            "仕上がってるよ！"
            ]
        async with ctx.channel.typing():
            await ctx.reply(random.choice(texts))

        
def setup(bot):
    bot.add_cog(Encourage(bot))
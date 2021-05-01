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
    "name": "ほめる",
    "description": "ほめる",
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json) 
#print(r.json())

class Encourage(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def ほめる(self,ctx,target:discord.Member=None):
        self.count+=1
        if target==None:
            target=ctx.author
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
        async with ctx.channel.typing():
            await ctx.reply(f"{target.mention} {random.choice(texts)}")
            
    @commands.command()
    async def ほめて(self,ctx,target:discord.Member=None):
        await self.ほめる(ctx,target)
    @commands.command()
    async def ほめろ(self,ctx,target:discord.Member=None):
        await self.ほめる(ctx,target)
        
def setup(bot):
    bot.add_cog(Encourage(bot))
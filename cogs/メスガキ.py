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
    "name": "メスガキ",
    "description": "メスガキがよ...",
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)
#print(r.json())

class Mesugaki(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def メスガキ(self,ctx):
        self.count+=1
        texts=[
            "ざ～こ❤",
            "よわよわ❤",
            "GPA低い🧡単位大丈夫だった？🧡",
            "進捗まだダメなの？💛💛",
            "ざこ❤ざこ❤ざこ❤",
            "生活リズム狂ってる❤",
            "社会性なし💛",
            "レポートまだ終わってないの？ざっこ🧡",
            "締め切り守れないんですか？❤",
            "がんばれ❤がんばれ❤",
            "え～？こんなことしてるなんて暇なんですね🧡",
            "読んだ本より積んでる本のが多いじゃん💛💛",
            "お前はいつもそうだ\n誰もお前を愛さない",
            "えっ…？",
            "ちょっ…やめてください",
            "体調管理しっかりしてくださいね❤",
            "お疲れ様です！"
            ]
        async with ctx.channel.typing():
            await ctx.reply(random.choice(texts))

        
def setup(bot):
    bot.add_cog(Mesugaki(bot))
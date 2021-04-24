from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 
import utility
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
    "name": "stop",
    "description": "Botを停止させる",
    "options": [
        {
            "name": "option",
            "description": "確認メッセージを表示させない",
            "type":3,
            "required": False,
        }
    ]
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)
#print(r.json())

class Stop(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.is_owner()
    @commands.command()
    async def stop(self,ctx,option=None):
        self.count+=1
        texts=[
            "ミ゜（絶命）",
            "Botを終了します。",
            "さよなら…さよなら…",
            "😴",
            "👋",
            "Bot has been stoped.",
            "Farewell, everyone",
            "Bot休止了",
            "死にたくない…死にたくない…",
            "Sleeping",
            "ぐあああああっ"
            ]
        try:
            if type(option)==type(None):
                stop_flag=await utility.yes_no(self.bot,ctx,"Botを停止させますか？")
                if stop_flag:
                    await ctx.reply(random.choice(texts))
                    await self.bot.close()
                else:
                    await ctx.reply("キャンセルします。")
            else:
                await ctx.reply(random.choice(texts))
                await self.bot.close()
        except asyncio.TimeoutError:
            await ctx.send(f"タイムアウトしました。")
        #await self.bot.logout()
        
def setup(bot):
    bot.add_cog(Stop(bot))
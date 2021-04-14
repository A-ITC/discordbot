from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 

class Stop(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.is_owner()
    @commands.command()
    async def stop(self,ctx):
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
        await ctx.reply(random.choice(texts))
        #await self.bot.logout()
        await self.bot.close()
        
def setup(bot):
    bot.add_cog(Stop(bot))
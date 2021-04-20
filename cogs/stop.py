from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 
import utility

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
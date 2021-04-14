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
        async with ctx.channel.typing():
            await ctx.reply("天気？分かりませんよそんなん")

        
def setup(bot):
    bot.add_cog(Weather(bot))
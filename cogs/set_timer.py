from discord.ext import commands
import discord
import config
import sys
import asyncio 
import datetime
import re
class SetTimer(commands.Cog):

    def __init__(self,bot):
        self.bot=bot
        self.count=0
        self.waiting_set_time=False
    @commands.command()
    async def set_timer(self,ctx):
        pass
    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        pass

def setup(bot):
    bot.add_cog(SetTimer(bot))
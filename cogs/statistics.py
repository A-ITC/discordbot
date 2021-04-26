from discord.ext import commands
import discord
import config
import sys
import asyncio 
import requests
import csv


class Statistics(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
        self.vc=None
        self.channel=None

    @commands.group()
    async def statistics(self, ctx ):
        self.count+=1
        if ctx.invoked_subcommand is None:
            await ctx.send('無効なコマンドです')

    @statistics.command()
    async def online(self,ctx):
        dir="data"
        path=f"{dir}/{ctx.guild.name}.csv"
        await ctx.send("ファイルを出力します",file=discord.File(path))

def setup(bot):
    bot.add_cog(Statistics(bot))

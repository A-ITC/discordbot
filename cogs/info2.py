from discord.ext import commands
import discord
import config
import sys
import asyncio 
import requests
import account
import zipfile
from glob import glob
from datetime import datetime, timedelta, timezone

class Info2(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def info2(self, ctx):
        pathes = glob('./accounts/**.json')
        JST = timezone(timedelta(hours=+9), 'JST')
        now=datetime.now(JST).strftime('%m-%d_%H-%M-%S')
        output_path=f'{now}_accountdata.zip'
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            for url in pathes:
                new_zip.write(url, arcname=url)
        await ctx.send("取得終了しました",file=discord.File(output_path))


def setup(bot):
    bot.add_cog(Info2(bot))
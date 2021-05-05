from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 
import csv
import os
import datetime
import requests
import utility
import zipfile
from datetime import datetime, timedelta, timezone

class TextData:
    def __init__(self,author,content,created_time,edited_time):
        self.author=author
        self.content=content
        self.created_time=created_time
        self.edited_time=edited_time

#未実装
class ExportImage(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def export_images(self, ctx ,channel_=None):
        self.count+=1
        channel=channel_
        if type(channel)is type(None):
            channel=ctx.channel
        else:
            channel=channel_.strip("<#>")
            channel=ctx.guild.get_channel(int(channel))
        await ctx.reply("履歴を取得中...")
        extention=["png","PNG","jpg","JPG"]
        dir_path="images"
        file_path=f"{dir_path}/{ctx.guild.name}_{ctx.channel.name}"
        file_urls=[]
        async for message in channel.history(limit=200):
            for attachment in message.attachments:
                filenames=attachment.filename.split(".")
                if filenames[-1] in extention:
                    save_name= f"{ctx.guild.name}_{ctx.channel.name}_{attachment.filename}"
                    utility.download_img(attachment.url,save_name)
                    file_urls.append(save_name)

        JST = timezone(timedelta(hours=+9), 'JST')
        now=datetime.now(JST).strftime('%m-%d_%H-%M-%S')
        output_path=f'data/{channel.id}_{now}.zip'
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            for url in file_urls:
                new_zip.write(url, arcname=url)
                os.remove(url)
        await ctx.send("取得終了しました",file=discord.File(output_path))

def setup(bot):
    bot.add_cog(ExportImage(bot))

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
import zipfile

class TextData:
    def __init__(self,author,content,created_time,edited_time):
        self.author=author
        self.content=content
        self.created_time=created_time
        self.edited_time=edited_time

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
        print(channel)
        await ctx.reply("履歴を取得中...")
        extention=["png","PNG","jpg","JPG"]
        dir_path="images"
        file_path=f"{dir_path}/{ctx.guild.name}_{ctx.channel.name}"

        async for message in channel.history(limit=200):
            for attachment in message.attachments:
                filenames=attachment.filename.split(".")
                if filenames[-1] in extention:
                    save_name= f"{ctx.guild.name}_{ctx.channel.name}_{attachment.filename}"
                    print(save_name)
                    download_img(attachment.url,save_name)

        with zipfile.ZipFile('data/temp/new_comp.zip', 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            new_zip.write('data/temp/test1.txt', arcname='test1.txt')
        await ctx.send("取得終了しました")

#https://qiita.com/mizunana/items/4afddc71f37df555078e
def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)
def setup(bot):
    bot.add_cog(ExportImage(bot))

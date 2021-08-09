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
    "name": "export_channel",
    "description": "対象のチャンネルのテキストをcsv形式で保存します",
    "options": [
        {
            "name": "channel",
            "description": "対象のチャンネル。指定しない場合、そのコマンドを入力したチャンネルが対象",
            "type": 7,
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

class TextData:
    def __init__(self,author,content,created_time,edited_time):
        self.author=author
        self.content=content
        self.created_time=created_time
        self.edited_time=edited_time

class ExportChannel(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def export_channel(self, ctx ,channel_=None):
        channel=channel_
        if type(channel)is type(None):
            channel=ctx.channel
        else:
            channel=channel_.strip("<#>")
            channel=ctx.guild.get_channel(int(channel))

        datas=[]
        print(channel)
        await ctx.reply("履歴を取得中...")
        async for message in channel.history(limit=200):
            datas.append(TextData(message.author,message.content,message.created_at,message.edited_at))
        dir_path="data"
        now=datetime.datetime.now().strftime('%m-%d %H-%M-%S')
        file_name=f"{ctx.guild.name}_{channel.name}_{now}.csv"
        path=f"{dir_path}/{file_name}"
        await ctx.send(f"履歴を取得しました。{file_name}に出力します")
        if not os.path.exists(dir_path):#
            print("ディレクトリがありません")
            os.mkdir(dir_path)
        with open(path, 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            for i in datas:
                row=[i.author,i.content,i.created_time,i.edited_time]
                writer.writerow(row)#ヘッダーを記入
        await ctx.send("ファイルを出力します",file=discord.File(path))
def setup(bot):
    bot.add_cog(ExportChannel(bot))

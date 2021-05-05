from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random
import traceback
from discord.ext import tasks
import csv
import os
from datetime import datetime, timedelta, timezone

#https://qiita.com/saira/items/e08c8849cea6c3b5eb0c
import sqlite3

dbname = 'TEST.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()
cur.execute("select * from sqlite_master where type='table'")
print(cur.fetchall())

# personsというtableを作成してみる
cur.execute('CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT,name STRING)')
cur.execute('INSERT INTO persons(name) values("Taro")')
# データベースへコミット。これで変更が反映される。
conn.commit()

# terminalで実行したSQL文と同じようにexecute()に書く
cur.execute('SELECT * FROM persons')

# 中身を全て取得するfetchall()を使って、printする。
print(cur.fetchall())
conn.close()

class ITCBot(commands.Bot):
    def __init__( self,command_prefix,**options):
        self.voice_count=0
        self.before_count=0
        super().__init__(command_prefix=command_prefix,  **options)

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print("on_ready")

intents = discord.Intents.default()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False  # typingを受け取らないように
intents.members=True
intents.presences =True

print("build bot")
#botインスタンスの作成
bot = ITCBot(command_prefix=["!","！","/"],intents=intents)
bot.load_extension("cogs.add_role") 
#bot.load_extension("cogs.client_app_info") 
bot.load_extension("cogs.count_members")
bot.load_extension("cogs.covid")
bot.load_extension("cogs.dice")
bot.load_extension("cogs.export_channel")
bot.load_extension("cogs.export_images")
bot.load_extension("cogs.get_roles") 
bot.load_extension("cogs.info") 
bot.load_extension("cogs.join") 
#bot.load_extension("cogs.move_messages") 
bot.load_extension("cogs.member_list_up") 
bot.load_extension("cogs.reload") 
bot.load_extension("cogs.send") 
bot.load_extension("cogs.statistics") 
bot.load_extension("cogs.status") 
bot.load_extension("cogs.stop")
bot.load_extension("cogs.おみくじ")
bot.load_extension("cogs.ほめる")
bot.load_extension("cogs.メスガキ")
bot.load_extension("cogs.召喚")
bot.load_extension("cogs.天気")

@bot.event
async def on_message(message):
    try:
        if message.author.bot:return # メッセージの送信者がBotなら何もしない
        if isinstance(message.channel,discord.channel.DMChannel):
            channel = bot.get_channel(config.PRIVATE_CHANNEL)
            mes=f"{message.author.mention}からのメッセージがDMから送られてきました。以下内容\n"
            mes+="=========================\n"
            mes+=message.content
            mes+="=========================\n"
            await channel.send(mes)
        await bot.process_commands(message)
    except Exception as e:
        print(e)
    
@bot.event
async def on_disconnect():
    print("on_disconnect")

@bot.event
async def on_command_error(ctx, error):
   # exc_type, exc_obj, exc_tb = sys.exc_info()
    #await ctx.reply(traceback.format_exc())
    await ctx.reply(error)

@bot.event
async def on_voice_state_update(member,before,after):
    print("on voice update")
    count=0
    try:
        def check_channel(channel):
            return channel.type==discord.ChannelType.voice
        voiceChannels = list(filter(check_channel ,member.guild.channels))
        print(f"channel count : {len(voiceChannels)}")
        for channel in voiceChannels : count += len(channel.members)
        bot.voice_count=count
        text=""
        if count!=0:text=f"{count}人の通話"
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    except Exception as e:
        print(e)

@bot.event
async def on_member_update(before, after):
    JST = timezone(timedelta(hours=+9), 'JST')
    now=datetime.now(JST).strftime('%y/%m/%d %H:%M:%S')
    print(now)
    print(before.name)
    print("before")
    print(f"mobile {before.mobile_status} desktop {before.desktop_status} web {before.web_status}")
    print("after")
    print(f"mobile {after.mobile_status} desktop {after.desktop_status} web {after.web_status}")

print("start run")
bot.run(config.TOKEN)#Botのトークン
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
import account
from datetime import datetime, timedelta, timezone

class ITCBot(commands.Bot):
    def __init__( self,command_prefix,**options):
        super().__init__(command_prefix=command_prefix,  **options)
        self.voice_count=0
        #self.accounts=account.AccountManager()

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
bot.load_extension("cogs.info2") 
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
#bot.load_extension("cogs.天気")

@bot.event
async def on_message(message):
    try:
        if message.author.bot:return # メッセージの送信者がBotなら何もしない
        if isinstance(message.channel,discord.channel.DMChannel):
            channel = bot.get_channel(config.PRIVATE_CHANNEL)
            mes=f"{message.author.mention}からのメッセージがDMから送られてきました。以下内容\n"
            mes+="=========================\n"
            mes+=message.content
            mes+="\n=========================\n"
            await channel.send(mes)
        #bot.accounts.on_message(message)
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
        text=""
        if count!=0:text=f"{count}人の通話"
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
        #bot.accounts.on_voice_update(member, before, after)
    except Exception as e:
        print(e)

@bot.event
async def on_member_update(before, after):
    JST = timezone(timedelta(hours=+9), 'JST')
    now=datetime.now(JST)
    #print(now.strftime('%y/%m/%d %H:%M:%S'))
    #print(before.name)
    #print("before")
    #print(f"mobile {before.mobile_status} desktop {before.desktop_status} web {before.web_status}")
    #print("after")
    #print(f"mobile {after.mobile_status} desktop {after.desktop_status} web {after.web_status}")
    #bot.accounts.on_status_update(before,after)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(config.REMOVE_NOTION)
    roles=""
    for role in member.roles:
        roles+=role.mention+"\n"
    await channel.send(f"{member.mention} {member.name}が脱退しました。\n{roles}")

print("start run")
bot.run(config.TOKEN)#Botのトークン

import message
check_interval=60*60*12 #秒*分*時間
@tasks.loop(seconds=check_interval)#30分に一回
async def check_atcoder():
    message.check_atcoder()
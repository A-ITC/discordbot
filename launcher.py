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
import ITCBot

intents = discord.Intents.default()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False  # typingを受け取らないように
intents.members=True
intents.presences =True

print("build bot")
#botインスタンスの作成
bot = ITCBot.ITCBot(command_prefix=["!","！","/"],intents=intents)
from discord_slash import SlashCommand # Importing the newly installed library.

slash = SlashCommand(bot, sync_commands=True, override_type=True) # Declares slash commands through the client.

bot.load_extension("cogs.add_role") 
bot.load_extension("cogs.count_members")
bot.load_extension("cogs.covid")
bot.load_extension("cogs.dice")
bot.load_extension("cogs.export_channel")
bot.load_extension("cogs.export_images")
bot.load_extension("cogs.get_roles") 
bot.load_extension("cogs.info") 
bot.load_extension("cogs.join") 
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
        await bot.process_commands(message)
    except Exception as e:
        print(e)
    
@bot.event
async def on_disconnect():
    print("on_disconnect")

@bot.event
async def on_command_error(ctx, error):
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
async def on_member_remove(member):
    channel = bot.get_channel(config.REMOVE_NOTION)
    roles=""
    for role in member.roles:
        roles+=role.mention+"\n"
    await channel.send(f"{member.mention} {member.name}が脱退しました。\n{roles}")


@bot.event
async def on_slash_command_error(ctx, ex):
    await ctx.send(str(ex))

print("start run")
bot.run(config.TOKEN)#Botのトークン

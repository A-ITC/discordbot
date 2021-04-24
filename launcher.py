from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random
from discord.ext import tasks
class ITCBot(commands.Bot):
    def __init__( self,command_prefix,**options):
        self.voice_count=0
        self.before_count=0
        super().__init__(command_prefix=command_prefix,  **options)

    # 任意のチャンネルで挨拶する非同期関数を定義
    async def greet(self):
        #channel = bot.get_channel(config.CHANNEL_ID)
        #if channel==None:
        #    print("error : get channel failed")
        return

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print("on_ready")

intents = discord.Intents.default()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False  # typingを受け取らないように
intents.members=True

print("build bot")
#botインスタンスの作成
bot = ITCBot(command_prefix=["!","！","/"],intents=intents)
bot.load_extension("cogs.add_role") 
bot.load_extension("cogs.client_app_info") 
bot.load_extension("cogs.count_members")
bot.load_extension("cogs.dice")
bot.load_extension("cogs.export_channel")
bot.load_extension("cogs.export_images")
bot.load_extension("cogs.get_roles") 
bot.load_extension("cogs.info") 
bot.load_extension("cogs.join") 
bot.load_extension("cogs.member_list_up") 
bot.load_extension("cogs.reload") 
bot.load_extension("cogs.send") 
bot.load_extension("cogs.stop")
bot.load_extension("cogs.おみくじ")
bot.load_extension("cogs.ほめる")
bot.load_extension("cogs.メスガキ")
bot.load_extension("cogs.召喚")
bot.load_extension("cogs.天気")


@bot.event
async def on_message(message):
    try:
        if message.author.bot: # メッセージの送信者がBotなら何もしない
            return
        #print(message.reference)
        await bot.process_commands(message)
    except Exception as e:
        print(e)
    
@bot.event
async def on_disconnect():
    print("on_disconnect")

@bot.event
async def on_command_error(ctx, error):
    await ctx.reply(f"{error}")

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
        print(f"{count}人")
        bot.voice_count=count
        if count==0:
            await bot.change_presence(activity=discord.Game(f""))
        else:
            await bot.change_presence(activity=discord.Game(f"現在{count}人が通話中"))
    except Exception as e:
        print(e)


@bot.command()
async def get_guilds(ctx):
    await ctx.send(bot.guilds)

print("start run")
bot.run(config.TOKEN)#Botのトークン
from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random
from discord.ext import tasks

class Timer:
    def __init__(self,year,month,day,hour,min,sec,span):
        self.begin_time=datetime(year,month,day,min,sec)
        self.span=span

class ITCBot(commands.Bot):
    def __init__( self,command_prefix,**options):
        self.voice_count=0
        self.timer_dat=[]#一日限り
        self.yobi_timer_dat=[]#決められた曜日で
        super().__init__(command_prefix=command_prefix,  **options)
    onAddTimer=[]
    def on_add_timer_event(self,func):
        self.onAddTimer.append(func)
    def invoke_add_timer(self):
        for eve in self.onAddTimer:
            eve()
    def add_timer(self,year,month,day,hour,min,sec,span):
    
        return
    
    
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
bot.load_extension("cogs.get_roles") 
bot.load_extension("cogs.guild_info") 
bot.load_extension("cogs.hello") 
bot.load_extension("cogs.info") 
bot.load_extension("cogs.man")
bot.load_extension("cogs.member_list_up") 
bot.load_extension("cogs.reload") 
bot.load_extension("cogs.send") 
bot.load_extension("cogs.set_timer") 
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
        print(message.reference)
        #elif "Kyoichi" in message.content or "kyoichi" in message.content :
        #    await message.channel.send(" はい、Kyoichi です ")
    except Exception as e:
        print(e)
    await bot.process_commands(message)
    
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
            #print(f"check channel {channel} {type(channel)}")
            return channel.type==discord.ChannelType.voice
        voiceChannels = list(filter(check_channel ,member.guild.channels))
        print(f"channel count : {len(voiceChannels)}")
        for channel in voiceChannels : count += len(channel.members)
        #if type(before.channel)==type(None) and type(after.channel)!=type(None):#以前にボイスチャンネルに入ってない
        #    print(f"on voice connected {count}")
        #    bot.voice_count+=1
        #if type(after.channel)==type(None):
        #    print(f"on voice disconnected {count}")
        #    bot.voice_count-=1
        #    if bot.voice_count<0:bot.voice_count=0
        if count==0:
            await bot.change_presence(activity=discord.Game(f""))
        else:
            await bot.change_presence(activity=discord.Game(f"現在{count}人が通話中"))
    except Exception as e:
        print(e)


#https://qiita.com/higuratu/items/033e6fa655ee4b1d2ff0
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%m:%d:%H:%M')
    index=0
    while index<len(bot.timer_dat):
        time= bot.timer_dat[index]
        if now == time[0]:
            channel = bot.get_channel(config.CHANNEL_ID)
            await channel.send(time[1])
            bot.timer_dat.pop(index)
            continue
        index+=1

#いったん中止
@bot.command()
async def count_cogs(ctx):
    cog_list=bot.cogs.values()
    sorted(cog_list)
        
    embed = discord.Embed(title="ロール一覧")
    # Embed の表示色を青色に設定
    embed.color = config.EMBED_COLOR
    for i in cog_list:
        embed.add_field(name=f"{i}", value=f"{bot.cogs[i].count}",inline=False)
    await ctx.send(embed=embed)

print("start run")
bot.run(config.TOKEN)#Botのトークン
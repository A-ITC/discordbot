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
intents.presences =True
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
bot.load_extension("cogs.statistics") 
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

import csv
import os
from datetime import datetime, timedelta, timezone
check_interval=60*30
@tasks.loop(seconds=check_interval)#30分に一回
async def check_online():
    print("check loop")
    for guild in bot.guilds:
        check_online_guild(guild)
        
def check_online_guild(guild):
    filename=guild.name
    dir_path="data"
    path=f"{dir_path}/{filename}.csv"
    data=read_csv(path)
    nrow=len(data["time"])#データの行数
    for role in guild.roles:
        if role.hoist:#そのロールが他のロールと分けて表示に設定されてたら
            if role.name not in data:#新しくロールが作られた場合
                data[role.name]=["" for i in range(nrow)]
            online_count=0
            for member in role.members:
                if member.status == discord.Status.online:online_count+=1
            data[role.name].append(online_count)
    JST = timezone(timedelta(hours=+9), 'JST')
    now=datetime.now(JST).strftime('%m/%d %H:%M:%S')
    data["time"].append(now)
    if not os.path.exists(dir_path):#
        print("ディレクトリがありません")
        os.mkdir(dir_path)
    print(f"{guild.name}について書き込みます")
    write_csv(path,data)

def read_csv(path):
    data={"time":[]}
    headers=[]#最初の要素は時間
    if not os.path.exists(path):return data#ファイルがなかったらとばす
    with open(path, 'r', encoding='utf-8') as f:
        print(f"既存のファイルが確認されました。{path}から読み込みます。")
        reader = csv.reader(f)
        is_header=False
        for row in reader:
            if not is_header:#最初の行（ヘッダー）
                is_header=True
                headers.extend(row)
                for header in headers:data[header]=[]
                continue
            if len(row)!=len(headers):
                print("フォーマットエラー")
                print(headers)
                print(row)
                break#rowのデータ数がヘッダ数とあってなかったら強制終了
            count=0
            for dat in row:
                data[headers[count]].append(dat)
                count+=1
        print(f"ヘッダー {headers}")
        return data

def write_csv(path,data):
    with open(path, 'w', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        headers=["time"]#ヘッダーの最初はtimeがくるように
        for i in data.keys():#ヘッダーに各ロール名を登録
            if i =="time":continue
            headers.append(i)
        writer.writerow(headers)#ヘッダーを記入
        output=[]
        nrow=len(data["time"])#データの行数
        for i in range(nrow):
            output.append([ data["time"][i] ])#最初の列はtimeに
        for v in data.keys():
            if v=="time":continue
            for i in range(nrow):
                output[i].append(data[v][i])
        for i in output:
            writer.writerow(i)

check_online.start()
print("start run")
bot.run(config.TOKEN)#Botのトークン
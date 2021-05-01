
import datetime
#https://qiita.com/higuratu/items/033e6fa655ee4b1d2ff0
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.datetime.now().strftime('%m:%d:%H:%M')
    index=0
    while index<len(bot.timer_dat):
        time= bot.timer_dat[index]
        if now == time[0]:
            channel = bot.get_channel(config.CHANNEL_ID)
            await channel.send(time[1])
            bot.timer_dat.pop(index)
            continue
        index+=1
import csv
import os
#中止


@tasks.loop(seconds=180)#1分に一回
async def change_avatar_timer():
    print("check avatar")
    try:
        if bot.voice_count!=bot.before_count:
            bot.before_count=bot.voice_count
            await asyncio.wait_for(change_avatar(), timeout=10.0)
    except Exception as e:
        print(e)

async def change_avatar():
    print("change avatar")
    try:
        for i in range(0,6):
            if bot.voice_count<=i:
                with open(f'image/ITC-icon-{i}.png', 'rb') as image:
                    await bot.user.edit(avatar=image.read())
                    print("change avatar finished")
                return
    except Exception as e:
        print(e)
change_avatar_timer.start()



import csv
import os
from datetime import datetime, timedelta, timezone
check_interval=60*20
@tasks.loop(seconds=check_interval)#30分に一回
async def check_online():
    try:
        print("check loop")
        for guild in bot.guilds:
            check_online_guild(guild)
    except Exception as e:
        print(e)
        
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

#check_online.start()

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
check_interval=60
@tasks.loop(seconds=check_interval)#30分に一回
async def check_online():
    print("check loop")
    print(f"{config.CHANNEL_ID}を探します")
    channel = bot.get_channel(config.CHANNEL_ID)
    print(channel)
    if type(channel)==type(None):
        print("error : get channel failed")
    else:
        await channel.send("30分タイマーテスト")

    now = datetime.datetime.now().strftime('%m/%d %H:%M:%S')
    print(now)
    print(bot.guilds)
    for guild in bot.guilds:
        check_online_guild(guild)
        
def check_online_guild(guild):
    filename=guild.name
    dir_path="data"
    path=dir_path+f"/{filename}.csv"
    data=read_csv(path)
    for role in guild.roles:
        if role.hoist:#そのロールが他のロールと分けて表示に設定されてたら
            if role.name not in data:
                data[role.name]=[]
            data[role.name].append(len(role.members))
    if not os.path.exists(dir_path):#
        print("ディレクトリがありません")
        os.mkdir(dir_path)
    print(f"{guild.name}について書き込みます")
    with open(path, 'w') as f:
        writer = csv.writer(f)
        headers=[]
        for i in data.keys():
            print(i)
            headers.append(i)
        writer.writerow(headers)#ヘッダーを記入
        output=[]
        for i in range(0,len(data["time"])):
            output.append([])
            output[i].append(data["time"][i])
        now=datetime.datetime.now().strftime('%m/%d %H:%M:%S')
        output.append([])
        output[-1].append(now)
        for v in data.values():
            count=0
            for i in v:
                output[count].append(i)
            count+=1
        for i in output:
            print(f"書き込む内容 {i}")
            writer.writerow(i)

def read_csv(path):
    data={"time":[]}
    headers=[]#最初の要素は時間
    if not os.path.exists(path):return data#ファイルがなかったらとばす
    with open(path, 'r') as f:
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
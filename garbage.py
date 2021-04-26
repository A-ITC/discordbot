
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
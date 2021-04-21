from discord.ext import commands
import discord
import config
import sys
import asyncio 
import datetime
import re


#今日と曜日が与えられて、今日からみて初めてその曜日になる日を返す
#yobi_num 0が月曜日 6が日曜日
def yobi_begin(today,yobi_num):
    weekday=today.weekday()
    if yobi_num<weekday:#対象の曜日が今日よりも前なら
        return today+datetime.timedelta(yobi_num-weekday+7)
    return today+datetime.timedelta(yobi_num-weekday)
#曜日から漢字へ
#0が月曜日
def convert_yobi(yobi_num):
    if yobi_num<0:return "?"
    kanji=["月","火","水","木","金","土","日"]
    return kanji[yobi_num]

class SetTimer2(commands.Cog):

    def __init__(self,bot):
        self.bot=bot
        self.count=0
        self.target_person=None#コマンドを売ってきた人しか受け付けない
        self.waiting_set_time=False#時間の入力を受け付けているか
        self.waiting_set_day=False#日付の入力を受け付けているか
        self.hour=0
        self.min=0
        self.month=0
        self.day=0
        self.timers=TimerList()

    @commands.command()
    async def set_timer2(self,ctx):
        self.count+=1
        self.waiting_set_time=False
        self.target_person=ctx.author
        self.dates=[]
        
        sent_msg = await ctx.reply(
        f"日にちと時刻に合わせてタイマーをセットすることができます。まずは時刻を指定してください。"
        )
        #===========================================================================================
        #時刻の入力待ち
        #===========================================================================================
        self.waiting_set_time=True
        while self.waiting_set_time:
            await asyncio.sleep(0.3)

        embed = discord.Embed(title="Timer")
        embed.color = discord.Color.blue()
        embed.add_field(name="1", value="日にちで直接指定")
        embed.add_field(name="2", value="曜日で指定（毎週定期的に）")
        sent_msg = await ctx.reply(
            f"日付はどうしますか？番号を教えてください。\n"
            f"キャンセルするときは❌とリアクションしてください。"
            ,embed=embed)
        await sent_msg.add_reaction("1️⃣")
        await sent_msg.add_reaction("2️⃣")
        await sent_msg.add_reaction("❌")

        #https://qiita.com/coolwind0202/items/12951aba312e0d13afae
        def reaction_check(reaction_, user_):
            is_author=user_==ctx.author
            are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
            is_ok=  are_same_messages and is_author
            return is_ok
        emoji = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
        if emoji[0].emoji=="1️⃣":#日付でセット
            await self.set_with_day(ctx)
        elif emoji[0].emoji=="2️⃣":#曜日でセット
            while True:
                retryFlag=await self.set_with_yobi(ctx)
                if not retryFlag:
                    break
        elif emoji[0].emoji=="❌":
            await ctx.send("キャンセルします")
            return
        
        #==================================================================================================
        #入力の最終確認
        #==================================================================================================
        text=""
        for i in self.dates:
            text+=f"{i.year}年{i.month}月{i.day}日({convert_yobi(i.weekday)})　{self.hour}時{self.min}分\n"
        text+="にセットします。よろしいですか？"
        sent_msg=await ctx.send(text)
        await sent_msg.add_reaction("✅")
        await sent_msg.add_reaction("❌")
        def reaction_check5(reaction_, user_):
            is_author=user_==ctx.author
            are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
            return are_same_messages and is_author
        #チェック関数に合格するようなメッセージを待つ
        emoji = await self.bot.wait_for('reaction_add', check=reaction_check5, timeout=180)
        if emoji[0].emoji=="✅":
            await ctx.send("曜日をセットしました。")
            for i in self.dates:
                self.bot.add_timer(i.year,i.month,i.day,self.hour,self.min,0,-1)
        elif emoji[0].emoji=="❌":
            await ctx.send("キャンセルします。")


    async def set_with_day(self,ctx):
        self.waiting_set_day=True
        sent_msg=await ctx.send(
            f"日にちで指定します。\n"
            f"何日にしますか？今日なら1️⃣、明日なら2️⃣とリアクションすることで指定できます。\n"
            f"日付を入力する場合、0️⃣とリアクションしてください。"
            )
        await sent_msg.add_reaction("0️⃣")
        await sent_msg.add_reaction("1️⃣")
        await sent_msg.add_reaction("2️⃣")
        await sent_msg.add_reaction("❌")
        def reaction_check(reaction_, user_):
            is_author=user_==ctx.author
            are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
            return are_same_messages and is_author
        emoji = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
        if emoji[0].emoji=="0️⃣":
            await ctx.send("日付の入力待ちをします。??月??日と入力してください。（例 12月30日）")
            while self.waiting_set_day:
                await asyncio.sleep(0.3)
        if emoji[0].emoji=="1️⃣":
            await ctx.send("タイマーを今日にセットします。")
            today= datetime.date.today()
            self.dates.append(TimerList.BeginDate(today.year,today.month,today.day,today.weekday()))
        if emoji[0].emoji=="2️⃣":
            await ctx.send("タイマーを明日にセットします。")
            today= datetime.date.today()+datetime.timedelta(days = 1)
            self.dates.append(TimerList.BeginDate(today.year,today.month,today.day,today.weekday()))
        if emoji[0].emoji=="❌":
            await ctx.send("キャンセルします。")

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if message.author != self.target_person:return#コマンドを入力してきた本人なら
        if  self.waiting_set_time: #時間のセットを待っていれば
            self.waiting_set_time=False
            print(message.content)
            times=message.content.split(":")
            if len(times)<2:
                await message.reply("エラー！不正な時刻です。もう一度最初からやり直してください。")
                return
            hour=int(times[0])
            min=int(times[1])
            if hour<0 or hour>=60 or min <0 or min>=60:
                await message.reply("エラー！不正な時刻です。もう一度最初からやり直してください。")
                return
            self.hour=hour
            self.min=min
            return
        #====================================================================================
        #日付入力待ち
        #====================================================================================
        if self.waiting_set_day:
            self.waiting_set_day=False
            month=re.findall(r'\d+月', message.content)
            month=int(month[:-1])
            day=re.findall(r'\d+日', message.content)
            day=int(day[:-1])
            if month<=0 or month>12 or day<=0 or day>=31:
                await message.reply("エラー！不正な日付です。もう一度最初からやり直してください。")
                return
            self.month=month
            self.day=day
        return True,""

class YobiSetter:
    def __init__(self,bot,ctx):
        self.bot=bot
        self.ctx=ctx

    async def set_with_yobi(self):#day of the week もしくは weekday は長い
        selected=[False,False,False,False,False,False,False]
        yobi=["月","火","水","木","金","土","日"]
        yobi_emoji=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","☀"]
        sent_msg=await self.ctx.send(
            f"曜日で指定します。（毎週）\n"
            f"何曜日にするかリアクションで指定をお願いします。\n"
            f"{''.join(yobi_emoji)}で{''.join(yobi)}の順番です。決定する際は✅をお願いします。"
            )
        for emj in yobi_emoji:
            await sent_msg.add_reaction(emj)
        await sent_msg.add_reaction("✅")
        await sent_msg.add_reaction("❌")
        while True:#✅❌が押されるまでループ
            def reaction_check2(reaction_, user_):
                is_author=user_==self.ctx.author
                are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                return are_same_messages and is_author
            #チェック関数に合格するようなメッセージを待つ
            emoji = await self.bot.wait_for('reaction_add', check=reaction_check2, timeout=180)
            for i in range(len(yobi_emoji)):#各曜日についてチェック
                if emoji[0].emoji==yobi_emoji[i]:
                    selected[i]=True

            if emoji[0].emoji=="✅":
                #なぜかMessage.reactionsを取得できない
                #for i in sent_msg.reactions:
                #    print(i.emoji)

                msg=""
                for i in range(len(selected)):
                    if selected[i]:
                        msg+=f"{yobi[i]}曜日と"
                sent_msg=await self.ctx.send(f"選択したのは{msg[:-1]}でよろしいですか？")
                await sent_msg.add_reaction("✅")
                await sent_msg.add_reaction("♻")
                await sent_msg.add_reaction("❌")
                def reaction_check(reaction_, user_):
                    is_author=user_==self.ctx.author
                    are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                    return are_same_messages and is_author
                emoji = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
                if emoji[0].emoji=="✅":
                    today= datetime.date.today()
                    for i in range(len(selected)):
                        if selected[i]:
                            day=yobi_begin(today,i)
                            self.timers.add_day(day.year,day.month,day.day,day.weekday())
                    await self.ctx.send("曜日をセットしました。")
                    return False
                elif emoji[0].emoji=="♻":
                    await self.ctx.send("曜日を選択しなおしてください。")
                    return True
                elif emoji[0].emoji=="❌":
                    return False
            elif emoji[0].emoji=="❌":
                return False



class TimerList:
    class BeginDate:
        def __init__(self,year,month,day,weekday=-1):
            self.year=year
            self.month=month
            self.day=day
            self.weekday=weekday

    def __init__(self):
        self.dates=[]#
            
    def add_day(self,year,month,day,hour,min):
        target=datetime.datetime(year,month,day,hour=hour,minute=min, second=0)
        if target<datetime.datetime.now():
            return False,"エラー！現在時刻よりも前の時刻が指定されています。"
        self.dates.append(TimerList.BeginDate(year,month,day))

        

def setup(bot):
    bot.add_cog(SetTimer2(bot))
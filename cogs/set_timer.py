from discord.ext import commands
import discord
import config
import sys
import asyncio 
class SetTimer(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.waiting_set_time=False#時間の入力を受け付けているか
        self.count=0
        self.target_person=None#コマンドを売ってきた人しか受け付けない

    @commands.command()
    async def set_timer(self,ctx):
        self.count+=1
        self.target_person=ctx.author
        embed = discord.Embed(title="Timer")
        embed.color = discord.Color.blue()
        embed.add_field(name="1", value="日にちで直接指定")
        embed.add_field(name="2", value="曜日で指定（毎週定期的に）")
        
        async with ctx.channel.typing():
            sent_msg = await ctx.reply(
        f"日にちと時刻に合わせてタイマーをセットすることができます。まずは日にちを指定してください。\n"
        f"どのように指定しますか？番号を教えてください。\n"
        f"キャンセルするときは❌とリアクションしてください。"
        ,embed=embed)
            await sent_msg.add_reaction("1️⃣")
            await sent_msg.add_reaction("2️⃣")
            await sent_msg.add_reaction("❌")

        try:
            #https://qiita.com/coolwind0202/items/12951aba312e0d13afae
            #def check_message_author(msg): return msg.author is ctx.author
            def reaction_check(reaction_, user_):
                is_author=user_==ctx.author
                are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                is_ok=  are_same_messages and is_author
                return is_ok
            #チェック関数に合格するようなメッセージを待つ
            emoji = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
            set_time_flag=False#時間を指定できるか（できなかったら終了）
            if emoji[0].emoji=="1️⃣":#日付でセット
                set_time_flag=await self.set_with_day(ctx)
            elif emoji[0].emoji=="2️⃣":#曜日でセット
                while True:
                    retryFlag,set_time_flag=await self.set_with_yobi(ctx)
                    if not retryFlag:
                        break
            elif emoji[0].emoji=="❌":
                await ctx.send("キャンセルします")
                return
            if set_time_flag:
                await self.set_time(ctx)
            else:
                return
        except asyncio.TimeoutError:
            await ctx.send(" タイムアウトしました。")
            return

    async def set_with_day(self,ctx):
        sent_msg=await ctx.send(
            f"日にちで指定します。\n"
            f"何日にしますか？今日なら1️⃣、明日なら2️⃣とリアクションすることで指定できます。\n"
            f"日付は??????と入力してください。"
            )
        await sent_msg.add_reaction("1️⃣")
        await sent_msg.add_reaction("2️⃣")
        await sent_msg.add_reaction("❌")
        def reaction_check(reaction_, user_):
            is_author=user_==ctx.author
            are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
            return are_same_messages and is_author
        emoji = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
        if emoji[0].emoji=="1️⃣":
            await ctx.send("タイマーを今日にセットします。")
            return True
        if emoji[0].emoji=="2️⃣":
            await ctx.send("タイマーを明日にセットします。")
            return True
        if emoji[0].emoji=="❌":
            await ctx.send("キャンセルします。")
            return False

    async def set_with_yobi(self,ctx):#day of the week は長い
        selected=[False,False,False,False,False,False,False]
        yobi=["日","月","火","水","木","金","土"]
        yobi_emoji=["☀","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"]
        sent_msg=await ctx.send(
            f"曜日で指定します。（毎週）\n"
            f"何曜日にするかリアクションで指定をお願いします。\n"
            f"☀1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣で日月火水木金土の順番です。決定する際は✅をお願いします。"
            )
        for emj in yobi_emoji:
            await sent_msg.add_reaction(emj)
        await sent_msg.add_reaction("✅")
        await sent_msg.add_reaction("❌")
        try:
            while True:#✅❌が押されるまでループ
                def reaction_check2(reaction_, user_):
                    is_author=user_==ctx.author
                    are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                    return are_same_messages and is_author
                #チェック関数に合格するようなメッセージを待つ
                emoji = await self.bot.wait_for('reaction_add', check=reaction_check2, timeout=180)
                for i in range(len(yobi_emoji)):#各曜日についてチェック
                    if emoji[0].emoji==yobi_emoji[i]:
                        selected[i]=True

                if emoji[0].emoji=="✅":
                    #なぜかMessage.reactionsを取得できない
                    #print(sent_msg.content)
                    #print(sent_msg.reactions)
                    #for i in sent_msg.reactions:
                    #    print(i.emoji)

                    msg=""
                    for i in range(len(selected)):
                        if selected[i]:
                            msg+=f"{yobi[i]}曜日と"
                    sent_msg=await ctx.send(f"選択したのは{msg[:-1]}でよろしいですか？")
                    await sent_msg.add_reaction("✅")
                    await sent_msg.add_reaction("♻")
                    await sent_msg.add_reaction("❌")
                    def reaction_check3(reaction_, user_):
                        is_author=user_==ctx.author
                        are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                        return are_same_messages and is_author
                    emoji = await self.bot.wait_for('reaction_add', check=reaction_check3, timeout=180)
                    if emoji[0].emoji=="✅":
                        
                        await ctx.send("曜日をセットしました。")
                        return False,True
                    elif emoji[0].emoji=="♻":
                        await ctx.send("曜日を選択しなおしてください。")
                        return True,False
                    elif emoji[0].emoji=="❌":
                        await ctx.send("キャンセルします。")
                        return False,False
                elif emoji[0].emoji=="❌":
                    await ctx.send("キャンセルします。")
                    return False,False
            
        except asyncio.TimeoutError:
            await ctx.send(" タイムアウトしました。")
            return False,False

    async def set_time(self,ctx):
        await ctx.send("時間を指定してください。例) 19:49")
        self.waiting_set_time=True
        return

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if not self.waiting_set_time:return
        if message.author == self.target_person:
            min,sec=message.content.split(":")
            message.reply(f"{0}時{0}分 {min}:{sec}にタイマーをセットします。")
            self.bot.add_timer(0,0,int(min),int(sec),-1)
def setup(bot):
    bot.add_cog(SetTimer(bot))
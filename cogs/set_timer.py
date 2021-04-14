from discord.ext import commands
import discord
import config
import sys
import asyncio 
class SetTimer(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def set_timer(self,ctx):
        self.count+=1
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
            if emoji[0].emoji=="1️⃣":
                await self.set_with_day(ctx)
            elif emoji[0].emoji=="2️⃣":
                await self.set_with_yobi(ctx)
            elif emoji[0].emoji=="❌":
                await ctx.send("キャンセルします")
                return
            else:
                await ctx.send("間違っています！")
        except asyncio.TimeoutError:
            async with ctx.channel.typing():
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
            await ctx.send("今日ですね。何時にしますか？時刻は??????と入力してください。")
        elif emoji[0].emoji=="2️⃣":
            await ctx.send("明日ですね。何時にしますか？時刻は??????と入力してください。")
        elif emoji[0].emoji=="❌":
            await ctx.send("キャンセルします。")
            return

    async def set_with_yobi(self,ctx):#day of the week は長い
        sent_msg=await ctx.send(
            f"曜日で指定します。（毎週）\n"
            f"何曜日にするかリアクションで指定をお願いします。\n"
            f"☀1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣で日月火水木金土の順番です。決定する際は✅をお願いします。"
            )
        yobi_emoji=["☀","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"]
        for emj in yobi_emoji:
            await sent_msg.add_reaction(emj)
        await sent_msg.add_reaction("✅")
        await sent_msg.add_reaction("❌")
        try:
            selected=[False,False,False,False,False,False,False]
            yobi=["日","月","火","水","木","金","土"]
            while True:
                print("timer reaction wait")
                def reaction_check2(reaction_, user_):
                    is_author=user_==ctx.author
                    are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                    return are_same_messages and is_author
                #チェック関数に合格するようなメッセージを待つ
                emoji = await self.bot.wait_for('reaction_add', check=reaction_check2, timeout=180)
                print("timer reaction detected")
                for i in range(len(yobi_emoji)):
                    if emoji[0].emoji==yobi_emoji[i]:
                        selected[i]=True
                if emoji[0].emoji=="✅":
                    msg=""
                    for i in range(len(selected)):
                        if selected[i]:
                            msg+=f"{yobi[i]}曜日と"
                    await ctx.send(f"選択したのは{msg[:-1]}ですね。")
                    return
                elif emoji[0].emoji=="❌":
                    await ctx.send("キャンセルします。")
                    return
            
        except asyncio.TimeoutError:
            async with ctx.channel.typing():
                await ctx.send(" タイムアウトしました。")
            return

def setup(bot):
    bot.add_cog(SetTimer(bot))
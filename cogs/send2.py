from discord.ext import commands
import discord
import config
import sys
import asyncio 

class Send2(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.waiting_message=False
        self.message=""
        self.count=0
        self.target_person=None#その人にしか送信できないように
    
    #https://discordpy.readthedocs.io/ja/latest/ext/commands/commands.html
    @commands.command()
    async def send2(self, ctx,arg):
        self.count+=1
        if type(arg) is type(None):
            await ctx.reply("指定されていません")
            return
        print(type(arg))
        print(arg)
        print(str(arg))
        target=arg.strip("<!&@>")
        role_=ctx.guild.get_role(int(target))
        member_=ctx.guild.get_member(int(target))
        targets=[]
        sent_msg=None
        if type(role_) is not type(None):
            targets=role_.members
            sent_msg= await self.send_message(ctx,role_)
        elif type(member_) is not type(None):
            targets=[member_]
            sent_msg= await self.send_message(ctx,member_)
        else:
            await ctx.reply("error")
        self.target_person=ctx.author

        try:
            while True:
                print("wait message")
                sent_msg,wait_responce = await self.await_finish(ctx,targets,sent_msg)
                retryFlag=False
                if not wait_responce:return
                retryFlag = await self.await_responce(ctx,targets,sent_msg)
                if not retryFlag:return
                sent_msg=await ctx.reply(f"'{arg.name}' に DM を一斉送信します。内容を記入が終わりましたら「✅」、キャンセルする場合は「❌」とリアクションしてください。")
                await sent_msg.add_reaction("✅")
                await sent_msg.add_reaction("❌")
                self.waiting_message=True
        except asyncio.TimeoutError:
            await ctx.send(f"タイムアウトしました。")
            self.waiting_message=False
            self.message=""
            return

    async def send_message(self,ctx,target):
        sent_msg=await ctx.reply(f"'{target.name}' に DM を一斉送信します。内容を記入が終わりましたら「✅」、キャンセルする場合は「❌」とリアクションしてください。")
        await sent_msg.add_reaction("✅")
        await sent_msg.add_reaction("❌")
        self.message=""
        self.waiting_message=True
        return sent_msg

    async def await_finish(self,ctx,members,sent_msg):
        def reaction_check(reaction_, user_):
            is_author=user_==self.target_person
            are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
            return are_same_messages and is_author
        emoji = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
        if emoji[0].emoji=="✅":
            member_str=""
            for i in members:
                member_str+=f"{i.mention}\n"
            sent_msg= await ctx.send(
                f"完了が確認されました。以下の内容でよろしいでしょうか？\n"
                f"=======================\n"
                f"{self.message}\n"
                f"=======================\n"
                f"送信する人は\n"
                f"{member_str}"
                f"です。\n"
                f"よろしければもう一度「✅」、キャンセルし編集を続ける場合は「♻」、コマンドを終了する場合は「❌」とリアクションしてください。"
                )
            self.waiting_message=False
            await sent_msg.add_reaction("✅")
            await sent_msg.add_reaction("♻")
            await sent_msg.add_reaction("❌")
            return sent_msg,True
        if emoji[0].emoji=="❌":
            await ctx.send("キャンセルされました。終了します。")
            self.waiting_message=False
            self.message=""
            return None,False

    async def await_responce(self,ctx,members,sent_msg):
        def reaction_check2(reaction_, user_):
            is_author=user_==self.target_person
            are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
            return are_same_messages and is_author
        emoji = await self.bot.wait_for('reaction_add', check=reaction_check2, timeout=180)
        print(f"checkkkkk {emoji} {type(emoji)}")
        if emoji[0].emoji=="❌":
            await ctx.send("キャンセルされました。終了します。")
            self.waiting_message=False
            self.message=""
            return False
        if emoji[0].emoji=="✅":
            await ctx.send("送信します。")
            if self.message =="":
                await ctx.send("空メッセージは送信できません。終了します")
                return False
            for i in members:
                await i.send(content=self.message)
            await ctx.send("送信が完了しました。")
            return False
        if emoji[0].emoji=="♻":
            await ctx.send("編集を続けてください。")
            return True
        
    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if not self.waiting_message:return
        #if message.content=="完了":return
        if message.author == self.target_person:
            self.message += message.content + "\n"


def setup(bot):
    bot.add_cog(Send2(bot))
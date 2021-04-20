from discord.ext import commands
import discord
import config
import sys
import asyncio 
import utility

class Send2(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.waiting_message=False
        self.message=""
        self.count=0
        self.target_person=None#その人にしか送信できないように
    
    #https://discordpy.readthedocs.io/ja/latest/ext/commands/commands.html
    @commands.command()
    async def send2(self, ctx,*arg):
        self.count+=1
        if type(arg) is type(None):
            await ctx.reply("送信先が指定されていません")
            return
        targets=[]
        for t in arg:
            targets.append(t)
        if len(targets)==0:
            await ctx.reply("送信先が指定されていません")
            return
        target_members,target_mentions=self.get_targets(ctx,targets)
        self.target_person=ctx.author
        sent_msg= await self.send_message(ctx,target_mentions)

        try:
            while True:
                print("wait message")
                sent_msg,wait_responce = await self.await_finish(ctx,target_members,sent_msg)
                retryFlag=False
                if not wait_responce:return
                retryFlag = await self.await_responce(ctx,target_members,sent_msg)
                if not retryFlag:return#キャンセルされたらコマンドを終了
                #再確認
                sent_msg= await self.send_message(ctx,target_mentions)
                self.waiting_message=True
        except asyncio.TimeoutError:
            await ctx.send(f"タイムアウトしました。")
            self.waiting_message=False
            self.message=""
            return

    async def send_message(self,ctx,target_mentions):
        targets="\n".join(target_mentions)
        sent_msg=await ctx.reply(f"'{targets}' に DM を一斉送信します。内容を記入が終わりましたら「✅」、キャンセルする場合は「❌」とリアクションしてください。")
        self.waiting_message=True
        return sent_msg

    async def await_finish(self,ctx,target_members,sent_msg):
        send_flag=await utility.check_yes_no(self.bot,ctx,sent_msg)
        if send_flag:
            member_str=""
            for target in target_members:
                member_str+=f"{target.mention}\n"
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
            return sent_msg,True
        else:
            await ctx.send("キャンセルされました。終了します。")
            self.waiting_message=False
            self.message=""
            return None,False

    async def await_responce(self,ctx,target_members,sent_msg):
        state=await utility.check_yes_no_cancel(self.bot,ctx,sent_msg)
        if state==0:
            await ctx.send("キャンセルされました。終了します。")
            self.waiting_message=False
            self.message=""
            return False
        if state==1:
            await ctx.send("送信します。")
            if self.message =="":
                await ctx.send("空メッセージは送信できません。終了します")
                return False
            for i in target_members:
                await i.send(content=self.message)
            await ctx.send("送信が完了しました。")
            return False
        if state==-1:
            await ctx.send("編集を続けてください。")
            return True
        
    def get_targets(self,ctx,targets):
        target_roles=[]
        target_members=[]
        target_names=[]
        for target in targets:
            id=target.strip("<!&@>")#argはroleもしくはmember がstr形式で送られてくるので、id(int)を抽出する
            role_=ctx.guild.get_role(int(id))
            member_=ctx.guild.get_member(int(id))
            if type(role_) is not type(None):
                target_roles.append(role_)
                target_names.append(role_.mention)
            elif type(member_) is not type(None):
                target_members.append(member_)
                target_names.append(member_.mention)
            else:
                print("error")
        print(f"target roles is {target_roles}")
        for member in ctx.guild.members:
            if self.check_condition(member,target_roles):
                print(f"send2 append {member}")
                if member not in target_members:#すでに入ってたら２重に送信しないようスキップ
                    target_members.append(member)
        return target_members,target_names

    def check_condition(self,member,roles):#そのmemberがrolesをすべて持っていたらtrue
        if len(roles)==0:return False
        for i in roles:
            if i not in member.roles:return False
        return True

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if not self.waiting_message:return
        #if message.content=="完了":return
        if message.author == self.target_person:
            self.message += message.content + "\n"


def setup(bot):
    bot.add_cog(Send2(bot))
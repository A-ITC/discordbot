from discord.ext import commands
import discord
import config
import sys
import asyncio 
import utility
import requests
import os
"""
type
1 SUB_COMMAND
2 SUB_COMMAND_GROUP
3 STRING
4 INTEGER
5 BOOLEAN
6 USER
7 CHANNEL
8 ROLE
"""

json = {
    "name": "send",
    "description": "条件に合うメンバーにDMを一斉送信",
    "options": [
        {
            "name": "target",
            "required": True,
            "choices": [
                {
                    "name": "role",
                    "description": "特定のロールの人に一斉送信",
                    "type":8
                },
                {
                    "name": "member",
                    "description": "特定の人に送信",
                    "type":6
                },
            ]
        }
    ]
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)
#print(r.json())
class Send(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.waiting_message=False
        self.message=""
        self.target_person=None#その人にしか送信できないように
        self.files=[]
    
    #https://discordpy.readthedocs.io/ja/latest/ext/commands/commands.html
    @commands.command()
    async def send(self, ctx,*arg):
        self.files=[]
        if type(arg) is type(None):
            await ctx.reply("送信先が指定されていません")
            return
        targets=[]
        not_targets=[]
        self.message=""
        self.waiting_message=False
        for t in arg:
            print(t)
            if t[0]=="!":
                t.lstrip("!")
                not_targets.append(t)
            else:
                targets.append(t)
        if len(targets)==0:
            await ctx.reply("送信先が指定されていません")
            return
        target_members,target_mentions,not_target_memtions=utility.get_targets(ctx.guild,targets,not_targets)
        print(not_target_memtions)
        if len(target_members)==0:
            await ctx.reply("条件に合うメンバーがいません")
            return

        self.target_person=ctx.author
        sent_msg= await self.send_message(ctx,target_mentions,not_target_memtions)

        try:
            while True:
                print("wait message")
                sent_msg,wait_responce = await self.await_finish(ctx,target_members,sent_msg)
                retryFlag=False
                if not wait_responce:return
                retryFlag = await self.await_responce(ctx,target_members,sent_msg)
                if not retryFlag:return#キャンセルされたらコマンドを終了
                #再確認
                sent_msg= await self.send_message(ctx,target_mentions,not_target_memtions)
                self.waiting_message=True
        except asyncio.TimeoutError:
            await ctx.send(f"タイムアウトしました。")
            self.waiting_message=False
            return

    async def send_message(self,ctx,target_mentions,not_target_memtions):
        targets="\n".join(target_mentions)
        not_targets="\n".join(not_target_memtions)
        if len(not_target_memtions)!=0:
            not_targets+="には送信しません。"
        sent_msg=await ctx.reply(f"'{targets}' に DM を一斉送信します。{not_targets}内容を記入が終わりましたら「✅」、キャンセルする場合は「❌」とリアクションしてください。")
        self.waiting_message=True
        return sent_msg

    async def await_finish(self,ctx,target_members,sent_msg):
        send_flag=await utility.check_yes_no(self.bot,ctx,sent_msg)
        if not send_flag:
            await ctx.send("キャンセルされました。終了します。")
            self.waiting_message=False
            return None,False
        member_str=""
        for target in target_members:
            member_str+=f"{target.mention}\n"
        files=[]
        for i in self.files:files.append(discord.File(i))
        sent_msg= await ctx.send(
            f"完了が確認されました。以下の内容でよろしいでしょうか？\n"
            f"=======================\n"
            f"{self.message}\n"
            f"=======================\n"
            f"送信する人は\n"
            f"{member_str}"
            f"です。\n"
            f"よろしければもう一度「✅」、キャンセルし編集を続ける場合は「♻」、コマンドを終了する場合は「❌」とリアクションしてください。"
           ,files=files)
        self.waiting_message=False
        return sent_msg,True

    async def await_responce(self,ctx,target_members,sent_msg):
        state=await utility.check_yes_no_cancel(self.bot,ctx,sent_msg)
        if state==0:
            await ctx.send("キャンセルされました。終了します。")
            self.waiting_message=False
            return False
        if state==1:
            if self.message =="":
                await ctx.send("空メッセージは送信できません。終了します")
                return False
            await ctx.send("送信します。")
            for member in target_members:
                files=[]
                for i in self.files:files.append(discord.File(i))
                await member.send(content=self.message,files=files)
            for i in self.files:os.remove(i)
            await ctx.send("送信が完了しました。")
            return False
        if state==-1:
            await ctx.send("編集を続けてください。")
            return True

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if not self.waiting_message:return
        if message.author != self.target_person:return
        self.message += message.content + "\n"
        for attachment in message.attachments:
            save_name= f"{attachment.filename}"
            utility.download_img(attachment.url,save_name)
            self.files.append(save_name)
                    
def setup(bot):
    bot.add_cog(Send(bot))
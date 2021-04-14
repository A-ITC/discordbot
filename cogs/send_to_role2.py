from discord.ext import commands
import discord
import config
import sys
import asyncio 

#複数のロールを指定したかった

class SendToRole2(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.waiting_message=False
        self.message=""
        self.count=0

    def get_role_str(self,roles_):
        roles_str=""
        roles=roles_
        for i in roles_:
            roles_str+=f"{i.name} かつ"
        roles_str=roles_str.rstrip("かつ")
        return roles_str

    #https://discordpy.readthedocs.io/ja/latest/ext/commands/commands.html
    @commands.command()
    async def send_to_role2(self, ctx,roles_ : commands.Greedy[discord.Role]=None):
        if type(roles_) is type(None):
            await ctx.reply("ロールが指定されていません")
            return
        def check_message(msg): return msg.content=="完了" or  msg.content=="キャンセル" 
        async with ctx.channel.typing():
            sent_msg=await ctx.reply(f"'{self.get_role_str(roles_)}' の人に DM を一斉送信します。内容を記入が終わりましたら「✅」、キャンセルする場合は「❌」とリアクションしてください。")
            await sent_msg.add_reaction("✅")
            await sent_msg.add_reaction("❌")
            self.waiting_message=True
        try:
            def reaction_check1(reaction_, user_):
                is_author=reaction_.message.author!=ctx.author
                are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                is_ok=  are_same_messages and is_author
                return is_ok
            emoji = await self.bot.wait_for('reaction_add', check=reaction_check1, timeout=180)
            if emoji[0].emoji=="❌":
                await ctx.send("キャンセルされました。終了します。")
                self.message=""
                return
            if emoji[0].emoji=="✅":
                self.waiting_message=False
                sent_msg= await ctx.send(
                    f"「完了」が確認されました。以下の内容でよろしいでしょうか？\n"
                    f"{self.message}\n"
                    f"よろしければもう一度「✅」、キャンセルする場合は「❌」とリアクションしてください。"
                    )
                await sent_msg.add_reaction("✅")
                await sent_msg.add_reaction("❌")
            def reaction_check2(reaction_, user_):
                is_author=reaction_.message.author!=ctx.author
                are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                is_ok=  are_same_messages and is_author
                return is_ok
            emoji = await self.bot.wait_for('reaction_add', check=reaction_check2, timeout=180)
            if emoji[0].emoji=="❌":
                await ctx.send("キャンセルされました。終了します。")
                self.message=""
                return
            if emoji[0].emoji=="✅":
                await ctx.send("送信します。")
                for i in role_.members:
                    await i.send(content=self.message)
                await ctx.send("送信が完了しました。")
                self.message=""
        except asyncio.TimeoutError as e:
            async with ctx.channel.typing():
                await ctx.send(f"タイムアウトしました。")
                self.waiting_message=False
                self.message=""
                return
        
    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if not self.waiting_message:return
    #    if message.content=="完了":return
        self.message+=message.content+"\n"


def setup(bot):
    bot.add_cog(SendToRole2(bot))
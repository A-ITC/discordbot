from discord.ext import commands
import discord
import config
import sys
import asyncio 

class AddRole(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def add_role(self,ctx,target_role_:discord.Role,new_role_:discord.Role):
        self.count+=1
        sent_msg = await ctx.reply(f"{target_role_.name} を持つ人全員に {new_role_.name} を追加します。よろしいですか？\nこのコマンドはやり直しができません。")
        await sent_msg.add_reaction("✅")
        await sent_msg.add_reaction("❌")
        try:
            def reaction_check(reaction_, user_):
                is_author=user_==ctx.author
                are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                return are_same_messages and is_author
            emoji = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
            if emoji[0].emoji=="✅":
                await ctx.send("追加します。")
                return
            if emoji[0].emoji=="❌":
                await ctx.send("キャンセルします。")
                return
        except asyncio.TimeoutError as e:
            await ctx.send("タイムアウトしました。")
            return
def setup(bot):
    bot.add_cog(AddRole(bot))
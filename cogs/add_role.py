from discord.ext import commands
import discord
import config
import sys
import asyncio 

import requests
import utility

class AddRole(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def add_role(self,ctx,target_role_:discord.Role,new_role_:discord.Role):
        self.count+=1
        sent_msg = await ctx.reply(f"{target_role_.name} を持つ人全員に {new_role_.name} のロールを追加します。よろしいですか？")
        try:
            flag=await utility.check_yes_no(self.bot,ctx,sent_msg)
            if flag:
                await ctx.send("追加します。")
                for member in target_role_.members:
                    await member.add_roles(new_role_,reason="bot.add_role")
                await ctx.send("追加しました。")
            else:
                await ctx.send("キャンセルします。")
                return
        except asyncio.TimeoutError as e:
            await ctx.send("タイムアウトしました。")
            return

    @commands.command()
    async def remove_role(self,ctx,target_role_:discord.Role,new_role_:discord.Role):
        self.count+=1
        sent_msg = await ctx.reply(f"{target_role_.name} を持つ人全員から {new_role_.name} のロールを削除します。よろしいですか？")
        try:
            flag=await utility.check_yes_no(self.bot,ctx,sent_msg)
            if flag:
                await ctx.send("削除します。")
                for member in target_role_.members:
                    await member.remove_roles(new_role_,reason="bot.remove_role")
                await ctx.send("削除しました。")
            else:
                await ctx.send("キャンセルします。")
                return
        except asyncio.TimeoutError as e:
            await ctx.send("タイムアウトしました。")
            return
    
def setup(bot):
    bot.add_cog(AddRole(bot))
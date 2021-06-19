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

    @commands.command()
    async def add_role(self,ctx,new_role_:discord.Role,target_roles_:discord.Role,):
        target_roles_name=""
        for role in target_roles_:
            target_roles_name+=role.mention+" "
        sent_msg = await ctx.reply(f"{target_roles_name} すべてを持つ人全員に {new_role_.name} のロールを追加します。よろしいですか？")
        try:
            flag=await utility.check_yes_no(self.bot,ctx,sent_msg)
            if flag:
                await ctx.send("追加します。")
                for member in ctx.guild.members:
                    if utility.check_condition(member,target_roles_):
                        await member.add_roles(new_role_,reason="bot.add_role")
                await ctx.send("追加しました。")
            else:
                await ctx.send("キャンセルします。")
                return
        except asyncio.TimeoutError as e:
            await ctx.send("タイムアウトしました。")
            return

    @commands.command()
    async def remove_role(self,ctx,new_role_:discord.Role,target_roles_:discord.Role):
        target_roles_name=""
        for role in target_roles_:
            target_roles_name+=role.mention+" "
        sent_msg = await ctx.reply(f"{target_roles_name} を持つ人全員から {new_role_.name} のロールを削除します。よろしいですか？")
        try:
            flag=await utility.check_yes_no(self.bot,ctx,sent_msg)
            if flag:
                await ctx.send("削除します。")
                for member in ctx.guild.members:
                    if utility.check_condition(member,target_roles_):
                        await member.remove_roles(new_role_,reason="bot.add_role")
                await ctx.send("削除しました。")
            else:
                await ctx.send("キャンセルします。")
                return
        except asyncio.TimeoutError as e:
            await ctx.send("タイムアウトしました。")
            return
    
def setup(bot):
    bot.add_cog(AddRole(bot))
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
    async def add_role(self,ctx,new_role_:discord.Role,*target_roles_):
        target_roles_name=""
        target_roles=[]
        target_members_name=""
        target_members=[]
        for role in target_roles_:
            role_num=role.strip("<!&@>")
            role_=ctx.guild.get_role(int(role_num))
            member_=ctx.guild.get_member(int(role_num))
            if type(role_) is not type(None):
                target_roles.append(ctx.guild.get_role(int(role_num)))
                target_roles_name+=target_roles[-1].mention+" "
            elif type(member_) is not type(None):
                target_members.append(ctx.guild.get_role(int(role_num)))
                target_members_name+=target_members[-1].mention+" "
        message=""
        if len(target_roles)!=0 and len(target_members)==0:
            message=f"{target_roles_name} すべてを持つ人全員に {new_role_.mention} のロールを追加します。よろしいですか？"
        elif len(target_roles)==0 and len(target_members)!=0:
            message=f"{target_members_name} に {new_role_.mention} のロールを追加します。よろしいですか？"
        else:
            message=f"{target_roles_name} すべてを持つ人全員もしくは {target_members_name} に {new_role_.mention} のロールを追加します。よろしいですか？"

        sent_msg = await ctx.reply(message)
        try:
            flag=await utility.check_yes_no(self.bot,ctx,sent_msg)
            if flag:
                await ctx.send("追加します。")
                for member in ctx.guild.members:
                    if utility.check_condition(member,target_roles):
                        print(member.name+"に追加")
                        await member.add_roles(new_role_,reason="bot.add_role")
                for member in target_members:
                    print(member.name+"に追加")
                    await member.add_roles(new_role_,reason="bot.add_role")
                await ctx.send("追加しました。")
            else:
                await ctx.send("キャンセルします。")
                return
        except asyncio.TimeoutError as e:
            await ctx.send("タイムアウトしました。")
            return

    @commands.command()
    async def remove_role(self,ctx,new_role_:discord.Role,*target_roles_):
        target_roles_name=""
        target_roles=[]
        for role in target_roles_:
            role_num=role.strip("<!&@>")
            target_roles.append(ctx.guild.get_role(int(role_num)))
            target_roles_name+=target_roles[-1].mention+" "
        sent_msg = await ctx.reply(f"{target_roles_name} を持つ人全員から {new_role_.mention} のロールを削除します。よろしいですか？")
        try:
            flag=await utility.check_yes_no(self.bot,ctx,sent_msg)
            if flag:
                await ctx.send("削除します。")
                for member in ctx.guild.members:
                    if utility.check_condition(member,target_roles):
                        print(member.name+"から削除")
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
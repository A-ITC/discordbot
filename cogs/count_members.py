from discord.ext import commands
import discord
import config
import utility
import sys
import asyncio 
import requests

class CountMembers(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def count_members(self, ctx ,*roles_):
        self.count+=1
        targets=[]
        not_targets=[]
        for role in roles_:
            print(role)
            if role[0]=="!":
                role.lstrip("!")
                role_num=role.strip("<!&@>")
                role_id=ctx.guild.get_role(int(role_num))
                not_targets.append(role_id)
            else:
                role_num=role.strip("<!&@>")
                role_id=ctx.guild.get_role(int(role_num))
                targets.append(role_id)
            print(role_num)

        num=0
        print(targets)
        
        for member in ctx.guild.members:
            if utility.check_condition(member,targets,not_targets):num+=1
        
        role_str=""
        for i in targets:
            role_str+=i.mention+" "
        not_role_str=""
        for i in not_targets:
            not_role_str+=i.mention+" "
        if len(not_targets)!=0:
            not_role_str+="のない"
        await ctx.reply(f"役職 '{role_str}' を持っている{not_role_str}メンバー数: {num} 人 / {ctx.guild.member_count} 人")

def setup(bot):
    bot.add_cog(CountMembers(bot))

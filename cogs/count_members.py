from discord.ext import commands
import discord
import config
import sys
import asyncio 

class CountMembers(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def count_members(self, ctx ,*roles_):
        self.count+=1
        targets=[]
        for role in roles_:
            print(role)
            role_num=role.strip("<!&@>")
            print(role_num)
            role_id=ctx.guild.get_role(int(role_num))
            targets.append(role_id)

        num=0
        print(targets)
        
        for member in ctx.guild.members:
            if self.check_condition(member,targets):num+=1
        
        role_str=""

        for i in targets:
            role_str+=i.name+" "
        await ctx.reply(f"役職 '{role_str}' を持っているメンバー数: {num} 人 / {ctx.guild.member_count} 人")

    def check_condition(self,member,roles):
        for i in roles:
            if i not in member.roles:return False
        return True

def setup(bot):
    bot.add_cog(CountMembers(bot))

from discord.ext import commands
import discord
import config
import sys
import asyncio 
import utility

class MemberListUp(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.waiting_message=False
        self.message=""
        self.count=0
        self.target_person=None#その人にしか送信できないように
    
    #https://discordpy.readthedocs.io/ja/latest/ext/commands/commands.html
    @commands.command()
    async def member_list_up(self, ctx,*roles_):
        self.count+=1
        if type(roles_)is type(None):
            await ctx.reply("ロールが指定されていません")
        targets=[]
        for role in roles_:
            print(role)
            role_num=role.strip("<!&@>")
            print(role_num)
            role_id=ctx.guild.get_role(int(role_num))
            targets.append(role_id)
        role_str=""
        for i in targets:
            role_str+=f"{i.mention}\n"

        members=[]
        for member in ctx.guild.members:
            if utility.check_condition(member,targets):members.append(member.mention)
        
        role_str="\n".join(members)
        await ctx.reply(f"{role_str}")

def setup(bot):
    bot.add_cog(MemberListUp(bot))
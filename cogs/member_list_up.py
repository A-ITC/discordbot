from discord.ext import commands
import discord
import config
import sys
import asyncio 

class MemberListUp(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.waiting_message=False
        self.message=""
        self.count=0
        self.target_person=None#その人にしか送信できないように
    
    #https://discordpy.readthedocs.io/ja/latest/ext/commands/commands.html
    @commands.command()
    async def member_list_up(self, ctx,role_:discord.Role):
        self.count+=1
        member_str=""
        for i in role_.members:
            member_str+=f"{i.mention}\n"
        await ctx.reply(member_str)

def setup(bot):
    bot.add_cog(MemberListUp(bot))
from discord.ext import commands
import discord
import config
import sys
import asyncio 
import utility
import requests

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
    "name": "member_list_up",
    "description": "対象のロールを持つメンバーをリストアップ",
    "options": [
        {
            "name": "role",
            "description": "対象となるロール",
            "type": 8,
            "required": True,
        }
    ]
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)
#print(r.json())
class MemberListUp(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.waiting_message=False
        self.message=""
        self.target_person=None#その人にしか送信できないように
    
    #https://discordpy.readthedocs.io/ja/latest/ext/commands/commands.html
    @commands.command()
    async def member_list_up(self, ctx,*roles_):
        if type(roles_)is type(None):
            await ctx.reply("ロールが指定されていません")
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
        members=[]
        for member in ctx.guild.members:
            if utility.check_condition(member,targets,not_targets):members.append(member.mention)
        
        role_str="\n".join(members)
        if role_str=="":
            await ctx.reply("ロールを持っているがいません")
        else:
            await ctx.reply(f"{role_str}")

def setup(bot):
    bot.add_cog(MemberListUp(bot))
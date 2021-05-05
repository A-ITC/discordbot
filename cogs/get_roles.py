from discord.ext import commands
import discord
import config
import sys
import asyncio 

class GetRoles(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def get_roles(self,ctx,role_=None):
        self.count+=1
        output="ロール：\n"
        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title="ロール一覧")
        # Embed の表示色を青色に設定
        embed.color = config.EMBED_COLOR

        ans={}
        target_members=[]
        if type(role_)==type(None):
            target_members=ctx.guild.members
        else:
            target_members.append(role_.members)

        for member in target_members:
            self.count_members(member,ans)

        for k,v in ans.items():
            embed.add_field(name=f"{k}", value=f"{v}",inline=False)

        async with ctx.channel.typing():
            await ctx.reply(embed=embed)
    def count_members(self,member_,ans):
        for rol in member_.roles:
            if rol.name not in ans:
                ans[rol.name]=0
            else:
                ans[rol.name]+=1

def setup(bot):
    bot.add_cog(GetRoles(bot))
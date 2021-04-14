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
    async def count_members(self, ctx ,role_ :discord.Role=None):
        self.count+=1
        print(f"{role_}")
        role = discord.utils.get(ctx.guild.roles, name=f"{role_}")
        if role is None:
            async with ctx.channel.typing():
                await ctx.reply("ロールが見つかりません")
            return
        async with ctx.channel.typing():
            await ctx.reply(f"役職 '{role.name}'' を持っているメンバー数: {len(role.members)} 人 / {ctx.guild.member_count} 人")


def setup(bot):
    bot.add_cog(CountMembers(bot))

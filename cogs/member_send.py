from discord.ext import commands
import discord
import config
import sys
import asyncio 

class MemberSend(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def member_send(self,ctx, member: discord.Member, content):
        self.count+=1
        async with ctx.channel.typing():
            await ctx.reply(f"{member.name} に DM を送信します。")
        await member.send(content=content)
        await ctx.send("送信が完了しました")


def setup(bot):
    bot.add_cog(MemberSend(bot))

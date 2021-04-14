from discord.ext import commands
import discord
import config
import sys
import asyncio 

class Invoke(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def 召喚(self,ctx, member: discord.Member, content=""):
        self.count+=1
        async with ctx.channel.typing():
            await ctx.reply(f"{member.name} を召喚する DM を送信します。")
        if content=="":
            if type(ctx.author.voice)!=type(None):
                pass
            await member.send(content=f"こんにちは{member.name}！{ctx.author.name}が呼んでいます。")
        else:
            await member.send(content=content)
        await ctx.send("送信が完了しました")


def setup(bot):
    bot.add_cog(Invoke(bot))

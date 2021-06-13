from discord.ext import commands
import discord
import config
import sys
import asyncio 

from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
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

    @cog_ext.cog_slash(name="召喚",  description= "召喚する DM を送信します。",options=[
            create_option(
                name="target",
                description="対象となるアカウント",
                option_type=6,
                required=False
            ),
            create_option(
                name="content",
                description="文面",
                option_type=3,
                required=False
            )
            ],guild_ids=config.guild_ids)
    async def _召喚(self, ctx: SlashContext, target: discord.Member, content=""):
        async with ctx.channel.typing():
            await ctx.reply(f"{target.name} を召喚する DM を送信します。")
        if content=="":
            if type(ctx.author.voice)!=type(None):
                pass
            await target.send(content=f"こんにちは{target.name}！{ctx.author.name}が呼んでいます。")
        else:
            await target.send(content=content)
        await ctx.send("送信が完了しました")


def setup(bot):
    bot.add_cog(Invoke(bot))

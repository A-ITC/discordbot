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
    async def get_roles(self,ctx):
        self.count+=1
        roles=ctx.guild.roles
        output="ロール：\n"
        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title="ロール一覧")
        # Embed の表示色を青色に設定
        embed.color = config.EMBED_COLOR
        for i in roles:
            output += f"{i.name} , {len(i.members)}\n"
            # 気分を Field として表示
            embed.add_field(name=f"{i.name}", value=f"{len(i.members)}",inline=False)
        async with ctx.channel.typing():
            await ctx.reply(embed=embed)
        #await ctx.reply(output)

def setup(bot):
    bot.add_cog(GetRoles(bot))
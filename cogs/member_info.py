
from discord.ext import commands
import discord
import config
import sys
import asyncio 

class MemberInfo(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def member_info(self, ctx,member_: discord.Member=None):
        self.count+=1
        from datetime import timedelta
        member = member_
        if member is None:
            member=ctx.author
        roles=""
        for i in member.roles:
            if i.name =="@everyone":continue
            roles+=f"{i.name},"

        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title="ユーザー情報")
        # Embed の表示色を青色に設定
        embed.color = config.EMBED_COLOR
        embed.add_field(name="ユーザー名", value=member.name,inline=False)
        embed.add_field(name="ニックネーム", value=member.nick,inline=False)
        embed.add_field(name="ユーザー ID", value=member.id,inline=False)
        embed.add_field(name="ロール", value=roles,inline=False)
        embed.add_field(name="Discord への参加日", value=member.created_at + timedelta(hours=9),inline=False)
        embed.add_field(name="Guild への参加日", value=member.joined_at + timedelta(hours=9),inline=False)
        embed.add_field(name="ステータス", value=member.status,inline=False)
        embed.add_field(name="モバイルからのログイン？", value=member.is_on_mobile(),inline=False)
        embed.add_field(name="BOT?", value=member.bot,inline=False)
        embed.set_thumbnail(url=member.avatar_url)

        async with ctx.channel.typing():
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(MemberInfo(bot))

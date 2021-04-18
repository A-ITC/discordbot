from discord.ext import commands
import discord
import config
import sys
import asyncio 

class Info(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def info(self, ctx,target):
        self.count+=1
        print(type(target))
        print(target)
        target=target.strip("<!&@>")
        role_=ctx.guild.get_role(int(target))
        member_=ctx.guild.get_member(int(target))
        if type(role_) is not type(None):
            self.role(ctx,role_)
        elif type(member_) is not type(None):
            self.member(ctx,member_)
        else:
            await ctx.reply("error")
        return
        
    async def role(self,ctx,role_):
        from datetime import timedelta
        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title="ロール情報")
        # Embed の表示色を青色に設定
        embed.color = config.EMBED_COLOR
        embed.add_field(name="ロール名", value=role_.name,inline=False)
        embed.add_field(name="ID", value=role_.id,inline=False)
        embed.add_field(name="色", value=role_.color,inline=False)
        embed.add_field(name="作成日時", value=role_.created_at+ timedelta(hours=9),inline=False)
        embed.add_field(name="メンバー数", value=len(role_.members),inline=False)
        embed.add_field(name="メンション可能", value=role_.mentionable,inline=False)
        async with ctx.channel.typing():
            await ctx.reply(embed=embed)

    async def member(self,ctx,member_):
        from datetime import timedelta
        member = member_
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
    bot.add_cog(Info(bot))
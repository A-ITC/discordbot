from discord.ext import commands
import discord
import config
import sys
import asyncio 
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
    "name": "info",
    "description": "対象のギルドについての情報を出力",
    "options": [
        {
            "name": "role",
            "description": "対象のロールについての情報を出力",
            "type": 8,
            "required": False,
        },
        {
            "name": "member",
            "description": "対象のメンバーについての情報を出力",
            "type": 6,
            "required": False,
        }
    ]
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)
#print(r.json())

class Info(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
                
    @commands.command()
    async def info(self, ctx,target=None):
        if type(target)is type(None):
            await self.guild(ctx)
            return
        print(type(target))
        print(target)
        target=target.strip("<!&@>")
        role_=ctx.guild.get_role(int(target))
        member_=ctx.guild.get_member(int(target))
        if type(role_) is not type(None):
            await self.role(ctx,role_)
        elif type(member_) is not type(None):
            await self.member(ctx,member_)
        else:
            await ctx.reply("error")
        return
        
    async def guild(self,ctx):
        from datetime import timedelta
        guild = ctx.guild
        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title="サーバー情報")
        # Embed の表示色を青色に設定
        embed.color = config.EMBED_COLOR
        embed.add_field(name="サーバー名", value=guild.name,inline=False)
        embed.add_field(name="サーバー ID", value=guild.id,inline=False)
        embed.add_field(name="サーバー所有者", value=guild.owner.name,inline=False)
        embed.add_field(name="参加人数", value=guild.member_count,inline=False)
        embed.add_field(name="設立日時", value=guild.created_at + timedelta(hours=9),inline=False)
        embed.add_field(name="テキストチャンネル数", value=len(guild.text_channels),inline=False)
        embed.add_field(name="ボイスチャンネル数", value=len(guild.voice_channels),inline=False)
        embed.set_thumbnail(url=guild.icon_url)
        async with ctx.channel.typing():
            await ctx.reply(embed=embed)

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
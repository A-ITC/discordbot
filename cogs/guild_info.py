from discord.ext import commands
import discord
import config
import sys
import asyncio 

class GuildInfo(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def guild_info(self,ctx):
        self.count+=1
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
def setup(bot):
    bot.add_cog(GuildInfo(bot))
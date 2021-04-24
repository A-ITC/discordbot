from discord.ext import commands
import discord
import config
import sys
import asyncio 
import requests

class ClientAppInfo(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def client_app_info(self,ctx):
        self.count+=1
        client = self.bot
        app_info = await client.application_info()
        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title="アプリケーション情報")
        # Embed の表示色を青色に設定
        embed.color = config.EMBED_COLOR
        embed.add_field(name="アプリケーション ID", value=app_info.id)
        embed.add_field(name="Bot オーナー", value=app_info.owner.name)
        embed.add_field(name="Public Bot?", value=app_info.bot_public)
        async with ctx.channel.typing():
            await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(ClientAppInfo(bot))
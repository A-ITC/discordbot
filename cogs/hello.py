from discord.ext import commands
import discord
import config
import sys
import asyncio 

class Hello(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def hello(self,ctx):
        self.count+=1
        await ctx.reply(
    f"""
    こんにちは、{ctx.author.name} さん。
    ご気分はいかがでしょうか？
    """)

        try:
            def check_message_author(msg): return msg.author is ctx.author
            #チェック関数に合格するようなメッセージを待つ
            msg = await self.bot.wait_for('message', check=check_message_author, timeout=10)
            # 受け取ったメッセージの内容を使って返信
            embed = discord.Embed(title="Hello")
            # Embed の表示色を青色に設定
            embed.color = config.EMBED_COLOR
            # Embed の説明文を設定
            embed.description = " あなたの気分を把握しました。"
            # 気分を Field として表示
            embed.add_field(name=" あなたの気分 ", value=msg.content)
            async with ctx.channel.typing():
                await ctx.reply(embed=embed)
        except asyncio.TimeoutError:
            async with ctx.channel.typing():
                await ctx.send(" タイムアウトしました。")
            return
        
def setup(bot):
    bot.add_cog(Hello(bot))
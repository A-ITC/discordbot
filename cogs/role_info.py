from discord.ext import commands
import discord
import config
import sys
import asyncio 

class RoleInfo(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.is_owner()
    @commands.command()
    async def role_info(self, ctx,role_:discord.Role):#cogs.***としないとエラー
        self.count+=1
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

        return

def setup(bot):
    bot.add_cog(RoleInfo(bot))
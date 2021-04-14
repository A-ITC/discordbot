from discord.ext import commands
import discord
import config
import sys
import asyncio 

class Reload(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, module_name):#cogs.***としないとエラー
        self.count+=1
        async with ctx.channel.typing():
            await ctx.reply(f" モジュール {module_name} の再読み込みを開始します。")
        try:
            self.bot.reload_extension(module_name)
            async with ctx.channel.typing():
                await ctx.send(f" モジュール {module_name} の再読み込みを終了しました。")
        except (commands.errors.ExtensionNotLoaded, commands.errors.ExtensionNotFound,
        commands.errors.NoEntryPointError, commands.errors.ExtensionFailed) as e:
            async with ctx.channel.typing():
                await ctx.send(f" モジュール {module_name} の再読み込みに失敗しました。理由：{e}")
        return

def setup(bot):
    bot.add_cog(Reload(bot))
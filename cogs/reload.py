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
    "name": "reload",
    "description": "対象のコマンドを再読み込み",
    "options": [
        {
            "name": "command",
            "description": "cogs.***",
            "type": 3,
            "required": True,
        }
    ]
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)
#print(r.json())
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
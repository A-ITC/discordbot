from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 
import utility
import requests

from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

texts=[
    "ミ゜（絶命）",
    "Botを終了します。",
    "さよなら…さよなら…",
    "😴",
    "👋",
    "Bot has been stoped.",
    "Farewell, everyone",
    "Bot休止了",
    "死にたくない…死にたくない…",
    "Sleeping",
    "ぐあああああっ"
    ]

class Stop(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.is_owner()
    @commands.command()
    async def stop(self,ctx,option=None):
        self.count+=1
        try:
            if type(option)==type(None):
                stop_flag=await utility.yes_no(self.bot,ctx,"Botを停止させますか？")
                if stop_flag:
                    await ctx.reply(random.choice(texts))
                    await self.bot.close()
                else:
                    await ctx.reply("キャンセルします。")
            else:
                await ctx.reply(random.choice(texts))
                await self.bot.close()
        except asyncio.TimeoutError:
            await ctx.send(f"タイムアウトしました。")
        #await self.bot.logout()

    @cog_ext.cog_slash(name="stop",  description= "Botを終了します。",options=[
            create_option(
                name="option",
                description="確認メッセージを省略します",
                option_type=3,
                required=False
            )
            ],guild_ids=config.guild_ids)
    async def _stop(self, ctx: SlashContext, option: str=None):
        try:
            if type(option)==type(None):
                stop_flag=await utility.yes_no(self.bot,ctx,"Botを停止させますか？")
                if stop_flag:
                    await ctx.send(random.choice(texts))
                    await self.bot.close()
                else:
                    await ctx.send("キャンセルします。")
            else:
                await ctx.send(random.choice(texts))
                await self.bot.close()
        except asyncio.TimeoutError:
            await ctx.send(f"タイムアウトしました。")
        
def setup(bot):
    bot.add_cog(Stop(bot))
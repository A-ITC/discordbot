from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 
import requests


from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
texts=[
    "ざ～こ❤",
    "よわよわ❤",
    "GPA低い🧡単位大丈夫だった？🧡",
    "進捗まだダメなの？💛💛",
    "ざこ❤ざこ❤ざこ❤",
    "生活リズム狂ってる❤",
    "社会性なし💛",
    "レポートまだ終わってないの？ざっこ🧡",
    "締め切り守れないんですか？❤",
    "がんばれ❤がんばれ❤",
    "え～？こんなことしてるなんて暇なんですね🧡",
    "読んだ本より積んでる本のが多いじゃん💛💛",
    "お前はいつもそうだ\n誰もお前を愛さない",
    "えっ…？",
    "ちょっ…やめてください",
    "体調管理しっかりしてくださいね❤",
    "お疲れ様です！"
    ]
class Mesugaki(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
                
    @commands.command()
    async def メスガキ(self,ctx):
        async with ctx.channel.typing():
            await ctx.reply(random.choice(texts))
            
    @cog_ext.cog_slash(name="メスガキ",  description= "メスガキがよ...",guild_ids=config.guild_ids)
    async def _メスガキ(self,ctx):
        self.count+=1
        await ctx.send(random.choice(texts))

        
def setup(bot):
    bot.add_cog(Mesugaki(bot))
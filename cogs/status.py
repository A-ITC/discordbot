from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 

class Status(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def status(self,ctx):
        self.count+=1
        embed = discord.Embed(title=f"{ctx.author.name} のステータス")
        embed.color = config.EMBED_COLOR
        str_=random.randint(3, 20)#筋力
        embed.add_field(name=f"💪筋力 (STR)", value=str_,inline=False)
        con_=random.randint(3, 20)#体力
        embed.add_field(name=f"❤体力 (CON)", value=con_,inline=False)
        pow_=random.randint(3, 20)#精神力
        embed.add_field(name=f"🙂精神力 (POW)", value=pow_,inline=False)
        dex_=random.randint(3, 20)#敏捷性
        embed.add_field(name=f"🦶敏捷性 (DEX)", value=dex_,inline=False)
        app_=random.randint(3, 20)#外見
        embed.add_field(name=f"✨外見 (APP)", value=app_,inline=False)
        siz_=random.randint(3, 20)#体格
        embed.add_field(name=f"🩺体格 (SIZ)", value=siz_,inline=False)
        int_=random.randint(3, 20)#知性
        embed.add_field(name=f"💭知性 (INT)", value=int_,inline=False)
        edu_=random.randint(3, 20)#教育
        embed.add_field(name=f"🎓教育 (EDU)", value=edu_,inline=False)
        san_=pow_*5#正気度
        embed.add_field(name=f"👀正気度 (SAN)", value=san_,inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        
        await ctx.reply(embed=embed)

        
def setup(bot):
    bot.add_cog(Status(bot))
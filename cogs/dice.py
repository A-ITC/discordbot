from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 

class Dice(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def dice(self, ctx ,content):
        self.count+=1
        num=content.split("d")
        if len(num)<2:
            await ctx.reply("入力がおかしいです。*d*としてください。（半角数字）")
            return
        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title=f"ダイス : {content}")
        # Embed の表示色を青色に設定
        embed.color = config.EMBED_COLOR
        sum=0
        dice_num=int(num[0])
        if dice_num>8:dice_num=8
        for i in range(0,dice_num):
            value=random.randint(1,int(num[1]))
            embed.add_field(name=f"{i+1}ダイス目", value=value,inline=False)
            sum+=value
        embed.add_field(name="合計", value=sum,inline=False)
        await ctx.reply(embed=embed)
def setup(bot):
    bot.add_cog(Dice(bot))

from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 
import requests

json = {
    "name": "dice",
    "description": "さいころを振ります",
    "options": [
        {
            "name": "dice",
            "description": "ダイスのタイプ（例 1d3）",
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

class Dice(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def dice(self, ctx ,content):
        self.count+=1
        num=content.split("d")
        if len(num)<2:
            await ctx.reply("入力がおかしいです。*d*としてください。例 1d43")
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
        embed.set_thumbnail(url="https://www.ed.tus.ac.jp/tusitclub/discord/dice.png")
        embed.add_field(name="合計", value=sum,inline=False)
        await ctx.reply(embed=embed)
def setup(bot):
    bot.add_cog(Dice(bot))

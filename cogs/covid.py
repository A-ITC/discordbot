from discord.ext import commands
import discord
import config
import sys
import requests
import csv
import io

class Covid(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def covid(self, ctx, target = None):
        URL = 'https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv'
        response = requests.get(URL)
        response.raise_for_status()

        f = io.StringIO()
        f.write(response.text)
        f.seek(0)

        csv_reader = csv.reader(f)
        read_data = [row for row in csv_reader]

        f.close()

        prefecture_data = []
        
        if target != None:
            prefecture = target
        else:
            prefecture = "東京都"


        for data in read_data:
            if data[2] == prefecture:
                prefecture_data.append(data)
    
        if len(prefecture_data) == 0 or target == "都道府県名":
            await ctx.reply("you どこに住んでいるの？")
            return 

        request_data = prefecture_data[-1]
        text = request_data[0] + " : "+ request_data[2] +" の感染者数は " + request_data[3] + " 人です。\n データは 20 時ごろに更新されます。"
        await ctx.reply(text)

def setup(bot):
    bot.add_cog(Covid(bot))
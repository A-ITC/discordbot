from discord.ext import commands
from matplotlib import pyplot as plt

import discord
import config
import sys
import requests
import csv
import io
import os

class Covid(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def covid(self, ctx, target=None, target_graph=None):
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
        
        if len(prefecture_data) == 0:
            await ctx.send("you どこに住んでいるの？")
            return 

        request_data = prefecture_data[-1]
        text = request_data[0] + " : "+ request_data[2] +" の感染者数は " + request_data[3] + " 人です。\n データは 20 時ごろに更新されます。"
        await ctx.send(text)


        if target_graph == "-g":
            x = [prefecture_data_by_day[0] for prefecture_data_by_day in prefecture_data]
            y = [int(prefecture_data_by_day[3]) for prefecture_data_by_day in prefecture_data]
            
            nx = []
            tmp = prefecture_data[0][0].split('/')
            nx.append(prefecture_data[0][0])
            month = tmp[1]
            for prefecture_data_by_day in prefecture_data:
                tmp = prefecture_data_by_day[0].split('/')
                if month != tmp[1]:
                    nx.append(prefecture_data_by_day[0])
                    month = tmp[1]

            fig = plt.figure(figsize=(12.8, 10.24), dpi=100)
            plt.plot(x, y, color='green', linestyle='-')
            plt.plot(x[-1], y[-1], 'ms', ms=5, label='Intersection', color='blue')
            plt.text(x[-1], y[-1], '({x}, {y})'.format(x=x[-1], y=y[-1]), fontsize=11)
            plt.title(request_data[2]+"の感染者数", fontname="MS Gothic")
            plt.xticks(nx, rotation=60)
            plt.ylabel("感染者数", fontname="MS Gothic")
            plt.xlabel("日付", fontname="MS Gothic")
            fig.savefig("tmp.png")
            image_file = discord.File("tmp.png")

            await ctx.send(file=image_file)
            os.remove("tmp.png")

def setup(bot):
    bot.add_cog(Covid(bot))
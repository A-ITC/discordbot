from discord.ext import commands
import discord
import config
import sys
import asyncio 
import requests
import csv

#ファイルに保存する情報（過去に何人ボイスチャンネルに入ったかなど）
class SaveData:
    def __init__(self):
        self.name=""#パラメータの名前
        self.value=None#保存される値

#実績クラスのインターフェース
class IAchievement:
    def __init__(self):
        self.accomplished=False#達成できたか
        self.img_url=""#実績のアイコンURL
        self.title=""#実績の名前
        self.description=""#詳しい説明
    def check(self):#実績達成状況の確認
        pass

#セーブデータ書き込み
def write(path):
    with open(path, 'w') as f:
        writer = csv.writer(f)

class AchievementCog(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def achievement(self,ctx):
        self.count+=1

def setup(bot):
    bot.add_cog(AchievementCog(bot))
from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 
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
    "name": "おみくじ",
    "description": "おみくじをひく",
}

# For authorization, you can use either your bot token 
headers = {
    "Authorization": f"Bot {config.TOKEN}"
}

#r = requests.post(config.SLASH_URL, headers=headers, json=json)
#print(r.json())
class Omikuji(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def おみくじ(self,ctx):
        self.count+=1
        omikujis=[
            ("大凶","今日は運勢がかなり悪いようです。今まで後回しにしてきたつけが回ってきたり、変なトラブルに見舞われるでしょう。寝坊に気を付けよう。"),
            ("凶","運勢がちょっと不安ですね。不安があれば家でゆっくり休むといいかもしれません。お腹を壊さないよう注意。"),
            ("小凶","運のめぐりがアレなことになってます。頑張れ。"),
            ("末吉","特にいうことのない平凡な運勢です。でも何も起こらないことが幸せなこともあります。"),
            ("吉","今日はラッキーになりそうな予感！外を歩くと新しい発見があるかもしれません。"),
            ("大吉","今日は運という運があなたを味方しています。街中を歩くだけで天変地異が起こる勢いでしょう。"),
            ("ばなな","フルーツでも食べて元気だしましょう。健康がいちばん"),
            ("単位","あなたの行動が今後大きな結果を巻き起こすでしょう。落とすも取るもあなた次第"),
            ("酒池肉林","今日はぜいたくをするとなにやらいいことが起こりそうです！"),
            ("爆死","もう何もいうまい"),
            ("404","Not found"),
            ("Segementation fault","internal error"),
            ]
        rucky_items=[
            ("リンゴ","甘酸っぱい味が脳を刺激し、柔軟な発想が得られるかも"),
            ("カレー","食欲をそそるスパイスの香りが気分転換にいいかも？異国情緒を味わおう！"),
            ("地球","母なる大地"),
            ("無",""),
            ("テンキー","持ち歩くと意外なところで役に立つかも？"),
            ("ピーナッツ","ミネラルを補給することでうんぬんかんぬん"),
            ("信号機","三色の色鮮やかな光があなたを照らしてくれます"),
            ("サラダチキン","ヘルシーでおいしい"),
            ("炭酸水","色々なものと混ぜるとより効果的"),
            ("ラーメン","とんこつスープを飲みあったまるとリフレッシュできます。"),
            ("エスカルゴ","サイゼリヤにあるやつ"),
            ("マイクスタンド","遠隔授業に備えて音響機材を整えよう！"),
            ("???","えっ…？"),
            ("インド映画","踊りを見て気分を変えましょう"),
            ("ヨガ","運動をすることでストレスを発散してみましょう"),
            ("みたらし団子","スイーツおいしい"),
            ("馬","乗るもよし、賭けるもよし"),
            ("ボードゲーム","大勢で遊んでください。"),
        ]

        omikuj=random.choice(omikujis)
        item=random.choice(rucky_items)
        text=f"あなたの運勢は…{omikuj[0]}。{omikuj[1]}\nラッキーアイテムは{item[0]}！{item[1]}"
        async with ctx.channel.typing():
            await ctx.reply(text)

        
def setup(bot):
    bot.add_cog(Omikuji(bot))
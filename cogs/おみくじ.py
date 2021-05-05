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
        unsei=["大吉","吉","末吉","小凶","凶","大凶"]
        omi_color=["🟥","🟧","🟨","🟩","🟦","🟪"]
        color_codes=[0xe23d2e,0xdb740d,0xd5d11d,0x20d017,0x1c74e0,0x4c10c6]
        omikujis=[
            (5,"もう何もいうまい"),
            (5,"今日死にます。"),
            (5,"今日は運勢がかなり悪いようです。今まで後回しにしてきたつけが回ってきたり、変なトラブルに見舞われるでしょう。寝坊に気を付けよう。"),
            (4,"少し調子の悪い日になりそうです。気分転換をおススメします。"),
            (4,"運勢がちょっと不安ですね。不安があれば家でゆっくり休むといいかもしれません。お腹を壊さないよう注意。"),
            (4,"通学中イヤホンを落とす確率が上がっています。"),
            (4,"あなたの行動が今後大きな結果を巻き起こすでしょう。"),
            (4,"日常生活に支障はあまりありませんが、様子をみましょう。"),
            (3,"これって悪いのか悪くないのか微妙なラインですよね。"),
            (3,"運のめぐりがアレなことになってます。頑張れ。"),
            (3,"安静にしててください。"),
            (2,"小吉と末吉ってどっちが良いんですか。"),
            (2,"特にいうことのない平凡な運勢です。でも何も起こらないことが幸せなこともあります。"),
            (2,"無くしものに注意。探すのをやめたとき見つかることもよくある話です。"),
            (2,"フルーツでも食べて元気だしましょう。健康がいちばん"),
            (1,"ラッキーな一日が訪れます。普段通らない道を通ると思わぬ発見があるかも。"),
            (1,"良さげな日になりそうです。"),
            (1,"今日はラッキーになりそうな予感！外を歩くと新しい発見があるかもしれません。"),
            (1,"アイスを買うともれなくおまけがついてくる。"),
            (1,"今日はぜいたくをするとなにやらいいことが起こりそうです！"),
            (0,"今日は運という運があなたを味方しています。街中を歩くだけで天変地異が起こる勢いでしょう。"),
            (-1,"400","Bad request"),
            (-1,"403","Forbidden"),
            (-1,"404","Not found"),
            (-1,"408","Request timeout"),
            (-1,"500","Internal server error"),
            (-1,"502","Bad gateway"),
            (-1,"Sorry! :(","This page has been deleted."),
            (-1,"Segementation fault","internal error"),
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

        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title=f"おみくじ")
        # Embed の表示色を青色に設定
        omikuj=random.choice(omikujis)
        item=random.choice(rucky_items)
        omi_num=omikuj[0]
        if omi_num==-1:
            embed.color = 0x777777
            embed.add_field(name=f"あなたの運勢は…", value=f"{omikuj[1]}\n{omikuj[2]}",inline=False)
        else:
            embed.color = color_codes[omi_num]
            embed.add_field(name=f"あなたの運勢は…", value=f"{omi_color[omi_num]}{unsei[omi_num]}{omi_color[omi_num]}\n{omikuj[1]}",inline=False)
            embed.add_field(name="ラッキーアイテム",value=f"**{item[0]}** {item[1]}",inline=False)
            embed.set_thumbnail(url=f"https://www.ed.tus.ac.jp/tusitclub/discord/om{omi_num}.png")
        async with ctx.channel.typing():
            await ctx.reply(embed=embed)
        
def setup(bot):
    bot.add_cog(Omikuji(bot))
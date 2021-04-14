from discord.ext import commands
import discord
import config
import sys
import asyncio 

class Man(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.command()
    async def man(self,ctx):#helpだと標準ライブラリであるらしくエラーになる
        self.count+=1
        # 受け取ったメッセージの内容を使って返信
        embed = discord.Embed(title="マニュアル")
        # Embed の表示色を青色に設定
        embed.color = config.EMBED_COLOR
        #embed.add_field(name="!client_app_info", value="このBOTについての情報を表示します",inline=False)
        #embed.add_field(name="!count_members <role>", value="対象となるロールのメンバー数を表示します",inline=False)
        embed.add_field(name="!get_roles", value="このサーバーでの各ロールのメンバー数を表示します",inline=False)
        embed.add_field(name="!guild_info", value="このサーバーの情報を表示します",inline=False)
        embed.add_field(name="!man", value="このBOTのコマンドを説明します",inline=False)
        #embed.add_field(name="!member_info <member>", value="対象となるアカウントの情報を表示します",inline=False)
        embed.add_field(name="!member_send <member> <content>", value="対象となるアカウントにDMを送信します",inline=False)
        #embed.add_field(name="!reload <module_name>", value="コマンドのスクリプトを更新します。cogs.コマンド名と入力してください。",inline=False)
        #embed.add_field(name="!stop", value="BOTを停止させます",inline=False)
        embed.add_field(name="!おみくじ", value="おみくじをひける",inline=False)
        embed.add_field(name="!ほめる", value="ほめる",inline=False)
        async with ctx.channel.typing():
            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Man(bot))
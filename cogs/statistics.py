from discord.ext import commands
import discord
import config
import sys
import asyncio 
import requests
import csv
import os
import shutil
from discord.ext import tasks

class Statistics(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.vc=None
        self.channel=None

    @commands.group()
    async def stat(self, ctx ):
        if ctx.invoked_subcommand is None:
            await ctx.reply('無効なコマンドです')

    @stat.command()
    async def online(self,ctx):
        dir="data"
        path=f"{dir}/{ctx.guild.name}.csv"
        await ctx.reply("ファイルを出力します",file=discord.File(path))

    @stat.command()
    async def clear(self,ctx):
        dir="data"
        path=f"{dir}/{ctx.guild.name}.csv"
        os.remove(path)
        await ctx.reply("このサーバーについての統計データを削除しました")
        
    @stat.command()
    async def count_reaction(self,ctx,channel_):
        channel=channel_
        if type(channel)is type(None):
            channel=ctx.channel
        else:
            channel=channel_.strip("<#>")
            channel=ctx.guild.get_channel(int(channel))
        user_data={}
        async with ctx.channel.typing():
            async for message in channel.history(limit=200):
                for reaction in message.reactions:
                    async for user in reaction.users():
                        if user.name not in user_data: user_data[user.name]=0
                        user_data[user.name]+=1
            res=""
            for key,value in user_data.items():
                res+=f"{key}    :    {value}\n"
            await ctx.reply(res)
    @stat.command()
    async def count_message(self,ctx,channel_):
        channel=channel_
        if type(channel)is type(None):
            channel=ctx.channel
        else:
            channel=channel_.strip("<#>")
            channel=ctx.guild.get_channel(int(channel))
        user_data={}
        async with ctx.channel.typing():
            async for message in channel.history(limit=200):
                if message.author not in user_data: user_data[message.author]=0
                user_data[message.author]+=1
            res=""
            for key,value in user_data.items():
                res+=f"{key}    :    {value}\n"
            await ctx.reply(res)

    @stat.command()
    async def delete_account_data(self,ctx,path):
        shutil.rmtree(path)

    @stat.command()
    async def count_online(self,ctx):
        res=""
        for role in ctx.guild.roles:
            if role.hoist:#そのロールが他のロールと分けて表示に設定されてたら
                online_count=0
                print(len(role.members))
                for member in role.members:
                    if member.status == discord.Status.online:online_count+=1
                res+=f"{role.name}のオンライン {online_count}人\n"
                print(online_count)
        await ctx.reply(res)

def setup(bot):
    bot.add_cog(Statistics(bot))

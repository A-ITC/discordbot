from discord.ext import commands
import discord
import config
import sys
import asyncio 
import requests
from json import dumps
from urllib.request import Request, urlopen

class RetrieveIDs(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
                
    @commands.is_owner()
    @commands.command()
    async def retrieve_ids(self, ctx):#cogs.***としないとエラー
        data = {}
        await ctx.send("データを取得")
        for member in ctx.guild.members:
            data[member.id]=[]
            for role in member.roles:
                if role.name=="@everyone":continue
                data[member.id].append(
                    {
                        "name":role.name,
                        "color":role.color.value
                    }
                )
        urlopen(Request(
            'https://qqhitvdf6b.execute-api.ap-northeast-1.amazonaws.com/itcobkai/external',
            dumps(data).encode(),
            {'Content-Type': 'application/json'}
        ))
        await ctx.send(data)
        
def setup(bot):
    bot.add_cog(RetrieveIDs(bot))


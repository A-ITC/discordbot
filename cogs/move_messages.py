from discord.ext import commands
import discord
import config
import sys
import asyncio 

import requests
import utility
from datetime import datetime, timedelta, timezone

class MoveMessages(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0

    @commands.command()
    async def move_messages(self,ctx,form_channel_,to_channel_,target_reaction_):
        self.count+=1
        form_channel=form_channel_
        if type(form_channel)is type(None):
            form_channel=ctx.channel
        else:
            form_channel=form_channel.strip("<#>")
            form_channel=ctx.guild.get_channel(int(form_channel))
        to_channel=to_channel_.strip("<#>")
        to_channel=ctx.guild.get_channel(int(to_channel))
        JST=timedelta(hours=+9)
        await ctx.reply("履歴を取得中...")
        async for message in form_channel.history(limit=200):
            for reaction in message.reactions:
                if reaction.emoji==target_reaction_:
                    create_time=message.created_at+JST
                    time_str=create_time.strftime('%y/%m/%d %H:%M:%S')
                    sent_msg=await to_channel.send(f"{time_str} {message.author.mention}から\n{message.content}")
                    await sent_msg.add_reaction(target_reaction_)
        await ctx.reply("完了しました")
    
def setup(bot):
    bot.add_cog(MoveMessages(bot))
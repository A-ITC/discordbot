from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 

class Stop(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.count=0
                
    @commands.is_owner()
    @commands.command()
    async def stop(self,ctx,option=None):
        self.count+=1
        texts=[
            "ミ゜（絶命）",
            "Botを終了します。",
            "さよなら…さよなら…",
            "😴",
            "👋",
            "Bot has been stoped.",
            "Farewell, everyone",
            "Bot休止了",
            "死にたくない…死にたくない…",
            "Sleeping",
            "ぐあああああっ"
            ]
        try:
            if type(option)==type(None):
                sent_msg=await ctx.reply("Botを停止させますか？")
                await sent_msg.add_reaction("✅")
                await sent_msg.add_reaction("❌")
                def reaction_check(reaction_, user_):
                    is_author=user_==ctx.author
                    are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
                    return are_same_messages and is_author
                emoji = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=180)
                if emoji[0].emoji=="✅":
                    await ctx.reply(random.choice(texts))
                    await self.bot.close()
                elif emoji[0].emoji=="❌":
                    await ctx.reply("キャンセルします。")
            else:
                await ctx.reply(random.choice(texts))
                await self.bot.close()
        except asyncio.TimeoutError:
            await ctx.send(f"タイムアウトしました。")
        #await self.bot.logout()
        
def setup(bot):
    bot.add_cog(Stop(bot))
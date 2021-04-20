from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 

async def yes_no(bot,ctx,text,yes_func,no_func,timeout=300):
    sent_msg=await ctx.reply(text)
    await sent_msg.add_reaction("✅")
    await sent_msg.add_reaction("❌")
    def reaction_check(reaction_, user_):
        is_author=user_==ctx.author
        are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
        return are_same_messages and is_author
    emoji = await bot.wait_for('reaction_add', check=reaction_check, timeout=timeout)
    if emoji[0].emoji=="✅":
        await yes_func()
    if emoji[0].emoji=="❌":
        await no_func()

async def yes_no_cancel(bot,ctx,text,yes_func,no_func,cancel_func,timeout=300):
    sent_msg=await ctx.reply(text)
    await sent_msg.add_reaction("✅")
    await sent_msg.add_reaction("♻")
    await sent_msg.add_reaction("❌")
    def reaction_check(reaction_, user_):
        is_author=user_==ctx.author
        are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
        return are_same_messages and is_author
    emoji = await bot.wait_for('reaction_add', check=reaction_check, timeout=timeout)
    if emoji[0].emoji=="✅":
        await yes_func()
    if emoji[0].emoji=="♻":
        await cancel_func()
    if emoji[0].emoji=="❌":
        await no_func()
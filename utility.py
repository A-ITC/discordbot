from discord.ext import commands
import discord
import config
import sys
import asyncio 
import random 

async def check_yes_no(bot,ctx,message,timeout=300):
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    def reaction_check(reaction_, user_):
        is_author=user_==ctx.author
        are_same_messages = reaction_.message.channel == message.channel and reaction_.message.id == message.id
        return are_same_messages and is_author
    emoji = await bot.wait_for('reaction_add', check=reaction_check, timeout=timeout)
    if emoji[0].emoji=="✅":
        return True
    if emoji[0].emoji=="❌":
        return False
    return None
async def check_yes_no_cancel(bot,ctx,message,timeout=300):
    await message.add_reaction("✅")
    await message.add_reaction("♻")
    await message.add_reaction("❌")
    def reaction_check(reaction_, user_):
        is_author=user_==ctx.author
        are_same_messages = reaction_.message.channel == message.channel and reaction_.message.id == message.id
        return are_same_messages and is_author
    emoji = await bot.wait_for('reaction_add', check=reaction_check, timeout=timeout)
    if emoji[0].emoji=="✅":
        return 1
    if emoji[0].emoji=="♻":
        return -1
    if emoji[0].emoji=="❌":
        return 0
    return None

async def yes_no(bot,ctx,text,timeout=300):
    sent_msg=await ctx.reply(text)
    await sent_msg.add_reaction("✅")
    await sent_msg.add_reaction("❌")
    def reaction_check(reaction_, user_):
        is_author=user_==ctx.author
        are_same_messages = reaction_.message.channel == sent_msg.channel and reaction_.message.id == sent_msg.id
        return are_same_messages and is_author
    emoji = await bot.wait_for('reaction_add', check=reaction_check, timeout=timeout)
    if emoji[0].emoji=="✅":
        return True
    if emoji[0].emoji=="❌":
        return False
    return None
        
async def yes_no_cancel(bot,ctx,text,timeout=300):
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
        return 1
    if emoji[0].emoji=="♻":
        return -1
    if emoji[0].emoji=="❌":
        return 0
    return None

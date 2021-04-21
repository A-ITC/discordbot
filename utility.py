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

#そのmemberがrolesをすべて持っていたらtrue
def check_condition(member,roles):
    if len(roles)==0:return False
    for i in roles:
        if i not in member.roles:return False
    return True

#そのギルド内のメンバーで、targetsリストにあるロールすべて持っているメンバーを返す
#targetsにメンバーが含まれている場合、そのメンバー＋指定ロールを持っている人となる
def get_targets(guild,targets):
    target_roles=[]
    target_members=[]
    target_mentions=[]
    for target in targets:
        id=target.strip("<!&@>")#argはroleもしくはmember がstr形式で送られてくるので、id(int)を抽出する
        role_=guild.get_role(int(id))
        member_=guild.get_member(int(id))
        if type(role_) is not type(None):#指定がロールのとき
            target_roles.append(role_)
            target_mentions.append(role_.mention)
        elif type(member_) is not type(None):#指定がメンバーのとき
            target_members.append(member_)
            target_mentions.append(member_.mention)
    for member in guild.members:
        if check_condition(member,target_roles):
            if member not in target_members:#すでに入ってたら２重に送信しないようスキップ
                target_members.append(member)
    return target_members,target_mentions
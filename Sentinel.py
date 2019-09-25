import discord
import json
from discord import Game
from discord.ext import commands
import random
import asyncio
import datetime, time

with open('config.json') as f:
    config = json.load(f)
    f.close()

with open('intro.json') as f_data:
     intro = json.load(f_data)
     f_data.close()

TOKEN = config["token"]
BOT_PREFIX = config["prefix"]

bot = commands.Bot(command_prefix=BOT_PREFIX)
start_time = time.time()

#--------------------------------------------#
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------')
    bot.loop.create_task(status_task())

#--------------------------------------------#
async def status_task():

    status_messages = config["status_messages"]

    while True:

        status_num = random.randint(0, len(status_messages) - 1)
        new_status = status_messages[status_num]
        await bot.change_presence(activity=Game(name=new_status))

        await asyncio.sleep(300)

#---------------------------------------------#
@bot.command(name='stop')
async def stop(ctx):

    role = discord.utils.get(ctx.guild.roles, name="Moderator")
    m = ctx.message.author
    if m.guild_permissions.administrator or role in m.roles:
        await bot.close()
    else:
        return

#---------------------------------------------#
@bot.command(name='uptime',
            aliases=['up', 'Uptime', 'Up'])
async def uptime(ctx):

    current_time = time.time()
    uptime = int(round(current_time - start_time))
    await ctx.send("Uptime: {}".format(str(datetime.timedelta(seconds=uptime))))

#---------------------------------------------#

@bot.command(name='source',
            aliases=['sc', 'sourcecode'])
async def source(ctx):

    await ctx.send("https://github.com/crewsz96/Sentinel")

#----------------------------------------------#
@bot.command(name='addrole',
            aliases=['add', 'addRole', 'AddRole', 'Add'])
async def addrole(ctx):
    if ctx.channel.name != 'role-requests':
        return

    valid_roles = config["valid_roles"]
    msg = ctx.message
    entered_role = ctx.message.content.split(' ', 1)[1]
    member = ctx.author
    role = discord.utils.get(ctx.guild.roles, name=entered_role)

    if role == None or role.name not in valid_roles:
        bot_msg = await ctx.send("Invalid Role {0.message.author.mention}, roles you are able to add are: \n`\"UNIST\" \"DBFZ\", \"BBTAG\", \"MK11\", \"GG\", \"SVF\"`".format(ctx))
    else:
        await member.add_roles(role)
        bot_msg = await ctx.send('I\'ve given {0.message.author.mention} the role **{1.name}**'.format(ctx, role))

    await asyncio.sleep(10)
    await msg.delete()
    await bot_msg.delete()
#----------------------------------------------#
@bot.command(name='removerole',
            aliases=['Removerole', 'RemoveRole', 'removeRole','Rm', 'rm', 'rM', 'remove'])
async def removerole(ctx):
    if ctx.channel.name != 'role-requests':
        return

    msg = ctx.message
    entered_role = ctx.message.content.split(' ', 1)[1]
    member = ctx.author
    role = discord.utils.get(ctx.guild.roles, name=entered_role)

    if role == None:
        bot_msg = await ctx.send("Invalid Role {0.message.author.mention}, roles avaiable to remove are: \n`\"UNIST\" \"DBFZ\", \"BBTAG\", \"MK11\", \"GG\", \"SVF\"`".format(ctx))
    elif role not in ctx.author.roles:
        bot_msg = await ctx.send("{0.message.author.mention} You do not have this role.".format(ctx))
    else:
        await member.remove_roles(role)
        bot_msg = await ctx.send('I\'ve removed the role **{0.name}** from {1.message.author.mention} '.format(role, ctx))

    await asyncio.sleep(10)
    await msg.delete()
    await bot_msg.delete()

#----------------------------------------------#
@bot.command(name='itbelikethat',
            aliases=['belike','itbe'])
async def itbelikethat(ctx):

    await ctx.send(file=discord.File('itbelikethat.mp4'))

#----------------------------------------------#
@bot.command(name='jp')
async def jp(ctx):

    await ctx.send(file=discord.File('jp.jpg'))

#----------------------------------------------#
@bot.command(name='divide')
async def divide(ctx):

    char = ctx.message.content.split(' ', 1)[1]

    text = {}
    for obj in intro:
        if obj['Character'].upper() == char.upper():
            text = obj
            break

    if text == {}:
        await ctx.send("That character doesn't exist.")
    else:
        msg = text['Intro']
        await ctx.send('**{0}**\n`{1}`'.format(char, msg))


#----------------------------------------------#
# Greets members when they join the server.
@bot.event
async def on_member_join(member):

    channel = member.guild.get_channel(569976242028150832)

    await channel.send('Hello ' + member.mention + '! Please take a moment to look at ' + member.guild.get_channel(618960796743106580).mention + '.')
#----------------------------------------------#
@bot.command(name='piano',
            aliases=['giogio','GioGio', 'Giorno', 'giorno'])
async def piano(ctx):

    await ctx.send(file=discord.File('345.mp4'))
#----------------------------------------------#
# @bot.command(name='momma',
#             aliases=['moms', "mom", "ma"])
# async def momma(ctx):
#
#     member = ctx.author.nick
#     await ctx.send('{0}'.format(member))
#
#     try: # If the goon exists
#
#         tmp = data[member]
#         data[member] = str(int(data[member], 10))
#         f_data
#         f_data.dump(data)
#
#     except (KeyError, AttributeError): # If we need to create a new goon
#         await ctx.send("Error")
#
#     await ctx.send('Momma count for {0.mention} is {1}'.format(member, tmp))


#----------------------------------------------#
bot.run(TOKEN)

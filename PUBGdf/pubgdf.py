import discord
from discord.ext import commands
import yaml, operator, asyncio

client = discord.Client()
client = commands.Bot(command_prefix='?', description='pubg')

deaths = {}
title =["Daenerys of the House Targaryen", "The First of Her Name", "The Unburnt", "Queen of the Andals", "The Rhoynar and the First Men", "Queen of Meereen", "Khaleesi of the Great Grass Sea", "Protector of the Realm", "Lady Regnant of the Seven Kingdoms", "Breaker of Chains and Mother of Dragons"]

with open('config.yml') as f:
    config = yaml.load(f.read())
deaths = config

@client.command()
async def danny():
    for s in title:
        await client.say(s)
        await asyncio.sleep(1)

@client.command(pass_context=True)
async def leaderboard(ctx):
    await client.say(ctx.message.author.mention + getLeaderboard())

@client.command(pass_context=True)
async def donkey(ctx):
    await client.say(ctx.message.author.mention + ' The current donkey is {}'.format(max(deaths.items(), key=operator.itemgetter(1))[0]))

@client.command(pass_context=True)
async def died(ctx, who : str, *num : str):
    lax = hasPerm(ctx.message.author.id)
    if not lax:
        return
    if who.title() in deaths and not num:
        deaths[who.title()] = deaths.get(who.title())+1
        saveFile()
        await client.say(ctx.message.author.mention + " Updated" + getLeaderboard())
        return
    if num[0].lstrip("-").isdigit() and who.title() in deaths:
        number = int(num[0])
        if number > 0:
            deaths[who.title()] = deaths.get(who.title())+number
        else:
            deaths[who.title()] = deaths.get(who.title())-abs(number)
        saveFile()
        await client.say(ctx.message.author.mention + " Updated" + getLeaderboard())

def getLeaderboard():
    leaderboard = "\n``` Who Died First - Leaderboard \n\n"
    for key, value in deaths.items():
        leaderboard += '{0:6}| {1}\n'.format(key, value)
    leaderboard += "\n```"
    return leaderboard

def hasPerm(userID):
    return userID == '171458204167831552'

def saveFile():
    with open('config.yml', 'w') as outfile:
        yaml.dump(deaths, outfile, default_flow_style=False)

@client.event
async def on_ready():
    print("Running version 0.1")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_status(game=discord.Game(name='PUBG'))

client.run('TOKEN HERE')

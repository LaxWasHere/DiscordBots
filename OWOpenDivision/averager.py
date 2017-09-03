import discord
from discord.ext import commands
import requests, asyncio, re, json
from bs4 import BeautifulSoup

client = discord.Client()
client = commands.Bot(command_prefix='!', description='Averages Teams SR')


@client.command(pass_context=True)
async def average(ctx, id : str):
    if len(id) is not 8 or not id.isdigit():
        await client.say("!average TeamId")
        return
    await client.say(ctx.message.author.mention + " Averaging team, this may take awhile")
    formatted = getFormmated(id)
    await client.say(ctx.message.author.mention + formatted)


def getFormmated(id):
    testurl = "https://play.eslgaming.com/team/members/{}/".format(id) #11430231
    try:
        req = requests.get(testurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'})
        req.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        return "Could not find team"
    soup = BeautifulSoup(req.text, "lxml")
    table = soup.find("table")
    name = soup.title.string

    response = "```\n"+ name.split("|")[0] + "Members\n"
    response += "https://play.eslgaming.com/team/{}/".format(id)+"\n\n"

    rows=list()
    for row in table.findAll("div"):
        for s in re.split("\t", row.text):
            ns = s.rstrip("\n")
            if "#" in ns and ns not in rows and len(ns) < 20:
                rows.append(ns)

    i = 0
    rowlen = len(rows)
    for players in rows:
        rank = getRank(players)
        if rank is not '0': #Just put band aids everywhere.
            i += int(rank)
            response += '{0:17}  {1}'.format(players, "Rank: "+rank+"\n")
        else:
            rowlen -= 1
            response += '{0:17}  {1}'.format(players, "Rank: Unranked\n")
    response += "\nTeam Average: " + str(int(i / rowlen))+"\n```"
    return response


def getRankOwApi(user): #This should be faster, who knows
    print("Requesting OWAPI rank for " + user)
    url = "https://owapi.net/api/v3/u/{}/blob".format(user.replace("#","-"))

    try:
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        req.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print("Could not find stats " + str(e)) #What's the point of an API if you have a shitty rate limit
        return getRank(user)
    if json.loads(req.text)["us"] is not None:
        return str(json.loads(req.text)["us"]["stats"]["competitive"]["overall_stats"]["comprank"]) #¯\_(ツ)_/¯
    else:
        return getRank(user)


def getRank(user):
    print("Requesting Vanilla rank for " + user)
    url = "https://playoverwatch.com/en-us/career/pc/us/{}".format(user.replace("#","-"))

    try:
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        req.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print("Could not find stats " + str(e))
        return "0"
    try:
        soup = BeautifulSoup(req.text, "lxml")
        stuff = soup.find_all(attrs={'class': 'u-align-center h6'})
        return stuff[0].text
    except IndexError:
        return getRankOverbuff(user) #Use backup site if player has not played a game in the current season


def getRankOverbuff(user):
    print("Requesting overbuff rank for " + user)
    url = "https://www.overbuff.com/players/pc/{}".format(user.replace("#","-"))

    try:
        req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        req.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print("Could not find stats " + str(e))
        return "0"
    try:
        soup = BeautifulSoup(req.text, "lxml")
        stuff = soup.find_all(attrs={'class': 'color-stat-rating'})
        return stuff[0].text
    except IndexError:
        return str(1) #Return 1 if player has never played any competitive game


@client.event
async def on_ready():
    print("Running version 0.1")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name="OW Open Division"))
    print('Status OK')


def main():
    client.run('TOKEN HERE')

if __name__ == '__main__':
    main()

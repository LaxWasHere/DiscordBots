import discord
from discord.ext import commands
import asyncio

client = discord.Client()
client = commands.Bot(command_prefix='?', description='Baenerys')
running = False

title = ["Daenerys Stormborn of House Targaryen.", "Rightful heir to the Iron Throne.", "Rightful Queen to the Andals and First Men.", "Protector of the Seven Kingdoms.", "The Mother of Dragons.", "The Khaleesi of the Great Grass Sea.", "The Unburnt.", "The Breaker of Chains."]


@client.command()
async def baenarys():
    for s in title:
        await client.say(s)
        await asyncio.sleep(1.5)

@client.command(pass_context=True)
async def danny(ctx):
    try:
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await client.say('You are not in a voice channel.')
        else:
            voice = await client.join_voice_channel(summoned_channel)
            player = voice.create_ffmpeg_player('assets/Baenerys.mp3')
            player.start()
            while player.is_playing():
                pass
            await voice.disconnect()
    except discord.ClientException as e:
        print(e)


@client.event
async def on_ready():
    print("Running version 0.1")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name="A Game of Thrones"))
    print('Status OK')


def main():
    client.run('TOKEN HERE')

if __name__ == '__main__':
    main()

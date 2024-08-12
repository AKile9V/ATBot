import discord
import APIKeys
import os
import asyncio
from discord.ext import commands
import os
# sys.path.append("./cogs/")

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix='#', intents=intents)


@client.event
async def on_ready():
    print("I'm here!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='the Hall of Fame'))


async def load_client_extensions():
    # for filename in os.listdir('./GreenBot/cogs'):
    client.remove_command('help')
    cogsPth = os.path.join(".", "cogs")
    for filename in os.listdir(cogsPth):
        if filename.endswith('.py'):
            await client.load_extension("cogs." + filename[:-3])


async def main():
    async with client:
        client.loop.create_task(load_client_extensions())
        await client.start(APIKeys.BOT_TEST_TOKEN)

asyncio.run(main())

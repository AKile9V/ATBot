from discord.ext import commands, tasks
import discord
from Wow import *
import os
import json
from Util import *


class Timed(commands.Cog):

    def __init__(self, client):
        self.client = client

    @tasks.loop(hours=2)
    async def player_guild_rank_check(self):
        message_cog = self.client.get_cog("Messages")
        with open("TemporaryAlbinos.json", 'r', encoding="utf-8") as fp:
            data = json.load(fp)
        for albino in data["temp_albinos"]:
            user = await self.client.fetch_user(albino["author"])
            head_url, url_name = os.path.split(albino["url"])
            found_member = await message_cog.check_rank(url_name, user)
            if found_member:
                remove_from_json("TemporaryAlbinos.json", "temp_albinos", "url", albino["url"])

    @commands.command()
    async def checkalbinos(self, ctx):
        only_officers(ctx)
        await self.player_guild_rank_check()


async def setup(client):
    await client.add_cog(Timed(client))

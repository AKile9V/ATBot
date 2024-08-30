from Util import remove_from_json, add_to_json
from discord.ext import commands
from discord import Streaming as st
from objectIds import regular_bot_channel, offtopic_channel
import discord
import json


class Streaming(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        message_cog = self.client.get_cog("Messages")
        with open("Streamers.json", 'r', encoding="utf-8") as fp:
            data = json.load(fp)
        found = False

        for streamer_data in data["streamers"]:
            if before.id == streamer_data["id"]:
                found = True
                break
        if before.activity == after.activity or not found:
            return
        
        if isinstance(after.activity, st):
            await message_cog.make_embed(str(after.nick) + " je počeo da strima!", "", str(after.activity.url), discord.Color.dark_green(), send_channel = offtopic_channel)
        return

    @commands.command()
    async def addstream(self, ctx):
        message_cog = self.client.get_cog("Messages")
        member_id = ctx.author.id
        with open("Streamers.json", 'r', encoding="utf-8") as fp:
            data = json.load(fp)
        for streamer_data in data["streamers"]:
            if member_id == streamer_data["id"]:
                return

        add_to_json("Streamers.json", "streamers", {"id" : member_id})
        await message_cog.make_embed("Dodat si na listu streamer-a!", "", "", discord.Color.dark_green(), delete_after_time=15, send_channel = regular_bot_channel)

    @commands.command()
    async def removestream(self, ctx):
        message_cog = self.client.get_cog("Messages")
        member_id = ctx.author.id
        remove_from_json("Streamers.json", "streamers", "name", member_id)
        await message_cog.make_embed("Skinut si sa liste streamer-a!", "", "", discord.Color.dark_green(), delete_after_time=15, send_channel = regular_bot_channel)


async def setup(client):
    await client.add_cog(Streaming(client))

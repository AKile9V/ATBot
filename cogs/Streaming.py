from Util import only_officers, remove_from_json, add_to_json
from discord.ext import commands
from discord import Streaming as st
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
            if str(before.nick) == streamer_data["name"]:
                found = True
                break
        if before.activity == after.activity and not found:
            return
        # embed_title, field_name, field_value, color, message = ""
        if isinstance(after.activity, st):
            await message_cog.make_embed(str(after.nick) + " je počeo da strima!", "", str(after.activity.url), discord.Color.dark_green())
        return

    @commands.command()
    async def addstream(self, ctx):
        message_cog = self.client.get_cog("Messages")
        member = ctx.author.nick
        with open("Streamers.json", 'r', encoding="utf-8") as fp:
            data = json.load(fp)
        for streamer_data in data["streamers"]:
            if str(member) == streamer_data["name"]:
                print("found ya")
                return
            
        add_to_json("Streamers.json", "streamers", "name", member)
        await message_cog.make_embed("Dodat si na listu streamer-a!", "", "", discord.Color.dark_green(), delete_after_time = 15)

    @commands.command()
    async def removestream(self, ctx):
        message_cog = self.client.get_cog("Messages")
        member = ctx.author.nick
        remove_from_json("Streamers.json", "streamers", "name", member)
        await message_cog.make_embed("Skinut si sa liste streamer-a!", "", "", discord.Color.dark_green(), delete_after_time = 15)

async def setup(client):
    await client.add_cog(Streaming(client))
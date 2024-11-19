from discord.ext import commands
import discord
import os
import validators
from Roles import *
from objectIds import *
from ImportantMessages import *
from Util import *
from Wow import *
from datetime import datetime, timedelta
import urllib.parse
import os.path
from urllib.parse import unquote

class Messages(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def charinfo(self, url_path, author):
        full_url_path = url_path.path
        if full_url_path[-1] == '/':
            full_url_path = full_url_path[:-1]
        head_url, url_name = os.path.split(full_url_path)
        
        if await self.check_rank(url_name, author):
            return
        realm = os.path.split(head_url)
        user_guild_id = await get_character_guild(realm[1], url_name)
        if (user_guild_id == guild_id):
            add_to_json("TemporaryAlbinos.json", "temp_albinos",  {"url" : full_url_path , "author" : author.id})
            await self.send_dm_embed(author, warning_message, "", in_guild_but_slow_message, discord.Color.orange())
            member_in_server = await self.client.get_guild(test_guild).fetch_member(author.id)
            await member_in_server.edit(roles=[get_role_by_name(self.client.get_guild(test_guild), "Albino Frend")])
            return

        await self.send_dm_embed(author, failure_message, "", not_in_guild_message, discord.Color.brand_red())
        return

    async def check_rank(self, url_name, author):
        roster_json, roster_response = await get_roster()
        for member in roster_json["members"]:
            unqouted_url_name = unquote(url_name)
            if str.lower(member["character"]["name"]) == unqouted_url_name:
                if member["rank"] != 9:
                    await self.send_dm_embed(author, failure_message, "", already_exists_message, discord.Color.brand_red())
                else:  # dodaj rolu
                    member_in_server = await self.client.get_guild(test_guild).fetch_member(author.id)
                    await member_in_server.edit(roles=[get_role_by_name(self.client.get_guild(test_guild), "Albino")])
                    new_nick = unqouted_url_name.title()
                    clickable_officer = "<@&" + \
                        str(ImportantRoles["officer_id"])+">"
                    clickable_user = "<@"+str(member_in_server.id)+">"
                    await self.make_embed("", "", "(" + author.name + ")" + clickable_user + " je dobio/la Albino rolu!", discord.Color.dark_green(), clickable_officer)
                    await self.send_dm_embed(author, success_message, "", role_acquired_message, discord.Color.dark_green())
                    await member_in_server.edit(nick=new_nick)
                return True
        return False
        
    @commands.Cog.listener()
    async def on_message(self, message):
        member_in_server = await self.client.get_guild(test_guild).fetch_member(message.author.id)
        url_path = urllib.parse.urlparse(str.lower(message.content))
        with open("TemporaryAlbinos.json", 'r', encoding="utf-8") as fp:
            data = json.load(fp)
        
        if message.author.bot or member_in_server.get_role(Roles["Albino"]):
            return
        
        # for albino in data["temp_albinos"]:
        #     if str(url_path.path) == albino["url"]:
        #         return

        if isinstance(message.channel, discord.channel.DMChannel):
            url_hostname = url_path.hostname
            clickable_user = "<@"+str(member_in_server.id)+">"
            await self.make_embed("", "", "(" + message.author.name + ")" + clickable_user + " je poslao bot-u:\n\n" + message.content, discord.Color.brand_red())
            for albino in data["temp_albinos"]:
                if message.author.id == albino["author"]:
                    await self.send_dm_embed(message.author, warning_message, "", processing_user_message, discord.Color.orange())
                    return
            if not validators.url(message.content) and not url_hostname in armory_hostnames:
                await self.send_dm_embed(message.author, failure_message, "", invalid_url_message, discord.Color.brand_red())
                return

            await self.charinfo(url_path, message.author)
            return

    async def make_embed(self, embed_title, field_name, field_value, color, message="", send_channel=bot_report_channel, delete_after_time=None):
        embed = discord.Embed(title=embed_title, colour=color)
        embed.add_field(name=field_name, value=field_value, inline=True)
        await self.client.get_guild(test_guild).get_channel(send_channel).send(content=message, embed=embed, delete_after=delete_after_time)

    async def send_dm_embed(self, author, embed_title, field_name, field_value, color):
        embed = discord.Embed(title=embed_title, colour=color)
        embed.add_field(name=field_name, value=field_value, inline=True)
        await author.send(embed=embed)


async def setup(client):
    await client.add_cog(Messages(client))

from Roles import *
import discord
from discord.ext import commands
from objectIds import *
from Emojis import *
from ImportantMessages import *
import os
import json


class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print("Member "+str(member)+" left")

    # member is of type [member]
    async def dm(self, member, message):
        messages_cog = self.client.get_cog("Messages")
        await messages_cog.send_dm_embed(member, title_to_new, "", message, discord.Color.dark_green())

    # member is of type [member]
    async def dm_error(self, member, message):
        messages_cog = self.client.get_cog("Messages")
        await messages_cog.send_dm_embed(member, failure_message, "", message, discord.Color.brand_red())

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, rawReactionActionEvent):
        channel = self.client.get_channel(rawReactionActionEvent.channel_id)
        message = await channel.fetch_message(rawReactionActionEvent.message_id)
        member = rawReactionActionEvent.member
        emoji_name = rawReactionActionEvent.emoji.name
        emoji = rawReactionActionEvent.emoji
        guild = channel.guild

        if (rawReactionActionEvent.member.bot):
            return

        if (rawReactionActionEvent.message_id == role_message_id):
            for role in Roles:
                if EmojiToRole[str(emoji_name)] == "Albino" and role == "Albino":
                    if member.get_role(Roles["Albino"]):
                        return
                    await self.dm(member, send_to_new)
                    return
                if EmojiToRole[str(emoji_name)] == "Raider" and role == "Raider":
                    if member.get_role(Roles["Albino"]):
                        await member.add_roles(get_role_by_name(guild, role))
                    else:
                        await self.dm_error(member, albino_role_first_message)
                        return
                    return
                if EmojiToRole[str(emoji_name)] == role:
                    await member.add_roles(get_role_by_name(guild, role))
                    await member.remove_roles(get_role_by_name(self.client.get_guild(test_guild), "Intruder"))
            return

        if (rawReactionActionEvent.message_id == first_role_message_id):
            for role in Roles:
                if member.get_role(Roles["Albino"]) or member.get_role(Roles["Albino Frend"]):
                    return
                if EmojiToRole[str(emoji_name)] == role:
                    await member.add_roles(get_role_by_name(guild, role))
                    return
            return

        bedne_path = os.path.join(".", "BedneIgre.json")
        with open(bedne_path, "r+", encoding="utf-8") as file:
            bedne_info = json.load(file)

        if (rawReactionActionEvent.message_id == choose_bednu_igru_message):
            for role in bedne_info:
                if str(emoji) == str(role["emoji"]):
                    await member.add_roles(guild.get_role(int(role["role"])))
                    return
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, rawReactionActionEvent):
        channel = self.client.get_channel(rawReactionActionEvent.channel_id)
        message = await channel.fetch_message(rawReactionActionEvent.message_id)
        emoji_name = rawReactionActionEvent.emoji.name
        emoji = rawReactionActionEvent.emoji
        guild = channel.guild
        member = await guild.fetch_member(rawReactionActionEvent.user_id)

        if (rawReactionActionEvent.message_id == role_message_id):
            for role in Roles:
                if EmojiToRole[str(emoji_name)] == "Albino":
                    return
                if EmojiToRole[str(emoji_name)] == role:
                    await member.remove_roles(get_role_by_name(guild, role))
            return

        bedne_path = os.path.join(".", "BedneIgre.json")
        with open(bedne_path, "r+", encoding="utf-8") as file:
            bedne_info = json.load(file)

        if (rawReactionActionEvent.message_id == choose_bednu_igru_message):
            for role in bedne_info:
                if str(emoji) == str(role["emoji"]):
                    await member.remove_roles(guild.get_role(int(role["role"])))
                    return
            return


async def setup(client):
    await client.add_cog(User(client))

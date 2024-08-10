import discord
import heapq
import csv
import io
from objectIds import *
from Roles import *
from discord.ext import commands
from ImportantMessages import *
from Emojis import *
from discord.utils import get
from Wow import *
import requests
import json
import os
import random
from Util import only_officers


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # !hi command
    @commands.command()
    async def hi(self, ctx):
        only_officers(ctx)
        print('Hi command')
        await ctx.send("Hi, I'm ATbot!")

    @commands.command()
    async def say(self, ctx):
        only_officers(ctx)
    
    @commands.command()
    async def bye(self, ctx):
        only_officers(ctx)
        await ctx.send("Goodbye!")

    # !setup command
    @commands.command()
    async def setup(self, ctx):
        only_officers(ctx)
        return
    
    @commands.command()
    async def imalraida(self, ctx):
        imalraida_embed = discord.Embed(colour=discord.Color.dark_green())
        imalraida_embed.add_field(name = "", value = "Naravno", inline=True)
        await ctx.channel.send(embed = imalraida_embed)
    
    @commands.command()
    async def addwa(self, ctx, arg):
        only_officers(ctx)
        global weakaura_link
        weakaura_link = arg

    @commands.command()
    async def wa(self, ctx):
        await ctx.send(weakaura_link)

    @commands.command()
    async def get_name_from_sim(self, ctx, arg):
        r = requests.get(arg + "/data.json")
        json_object = json.loads(r.content)
        with open('govno.json', "w" , encoding="utf-8") as file:
            json.dump(json_object["sim"]["players"][0]["name"], file, indent=4)
            await ctx.send(json_object["sim"]["players"][0]["name"])

    @commands.command()
    async def dratojoke(self, ctx):
        jokes_path = os.path.join(".", "DratoJokes.json")
        with open(jokes_path, "r+" , encoding="utf-8") as file:
            jokes_info = json.load(file)
            
        joke = random.choice(jokes_info)
        joke_embed = discord.Embed(colour=discord.Color.dark_green())
        joke_embed.add_field(value = joke["question"] + "\n", name = "", inline=False)
        joke_embed.add_field(value = joke["answer"], name = "", inline=False)
        await ctx.channel.send(embed = joke_embed)

    async def manage_own_message(self, ctx, message):
        choose_bedna_igra_embed = message.embeds[0]

        bedne_path = os.path.join(".", "BedneIgre.json")
        with open(bedne_path, "r+", encoding="utf-8") as file:
            bedne_info = json.load(file)

        emoji_role_string = ""
        emoji_active = []
        for emoji_role in bedne_info:
            final_emoji = get(ctx.guild.emojis, name=emoji_role["emoji"]) or emoji_role["emoji"]
            emoji_role_string = emoji_role_string + additional_games_emoji_template_message.format(final_emoji, ctx.guild.get_role(int(emoji_role["role"])))
            await message.add_reaction(final_emoji)
            emoji_active.append(str(final_emoji))
            
        for emoji_reaction in message.reactions:
            if not str(emoji_reaction.emoji) in emoji_active:
                await message.clear_reaction(emoji_reaction)

        new_message = additional_games_message + emoji_role_string
        choose_bedna_igra_embed.clear_fields()
        choose_bedna_igra_embed.add_field(name = "", value = new_message, inline=True)
        await message.edit(embed = choose_bedna_igra_embed)

    #Napravi message za brianje rola
    @commands.command()
    async def bedneigre(self, ctx):
        only_officers(ctx)
        bedne_igre_embed = discord.Embed(title = additional_games_title_message,colour=discord.Color.dark_green())
        bedne_igre_embed.add_field(name = "", value = additional_games_message, inline=True)
        await ctx.guild.get_channel(choose_bednu_igru_channel).send(embed = bedne_igre_embed)


    @commands.command()
    async def updatebi(self, ctx):
        only_officers(ctx)
        await self.manage_own_message(ctx, await ctx.guild.get_channel(choose_bednu_igru_channel).fetch_message(choose_bednu_igru_message))

    @commands.command()
    async def dodajbednuigru(self, ctx, *arg):
        only_officers(ctx)
        new_role = await ctx.guild.create_role(name = str(arg[0]), colour = discord.Colour.dark_orange())
        all_games_role = ctx.guild.get_role(1259251163170340914)
        bot_role = ctx.guild.get_role(719627362907717686)
        choose_bedna_igra_message = await ctx.guild.get_channel(choose_bednu_igru_channel).fetch_message(choose_bednu_igru_message)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            all_games_role : discord.PermissionOverwrite(view_channel=True),
            new_role: discord.PermissionOverwrite(view_channel=True)
        }
        
        category = ctx.guild.get_channel(bedne_igre_category)
        await ctx.guild.create_text_channel(name = str(arg[0]), category = category, overwrites=overwrites)

        bedne_path = os.path.join(".", "BedneIgre.json")
        with open(bedne_path, "r+", encoding="utf-8") as file:
            bedne_info = json.load(file)

        new_role = {
            "emoji" : str(arg[1]),
            "role" : str(new_role.id)
        }

        bedne_info.append(new_role)
        with open('BedneIgre.json', "w" , encoding="utf-8") as file:
            json.dump(bedne_info, file, indent=4)

        await self.manage_own_message(ctx, choose_bedna_igra_message)
    
    #WOW API
    @commands.command()
    async def wowtoken(self, ctx):
        info = await wow_token_price("eu")
        wow_token_embed = discord.Embed(colour=discord.Color.dark_green())
        wow_token_embed.add_field(name = "Trenutna cena wow tokena: ", value = info, inline=True)
        await ctx.channel.send(embed = wow_token_embed)

    @commands.command()
    async def rolemessages(self, ctx):
        only_officers(ctx)
        roles_embed = discord.Embed(title=str(role_note), colour=discord.Color.dark_green())

        albino_rola = get(ctx.guild.emojis, name='atbpepe')
        albino_friend_rola = get(ctx.guild.emojis, name='Yep')
        raider_rola = get(ctx.guild.emojis, name='heroicrejder')
        values = str(albino_rola) +" za albino rolu, " + str(albino_friend_rola) +" za alibno friend rolu, " + str(raider_rola) +" za raider rolu"
        reactions = [albino_rola, albino_friend_rola, raider_rola]
        roles_embed.add_field(name = "Roles", value = values, inline=True)
        embeded_role_message = await ctx.guild.get_channel(role_channel).send(embed = roles_embed)
        for reaction in reactions:
            await embeded_role_message.add_reaction(reaction)

    @commands.command()
    async def editrolemessages(self, ctx):
        only_officers(ctx)
        role_message_edit = await ctx.guild.get_channel(role_channel).fetch_message(role_message_id)
        roles_embed = discord.Embed(title=str(role_note), colour=discord.Color.dark_green())

        albino_rola = get(ctx.guild.emojis, name='atbpepe')
        albino_friend_rola = get(ctx.guild.emojis, name='Yep')
        raider_rola = get(ctx.guild.emojis, name='heroicrejder')
        values = str(albino_rola) +" za <@&"+str(Roles["Albino"])+">\n" + str(albino_friend_rola)+" za <@&"+str(Roles["Albino Frend"])+">\n" + str(raider_rola) +" za <@&"+str(Roles["Raider"])+">"
        reactions = [albino_rola, albino_friend_rola, raider_rola]
        roles_embed.add_field(name = "", value = values, inline=True)
        await role_message_edit.edit(embed = roles_embed)
        #embeded_role_message = await ctx.guild.get_channel(role_channel).send(embed = roles_embed)

        await role_message_edit.clear_reactions()
        for reaction in reactions:
            await role_message_edit.add_reaction(reaction)
                

    @commands.command()
    async def attendance(self, ctx):
        only_officers(ctx)
        member_names = ""
        for member in ctx.author.voice.channel.members:
            member_names = str(member_names) + str(member.nick) + " "
        await ctx.send(member_names)

    
    @commands.command()
    async def checkroles(self, ctx):
        if(not ctx.author.top_role.permissions.administrator):
            return 0
        
        guild = ctx.guild
        leveling_cog = self.client.get_cog("Leveling")
        user_info = await leveling_cog.open_users_file()

        for user in user_info:
            member = await guild.fetch_member(user["id"])
            role = leveling_cog.get_role_by_level(guild, user["level"])

            if not role is None:
                 await member.add_roles(role)
        print("Finished checking roles!")
        return
    
    @commands.command(pass_context=True)
    async def poll(self, ctx, question, *options: str):
        if(not ctx.author.top_role.permissions.administrator):
            return 0
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return
        
        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description), colour=discord.Color.dark_green())
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)

    @commands.command(pass_context=True)
    async def tally(self, ctx, id=None):
        if(not ctx.author.top_role.permissions.administrator):
            return 0
        leveling_cog = self.client.get_cog("Leveling")
        user_info = await leveling_cog.open_users_file()
        poll_message = await ctx.channel.fetch_message(id)
        embed = poll_message.embeds[0]
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [self.client.user.id]  # add the bot's ID to the list of voters to exclude it's votes
        
        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                users = [user async for user in reaction.users()]
                for user in users:
                    if user.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(user.id)
                        await leveling_cog.get_xp(user.name, 10)

        output = f"Results of the poll for '{embed.title}':\n" + '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await ctx.send(output)
        await poll_message.delete()

    @commands.command()
    async def csv(self, ctx):
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        leveling_cog = self.client.get_cog("Leveling")
        user_info = await leveling_cog.open_users_file()
        guild = ctx.guild
        
        for member in guild.members:
            for user in user_info:
                if user['name'] == member.name:
                    all_roles = []
                    for role in member.roles:
                        all_roles.append(role.name)
                    writer.writerow([[str(user['name'])], [str(member.created_at)] , [str(member.joined_at)], [user['level'] >= 1], [str(user['level'])], [str(user['xp'])], [all_roles]])
        buffer.seek(0) #Don't know why this is here, but it worked...

        await ctx.channel.send(file=discord.File(buffer, 'some-file.csv'))


async def setup(client):
    await client.add_cog(Commands(client))
    
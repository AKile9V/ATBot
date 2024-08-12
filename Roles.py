import discord

EmojiToRole = {
    "Yep": "Albino Frend",
    "atbpepe": "Albino",
    "heroicrejder": "Raider",
    "🚽": "Intruder"
}

Roles = {
    "Albino Frend": 760200627187351583,
    "Albino": 719623918369112066,
    "Raider": 275622877255172097,
    "Intruder": 374292236097159178
}

ImportantRoles = {
    "officer_id": 278073428475379712
}


def get_role_by_name(guild, name):
    return guild.get_role(Roles[name])

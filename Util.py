#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from Settings import WOW_REGION
import json


def split_query(message, content):
    """Helper function that splits a string and returns data
    in a predictable order. """

    # If the word 'worldofwarcraft' or 'battle.net' exist
    # it splits the string starting at 'character/'
    if "worldofwarcraft" in message or "battle.net" in message:
        url = re.split("\\bcharacter/\\b", message)[-1]
        split = url.split(" ", 1)[0].split("/")
        message = message.split(" ")

        # Check if a region was provided, otherwise use the region setting.
        try:
            return [split[1], split[0], content, message[3]]
        except IndexError:
            return [split[1], split[0], content, WOW_REGION]

    # Assumes it's not a url path, and splits the string normally.
    else:
        split = message.split(" ")

        # Handles the wow_token case
        if content == "wow_token":
            try:
                return [split[2]]
            except IndexError:
                return [WOW_REGION]

        else:
            try:
                return [split[2], split[3], content, split[4]]
            except IndexError:
                return [split[2], split[3], content, WOW_REGION]


def remove_from_json(filepath, json_list, key, value):
    with open(filepath, 'r', encoding="utf-8") as fp:
        data = json.load(fp)

    for data_obj in data[json_list]:
        if str(data_obj[key]) == str(value):
            data[json_list].remove(data_obj)

    with open(filepath, 'w', encoding="utf-8") as fp:
        json.dump(data, fp)


def add_to_json(filepath, json_list, key, value):
    with open(filepath, 'r', encoding="utf-8") as fp:
        data = json.load(fp)

    member_dict = {str(key): str(value)}
    data[json_list].append(member_dict)

    with open(filepath, 'w', encoding="utf-8") as fp:
        json.dump(data, fp)


def append_to_json(filepath, json_list, json_obj):
    return


def only_officers(ctx):
    print(ctx.author.top_role.name)
    print(ctx.author.top_role.permissions.administrator)
    print(str(ctx.author.top_role.name) == "Officer")
    if (not (ctx.author.top_role.permissions.administrator or str(ctx.author.top_role.name) == "Officer")):
        print("?")
        return 0

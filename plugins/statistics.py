###
# This plugin creates statistics
###
from plugins.utilities import commands
from plugins.utilities import config
from plugins.utilities import formatter

import asyncio
import datetime
import sched
import os
import json
from shutil import copyfile

stats = {}
directory = "plugins/statistics"


def initialize_commands():
    global logger
    global stats

    logger = commands.logger
    if not os.path.isdir(directory):
        os.makedirs(directory)
    elif os.path.isfile(directory + "/stats.json"):
        try:
            with open(directory + "/stats.json") as f:
                stats = json.load(f)
        except ValueError:
            logger.error("stats json corrupted!")
            copyfile(directory + "/stats.json", directory + "/stats.corrupt")

    commands.create_command("statistics",
                            "process_message",
                            [],
                            "Keeps track of the statistics",
                            passive=True)


def save():
    with open(directory + "/stats.json", 'w') as f:
        json.dump(stats, f)


def command_in_message(client, message):
    if client.user.mentioned_in(message) or message.server is None:
        mentioned = True
    else:
        mentioned = False
    for plugin in commands.plugins['enabled']:
        for command, parameters in commands.commands[plugin].items():
            if not parameters['mention'] or mentioned:
                for keyword in parameters['keywords']:
                    if all(words in message.clean_content for words in keyword.split(" ")):
                        used_command = {}
                        used_command['plugin'] = plugin
                        used_command['command'] = command
                        return used_command
    return None


def process_message(client, message):
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    if message.server:
        server = message.server.id
    else:
        server = "private"
    user = message.author.id
    word_count = len(message.clean_content.split(" "))
    try:
        used_command = command_in_message(client, message)
        command = used_command['command']
        plugin = used_command['plugin']
    except TypeError:
        plugin = None

    if date not in stats:
        stats[date] = {}
    if server not in stats[date]:
        stats[date][server] = {}
    if user not in stats[date][server]:
        stats[date][server][user] = {}
        stats[date][server][user]['messages'] = 1
        stats[date][server][user]['words'] = word_count
    else:
        stats[date][server][user]['messages'] += 1
        stats[date][server][user]['words'] += word_count

    if plugin:
        if plugin not in stats[date][server][user]:
            stats[date][server][user][plugin] = {}
        if command not in stats[date][server][user][plugin]:
            stats[date][server][user][plugin][command] = {}
            stats[date][server][user][plugin][command]['count'] = 1
        else:
            stats[date][server][user][plugin][command]['count'] += 1
    save()

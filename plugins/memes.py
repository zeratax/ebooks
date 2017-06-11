###
# This plugin exports dank memes
###
from plugins.utilities import commands
from plugins.utilities import config
from plugins.utilities import formatter
from plugins.utilities import i18n
from plugins import statistics

import asyncio
import datetime
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
from random import randint


def initialize_commands():
    global logger
    global conf
    logger = commands.logger
    try:
        conf = config.c.plugin_c['memes']
    except NameError:
        logger.warning(
            "config is missing settings for meme module to work properly")

    # commands.create_command("memes",
    #                        "meme_image",
    #                        ["meme_image", "meme_img"],
    #                        "Sends a meme image")
    commands.create_command("memes",
                            "slot_machine",
                            ["slot machine"],
                            "animates a slot machine")
    commands.create_command("memes",
                            "dick_animated",
                            ["dick animated"],
                            "animates a slot machine")


def add_stats(message):
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    server = message.server.id
    user = message.author.id
    slot_stat = statistics.stats[date][server][user]['memes']['slot_machine']
    if 'win' not in slot_stat:
        slot_stat['win'] = 1
    else:
        slot_stat['win'] += 1


async def dick_animated(client, message):
    bot_message = "8"
    dick = await client.send_message(message.channel, bot_message)
    for i in range(randint(4, 15)):
        bot_message += "="
        await asyncio.sleep(1)
        await client.edit_message(dick, bot_message)
    bot_message += "D"
    await client.edit_message(dick, bot_message)


async def slot_machine(client, message):
    user = message.author.nick
    choice = ["", "", ""]
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    for y in range(3):
        choice[y] = random.choice(conf['slotmoji'])
    bot_message = "[" + choice[0] + "][" + choice[1] + "][" + choice[2] + "]"
    slot_machine = await client.send_message(message.channel, bot_message)
    for x in range(5):
        for y in range(3):
            choice[y] = random.choice(conf['slotmoji'])
            bot_message = "[" + choice[0] + "][" + \
                choice[1] + "][" + choice[2] + "]"
        await asyncio.sleep(1.5)
        await client.edit_message(slot_machine, bot_message)
    if choice[0] == choice[1] and choice[0] == choice[2]:
        await client.send_message(message.channel,
                                  formatter.win(i18n.loc(server_id,
                                                         "memes",
                                                         "slot_win").format(user)))
        add_stats(message)
    else:
        await client.send_message(message.channel,
                                  formatter.lost(i18n.loc(server_id,
                                                          "memes",
                                                          "slot_lost")))

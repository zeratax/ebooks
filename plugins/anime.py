###
# This plugin includes all anime related features
###

# from __future__ import unicode_literals
from plugins.utilities import commands
from plugins.utilities import config
from plugins.utilities import formatter
from plugins.utilities import i18n

import asyncio
from pybooru import Danbooru
import os
import random
from random import randint


def initialize_commands():
    global logger
    global conf
    logger = commands.logger

    try:
        conf = config.c.plugin_c['anime']
    except NameError:
        logger.warning("config is missing settings for the anime module")

    commands.create_command("anime",
                            "cute_image",
                            ["qt,img", "cute,image"],
                            "Sends a cute image")

    commands.create_command("anime",
                            "sleep",
                            ["sleep", "night", "let bed bugs bite you",
                             "tired"],
                            "kaga posting",
                            mention=False)


def get_img_by_tag(tags, pages):
    randompage = randint(1, pages)
    randompost = randint(1, 72)
    client = Danbooru(
        'danbooru', username=conf['login'], api_key=conf['token'])
    posts = client.post_list(tags=tags, page=randompage, limit=200)
    if posts[randompost]:
        try:
            file_url = 'http://danbooru.donmai.us' + \
                posts[randompost]['file_url']
        except NameError:
            file_url = posts[randompost]['source']
    else:
        return False
    return file_url


async def cute_image(client, message):
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    await client.send_typing(message.channel)
    for _ in range(5):
        image = get_img_by_tag(conf['tags'], conf['pages'])
        if image:
            break
    if image:
        # image = get_img_by_tag('order:score rating:s', 5)
        msg = await client.send_message(message.channel, image)
        await client.add_reaction(msg, '👍')
        await client.add_reaction(msg, '👎')
        # await asyncio.sleep(1)
        res = await client.wait_for_reaction(['👍', '👎'], message=msg,
                                             user=message.author, timeout=180)
        if res is None:
            await  client.send_message(message.channel,
                                       formatter.warning(i18n.loc(server_id,
                                                                  "anime",
                                                                  "timeout")))
        elif res.reaction.emoji == '👍':
            await cute_image(client, message)
        else:
            await client.send_message(message.channel,
                                      formatter.warning(i18n.loc(server_id,
                                                                 "anime",
                                                                 "no_mo_img")))
    else:
        await client.send_message(message.channel,
                                  formatter.error(i18n.loc(server_id,
                                                             "anime",
                                                             "adjust_tags")))

def kaga_posting():
    kaga = random.choice(open('plugins/anime/sleep.txt').readlines())
    return kaga


async def sleep(client, message):
    # image = kaga_posting()
    image = get_img_by_tag('rebecca_(keinelove) chibi', 5)
    await client.send_message(message.channel, image)

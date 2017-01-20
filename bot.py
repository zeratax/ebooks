import discord
import asyncio

import datetime
import importlib.util
import json
import logging
import os
import sys
import warnings

client = discord.Client()


@client.event
async def on_ready():
    # outputs general info about the bot
    if not hasattr(client, 'uptime'):
        client.uptime = datetime.datetime.utcnow()
    oauth = discord.utils.oauth_url(client.user.id)
    await set_profile()

    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(modules)
    print(oauth)
    print('------')


@client.event
async def on_message(message):
    if client.user.mentioned_in(message) or message.server == None:
        mentioned = True
    # checks new message for keywords and calls the appropiate commands if
    # found
    if (message.author != client.user):
        for plugin in plugins['enabled']:
            for command, parameters in commands.commands[plugin].items():
                if not parameters['mention'] or mentioned:
                    for keyword in parameters['keywords']:
                        if keyword in message.clean_content:
                            await eval("modules['{}'].{}(client, message)".format(
                                plugin, command))
                            return
        # await client.send_message(message.channel, "nice meme")


async def set_profile():
    await client.edit_profile(username=bot['username'])


def load_config():
    with open('config.json') as f:
        return json.load(f)


def load_plugins():
    commands.commands = {}
    for plugin in plugins['enabled']:
        try:
            modules[plugin] = importlib.import_module('plugins.' + plugin)
            for command, parameters in commands.commands[plugin].items():
                for keyword in parameters['keywords']:
                    if keyword in keywords:
                        warning = "WARNING: Keyword: '{}' is already used".format(
                            keyword)
                        logging.warning(warning)
                    else:
                        keywords.append(keyword)
            logging.info("Plugin: {} has been loaded".format(plugin))
        except Exception as e:
            warning = """WARNING: Plugin: '{}' failed to load
                        Reason:
                        {}
                        """.format(plugin, e)
            logging.warning(warning)

def unload_plugin(plugin):
    try:
        plugins['enabled'].remove(plugin)
        commands.commands.pop(plugin, None)
        logging.info("Plugin: {} has been unloaded".format(plugin))
    except:
        logging.info("Plugin: {} is not loaded".format(plugin))

def load_plugin(plugin):
    if not plugin in plugins['enabled']:
        plugins['enabled'].append(plugin)
        load_plugins()
    else:
        logging.info("Plugin: {} is already loaded".format(plugin))

if __name__ == '__main__':
    config = load_config()

    develop = any('develop' in arg.lower() for arg in sys.argv)
    if develop:
        bot = config['bot']['develop']
    else:
        bot = config['bot']['default']
    token = bot['token']

    logger = logging.getLogger('discord')

    debug = any('debug' in arg.lower() for arg in sys.argv)
    if debug:
        print("logging at DEBUG level")
        logger.setLevel(logging.DEBUG)
    else:
        print("logging at WARNING level")
        logger.setLevel(logging.WARNING)

    handler = logging.FileHandler(
        filename='ebooks.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    keywords = []
    modules = {}
    plugins = config['plugins']
    from plugins import commands
    load_plugins()

    client.run(token)

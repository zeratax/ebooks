import discord
import asyncio

import argparse
import datetime
import json
import logging
import sys
import warnings

from plugins.utilities import config
from plugins.utilities import commands

client = discord.Client()
modules = commands.modules


@client.event
async def on_ready():
    if not hasattr(client, 'uptime'):
        client.uptime = datetime.datetime.utcnow()
    await set_profile()
    oauth = await get_oauth_url()
    users = len(set(client.get_all_members()))
    servers = len(client.servers)

    # outputs general info about the bot
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(oauth)
    print(modules)
    print('serving {0} users on {1} servers'.format(users, servers))
    print('------')


@client.event
async def on_message(message):
    if client.user.mentioned_in(message) or message.server is None:
        mentioned = True
    else:
        mentioned = False
    # checks new message for keywords and calls the appropiate commands
    await start_plugin(message, mentioned)


@client.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)


async def set_profile():
    await client.edit_profile(username=config.c.bot_c['username'])


async def get_oauth_url():
    try:
        data = await client.application_info()
    except Exception as e:
        return "Couldn't get invite link"
    return discord.utils.oauth_url(data.id)


async def start_plugin(message, mentioned):
    # passive commands
    try:
        for plugin in commands.plugins['enabled']:
            for command, parameters in commands.commands[plugin].items():
                if parameters['passive']:
                    eval("modules['{}'].{}(client, message)".format(
                        plugin, command))
    except Exception as e:
        logger.warning(e, commands.get_error(e))
    # active commands
    try:
        if (message.author != client.user):
            for plugin in commands.plugins['enabled']:
                for command, parameters in commands.commands[plugin].items():
                    if not parameters['mention'] or mentioned:
                        for keyword in parameters['keywords']:
                            if all(words in message.clean_content.lower() for words in keyword.split(",")):
                                await eval("modules['{}'].{}(client, message)".format(
                                        plugin, command))
                                return
            # fallback function
            if "conversations" in bot_plugins['enabled'] and mentioned:
                await modules['conversations'].reply(client, message)
    except Exception as e:
        logger.warning(e, commands.get_error(e))
        await client.send_message(message.channel, str(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='discord bot')
    parser.add_argument("-c", "--config", help="Specify config file",
                        metavar="FILE")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    logger = commands.logger

    if args.verbose:
        print("verbose output enabled")
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logFormatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    consoleFormatter = logging.Formatter(
        '%(levelname)s:%(name)s: %(message)s')

    handler = logging.FileHandler(filename='ebooks.log',
                                  encoding='utf-8', mode='w')
    handler.setFormatter(logFormatter)
    logger.addHandler(handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(consoleFormatter)
    logger.addHandler(consoleHandler)

    if args.config:
        config_file = args.config
    else:
        config_file = input("Please enter a config file: ")
    config.set_config(config_file)


    bot_token = config.c.bot_c['token']
    bot_plugins = config.c.bot_c['plugins']
    commands.plugins['enabled'] = bot_plugins['enabled']
    commands.plugins['banned'] = bot_plugins['banned']

    commands.load_plugins()
    logger.debug(commands.commands)

    client.run(bot_token)

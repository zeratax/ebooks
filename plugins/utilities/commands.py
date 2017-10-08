###
# This module is supposed to give other plugins the ability to create and
# remove new bot commands
###

import discord
import asyncio
import importlib.util
import logging
import os
import sys

# check if commands is already initialized
try:
    logger
    plugins
    keywords
    modules
    commands
except NameError:
    logger = logging.getLogger("discord")
    plugins = {}
    plugins["enabled"] = []
    plugins["banned"] = []
    modules = {}
    commands = {}
    keywords = []


def create_command(plugin, name, keywords, description, mention=True,
                   passive=False):
    """
    function to create bot commands for other modules,
    will be stored in commands variable
    """
    logger.debug("Creating {} for {}: {}, {}, {}, {}".format(name, plugin,
                                                             keywords,
                                                             description,
                                                             mention, passive))
    for banned in plugins["banned"]:
        if banned["plugin"] == plugin and banned["command"] == name:
            logger.debug("{}:{} is banned".format(plugin, name))
            return
    if plugin not in commands:
        commands[plugin] = {}
    commands[plugin][name] = {}
    commands[plugin][name]["keywords"] = keywords
    commands[plugin][name]["description"] = description
    commands[plugin][name]["mention"] = mention
    commands[plugin][name]["passive"] = passive


def add_keywords(plugin):
    global keywords
    for command, parameters in commands[plugin].items():
        for keyword in parameters["keywords"]:
            if keyword in keywords:
                logger.warning(
                    "WARNING: Keyword: '{}' is already used".format(keyword))
            else:
                keywords.append(keyword)


def load_plugins():
    global keywords
    keywords = []
    logger.debug("Plugins enabled: {}".format(plugins["enabled"]))
    for plugin in plugins["enabled"]:
        logger.debug("Trying to load {}".format(plugin))
        try:
            if os.path.exists("plugins/" + plugin + ".py"):
                modules[plugin] = importlib.import_module("plugins." + plugin)
                eval("modules['{}'].initialize_commands()".format(plugin))
            else:
                logger.warning(
                    "WARNING: Plugin: {} does not exist".format(plugin))
            add_keywords(plugin)
            logger.info("Plugin: {} has been loaded".format(plugin))
        except Exception as e:
            logger.critical(e, get_error(e))


def reload_plugins():
    global keywords
    commands = {}
    keywords = []
    for plugin in plugins["enabled"]:
        logger.debug("Trying to load {}".format(plugin))
        try:
            importlib.reload(modules[plugin])
            eval("modules['{}'].initialize_commands()".format(plugin))
            add_keywords(plugin)
            logger.info("Plugin: {} has been loaded".format(plugin))
        except Exception as e:
            logger.critical(e, get_error(e))


def unload_plugin(plugin):
    if plugin in plugins["enabled"]:
        plugins["enabled"].remove(plugin)
        del modules[plugin]
        commands = {}
        load_plugins()
    else:
        logger.info("Plugin: {} is not loaded".format(plugin))


def load_plugin(plugin):
    if plugin not in enabled_plugins:
        plugins["enabled"].append(plugin)
        commands = {}
        load_plugins()
    else:
        logger.info("Plugin: {} is already loaded".format(plugin))


async def periodic():
    while True:
        logger.debug("saving...")
        try:
            for plugin in plugins["enabled"]:
                for command, parameters in commands[plugin].items():
                    if "save" in eval("dir(modules['{}'])".format(plugin)):
                        eval("modules['{}'].save()".format(plugin))
        except Exception as e:
            logger.warning(e, commands.get_error(e))
        await asyncio.sleep(10)


def stop():
    task.cancel()


# task = asyncio.Task(periodic())
# loop = asyncio.get_event_loop()


async def save_plugins():
     # loop.call_later(5, stop)
     try:
         loop.run_until_complete(task)
     except asyncio.CancelledError:
         pass


def remove_keywords(client, string, plugin, command):
    string_clean = string.replace(client.user.mention, "")
    string_clean = string_clean.replace("@" + client.user.name, "")
    for server in client.servers:
        for member in server.members:
            nickname = member.nick
            if nickname:
                string_clean = string_clean.replace("@" + nickname, "")
    for keyword in commands[plugin][command]["keywords"]:
        string_clean = string_clean.replace(keyword, "")
    return string_clean.strip()


def get_error(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return exc_type, fname, exc_tb.tb_lineno

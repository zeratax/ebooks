###
# This plugin  is used for general purpose commands like a help command to show
# all existing commands in a friendly descriptive way.
###
from plugins.utilities import commands
from plugins.utilities import formatter
from plugins.utilities import i18n

import discord


def initialize_commands():
    commands.create_command("main",
                            "help",
                            ["help"],
                            "Displays this help message")
    commands.create_command("main",
                            "invite_bot",
                            ["invite", "join me"],
                            "Creates a link to invite the bot to your server")
    commands.create_command("main",
                            "reload_plugins",
                            ["reload_bot", "reload_plugins"],
                            "Reloads all plugins")
    commands.create_command("main",
                            "load_plugin",
                            ["load_plugin", "start_plugin", "enable_plugin"],
                            "Enables a plugin")
    commands.create_command("main",
                            "unload_plugin",
                            ["unload_plugin", "remove_plugin",
                             "disable_plugin"],
                            "Disables a plugin")
    commands.create_command("main",
                            "set_config",
                            ["set_config", "reload_config"],
                            "Use this to switch to another config")
    commands.create_command("main",
                            "set_language",
                            ["set_language"],
                            "Change language for this server")


def help_list(commands):
    """
    creates a markdown formatted string with all commands sorted by module
    """
    bot_message = ""
    for module, command in commands.items():
        bot_message += "**__{}__**:\n".format(module)
        for key, value in command.items():
            bot_message += "    **{}:** {}\n".format(key, value)
    return bot_message


async def invite_bot(client, message):
    invite = discord.utils.oauth_url(client.user.id)
    await client.send_message(message.channel, invite)


async def help(client, message):
    await formatter.wrap_message(client, message.channel,
                                 help_list(commands.commands))


async def set_config(client, message):
    config_file = commands.remove_keywords(
        client, message.clean_content, "main", "set_config")
    if (message.author.id == (await client.application_info()).owner.id):
        try:
            config.set_config(config_file)
            client.send_message(message.channel,
                                formatter.success("Settings set!"))
        except Exception as e:
            client.send_message(message.channel, str(e))


async def unload_plugin(client, message):
    plugin = commands.remove_keywords(
        client, message.clean_content, "main", "unload_plugin")
    if (message.author.id == (await client.application_info()).owner.id):
        try:
            commands.unload_plugin(plugin)
            client.send_message(message.channel,
                                formatter.success("Plugin unloaded!"))
        except Exception as e:
            client.send_message(message.channel, str(e))


async def load_plugin(client, message):
    plugin = commands.remove_keywords(
        client, message.clean_content, "main", "load_plugin")
    if (message.author.id == (await client.application_info()).owner.id):
        try:
            commands.load_plugin(plugin)
            client.send_message(message.channel,
                                formatter.success("Plugin loaded!"))
        except Exception as e:
            client.send_message(message.channel, str(e))


async def reload_plugins(client, message):
    if (message.author.id == (await client.application_info()).owner.id):
        try:
            print("reloading plugins")
            commands.reload_plugins()
            client.send_message(message.channel,
                                formatter.success("Plugins reloaded!"))
        except Exception:
            client.send_message(message.channel,
                                formatter.error("check logs!"))


async def set_language(client, message):
    language = commands.remove_keywords(
        client, message.clean_content, "main", "set_language")
    server_id = message.server.id
    if (message.author.id == (await client.application_info()).owner.id):
        try:
            i18n.set_language(server_id, language)
        except Exception as e:
            client.send_message(message.channel, str(e))

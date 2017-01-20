###
# This plugin  is used for general purpose commands like a help command to show
# all existing commands in a friendly descriptive way.
###


import discord
import asyncio
from plugins import commands

commands.create_command("main",
                        "help",
                        ["help"],
                        "Displays this help message")

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

async def help(client, message):
    await client.send_message(message.channel, help_list(commands.commands))

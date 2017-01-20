###
# This plugin includes all conversation commands, like the main markov feature
###


import discord
import asyncio
from plugins import commands

commands.create_command("conversations",
                        "reply",
                        ["reply", "meme","markov"],
                        "Replies with a markov chain")
import markovify

def shitpost():
    with open("john.txt") as f:
        text = f.read()

        text_model = markovify.Text(text)
        shitpost = text_model.make_short_sentence(50, tries=100)
        if shitpost is not None:
            return shitpost
        else:
            shitpost = "I require more messages before I correctly work"

async def reply(client, message):
    await client.send_message(message.channel, shitpost())

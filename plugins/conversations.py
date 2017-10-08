###
# This plugin includes all conversation commands, like the main markov feature
###
from plugins.utilities import commands
from plugins.utilities import config
from plugins.utilities import formatter
from plugins.utilities import i18n

import markovify
import os
import random
import re

markov = {}
directory = "plugins/conversations/"


def initialize_commands():
    global logger
    global conf
    logger = commands.logger

    try:
        conf = config.c.plugin_c['conversations']
    except NameError:
        logger.warning(
            "config is missing settings for the conversations module")

    if not os.path.isdir(directory):
        os.makedirs(directory)

    commands.create_command("conversations",
                            "create_markov_model",
                            [],
                            "logs messages to generate markov models",
                            passive=True)
    commands.create_command("conversations",
                            "question",
                            ["?"],
                            "Answers your question (kinda...)")
    commands.create_command("conversations",
                            "rate",
                            ["rate ", " rate"],
                            "rates stuff")


def log_message(message):
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    text = message.clean_content
    log = "{}/{}.txt".format(directory, server_id)
    with open(log, "a") as f:
        for mention in message.mentions:
            if mention.bot:
                logger.debug("{} sent to bot".format(text))
                return
        if message.author.bot:
            logger.debug("{} sent by bot".format(text))
        elif text.startswith(("?", "!", "=", "`", "´", "^", ";", "~", "+",
                              "\/", "\\", "]", "}", ")", ":", "<")):
            logger.debug("{} probably sent to bot".format(text))
        elif text.endswith((".", "!", "?", ",")):
            f.write(text + "\n")
        else:
            f.write(text + ".\n")


def create_markov_model(client, message):
    log_message(message)
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    log = "{}/{}.txt".format(directory, server_id)
    if server_id not in markov:
        markov[server_id] = {}
        markov[server_id]["offset"] = 1
        markov[server_id]["model"] = False
    else:
        markov[server_id]["offset"] += 1

    if markov[server_id]["model"]:
        if markov[server_id]["offset"] == conf["offset"]:
            with open(log) as f:
                text = f.read()
                markov[server_id]["offset"] = 1
                markov[server_id]["model"] = markovify.Text(text)
    else:
        if os.path.getsize(log) > 12000:
            with open(log) as f:
                text = f.read()
                markov[server_id]["offset"] = 1
                markov[server_id]["model"] = markovify.Text(text)


def shitpost(model):
    if model:
        shitpost = model.make_short_sentence(50, tries=100)
        if shitpost:
            return shitpost


async def reply(client, message):
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    model = markov[server_id]["model"]
    bot_message = shitpost(model)
    if not bot_message:
        bot_message = formatter.error(
            i18n.loc(server_id, "conversations", "more_msg"))
    await client.send_message(message.channel, bot_message)


async def rate(client, message):
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    rating = random.randint(1, 10)
    if rating == 10:
        bot_message = i18n.loc(server_id, "conversations", "full_points")
    else:
        bot_message = str(rating) + "/10 " + random.choice(
            i18n.loc(server_id, "conversations", "points")) + ".\n"
        bot_message += ":star:" * rating
    await client.send_message(message.channel, bot_message)


async def question(client, message):
    if message.server:
        server_id = message.server.id
    else:
        server_id = message.author.id
    question = commands.remove_keywords(
        client, message.clean_content, "conversations", "question")
    if "or" in question:
        question = re.sub(i18n.loc(
            server_id, "conversations", "decide_re"), "", question)
        if question.endswith("more"):
            question = question.rsplit('more', 1)[0]
        decision = re.split('; |, | or |\n', question, flags=re.IGNORECASE)
        bot_message = " ".join(random.choice(decision).split())
    elif "who" in question:
        if message.server:
            bot_message = formatter.person(random.choice(
                list(message.server.members)).display_name)
        else:
            bot_message = formatter.person(random.choice(
                i18n.loc(server_id, "conversations", "private_who")))
    else:
        with open(directory + "yesno.txt") as f:
            yesno = f.read().split()
            answer = random.choice(yesno)
            bot_message = formatter.link(answer)
    await client.send_message(message.channel, bot_message)

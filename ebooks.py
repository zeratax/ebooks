import discord, asyncio, logging, time, threading, markovify, psutil, posixpath, platform, re, os, time
import random
from random import randint
import urllib
from urllib import parse
from urllib import request
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

logging.basicConfig(level=logging.INFO)

client = discord.Client()

p = psutil.Process(os.getpid())
p.create_time()
@client.event
async def on_ready():
    print('Discord: Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    path = ""
    print("'" + message.clean_content + "'")
    messagetobot = False
    if not message.author.bot:
        for mention in message.mentions:
            if mention.bot:
                print("message sent to bot")
                messagetobot = True
        print("message sent by " + message.author.name)
        servername = str(message.server)
        if not os.path.exists("server/" + servername):
            os.makedirs("server/" + servername)
            os.makedirs("server/" + servername + "/images")
            os.makedirs("server/" + servername + "/output")
        if not messagetobot:
            #for attachment in message.attachments:
            #   print(attachment["filename"] + ": " + attachment["proxy_url"])
            #WSS   urllib.request.urlretrieve(attachment["proxy_url"], attachment["filename"]).add_header("User-Agent", "DiscordBot (https://github.com/Rapptz/discord.py, v.0.11.0)")
            with open("server/" + servername + "/log.txt", "a") as myfile:
                if message.clean_content.endswith(".") or message.clean_content.endswith("!") or message.clean_content.endswith("?"):
                     myfile.write(message.clean_content.replace("@", ""))
                elif message.clean_content.startswith(".") or message.clean_content.startswith("!") or message.clean_content.startswith("?")  or message.clean_content.startswith("`"):
                    print("message sent to bot")
                    messagetobot = True
                else:
                    myfile.write(message.clean_content.replace("@", "") + ". ")
        images = re.findall('(https?:\/\/.*\.(?:png|jpg|jpeg))', message.clean_content.lower())
        for image in images:
            path = urllib.parse.urlsplit(image).path
            urllib.request.urlretrieve(image, "server/" + servername + "/images/" + posixpath.basename(path))
        
        if client.user.mentioned_in(message):
            if message.server.me.nick:
                name = message.server.me.nick
            else:
                name = client.user.name
            if message.content.endswith('?'):
                if ' or ' in message.clean_content.lower():
                    REMOVE_LIST = ["@", name, "\?", "should I rather", "should I", "would you rather", "what do you prefer", "who do you prefer", "do you prefer", "what is better", "what should I do", "what could I do" , "would you prefer", "decide between", "what do you like more", "decide for me between"]
                    remove = '|'.join(REMOVE_LIST)
                    regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
                    shitdecision = re.split('; |, | Or | oR | or | OR |\n', regex.sub("", " ".join(re.sub(r'.*:', '', message.clean_content).split())))
                    shitdecision = " ".join(random.choice (shitdecision).format(message).split())
                    await client.send_message(message.channel, shitdecision)
                else:
                    print(urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9'))
                    yesno = urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9').read().decode('utf-8').split()
                    shitanswer = random.choice (yesno).format(message)
                    await client.send_message(message.channel, shitanswer)
            elif " pic" in message.content.lower():
                await client.send_file(message.channel, "server/" + servername + "/output/" + shitimage(servername, message.channel)) 
            elif "info" in message.content.lower():
                num_lines = 0
                num_words = 0
                num_chars = 0

                with open("server/" + servername + "/log.txt", 'r') as f:
                    for line in f:
                        words = line.split()

                        num_lines += 1
                        num_words += len(words)
                        num_chars += len(line)
                path = "server/" + servername + "/images/"
                await client.send_message(message.channel, """*Information:*

I'm **""" + client.user.name + "**. I'm running on " + platform.dist()[0] + " *" + platform.dist()[1] + "* with python *" + platform.python_version() + "* using discord.py *" + discord.__version__ + """*.
I'm online since *""" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time())) + "* on *" + str(len(client.servers)) + """* servers.
The log file for **""" + servername + "** is currently **" + str(num_words) + "** words and **" + str(num_chars) + "** characters long, with **" + str(sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path)))+ """** images.
This bot was created by **""" + (await client.application_info()).owner.name + "**#" + (await client.application_info()).owner.discriminator + " with :heart:")
            elif "help" in message.content.lower():
                await client.send_message(message.channel, """*Mention me with:*

**set username** to change my username (this only works twice per hour)

    `""" + client.user.mention + " set username NEWUSERNAME`""""

**set avatar** to change my avatar

    `""" + client.user.mention + """ set avatar https://website.tld/imageurl`

**pic** to receive a custom image shitpost

    `""" + client.user.mention + """ pic`

**invite** to receive an invite link for another server

    `""" + client.user.mention + " invite`")
            elif "invite" in message.content.lower():
                await client.send_message(message.channel, discord.utils.oauth_url((await client.application_info())[0], permissions=None, server=None, redirect_uri="https://gezf.de/ebooks/"))
            elif " set avatar " in message.content.lower():
                print("new avatar: server/" + servername + "/images/" + posixpath.basename(path))
                if message.author.id == (await client.application_info()).owner.id:
                    with open("server/" + servername + "/images/" + posixpath.basename(path), 'rb') as f:
                        await client.edit_profile(password=None,avatar=f.read())
                        await client.send_message(message.channel, "Avatar set!")
                else:
                    await client.send_message(message.channel, "You are not allowed to do that!")
            elif " set username " in message.content.lower():
                if  message.author.id == (await client.application_info()).owner.id:
                    REMOVE_LIST = ["@", client.user.mention," new username "]
                    remove = '|'.join(REMOVE_LIST)
                    regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
                    name = regex.sub("", message.content)
                    print("New username: " + name)
                    await client.edit_profile(password=None, username=name)
                    await client.send_message(message.channel, "Username set!")
                else:
                    await client.send_message(message.channel, "You are not allowed to do that!")
            else:
                await client.send_message(message.channel, shitpost(servername, message.channel))
    else:
        print("message sent by bot")

@client.event
async def on_server_join(server):
    await client.send_message(server.default_channel, "**Yahallo!** Please don't expect me to talk right away, I'm *very* shy :3")
def getUptime():
    return time.time() - startTime

def shitpost(servername, channel):
    client.send_typing(channel)
    print("creating shitpost for server " + servername)
    with open("server/" + servername + "/log.txt") as f:
        text = f.read()

        text_model = markovify.Text(text)
        shitpost = text_model.make_short_sentence(50)
        if shitpost is not None:
            return shitpost
        else:
            shitpost = text_model.make_short_sentence(50)
            if shitpost is not None:
                return shitpost
            else:
                shitpost = "fuck off~"
                return shitpost

def shitimage(servername, channel):
    client.send_typing(channel)
    print("creating shitimage for server " + servername)
    imagename = random.choice(os.listdir("server/" + servername + "/images/"))
    base = Image.open("server/" + servername + "/images/" + imagename).convert('RGBA')
    width, height = base.size
    if height < 200:
        imagename = random.choice(os.listdir("images/"))
        base = Image.open("images/" + imagename).convert('RGBA')
        width, height = base.size
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255,255,255,0))
    quote = shitpost(servername, channel)
    img_fraction = 0.50
    dankfont = 'font/' + random.choice(os.listdir('font/'))
    print(dankfont)
    # get a font
    #fnt = ImageFont.truetype('font/' + random.choice(os.listdir("font/")), 30)
    fontsize = 1;
    font = ImageFont.truetype(dankfont  , fontsize)
    while font.getsize(quote)[0] < img_fraction*width:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(dankfont, fontsize)
    fontsize -= 1
    fnt = ImageFont.truetype(dankfont, fontsize)
    # get a drawing context
    d = ImageDraw.Draw(txt)
    randheight = randint(40,height)
    d.text((31,randheight + 1), quote, font=fnt, fill=(255,255,255,255))
    d.text((29,randheight + 1), quote, font=fnt, fill=(255,255,255,255))
    d.text((31,randheight - 1), quote, font=fnt, fill=(255,255,255,255))
    d.text((29,randheight - 1), quote, font=fnt, fill=(255,255,255,255))
    d.text((30,randheight), quote, font=fnt, fill=(0,0,0,255))
    out = Image.alpha_composite(base, txt)
    out.save("server/" + servername + "/output/" + imagename);
    print(imagename)
    return imagename




# def tweet():

#    shittweet = shitpost(important=False)
#    if shittweet is not None:
#        if (len(shittweet) > 0 and len(shittweet) < 141):
#            status = api.PostUpdate(shittweet)
#            print(status.text)
#        threading.Timer(3600, tweet).start()

# tweet()

client.run('token')

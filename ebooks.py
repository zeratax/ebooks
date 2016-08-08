import discord, asyncio, logging, time, threading, markovify, posixpath, re, os
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

@client.event
async def on_ready():
    print('Discord: Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
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
            #   urllib.request.urlretrieve(attachment["proxy_url"], attachment["filename"]).add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36")
            with open("server/" + servername + "/log.txt", "a") as myfile:
                myfile.write(message.clean_content.replace("@", "") + ". ")
        images = re.findall('(https?:\/\/.*\.(?:png|jpg|jpeg))', message.clean_content.lower())
        for image in images:
            path = urllib.parse.urlsplit(image).path
            urllib.request.urlretrieve(image, "server/" + servername + "/images/" + posixpath.basename(path))
        
        if client.user.mentioned_in(message):
            if message.content.endswith('?'):
                if ' or ' in message.clean_content.lower():
                    if message.server.me.nick:
                        name = message.server.me.nick
                    else:
                        name = client.user.name
                    REMOVE_LIST = ["@", name, "\?", "should I rather", "should I", "would you rather", "what do you prefer", "who do you prefer", "do you prefer", "what is better", "what should I do", "what could I do" , "would you prefer", "decide between", "what do you like more", "decide for me between"]
                    remove = '|'.join(REMOVE_LIST)
                    regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
                    shitdecision = re.split('; |, | Or | oR | or |\n', regex.sub("", " ".join(re.sub(r'.*:', '', message.clean_content).split())))
                    shitdecision = " ".join(random.choice (shitdecision).format(message).split())
                    await client.send_message(message.channel, shitdecision)
                else:
                    print(urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9'))
                    yesno = urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9').read().decode('utf-8').split()
                    shitanswer = random.choice (yesno).format(message)
                    await client.send_message(message.channel, shitanswer)
            else:
                if " pic" in message.content.lower():
                    await client.send_file(message.channel, "server/" + servername + "/output/" + shitimage(servername, message.channel)) 
                else:
                    if "invite" in message.content.lower():
                        await client.send_message(message.channel, discord.utils.oauth_url(189772464161685506, permissions=None, server=None, redirect_uri="https://gezf.de/ebooks/"))
                    else:
                        await client.send_message(message.channel, shitpost(servername, message.channel))
    else:
        print("message sent by bot")

@client.event
async def on_server_join(server):
    await client.send_message(server.default_channel, "**Yahallo!** Please don't expect me to talk right away, I'm *very* shy :3")

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
    if height > 200:
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', base.size, (255,255,255,0))
        quote = shitpost(servername, channel)
        img_fraction = 0.70
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
        randheight = randint(40,height) - 200
        d.text((31,randheight + 1), quote, font=fnt, fill=(255,255,255,255))
        d.text((29,randheight + 1), quote, font=fnt, fill=(255,255,255,255))
        d.text((31,randheight - 1), quote, font=fnt, fill=(255,255,255,255))
        d.text((29,randheight - 1), quote, font=fnt, fill=(255,255,255,255))
        d.text((30,randheight), quote, font=fnt, fill=(0,0,0,255))
        out = Image.alpha_composite(base, txt)
        out.save("server/" + servername + "/output/" + imagename);
        return imagename

client.run('token')

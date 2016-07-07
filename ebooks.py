import discord, asyncio, logging, time, threading, markovify, twitter, posixpath, re, os
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
api = twitter.Api(consumer_key='',
                      consumer_secret='',
                      access_token_key='',
                      access_token_secret='')
print('Twitter: Logged in as')
print(api.VerifyCredentials())
print('------')

@client.event
async def on_ready():
    print('Discord: Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    with open("log.txt", "a") as myfile:
        myfile.write(message.clean_content + " ")
    images = re.findall('(https?:\/\/.*\.(?:png|jpg|jpeg))', message.clean_content.lower())
    print(images)
    for image in images:
        print(image)
        path = urllib.parse.urlsplit(image).path
        urllib.request.urlretrieve(image, "images/" + posixpath.basename(path))
        base = Image.open("images/" + posixpath.basename(path)).convert('RGBA')
        width, height = base.size
        print(width)
        print(height)
        if height > 200:
            # make a blank image for the text, initialized to transparent text color
            txt = Image.new('RGBA', base.size, (255,255,255,0))
            quote = shitpost(important=True)
            img_fraction = 0.70
            dankfont = 'font/' + random.choice(os.listdir('font/'))
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
            out.save("output/"+ posixpath.basename(path));
    
    if client.user.mentioned_in(message):
        if message.content.endswith('?'):
            if ' or ' in message.clean_content.lower():
                REMOVE_LIST = ["@", message.server.me.nick, "\?", "should I rather", "should I", "would you rather", "what do you prefer", "who do you prefer", "do you prefer", "what is better", "what should I do", "what could I do" , "would you prefer", "decide between", "what do you like more", "decide for me between"]
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
                await client.send_file(message.channel, "output/" + random.choice(os.listdir("output/")))
            else:
                shitmessage = shitpost(important=True)
                await client.send_message(message.channel, shitmessage)

def shitpost(important):
     with open("log.txt") as f:
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
                if important is True:
                    shitpost = 'Fuck off~'
                else:
                    return

def tweet():

    shittweet = shitpost(important=False)
    if shittweet is not None:
        if (len(shittweet) > 0 and len(shittweet) < 141):
            status = api.PostUpdate(shittweet)
            print(status.text)
        threading.Timer(3600, tweet).start()

tweet()

client.run('')

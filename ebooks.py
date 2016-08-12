import discord, asyncio, logging, time, threading, markovify, psutil, posixpath, platform, re, requests, os, time, shutil, glob, textwrap
import json
from pprint import pprint
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

if not os.path.exists("images/"):
	os.makedirs("images")
if not os.path.exists("fonts/"):
	os.makedirs("fonts")
if not os.path.exists("server/"):
	os.makedirs("server")


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
	print("'" + message.clean_content + "'")
	message_to_bot = False
	image_in_message = False
	if not message.author.bot:
		for mention in message.mentions:
			if mention.bot:
				print("message sent to bot")
				message_to_bot = True
		print("message sent by " + message.author.name)
		if message.server:
			servername = message.server.name
			if message.server.me.nick:
				my_name = message.server.me.nick
			else:
				my_name = client.user.name
		else:
			servername = "None"
			my_name = client.user.name
		if not os.path.exists("server/" + servername):
			os.makedirs("server/" + servername)
			os.makedirs("server/" + servername + "/images")
			os.makedirs("server/" + servername + "/output")
		if not message_to_bot:
			for attachment in message.attachments:
				imagedownload(attachment["proxy_url"], "server/" + servername + "/images/", attachment["filename"])
				print(attachment)
				image_in_message = True
			with open("server/" + servername + "/log.txt", "a") as myfile:
				if message.clean_content.endswith(".") or message.clean_content.endswith("!") or message.clean_content.endswith("?"):
					 myfile.write(message.clean_content.replace("@", ""))
				elif message.clean_content.startswith(".") or message.clean_content.startswith("!") or message.clean_content.startswith("?")  or message.clean_content.startswith("`"):
					print("message sent to bot")
					message_to_bot = True
				else:
					myfile.write(message.clean_content.replace("@", "") + ". ")
		images = re.findall('(https?:\/\/.*\.(?:png|jpg|jpeg))', message.clean_content.lower())
		for image in images:
			image_in_message = True
			imagedownload(image, "server/" + servername + "/images/")
		if len(os.listdir("server/" + servername + "/images/")) > 0:
			latest_file = max(glob.iglob("server/" + servername + "/images/*"), key=os.path.getctime)
		else:
			latest_file = max(glob.iglob("images/*"), key=os.path.getctime)
		if client.user.mentioned_in(message) or servername == "None":
			if "create meme " in message.content.lower():
				client.send_typing(message.channel)
				REMOVE_LIST = ["@", my_name , "create meme "]
				remove = '|'.join(REMOVE_LIST)
				regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
				text = regex.sub("", message.clean_content)
				print("Text: " + text)
				await client.send_file(message.channel, "server/" + servername + "/output/" + meme_image(text, servername))
			elif message.content.endswith('?'):
				if " or " in message.clean_content.lower():
					REMOVE_LIST = ["@", my_name, "\?", "should I rather", "should I", "would you rather", "what do you prefer", "who do you prefer", "do you prefer", "what is better", "what should I do", "what could I do" , "would you prefer", "decide between", "what do you like more", "decide for me between"]
					remove = '|'.join(REMOVE_LIST)
					regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
					shitdecision = re.split('; |, | Or | oR | or | OR |\n', regex.sub("", " ".join(re.sub(r'.*:', '', message.clean_content).split())))
					shitdecision = " ".join(random.choice(shitdecision).format(message).split())
					await client.send_message(message.channel, shitdecision)
				elif " who" in message.content.lower() or "who " in message.content.lower() or "who?" in message.content.lower():
					if message.server:
						await client.send_message(message.channel, random.choice(list(message.server.members)).display_name)
					else:
						await client.send_message(message.channel, random.choice(["you", "I"]))
				else:
					print(urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9'))
					yesno = urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9').read().decode('utf-8').split()
					shitanswer = random.choice (yesno).format(message)
					await client.send_message(message.channel, shitanswer)
			elif " pic" in message.content.lower() or "pic " in message.content.lower():
				client.send_typing(message.channel)
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
				await client.send_message(message.channel, """*Information:*

I'm **""" + client.user.name + "**. I'm running on " + platform.dist()[0] + " *" + platform.dist()[1] + "* with python *" + platform.python_version() + "* using discord.py *" + discord.__version__ + """*.
I'm online since *""" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time())) + "* on *" + str(len(client.servers)) + """* servers.
The log file for **""" + servername + "** is currently **" + str(num_words) + "** words and **" + str(num_chars) + "** characters long, with **" + str(sum(os.path.isfile(os.path.join("server/" + servername + "/images/", f)) for f in os.listdir("server/" + servername + "/images/")))+ """** images.
This bot was created by **""" + (await client.application_info()).owner.name + "**#" + (await client.application_info()).owner.discriminator + " with :heart:")
			elif "help" in message.content.lower():
				await client.send_message(message.channel, """*Mention me with:*

**set username** to change my username (this only works twice per hour)

	`""" + client.user.mention + """" set username NEWUSERNAME`

**set avatar** to change my avatar

	`""" + client.user.mention + """ set avatar https://website.tld/imageurl`

**create meme** to get a dank meme

	`""" + client.user.mention + """ create meme text`

**pic** to receive a custom image shitpost

	`""" + client.user.mention + """ pic`

**invite** to receive an invite link for another server

	`""" + client.user.mention + " invite`")
			elif "invite" in message.content.lower():
				await client.send_message(message.channel, discord.utils.oauth_url((await client.application_info())[0], permissions=None, server=None, redirect_uri="https://gezf.de/ebooks/"))
			elif "set avatar " in message.content.lower():
				print("new avatar: " + latest_file)
				if message.author.id == (await client.application_info()).owner.id:
					if image_in_message:
						with open(latest_file, 'rb') as f:
							await client.edit_profile(password=None,avatar=f.read())
							await client.send_message(message.channel, "**Avatar set!**")
					else:
						await client.send_message(message.channel, "**No image given!**")
				else:
					await client.send_message(message.channel, "**You are not allowed to do that!**")
			elif "set username " in message.content.lower():
				if message.author.id == (await client.application_info()).owner.id:
					REMOVE_LIST = ["@", my_name , " set username "]
					remove = '|'.join(REMOVE_LIST)
					regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
					name = regex.sub("", message.clean_content)
					print("New username: " + name)
					await client.edit_profile(password=None, username=name)
					await client.send_message(message.channel, "**Username set!**")
				else:
					await client.send_message(message.channel, "**You are not allowed to do that!**")
			else:
				await client.send_message(message.channel, shitpost(servername, message.channel))
	else:
		print("message sent by bot")

@client.event
async def on_server_join(server):
	await client.send_message(server.default_channel, "**Yahallo!** Please don't expect me to talk right away, I'm *very* shy :3")

def imagedownload(image, dir, filename=None):
	if  "imgur" in image:
		print("imgur sucks ass")
	else:
		print("Downloading: " + image)       
		imagepath = urllib.parse.urlsplit(image).path
		r = requests.get(image, stream=True)
		if r.status_code == 200:
			if filename:
				print("Saving to: " + dir + filename)
				with open(dir + filename, 'wb') as f:
					r.raw.decode_content = True
					shutil.copyfileobj(r.raw, f)
			else:
				with open(dir +  posixpath.basename(imagepath), 'wb') as f:
					print("Saving to: " + dir + posixpath.basename(imagepath))
					r.raw.decode_content = True
					shutil.copyfileobj(r.raw, f)

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

def meme_image(text, servername):
	data = json.loads(urllib.request.urlopen('https://pastebin.com/raw/fAHJ6gbC').read().decode('utf-8'))
	meme = randint(0,(len(data["memes"]) -1))
	imagename = data["memes"][meme]["image"]

	

	margin = data["memes"][meme]["size"]["left"]
	offset = data["memes"][meme]["size"]["up"]
	style = data["memes"][meme]["style"]
	print("Creating meme: " + data["memes"][meme]["image"])

	if not os.path.isfile("images/" + imagename):
		print("Downloading new Images")
		imagedownload(data["memes"][meme]["image_url"], "images/", imagename)
	if not os.path.isfile("fonts/" + data["styles"][style]["font"]):
		print("Downloading new Font")
		urllib.request.urlretrieve(data["styles"][style]["font_url"], "fonts/" + data["styles"][style]["font"])

	meme_font = ImageFont.truetype("fonts/" + data["styles"][style]["font"]  , data["styles"][style]["font_size"])

	base = Image.open("images/" + imagename).convert('RGBA')
	width, height = base.size
	txt = Image.new('RGBA', base.size, (255,255,255,0))
	d = ImageDraw.Draw(txt)
	dif = (data["memes"][meme]["size"]["right"] - data["memes"][meme]["size"]["left"])
	wrap = textwrap.wrap(" ".join(text.split()), width=dif/data["styles"][style]["font_size"])
	offset += (data["memes"][meme]["size"]["bottom"]-offset)/2-(meme_font.getsize(wrap[0])[1]*len(wrap)/2)
	if offset < data["memes"][meme]["size"]["up"]:
		offset = data["memes"][meme]["size"]["up"]
	print(offset)
	for line in wrap:
		w, h = d.textsize(line)
		print(w)
		print(dif)
		d.text((margin+(data["memes"][meme]["size"]["center"]-meme_font.getsize(line)[0])/2, offset), line, font=meme_font, fill=data["styles"][style]["font_color"])
		offset += meme_font.getsize(text)[1]
		if offset > data["memes"][meme]["size"]["bottom"] - meme_font.getsize(line)[1]:
			break
	out = Image.alpha_composite(base, txt)
	out.save("server/" + servername + "/output/" + imagename);
	print("Meme saved to: server/" + servername + "/output/" + imagename)
	return imagename

def shitimage(servername, channel):
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
	dankfont = 'fonts/' + random.choice(os.listdir('fonts/'))
	print(dankfont)
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

client.run('token')

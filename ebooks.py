import discord, asyncio, logging, time, threading, markovify, psutil, posixpath, platform, re, requests, os, time, shutil, glob, textwrap, json
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
		images = re.findall('(?i)https?:\/\/.*\.(?:png|jpg|jpeg|gif)', message.clean_content)
		for image in images:
			image_in_message = True
			imagedownload(image, "server/" + servername + "/images/")
		if len(os.listdir("server/" + servername + "/images/")) > 0:
			latest_file = max(glob.iglob("server/" + servername + "/images/*"), key=os.path.getctime)
		else:
			meme_image(shitpost(servername), servername)
			latest_file = max(glob.iglob("server/" + servername + "/images/*"), key=os.path.getctime)
		if client.user.mentioned_in(message) or servername == "None":
			if "meme_text" in message.content.lower():
				client.send_typing(message.channel)
				REMOVE_LIST = ["@", my_name , "meme_text"]
				remove = '|'.join(REMOVE_LIST)
				regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
				text = regex.sub("", message.clean_content).strip()
				if len(text) == 0:
					print("no text entered")
					text = shitpost(servername)
				print("Text: " + text)
				await client.send_file(message.channel, meme_text(text, servername))
			elif "meme_image" in message.content.lower():
				client.send_typing(message.channel)
				REMOVE_LIST = ["@", my_name , "meme_image", "(?i)https?:\/\/.*\.(?:png|jpg|jpeg|gif)"]
				remove = '|'.join(REMOVE_LIST)
				regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
				text = regex.sub("", message.clean_content).strip().lower()
				data = json.loads(urllib.request.urlopen('https://pastebin.com/raw/fAHJ6gbC').read().decode('utf-8'))
				if text in data["memes_images"]: 
					print("Meme: " + text)
					await client.send_file(message.channel, meme_image(latest_file,text, servername))	
				else:
					available_memes = ""
					for memes in data["memes_images"]:	
						available_memes += memes + "\n"
					await client.send_message(message.channel, "You need to choose one of the following memes: \n**" + available_memes + "**")
			elif " rate" in message.content.lower() or "rate " in message.content.lower():
					rating = randint(1,10)
					if rating == 10:
						await client.send_message(message.channel, "i r8 8/8 m8")
					else:
						await client.send_message(message.channel, str(rating) + "/10 " + random.choice(["memepoints", "points", "goodboipoints", "faggotpoints"]) + ".")
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
				await client.send_file(message.channel, shitimage(servername))
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

**set username** to change my username *(this only works twice per hour)*

	`""" + client.user.mention + """" set username newusername`

**set avatar** to change my avatar

	`""" + client.user.mention + """ set avatar http(s)://website.tld/imageurl`

**meme_text** to get a dank meme *(if no text is given a random sentence will be generated)*

	`""" + client.user.mention + """ meme_text sentence`

**meme_image** to get a meme_image *(uses the last posted image on the server)*

	`""" + client.user.mention + """ meme_image`

**pic** to receive a custom image shitpost

	`""" + client.user.mention + """ pic`

**invite** to receive an invite link for another server

	`""" + client.user.mention + " invite`")
			elif "invite" in message.content.lower():
				await client.send_message(message.channel, discord.utils.oauth_url((await client.application_info())[0], permissions=None, server=None))
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
				await client.send_message(message.channel, shitpost(servername))
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

def shitpost(servername):
	print("Creating shitpost for server " + servername)
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

def meme_text(text, servername):
	data = json.loads(urllib.request.urlopen('https://pastebin.com/raw/fAHJ6gbC').read().decode('utf-8'))
	meme = randint(0,(len(data["memes_text"]) -1))
	imagename = data["memes_text"][meme]["image"]

	

	margin = data["memes_text"][meme]["size"]["left"]
	offset = data["memes_text"][meme]["size"]["up"]
	style = data["memes_text"][meme]["style"]
	print("Creating meme " + data["memes_text"][meme]["image"] + " for server " + servername)

	if not os.path.isfile("images/" + imagename):
		print("Downloading new Images")
		imagedownload(data["memes_text"][meme]["image_url"], "images/", imagename)
	if not os.path.isfile("fonts/" + data["styles"][style]["font"]):
		print("Downloading new Font")
		urllib.request.urlretrieve(data["styles"][style]["font_url"], "fonts/" + data["styles"][style]["font"])

	meme_font = ImageFont.truetype("fonts/" + data["styles"][style]["font"], data["styles"][style]["font_size"])

	base = Image.open("images/" + imagename).convert('RGBA')
	width, height = base.size
	txt = Image.new('RGBA', base.size, (255,255,255,0))
	d = ImageDraw.Draw(txt)
	dif = (data["memes_text"][meme]["size"]["right"] - data["memes_text"][meme]["size"]["left"])
	wrap = textwrap.wrap(" ".join(text.split()), width=dif/data["styles"][style]["font_size"])
	offset += (data["memes_text"][meme]["size"]["bottom"]-offset)/2-(meme_font.getsize(wrap[0])[1]*len(wrap)/2)
	if offset < data["memes_text"][meme]["size"]["up"]:
		offset = data["memes_text"][meme]["size"]["up"]
	for line in wrap:
		d.text((margin+(data["memes_text"][meme]["size"]["center"]-meme_font.getsize(line)[0])/2, offset), line, font=meme_font, fill=data["styles"][style]["font_color"])
		offset += meme_font.getsize(text)[1]
		if offset > data["memes_text"][meme]["size"]["bottom"] - meme_font.getsize(line)[1]:
			break
	out = Image.alpha_composite(base, txt)
	out.save("server/" + servername + "/output/" + imagename);
	print("Meme saved to: server/" + servername + "/output/" + imagename)
	return "server/" + servername + "/output/" + imagename

def meme_image(imagename, memename, servername):
	print("Creating " + memename + " meme using " + imagename + " for server " + servername)
	data = json.loads(urllib.request.urlopen('https://pastebin.com/raw/fAHJ6gbC').read().decode('utf-8'))
	if not os.path.isfile("images/" + data["memes_images"][memename]["image"]):
		print("Downloading new Images")
		imagedownload(data["memes_images"][memename]["image_url"], "images/", data["memes_images"][memename]["image"])

	frame = Image.open("images/" + data["memes_images"][memename]["image"]).convert("RGBA")
	pic = Image.open(imagename).convert("RGBA")
	if data["memes_images"][memename]["background"] == True:
		box = data["memes_images"][memename]["box"]
		if pic.size[0] < pic.size[1]:
			scale = (box[2]/pic.size[0])
			pic = pic.resize((box[2],int(pic.size[1]*scale)), PIL.Image.ANTIALIAS)
			if pic.size[1] < box[3] - box[1]:
				scale = (box[3]/pic.size[1])
				pic = pic.resize(((int(pic.size[0]*scale),box[3])), PIL.Image.ANTIALIAS)
		else:
			scale = (box[3]/pic.size[1])
			pic = pic.resize(((int(pic.size[0]*scale),box[3])), PIL.Image.ANTIALIAS)
			if pic.size[0] < box[2] - box[0]:
				scale = (box[2]/pic.size[0])
				pic = pic.resize((box[2],int(pic.size[1]*scale)), PIL.Image.ANTIALIAS)
		center = [(pic.size[0]-box[2])/2, (pic.size[1]-box[3])/2]
		
		pic = pic.crop((center[0],center[1],center[0]+box[2],center[1]+box[3]))

		frame.paste(pic,(box[0],box[1]))
		frame.save("server/" + servername + "/output/"+ data["memes_images"][memename]["image"]);
	else:
		if pic.size[1] < frame.size[1]:
			scale = (frame.size[1]/pic.size[1])
			pic = pic.resize(((int(pic.size[0]*scale),frame.size[1])), PIL.Image.ANTIALIAS)
		if pic.size[0] < frame.size[0]:
			scale = (frame.size[0]/pic.size[0])
			pic = pic.resize((frame.size[0],int(pic.size[1]*scale)), PIL.Image.ANTIALIAS)
		if pic.size[1] < frame.size[1]:
			scale = (frame.size[1]/pic.size[1])
			pic = pic.resize(((int(pic.size[0]*scale),frame.size[1])), PIL.Image.ANTIALIAS)
		if pic.size[0] < frame.size[0]:
			scale = (frame.size[0]/pic.size[0])
			pic = pic.resize((frame.size[0],int(pic.size[1]*scale)), PIL.Image.ANTIALIAS)
		pic.paste(frame, (10, pic.size[1]-frame.size[1]-30),frame)
		pic.save("server/" + servername + "/output/"+ data["memes_images"][memename]["image"]);

	print(memename + " meme saved to: server/" + servername + "/output/" + data["memes_images"][memename]["image"])
	return("server/" + servername + "/output/" + data["memes_images"][memename]["image"])


def shitimage(servername):
	print("Creating shitimage for server " + servername)
	imagename = random.choice(os.listdir("server/" + servername + "/images/"))
	base = Image.open("server/" + servername + "/images/" + imagename).convert('RGBA')
	width, height = base.size
	if height < 200:
		imagename = random.choice(os.listdir("images/"))
		base = Image.open("images/" + imagename).convert('RGBA')
		width, height = base.size
		return meme_text(shitpost(servername), servername)
	else:
		# make a blank image for the text, initialized to transparent text color
		txt = Image.new('RGBA', base.size, (255,255,255,0))
		quote = shitpost(servername)
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
		return "server/" + servername + "/output/" + imagename


client.run('token')

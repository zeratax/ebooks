import discord, asyncio, logging, time, threading, markovify, twitter, psutil, posixpath, platform, re, requests, os, time, shutil, glob, textwrap, datetime, json
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
from pyfiglet import Figlet

logging.basicConfig(level=logging.INFO)

if not os.path.exists("images/"):
	os.makedirs("images")
if not os.path.exists("fonts/"):
	os.makedirs("fonts")
if not os.path.exists("server/"):
	os.makedirs("server")
	print("created general folder structure")

settings_ver = "5"
latest_file = random.choice(urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9').read().decode('utf-8').split())

client = discord.Client()
p = psutil.Process(os.getpid())
p.create_time()

@client.event
async def on_ready():
	print('Discord: Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await status()

@client.event
async def on_message(message):
	print("'" + message.clean_content + "'")
	global latest_file
	message_to_bot = False
	image_in_message = False
	settings = ""
	old_settings = ""
	bot_message = ""
	if not message.author.bot:
		for mention in message.mentions:
			if mention.bot:
				print("message sent to bot")
				message_to_bot = True
		print("message sent by " + message.author.name)
		if message.server:
			serverid = message.server.id
			owner = message.server.owner
			if os.path.exists("server/" +  message.server.name):
				os.rename("server/" +  message.server.name, "server/" + serverid)
			if not os.path.exists("server/" + serverid):
				os.makedirs("server/" + serverid)
				os.makedirs("server/" + serverid + "/images")
				os.makedirs("server/" + serverid + "/output")
				print("created server folder structure for " + serverid)
			if os.path.isfile("server/" + serverid + "/settings.json"):
				with open("server/" + serverid + "/settings.json", "r") as settings_file:
					settings = settings_file.read()
					settings = json.loads(settings)
			if settings != "":
				current_settings_ver = str(settings["version"])
			else:
				current_settings_ver = "0"
			if current_settings_ver != settings_ver:
				with open("server/" + serverid + "/settings.json", "w") as settings_file:
					settings_file.write('{"version" : '+settings_ver+', "farewell": true, "farewell_text": "**Hope to see you soon again, $member <3**", "greetings": true, "greetings_text" : "**Welcome $mention to __$server__**!", "sadpanda": true,"animated": "'+message.server.default_role.id+'", "meme_txt": "'+message.server.default_role.id+'", "meme_img": "'+message.server.default_role.id+'", "image": "'+message.server.default_role.id+'", "say": "'+message.server.owner.top_role.id+'", "ascii": "'+message.server.default_role.id+'", "rate": true, "sleep": true, "question": true, "info": "'+message.server.default_role.id+'", "help": "'+message.server.default_role.id+'", "options": "'+message.server.owner.top_role.id+'", "slot_machine": [":pizza:", ":frog:", ":alien:", ":green_apple:", ":heart:"] }')
					print("created new settings_file")
			if message.server.me.nick:
				my_name = message.server.me.nick
			else:
				my_name = client.user.name
			if os.path.isfile("server/" + serverid + "/settings.json"):
				if current_settings_ver != settings_ver:
					old_settings = settings
			if os.path.isfile("server/" + serverid + "/settings.json"):
				with open("server/" + serverid + "/settings.json", "r") as settings_file:
					settings = settings_file.read()
					settings = json.loads(settings)
					if old_settings != "":
						for key, value in old_settings.items():
							if key != "version":
								settings[key] = old_settings[key]
						with open("server/" + serverid + "/settings.json", "w") as settings_file:
							json.dump(settings, settings_file)
							print("settings updated")
		else:
			serverid = "None"
			owner = message.author
			my_name = client.user.name
			settings = json.loads('{"slot_machine": [":pizza:", ":frog:", ":alien:", ":green_apple:", ":heart:"], "sadpanda": true, "question": true }')
		if not message_to_bot:
			for attachment in message.attachments:
				latest_file = attachment["proxy_url"]
				image_in_message = True
			images = re.findall('(?i)https?:\/\/.*\.(?:png|jpg|jpeg|gif)', message.content)
			for image in images:
				latest_file = image
			sadpanda = re.findall('(?i)https?:\/\/(?:ex|g.e-)hentai.org\/g\/(\S{6})\/(\S{10})', message.content)
			fakku = re.findall('(?i)https:\/\/(?:www\.)fakku\.net\/(?:hentai|manga)\/\S*', message.content)
			if settings["sadpanda"] == True:
				if sadpanda:
					gidlist = []
					manga_info = ""
					payload = json.loads('{"method" : "gdata", "gidlist" : [], "namespace": 1 }')
					for index, manga in enumerate(sadpanda):
						gid = int(manga[0])
						gt = manga[1]
						payload["gidlist"].append([gid, gt])
					url = 'http://g.e-hentai.org/api.php'
					header = {'Content-type' : 'application/json'}
					print("creating json request for mangas")
					ex_response = requests.post(url, data=json.dumps(payload), headers=header)
					if ex_response.status_code == 200:
						brackets = re.compile(r'(?:\(|\[|\{)[^(?:\)|\]|\})]*(?:\)|\]|\})')
						manga_info = ex_response.json()
						print(manga_info)
						for manga in manga_info["gmetadata"]:
							title_eng = re.sub(brackets, '', re.sub(brackets, '', manga["title"])).strip()
							title_jpn = re.sub(brackets, '', re.sub(brackets, '', manga["title_jpn"])).strip()
							date = datetime.datetime.fromtimestamp(
								int(manga["posted"])
							).strftime('%Y-%m-%d %H:%M')
							artists, male_tags, female_tags, misc_tags, parodies, groups, characters, languages = ([] for i in range(8))
							artist, male, female, misc, parody, group, character, language = ("" for i in range(8))
							for tag in manga["tags"]:
								if "artist:" in tag:
									artists.append(tag[7:])
								elif "female:" in tag:
									female_tags.append(tag[7:])
								elif "male:" in tag and not "female:" in tag:
									male_tags.append(tag[5:])
								elif "parody:" in tag:
									parodies.append(tag[7:])
								elif "group:" in tag:
									groups.append(tag[6:])
								elif "character:" in tag:
									characters.append(tag[10:])
								elif "language:" in tag:
									languages.append(tag[9:])
								else:
									misc_tags.append(tag)
							if artists:
								artist = "\n **Artist:** " + str(artists)[:-1][1:].replace("'", "")
							if groups:
								group = "\n **Group:** " + str(groups)[:-1][1:].replace("'", "")
							if parodies:
								parody = "\n  **Parody:** " + str(parodies)[:-1][1:].replace("'", "")
							if characters:
								character = "\n  **Character:** " + str(characters)[:-1][1:].replace("'", "")
							if female_tags:
								female = "\n  **Female:** " + str(female_tags)[:-1][1:].replace("'", "")
							if male_tags:
								male = "\n  **Male:** " + str(male_tags)[:-1][1:].replace("'", "")
							if misc_tags:
								misc = "\n  **Misc:** " + str(misc_tags)[:-1][1:].replace("'", "")
							if languages:
								language = "\n **Language:** " + str(languages)[:-1][1:].replace("'", "")
							rating = ""
							for i in range(round(float(manga["rating"])*2)):
								rating += ":star:"
							if title_jpn != title_eng:
								title = "__" + title_eng + "** / **" + title_jpn + "__"
							else:
								title = "__" + title_eng + "__"
							bot_message += title + "\n **Category:** " + manga["category"] + language + artist + group + "\n **Posted:** " + date + "\n **Rating:** " + rating + " (" + manga["rating"] + ")\n **Tags:** " + parody + character + female + male + misc + "\n **Thumb:** " + manga["thumb"]
							print("posting manga info")
						await client.send_message(message.channel, bot_message)
					else:
						manga_info = None
						print(ex_response)
				if fakku:
					for manga in fakku:
						manga = manga.replace("hentai", "manga")
						manga = manga.split('fakku.net', 1)[-1]
						manga = "https://api.fakku.net" + manga
						data = json.loads(urllib.request.urlopen(manga).read().decode('utf-8'))
						data = data["content"]
						date = datetime.datetime.fromtimestamp(
							int(data["content_date"])
						).strftime('%Y-%m-%d %H:%M')
						tags = "["
						for tag in data["content_tags"]:
							tags += "'" + tag["attribute"] + "', "
						tags = tags[:-2] + "]"
						if len(data["content_artists"]) > 1:
							artist_tag = "\n **Artists:** "
						else:
							artist_tag = "\n **Artist:** "
						for artist in data["content_artists"]:
							artist_tag += artist["attribute"] + ", "
						artist_tag = artist_tag[:-2]
						if len(data["content_series"]) > 1:
							parody_tag = "\n **Parodies:** "
						else:
							parody_tag = "\n **Parody:** "
						for serie in data["content_series"]:
							parody_tag += serie["attribute"] + ", "
						parody_tag = parody_tag[:-2]
						bot_message += "__" + data["content_name"] + "__\n **Category:** " + data["content_category"] + artist_tag + parody_tag + "\n **Posted:** " + date + "\n **Favorites:** " + str(data["content_favorites"]) + " :heart:\n **Description:** " + data["content_description"] + "\n **Tags: **" + tags[:-1][1:].replace("'", "")
					await client.send_message(message.channel, bot_message)
			with open("server/" + serverid + "/log.txt", "a") as myfile:
				if message.clean_content.endswith(".") or message.clean_content.endswith("!") or message.clean_content.endswith("?"):
					 myfile.write(message.clean_content.replace("@", ""))
				elif message.clean_content.startswith(".") or message.clean_content.startswith("!") or message.clean_content.startswith("?")  or message.clean_content.startswith("`"):
					print("message sent to bot")
					message_to_bot = True
				else:
					myfile.write(message.clean_content.replace("@", "") + ". ")
		if client.user.mentioned_in(message) or serverid == "None":
			if "roles" in message.content.lower() and message.author.id == (await client.application_info()).owner.id:
				if serverid == "None":
					await client.send_message(message.channel, "This only works on servers.")
				else:
					bot_message = "**top role:** " + str(owner.top_role.name) + " **position:** " + str(owner.top_role.position) + "\n**default role:** " + str(message.server.default_role.name) + " **position:** " + str(message.server.default_role.position) + "\n**your roles are:** " + str(user_role_ids(message.author))
					bot_message += " \n__role hierachy:__\n"
					for roles in message.server.roles:
						bot_message += "**name:** " + roles.name + " **position: **" + str(roles.position) + " **ID: **" + str(roles.id) + "\n"
					await client.send_message(message.channel, bot_message)
			elif "raw" in message.content.lower():
				await client.send_message(message.channel, "`" + message.content + "`")
			elif ( "settings" in message.content.lower() ) and ( message.author.id == owner.id or settings["options"] in user_role_ids(message.author) ):
				client.send_typing(message.channel)
				REMOVE_LIST = [client.user.mention[:2] + '!' + client.user.mention[2:], client.user.mention, "settings"]
				if " set " in message.content.lower():
					REMOVE_LIST.append("set")
					remove = '|'.join(REMOVE_LIST)
					regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
					text = regex.sub("", message.content.lower()).strip().split(' ', 1)
					if text[0] == "version":
						await client.send_message(message.channel, "**Error:** you can't change the version.")
					elif text[0] not in settings:
						await client.send_message(message.channel, "**Error:** this option doesn't exist.")
					elif text[0] == "slot_machine":
						settings["slot_machine"] = text[1].split()
					else:
						if text[1] == "true":
							settings[text[0]] = True
						elif text[1] == "false":
							settings[text[0]] = False
						elif text[1] == "@everyone":
							settings[text[0]] = message.server.default_role.id
						elif text[1].startswith("<"):
							settings[text[0]] = text[1][3:21]
						else:
							settings[text[0]] = text[1]
					if serverid == "None":
						await client.send_message(message.channel, "**Error:** You can not change settings in privat messages.")
					else:
						await client.send_message(message.channel, "**Success:** set *" + text[0] + "* to " + text[1] + ".")
					with open("server/" + serverid + "/settings.json", "w") as settings_file:
						json.dump(settings, settings_file)
						print("updated settings_file")
				elif " show" in message.content.lower():
					REMOVE_LIST.append("show")
					remove = '|'.join(REMOVE_LIST)
					regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
					text = regex.sub("", message.content.lower()).strip().split(' ', 1)
					bot_message = "__Settings:__\n"
					for key, value in settings.items():
						if isinstance(value, (int, bool, list)):
							value = str(value)
						elif key != "farewell_text" and key != "greetings_text":
							value = "<@&" + value + ">"
						if not text == ['']:
							if text[0] == "quiet":
								bot_message += "`Option:	" + key + "	Value:	" + value + "`\n"
							elif text[0] not in settings:
								bot_message = "**Error:** this option doesn't exist.\n"
								break
							else:
								if isinstance(settings[text[0]], (int, bool, list)):
									value = str(settings[text[0]])
								elif text[0] != "farewell_text" and text[0] != "greetings_text":
									value = "<@&" + settings[text[0]] + ">"
								else:
									value = settings[text[0]]
								if len(text) > 2:
									bot_message = "**Error**: too many arguments\n"
								elif len(text) > 1 and text[1] == "quiet":
									bot_message = "`Option:	" + text[0] + "	Value:	" + value + "`\n"
								elif len(text) > 1 and text[1] != "quiet":
									bot_message = "**Error**: wrong argument\n"
								else:
									bot_message = "**Option:** " + text[0] + " **Value:** " + value + "\n"
								break
						else:
							bot_message += "**Option:** " + key + " **Value:** " + value + "\n"
					await client.send_message(message.channel, bot_message)
				elif " json dump" in message.content.lower():
					await client.send_message(message.server.owner, "These were your old settings for your server: __"+message.server.name+"__\n```js\n" + json.dumps(settings) + "```")
				elif " settings set" in message.content.lower():
					for key, value in settings.items():
						bot_message += key + "\n"
					await client.send_message(message.channel, "**Error:** You need to choose one of the following options: \n**" + bot_message + "**\nFor current values use `settings show`")
				else:
					await client.send_message(message.channel, "**Error:** Further arguments are needed, eg: `show, set`")
			elif ( "say" in message.content.lower() and message.channel_mentions ) and ( message.author.id == owner.id or settings["say"] in user_role_ids(message.author) ):
				client.send_typing(message.channel)
				REMOVE_LIST = ["@" + my_name, "@", "say" ,"#"]
				for channel in message.channel_mentions:
					REMOVE_LIST.append(channel.name)
				remove = '|'.join(REMOVE_LIST)
				regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
				text = regex.sub("", message.clean_content).strip()
				for channel in message.channel_mentions:
					await client.send_message(channel, text)
			elif ( "animated" in message.content.lower() ) and ( message.author.id == owner.id or settings["animated"] in user_role_ids(message.author) ):
				if "dick" in message.content.lower():
					bot_message = "8"
					dick = await client.send_message(message.channel, bot_message)
					for i in range(randint(4,15)):
						bot_message += "="
						await asyncio.sleep(1)
						await client.edit_message(dick, bot_message)
					bot_message += "D"
					await client.edit_message(dick, bot_message)
				elif "slot" in message.content.lower() and "machine" in message.content.lower():
					choice = ["","",""]
					for y in range(3):
						choice[y] = random.choice(settings["slot_machine"])
					bot_message = "[" + choice[0] + "][" + choice[1] + "][" + choice[2] + "]"
					slot_machine = await client.send_message(message.channel, bot_message)
					for x in range(5):
						for y in range(3):
							choice[y] = random.choice(settings["slot_machine"])
						bot_message =  "[" + choice[0] + "][" + choice[1] + "][" + choice[2] + "]"
						await asyncio.sleep(1)
						await client.edit_message(slot_machine, bot_message)
					if choice[0]==choice[1] and choice[0]==choice[2]:
						await client.send_message(message.channel, ":trophy: **"+message.author.name.upper()+" WON!** :trophy:")
					else:
						await client.send_message(message.channel, "maybe next time.")
				else:
					await client.send_message(message.channel,  "**Error:** You need to choose one of the following memes: \n**dick**\n**slot_machine**")
			elif ( "meme_text" in message.content.lower() or  "meme_txt" in message.content.lower() ) and ( ( message.author.id == owner.id or settings["meme_txt"] in user_role_ids(message.author) ) ):
				client.send_typing(message.channel)
				REMOVE_LIST = ["@" + my_name, "@", "meme_text", "meme_txt"]
				remove = '|'.join(REMOVE_LIST)
				regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
				text = regex.sub("", message.clean_content).strip()
				if len(text) == 0:
					print("no text entered")
					text = shitpost(serverid)
				print("Text: " + text)
				await client.send_file(message.channel, meme_text(text, serverid))
			elif ( "meme_image" in message.content.lower() or  "meme_img" in message.content.lower() ) and (( message.author.id == owner.id or settings["meme_img"] in user_role_ids(message.author) )):
				client.send_typing(message.channel)
				REMOVE_LIST = ["@" + my_name, "@", "meme_image", "meme_img", "(?i)https?:\/\/.*\.(?:png|jpg|jpeg|gif)"]
				remove = '|'.join(REMOVE_LIST)
				regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
				text = regex.sub("", message.clean_content).strip().lower()
				data = json.loads(urllib.request.urlopen('https://pastebin.com/raw/fAHJ6gbC').read().decode('utf-8'))
				print(text)
				if text in data["memes_images"]:
					print("Meme: " + text)
					await client.send_file(message.channel, meme_image(latest_file, text, serverid))
				else:
					for memes in data["memes_images"]:
						bot_message += memes + "\n"
					await client.send_message(message.channel, "**Error:** You need to choose one of the following memes: \n**" + bot_message + "**")
			elif "ascii" in message.content.lower() and (( message.author.id == owner.id or settings["ascii"] in user_role_ids(message.author) )):
				client.send_typing(message.channel)
				emoji = re.findall('<(:\S*:)\d*>', message.clean_content)
				print(emoji)
				REMOVE_LIST = ["@" + my_name, "@", "ascii", "<:\S*:\d*>"]
				remove = '|'.join(REMOVE_LIST)
				regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
				text = regex.sub("", message.clean_content).strip().upper()
				f = Figlet(font='alphabet')
				if not text:
					await client.send_message(message.channel, "**Error:** You need to write some text")
				else:
					await client.send_message(message.channel, "```" + f.renderText(text) + "```")
			elif (" rate" in message.content.lower() or "rate " in message.content.lower()) and (settings["rate"] == True):
					rating = randint(1,10)
					if rating == 10:
						await client.send_message(message.channel, "i r8 8/8 m8")
					else:
						await client.send_message(message.channel, str(rating) + "/10 " + random.choice(["memepoints", "points", "goodboipoints", "faggotpoints"]) + ".")
			elif (" sleep" in message.content.lower() or "sleep " in message.content.lower() or "good night" in message.content.lower()) and (settings["sleep"] == True):
				kaga = urllib.request.urlopen('https://pastebin.com/raw/4DxVcG4n').read().decode('utf-8').split()
				kaga_posting = random.choice (kaga)
				await client.send_message(message.channel, kaga_posting)
			elif message.content.endswith('?') and (settings["question"] == True):
				if " or " in message.content.lower():
					REMOVE_LIST = ["@" + my_name, "@", "\?", "should I rather", "should I", "would you rather", "what do you prefer", "who do you prefer", "do you prefer", "what is better", "what should I do", "what could I do" , "would you prefer", "decide between", "what do you like more", "decide for me between"]
					remove = '|'.join(REMOVE_LIST)
					regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
					shitdecision = re.split('; |, | Or | oR | or | OR |\n', regex.sub("", message.clean_content))
					shitdecision = " ".join(random.choice(shitdecision).split())
					await client.send_message(message.channel, shitdecision)
				elif " who" in message.content.lower() or "who " in message.content.lower() or "who?" in message.content.lower():
					if message.server:
						await client.send_message(message.channel, random.choice(list(message.server.members)).display_name)
					else:
						await client.send_message(message.channel, random.choice(["you", "I"]))
				else:
					yesno = urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9').read().decode('utf-8').split()
					shitanswer = random.choice (yesno)
					await client.send_message(message.channel, shitanswer)
			elif "info" in message.content.lower() and ( ( message.author.id == owner.id or settings["info"] in user_role_ids(message.author) ) ):
				if serverid == "None":
					servername = "None"
				else:
					servername = message.server.name
				num_lines = 0
				num_words = 0
				num_chars = 0

				with open("server/" + serverid + "/log.txt", 'r') as f:
					for line in f:
						words = line.split()

						num_lines += 1
						num_words += len(words)
						num_chars += len(line)
				await client.send_message(message.channel, """*Information:*

I'm **""" + client.user.name + "**. I'm running on " + platform.dist()[0] + " *" + platform.dist()[1] + "* with python *" + platform.python_version() + "* using discord.py *" + discord.__version__ + """*.
I'm online since *""" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time())) + "* on *" + str(len(client.servers)) + """* servers.
The log file for **""" + servername + "** is currently **" + str(num_words) + "** words and **" + str(num_chars) + "** characters long, with **" + str(sum(os.path.isfile(os.path.join("server/" + serverid + "/images/", f)) for f in os.listdir("server/" + serverid + "/images/")))+ """** images.
This bot was created by """ + (await client.application_info()).owner.mention + " with :heart:\nSource: https://github.com/ZerataX/ebooks")
			elif "help" in message.content.lower() and ( ( message.author.id == owner.id or settings["help"] in user_role_ids(message.author) ) ):
				await client.send_message(message.author, """*Mention me with:*

**set username** to change my username *(this only works twice per hour)*

	`""" + client.user.mention + """" set username newusername`

**set avatar** to change my avatar

	`""" + client.user.mention + """ set avatar http(s)://website.tld/imageurl`

**settings set** to change an option

	`""" + client.user.mention + """ settings set option value`

**settings show** shows the currently set options

	`""" + client.user.mention + """ settings show`

**meme_text** to get a dank meme *(if no text is given a random sentence will be generated)*

	`""" + client.user.mention + """ meme_text sentence`

**meme_image** to get a meme_image *(uses the last posted image on the server)*

	`""" + client.user.mention + """ meme_image`

**invite** to receive an invite link for another server

	`""" + client.user.mention + """ invite`

A more detailed documentation is available here: https://github.com/ZerataX/ebooks/blob/master/README.md
	""")
			elif "invite" in message.content.lower():
				if "all" in message.content.lower() and message.author.id == (await client.application_info()).owner.id:
					print("creating invites")
					bot_message += "__Invites:__\n"
					for server in client.servers:
						print("trying to create invite for " + server.name)
						if server.me.server_permissions.create_instant_invite:
							print("succeeded")
							invite = await client.create_invite(server, max_age=30)
							bot_message += "**Server:** " + server.name + " **Invite**: " + invite.url + "\n"
						else:
							print("failed")
							bot_message += "**Server:** " + server.name + " **Invite**: could not create invite *(missing permission)*\n"
					await client.send_message(message.channel, bot_message)
				elif "delete" in message.content.lower() and message.author.id == (await client.application_info()).owner.id:
					invites = re.findall("(https?:\/\/discord\.gg\/[\da-zA-Z]+)", message.content)
					for invite in invites:
						print("trying to delete invite: '" + invite + "'")
						invite = await client.get_invite(invite)
						if invite.inviter == client.user:
							await client.delete_invite(invite)
							print("succeeded")
							await client.send_message(message.channel, "**Success:** deleted invite: " + invite.url)
						else:
							print("failed")
							await client.send_message(message.channel, "**Error:** could not deleted invite: " + invite.url)
				else:
					await client.send_message(message.author, discord.utils.oauth_url((await client.application_info())[0], permissions=None, server=None))
			elif "set avatar " in message.content.lower():
				if message.author.id == (await client.application_info()).owner.id:
					if image_in_message:
						print("new avatar: " + latest_file)
						imagedownload(latest_file, "server/images/", "avatar.png")
						with open("server/images/avatar.png", 'rb') as f:
							await client.edit_profile(password=None,avatar=f.read())
							await client.send_message(message.author, "**Success:** Avatar set!")
					else:
						await client.send_message(message.channel, "**Error:** No image given!")
				else:
					await client.send_message(message.channel, "**Error:** You are not allowed to do that!")
			elif "set username " in message.content.lower():
				if  message.author.id == (await client.application_info()).owner.id:
					REMOVE_LIST = ["@", my_name , " set username "]
					remove = '|'.join(REMOVE_LIST)
					regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
					name = regex.sub("", message.clean_content)
					print("New username: " + name)
					await client.edit_profile(password=None, username=name)
					await client.send_message(message.channel, "**Success:** Username set!")
				else:
					await client.send_message(message.channel, "**Error:** **You are not allowed to do that!")
			else:
				await client.send_message(message.channel, shitpost(serverid))
	else:
		print("message sent by bot")

@client.event
async def on_server_join(server):
	await client.send_message(server.default_channel, "**Yahallo!** Please don't expect me to talk right away, I'm *very* shy :3")
	await client.send_message(server.owner, "I was just added to your server, "+server.name+". Most interactions with me work by mentioning me. For more help on command-usage use:\n`" + client.user.mention + " help`\n\nFor a documentation or more help visit:\nhttps://github.com/ZerataX/ebooks\nor message the creator of this bot " + (await client.application_info()).owner.mention + ".")

@client.event
async def on_server_remove(server):
	await client.send_message(server.owner, "WHY DON'T YOU LOVE ME! ;_;")
	await client.send_message(server.owner, "You can invite me again with:\n" +discord.utils.oauth_url((await client.application_info())[0], permissions=None, server=server))
	await client.send_message(server.owner, "If you had any *trouble* or just want to give feedback you can message: " + (await client.application_info()).owner.mention + "\nor open an issue: https://github.com/ZerataX/ebooks/issues/new")

@client.event
async def on_member_join(member):
	with open("server/" + member.server.id + "/settings.json", "r") as settings_file:
		settings = settings_file.read()
		settings = json.loads(settings)
		if settings["greetings"] == True:
			await client.send_message(member.server.default_channel, str(settings["greetings_text"]).replace("$member", member.name).replace("$mention", member.mention).replace("$server", member.server.name))

@client.event
async def on_member_remove(member):
	with open("server/" + member.server.id + "/settings.json", "r") as settings_file:
		settings = settings_file.read()
		settings = json.loads(settings)
		if settings["farewell"] == True:
			await client.send_message(member.server.default_channel, str(settings["farewell_text"]).replace("$member", member.name).replace("$mention", member.mention).replace("$server", member.server.name))

def user_role_ids(user):
	roles = []
	for role in user.roles:
		roles.append(role.id)
	return roles

def substract(a, b):
    return "".join(a.rsplit(b))

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

def shitpost(serverid):
	print("Creating shitpost for server " + serverid)
	with open("server/" + serverid + "/log.txt") as f:
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

def meme_text(text, serverid):
	data = json.loads(urllib.request.urlopen('https://pastebin.com/raw/fAHJ6gbC').read().decode('utf-8'))
	meme = randint(0,(len(data["memes_text"]) -1))
	imagename = data["memes_text"][meme]["image"]



	margin = data["memes_text"][meme]["size"]["left"]
	offset = data["memes_text"][meme]["size"]["up"]
	style = data["memes_text"][meme]["style"]
	print("Creating meme " + data["memes_text"][meme]["image"] + " for server " + serverid)

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
	out.save("server/" + serverid + "/output/" + imagename);
	print("Meme saved to: server/" + serverid + "/output/" + imagename)
	return "server/" + serverid + "/output/" + imagename

def meme_image(imageurl, memename, serverid):
	imagedownload(imageurl, "server/" + serverid + "/images/", "meme_image")
	imagename = "server/" + serverid + "/images/meme_image"
	print("Creating " + memename + " meme using " + imageurl + " for server " + serverid)

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
		frame.save("server/" + serverid + "/output/"+ data["memes_images"][memename]["image"]);
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
		pic.save("server/" + serverid + "/output/"+ data["memes_images"][memename]["image"]);

	print(memename + " meme saved to: server/" + serverid + "/output/" + data["memes_images"][memename]["image"])
	return("server/" + serverid + "/output/" + data["memes_images"][memename]["image"])


def shitimage(serverid):
	print("Creating shitimage for server " + serverid)
	imagename = random.choice(os.listdir("server/" + serverid + "/images/"))
	base = Image.open("server/" + serverid + "/images/" + imagename).convert('RGBA')
	width, height = base.size
	if height < 200:
		imagename = random.choice(os.listdir("images/"))
		base = Image.open("images/" + imagename).convert('RGBA')
		width, height = base.size
		return meme_text(shitpost(serverid), serverid)
	else:
		# make a blank image for the text, initialized to transparent text color
		txt = Image.new('RGBA', base.size, (255,255,255,0))
		quote = shitpost(serverid)
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
		out.save("server/" + serverid + "/output/shitpost.png");
		print(imagename)
		return "server/" + serverid + "/output/shitpost.png"

async def status():
	await client.change_presence(game=discord.Game( name=shitpost("None")))
	await asyncio.sleep(300)
	await status()
	
client.run('token')

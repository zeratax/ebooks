# ebooks
Creates markov-chains from text gathered in a discord server to then post them or write them on images.
*And lots more*...

Uses [discord.py](https://github.com/Rapptz/discord.py), [markovify](https://github.com/jsvine/markovify), [python-pillow](https://github.com/python-pillow/Pillow) and [pyfiglet](https://github.com/pwaller/pyfiglet)

## setup
replace *token* on the last line
`client.run('token')`
with your bot token

or just **invite** the bot to your server with:

https://discordapp.com/oauth2/authorize?client_id=189772464161685506&scope=bot

## usage
### commands

**set username** to change my username *(this only works twice per hour)*

	@ebooks set username newusername

**set avatar** to change my avatar

	@ebooks set avatar http(s)://website.tld/imageurl

**settings set** to change an option

	@ebooks settings set option value

**settings show** shows the currently set options

	@ebooks settings show

**meme_text** to get a dank meme *(if no text is given a random sentence will be generated)*

	@ebooks meme_text sentence

**meme_image** to get a meme_image *(uses the last posted image on the server)*

	@ebooks meme_image
  
**animated** send an animated text message

	@ebooks animated animation

**invite** to receive an invite link for another server

	@ebooks invite

### manga preview
when *sadpanda* is set to *true* the bot will post the info
![manga preview](https://my.mixtape.moe/rmseba.png)
### farewell/greetings
if *farewell* or *greetings* is set to *true* the bot will post a configurable message as soon as a new member joins/leaves.

set this message with
`@ebooks settings set farewell_text/greetings_text **Hope to see you soon again, $member <3**`

possible **variables** are:

  1. **$member**   will be replaced with the name of the new/leaving member
  
  2. **$mention**  will be replaced with a mention of that user
  
  3. **$server**   will be replaced with the name of that server

### animated text
#### slot_machine
set the slot machine items with
`@ebooks settings set slot_machine emoji1 emoji2 emoji3 ... emojiN`

![slot_machine](https://my.mixtape.moe/ljzych.gif)

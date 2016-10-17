# ebooks
Creates markov-chains from text gathered in a discord server to then post them or write them on images. *And lots more…*

Uses [discord.py](https://github.com/Rapptz/discord.py), [markovify](https://github.com/jsvine/markovify), [python-pillow](https://github.com/python-pillow/Pillow) and [pyfiglet](https://github.com/pwaller/pyfiglet)

# Table of Contents
[Setup](#setup)

[Usage](#usage)

[Settings](#settings)

[Contributing](#contributing)

[License](#license)

# Setup
replace *token* on the last line
`client.run('token')`
with your bot token

make sure you have the correct libraries installed 

start with `python3.5 ebooks.py`
____________

or just **invite** the bot to your server with:

https://discordapp.com/oauth2/authorize?client_id=189772464161685506&scope=bot

# Usage
## Commands

**set username** to change my username *(this only works twice per hour)*

	@ebooks set username newusername

**set avatar** to change my avatar

	@ebooks set avatar http(s)://website.tld/imageurl

**[settings set](#settings-set)** to change an option

	@ebooks settings set option value

**[settings show](#settings-show)** shows the currently set options

	@ebooks settings show

**[meme text](#meme-text)** to get a dank meme *(if no text is given a random sentence will be generated)*

	@ebooks meme_text sentence

**[meme image](#meme-image)** to get a meme_image *(uses the last posted image on the server)*

	@ebooks meme_image
  
**[animated](#animated-text)** send an animated text message

	@ebooks animated animation
	
**[ascii](#ascii)** turns your message into huge ascii letters

	@ebooks ascii string
	
**say** sends a message to all mentioned channels

	@ebooks say string #channel-mention1 #channel-mention2 … #channel-mentionN

**invite** to receive an invite link for another server

	@ebooks invite
	
### Animated Text
#### slot machine
Set the slot machine items with
`@ebooks settings set slot_machine emoji1 emoji2 emoji3 … emojiN`

![slot_machine](https://my.mixtape.moe/ljzych.gif)

#### dick
*Yeah i know…*

![dick](https://my.mixtape.moe/oesvvd.gif)

### meme text
Alias: `meme_txt, meme_text`

![meme text](https://my.mixtape.moe/tvcner.gif)

### meme image
Alias: `meme_img, meme_image`
### ascii
Turns text into ascii:

![ascii text](https://my.mixtape.moe/rnufgu.png)

## Manga preview
When `sadpanda` is set to `true` the bot will post the info

![sadpanda manga preview](https://my.mixtape.moe/ukcncv.png)

when `fakku` is set to `true` the bot will post the info

![fakku manga preview](https://my.mixtape.moe/mqktst.png)
## Farewell and Greetings
If `farewell` or `greetings` is set to `true` the bot will post a configurable message as soon as a new member joins/leaves.

set this message with
`@ebooks settings set farewell_text/greetings_text **Hope to see you soon again, $member <3**`

possible **variables** are:

  1. **$member**   will be replaced with the name of the new/leaving member
  
  2. **$mention**  will be replaced with a mention of that user
  
  3. **$server**   will be replaced with the name of that server


##  Conversation
### Questions
Questions are messages with a bot mention and ending on a `?`

#### choice
If the [question](#questions) contains an `or` the bot will decide between the choices. You can add more choices with a `,`.

![choice](https://my.mixtape.moe/ozdgry.png)

#### yes/no
If no `or` is included the bot presumes this is a yes/no question and sends an image-url to an anime girl saying either yes or no.

### Sleep
If a message contains the word `sleep` or `night`, the bot will respond with an image-url to a [kagapost](http://knowyourmeme.com/memes/kancolle-sleep-kagaposting)
### Ratings
If you include the word `rate` in your message the bot will give a rating from 1 to 10.

# Settings
## settings set
For commands that only a certain role should be able to use, you can just use a role mention.

Currently those are: 

 1. [info](#settings) *(settings command)*
 2. [meme_img](#meme-image)
 3. [meme_txt](#meme-text)
 4. image (the deprecated pic command)
 5. help
 6. [ascii](#ascii)
 7. [animated](#animated-text)
 8. say
	
	
![role option](https://my.mixtape.moe/srpihy.png)

You can disable certain context cues by setting them to `false`.

Currently those are: 

 1. [question](#questions)
 2. [fakku](#manga-preview)
 3. [sadpanda](#manga-preview)
 4. [rate](#ratings)
 5. [farewell](#farewell-and-greetings)
 6. [greetings](#farewell-and-greetings)
 7. [animated](#animated-text)
 8. [sleep](#sleep)
	
![bool option](https://my.mixtape.moe/llvigt.png)

The other options are:

 1. [farewell_text](#farewell-and-greetings)
 2. [greetings_text](#farewell-and-greetings)
 3. [slot_machine](#slot-machine)
 
## settings show
If you don't give any further arguments every option will be displayed:

![settings show all](https://my.mixtape.moe/wtqjbz.png)

If you add the name of one option only that will be shown:

![settings show one](https://my.mixtape.moe/dwevli.png)

If you only want mentions and raw text add a `quiet` at the end:

![settings quiet](https://my.mixtape.moe/riikap.png)

## settings advanced
If you're hosting an instance yourself and want to manually edit the settings for a server, you can find a settings.json in every server directory (the directories are named after the server ids)
Example:
```js
{
	"info": "236706075779268609", 
	"meme_img": "236706075779268609", 
	"question": true, 
	"greetings_text": "**Welcome $mention to __$server__**!", 
	"version": 6, 
	"image": "236706075779268609", 
	"slot_machine": [":pizza:", ":frog:", ":alien:", ":green_apple:", ":heart:"], 
	"fakku": true, 
	"sadpanda": true, 
	"farewell_text": "**Hope to see you soon again, $member <3**", 
	"meme_txt": "236706075779268609", 
	"help": "236706075779268609", 
	"options": "236806163763560449", 
	"rate": true, 
	"farewell": false, 
	"ascii": "236706075779268609", 
	"greetings": false, 
	"animated": "236706075779268609", 
	"sleep": true, 
	"say": "236806163763560449"
}
```
the version key is need to add new options to the settings file.
the long numbers resemble the role id.
`189775065116573696` is the @everyone role

# contributing
Besides the usual code cleaning I should do and new memes, both commands [meme image](#meme-image) and [meme text](#meme-text) both use this json file: [info.json](info.json)

You can easily create new memes for these two commands by make pull requests for this file.

To add a new image for [meme text](#meme-text) add an entry in this form: *(play around with the size, it's not pixel based.=*
```js
{
  "memes_text": [
    {
      "image": "image name",
      "image_url": "image url",
      "style": "choose a style",
      "size": {
        "up": border top (integer),
        "left": border left (integer),
        "bottom": border bottom (integer),
        "right": border right (integer),
        "center": center point (integer)
      }
    }
  ]
}
```
If you want to use a different font, you can define a new style like this:
```js
{
  "styles": {
    "manga00": {
      "font": "font name",
      "font_size": font size,
      "font_color": "font color in hex-decimal",
      "font_url": "a link to the font"
    }
}
```
To add a new meme for [meme image](#meme-image) add an entry in this form: *(if background is set to true the original image will be placed on top)*
```js
{
  "memes_images": {
    "name of meme": {
      "image": "image name",
      "image_url": "image url",
      "background" : bool
    }
  }
}
```
#License
ebooks uses a gpl license available [here](LICENSE)

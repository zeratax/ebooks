import discord, asyncio, logging, time, threading, markovify, twitter
logging.basicConfig(level=logging.INFO)

client = discord.Client()
api = twitter.Api(consumer_key='token',
                      consumer_secret='token',
                      access_token_key='token',
                      access_token_secret='token')
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
        print(message.clean_content)
    yesno = urllib.request.urlopen('https://pastebin.com/raw/90WCeZp9').read().decode('utf-8').split() # it's a file like object and works just like a file

    if client.user.mentioned_in(message):
        if message.content.endswith('??'):
            if 'or' in message.clean_content:
                REMOVE_LIST = ["@tsumino_ebooks", "\?"]
                remove = '|'.join(REMOVE_LIST)
                regex = re.compile(r'('+remove+')', flags=re.IGNORECASE)
                shitdecision = regex.sub("", message.clean_content).split("or")
                shitdecision = random.choice (shitdecision).format(message)
                await client.send_message(message.channel, shitdecision)
                print(shitdecision)
            else:
                shitanswer = random.choice (yesno).format(message)
                await client.send_message(message.channel, shitanswer)
                print(shitanswer)
        else:
            with open("log.txt") as f:
                text = f.read()
                
            text_model = markovify.Text(text)
            shitpost = text_model.make_short_sentence(50)
            if shitpost is not None:
                shitpost = shitpost.format(message)
                await client.send_message(message.channel, shitpost)  
            else:
                shitpost = text_model.make_short_sentence(50)
                if shitpost is not None:
                    shitpost = shitpost.format(message)
                    await client.send_message(message.channel, shitpost)
                else:
                    await client.send_message(message.channel, 'Fuck off~')

def tweet():

    with open("log.txt") as f:
        text = f.read()

    text_model = markovify.Text(text)

    shittweet = text_model.make_short_sentence(50)
    print(shittweet)
    if shittweet is not None:
        if (len(shittweet) > 0 and len(shittweet) < 141):
            status = api.PostUpdate(shittweet)
            print(status.text)
    threading.Timer(3600, tweet).start()

tweet()

client.run('token')

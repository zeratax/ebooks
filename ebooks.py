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
        myfile.write(message.content + " ")
        print(message.content)

def tweet():
    # Get raw text as string.
    with open("log.txt") as f:
    	text = f.read()

    # Build the model.
    text_model = markovify.Text(text)
    # update Twitter status
    status = api.PostUpdate(text_model.make_short_sentence(140))
    print(status.text)
    threading.Timer(10800, tweet).start()

tweet()

client.run('token')

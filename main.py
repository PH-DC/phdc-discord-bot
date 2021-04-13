#Imports
import discord
import os
import requests
import json
import random
from keep_alive import keep_alive

#Variables
client = discord.Client()

bad_words = [
    "Fuck", "fuck", "Fuck You", "Shit", "Piss off", "Fuck off", "Dick head", "Asshole",
    "Son of a bitch", "Bastard", "Bitch", "Wanker"
]

sad_words = ["error", "build failed", "not working", "bug", "failed", "err", "buggy"]

warning = [
    ">>> ⚠ Please avoid using Swear Words it is against our server policy!",
    ">>> ⚠ Use of Swear Words are against our server policy!",
    ">>> ⚠ Bullying someone using Swear Words are against our server policy!"
]

solution = [
    ">>> 🤔 I think you should find something on stackoverflow !\n💡 Tip: Sharing your project link is also helpful"
]

projects = [
    ">>> **Live Projects** \n1. Discord Bot\n2. PDC Application\n3. PDC Website\n4. Hacktober Practice\n5. Hacktober Website\n6. API"
]

core_team_1 = [
    ">>> **Core Team** \n1. Lead: Random Name\n2. Co Lead: Random Name\n3. Web Lead: Random Name"
]

help_data = [
    ">>> **Help Commands** \n\nThese are the available commands:\n\n1. `!pdc help` - Dailogue of all commands\n2. `!pdc info` -  Gives info of bot\n3. `!pdc about` -  Returns server information\n4. `!pdc discord` - Provides invitation link for the discord server\n5. `!pdc github` - Provides link to the github organisation\n6. `!pdc core team` - Returns current Core Member\n7. `!pdc projects` - Returns active projects\n8. `!pdc quote`s - Returns random quote\n9. `!pdc events` - Returns upcoming events\n\n _Our bot is Open Source_"
]

#Setting up function for Quotes
def get_quote():
    response = requests.get(
        "https://zenquotes.io/api/random")  #API uses Random Quotes
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)

#Creating Login message
@client.event
async def on_ready():
    print('Bot is now live as {0.user}'.format(client) +
          (' at PHP-DC Discord Server'))

@client.event
async def on_message(message):
    #Variables Ease
    msg = message.content

    #Condition for self texting
    if message.author == client.user:
        return

#Condition help
    if msg.startswith('!pdc help'):
        await message.channel.send(''.join(help_data))

#Condition info
    if msg.startswith('!pdc info'):
        await message.channel.send('>>> PDC Bot v1.0.0')

#Condition about
    if msg.startswith('!pdc about'):
        await message.channel.send(
            '>>> **About** \nPDC is an university based community group for students interested in computer technology. \nStudents from any undergraduate or graduate programs with an interest in growing as a developer can join. \nWe aim in growing knowledge in a peer-to-peer learning environment and build solutions for local businesses and  community.'
        )

#Condition discord
    if msg.startswith('!pdc discord'):
        await message.channel.send('https://discord.gg/Gbanp7fYCZ')

#Condition github
    if msg.startswith('!pdc github'):
        await message.channel.send('https://github.com/PH-DC')

#Condition core team
    if msg.startswith('!pdc core team'):
        await message.channel.send(''.join(core_team_1))

#Condition projects
    if msg.startswith('!pdc projects'):
        await message.channel.send(''.join(projects))
 
#Condition requesting Quotes
    if msg.startswith('!pdc quote'):
        quote = get_quote()
        await message.channel.send('>>> ' + '_' + quote + '_')

#Condition for using bad words
    if any(word in msg for word in bad_words):
        await message.channel.send(random.choice(warning))

#Condition for using sad words
    if any(word in msg for word in sad_words):

        await message.channel.send(''.join(solution))

#Running Bot
keep_alive()

client.run(os.getenv('botTOKEN'))
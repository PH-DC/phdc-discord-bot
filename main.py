#Imports
import discord
import os
import requests
import json
import urllib
import random
from replit import db
from keep_alive import keep_alive


#Variables
client = discord.Client()

bad_words = [
    "Fuck", "fuck", "Fuck You", "Shit", "Piss off", "Fuck off", "Dick head",
    "Asshole", "Son of a bitch", "Bastard", "Bitch", "Wanker"
]

sad_words = [
    "error", "build failed", "not working", "bug", "failed", "err", "buggy"
]

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
     ">>> **Help Commands** \n\nThese are the available commands:\n\n1. `!pdc help` - Dailogue of all commands\n2. `!pdc info` -  Gives info of bot\n3. `!pdc about` -  Returns server information\n4. `!pdc discord` - Provides invitation link for the discord server\n5. `!pdc github` - Provides link to the github organisation\n6. `!pdc core team` - Returns current Core Member\n7. `!pdc list projects` - Returns active projects\n8. `!pdc quote`s - Returns random quote\n9. `!pdc events` - Returns upcoming events\n10. `!pdc new-event` - Add new event\n11. `!pdc delete-event` - Delete an event\n12. `!pdc list-events` - List all events\n13. `!pdc event-syntax` - List all syntax for events command\n14. `!pdc new project` - add new project to the list\n15. `!pdc delete project` - delete a project from the list\n16. `!pdc meme` - Returns meme\n17. `!pdc joke` - Returns a joke\n\n _Our bot is Open Source_"
]

event_syntax = [
    "`!pdc new-event | <event-title> | <event_time>`\n`!php delete index_value`"
]

#Setting up function for Quotes
def get_quote():
    response = requests.get(
        "https://zenquotes.io/api/random")  #API uses Random Quotes
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)

#Setting up funcyion for adding an 
def new_event(event_title, event_date, event_time):
  new_event = event_title, event_date, event_time
  if "events" in db.keys():
    events = db["events"]
    events.append(new_event)
    db["events"] = events
  else:
    db["events"] = [(new_event)]

def remove_event(index):
  events = db["events"]
  if len(events) > index:
    del events[index]
    db["events"] = events

#Setting up funcyion for adding an 
def new_projects(project_title):
  new_project = project_title
  if "projects" in db.keys():
    new_project = db["projects"]
    new_project.append(new_project)
    db["projects"] = new_project
  else:
    db["projects"] = [(new_project)]

def remove_projects(index):
  new_project = db["projects"]
  if len(new_project) > index:
    del new_project[index]
    db["projects"] = new_project

#Function to return random meme images URL
def random_meme():
  url =  "https://some-random-api.ml/meme"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  path = data["image"]
  return path
#Function to return random jokes 
def random_joke():
  url = "https://some-random-api.ml/joke"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  joke = data["joke"]
  return joke

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

#Condition to view all the events currently in the database
    if msg.startswith("!pdc list projects"):
        projects = db["projects"].value
        for project_title in projects:
          await message.channel.send(" {} |  ".format(project_title))

#Condition for adding an event
    if msg.startswith("!pdc new project"):
        msg_array = msg.split("|")
        project_title = msg_array[1]
        new_projects(project_title)
        await message.channel.send(">>> New Project added!")

#Condition for deleting events
    if msg.startswith("!pdc mark project completed"):
      index = int(msg.split("!pdc mark project completed",1)[1])
      remove_projects(index)
      await message.channel.send(">>> Projected Completed!")

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

#Condition to view all the events currently in the database
    if msg.startswith("!pdc list events"):
        events = db["events"].value
        for event_title, event_date, event_time in events:
          await message.channel.send(" {} | {} | {} ".format(event_title, event_date, event_time))

#Condition for adding an event
    if msg.startswith("!pdc new event"):
        msg_array = msg.split("|")
        event_title = msg_array[1]
        event_date = msg_array[2]
        event_time = msg_array[3]
        new_event(event_title, event_date, event_time)
        await message.channel.send(">>> New event added!")

#Condition for deleting events
    if msg.startswith("!pdc delete event"):
      index = int(msg.split("!pdc delete event",1)[1])
      remove_event(index)
      await message.channel.send(">>> Event Deleted")

#Condition to view all event related syntax
    if msg.startswith("!pdc event-syntax"):
        await message.channel.send('>>> '.join(event_syntax))

#Condition to return random meme
    if msg.startswith('!pdc meme'):
      meme = random_meme()
      await message.channel.send(meme)

#Condition to return random jokes
    if msg.startswith('!pdc joke'):
      joke = random_joke()
      await message.channel.send(">>> " + joke)

#Keep Alive
keep_alive()

client.run(os.getenv('botTOKEN'))

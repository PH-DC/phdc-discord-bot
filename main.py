#Imports
import discord
import os
import requests
import json
import urllib
import random
from replit import db
from keep_alive import keep_alive

#import sellenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# sellenium exception
from selenium.common.exceptions import NoSuchElementException    

# chrome driver options 
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# creating drivers for each website to scrape
microsoft_driver = webdriver.Chrome(options=chrome_options)
google_driver = webdriver.Chrome(options=chrome_options)
amazon_driver = webdriver.Chrome(options=chrome_options)
tech_crunch_driver = webdriver.Chrome(options=chrome_options)


# get html content of the webpage
microsoft_driver.get("https://events.microsoft.com/?timeperiod=next30Days&isSharedInLocalViewMode=false&eventsfor=Students&language=English")


# get the HTML content of webpage
google_driver.get("https://developers.google.com/events")


 # get the HTML content of the page
amazon_driver.get("https://aws.amazon.com/events/explore-aws-events/?events-master-main.sort-by=item.additionalFields.startDateTime&events-master-main.sort-order=asc&awsf.events-master-location=*all&awsf.events-master-type=type%23virtual&awsf.events-master-series=*all&awsf.events-master-audience=*all&awsf.events-master-category=*all&awsf.events-master-level=level%23100")


# get HTML content of the webpage
tech_crunch_driver.get("https://techcrunch.com/")

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

core_team_1 = [
    ">>> **Core Team** \n1. Lead: Random Name\n2. Co Lead: Random Name\n3. Web Lead: Random Name"
]

help_data = [
     ">>> **Help Commands** \n\nThese are the available commands:\n\n1. `!pdc help` - Dailogue of all commands\n2. `!pdc info` -  Gives info of bot\n3. `!pdc about` -  Returns server information\n4. `!pdc discord` - Provides invitation link for the discord server\n5. `!pdc github` - Provides link to the github organisation\n6. `!pdc core team` - Returns current Core Member\n7. `!pdc list projects` - Returns active projects\n8. `!pdc quote`s - Returns random quote\n9. `!pdc events` - Returns upcoming events\n10. `!pdc new-event` - Add new event\n11. `!pdc delete-event` - Delete an event\n12. `!pdc list-events` - List all events\n13. `!pdc event-syntax` - List all syntax for events command\n14. `!pdc new project` - add new project to the list\n15. `!pdc delete project` - delete a project from the list\n16. `!pdc meme` - Returns meme\n17. `!pdc joke` - Returns a joke\n18. `!pdc search github` - get the github url of a user\n 19. `!pdc get-microsoft-eve` - Get latest events of Mircosoft for students.\n 20. `!pdc get-google-eve` - Get latest upcoming events of Google for students\n 21. `!pdc amazon-eve` - Get latest upcoming events of Amazon (AWS) for students\n 22. `!pdc get-news` - Get latest technology related news. \n\n _Our bot is Open Source_"
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

#Setting up funcyion for adding events
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

#Setting up function for adding projects
def newProject(projectTitle, projectType):
  new_project = projectTitle, projectType
  if "projects" in db.keys():
    projects = db["projects"]
    projects.append(new_project)
    db["projects"] = projects
  else:
    db["projects"] = projects

def removeProject(index):
  projects = db["projects"]
  if len(projects) > index:
    del projects[index]
    db["projects"] = projects

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

#Function which return a github url
def github_search_user(user_name_to_search):
  response = urllib.request.urlopen("https://api.github.com/users/" + user_name_to_search )
  data = json.loads(response.read())
  git_url = data["html_url"]
  return git_url

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

#Condition to view projects
    if msg.startswith("!pdc list projects"):
      projects = db["projects"].value
      for projectTitle, projectType in projects:
        await message.channel.send("{} | {} ".format(projectTitle, projectType))

#Condition to Add Projects
    if msg.startswith("!pdc new project"):
      project_msg_array = msg.split("|")
      projectTitle = project_msg_array[1]
      projectType = project_msg_array[2]
      newProject(projectTitle, projectType)
      await message.channel.send(">>> Project Added")

#Condition to Delete Project
    if msg.startswith("!pdc project completed"):
      index = int(msg.split("!pdc project completed",1)[1])
      removeProject(index)
      await message.channel.send(">>> Project Completed")

#Condition to return random meme
    if msg.startswith('!pdc meme'):
      meme = random_meme()
      await message.channel.send(meme)

#Condition to return random jokes
    if msg.startswith('!pdc joke'):
      joke = random_joke()
      await message.channel.send(">>> " + joke)

#Condition to search a user in github
    if msg.startswith('!pdc search github'):
      user_to_be_searched = msg.split(" ",3)[3]
      git_result = github_search_user(user_to_be_searched)
      await message.channel.send(">>> " + git_result[0])

# Condition to get latest events from microsoft
  if msg.startswith("!pdc get-microsoft-eve"):

    # get the event div using its class name
    event_div = microsoft_driver.find_elements(By.CLASS_NAME, 'eventSection')

    # creating empty arrays to store the 
    # 1. event titles
    list_m_events = []
    # 2. links to those events
    links_reg = []

    # get titles and links to those events
    for event in event_div:
      # get element: titles
      mircosoft_events = event.find_elements(By.CLASS_NAME, 'eventTitle')
      # get element: links
      event_links = event.find_elements(By.CLASS_NAME, 'registerBtnSmall')

      # loop through the event titles and store the text 
      # into list_m_events array
      for e in mircosoft_events:
        # the title must not be empty
        if(e.text != ''):
          list_m_events.append(e.text)

      # loop through the event titles and store the text 
      # into list_m_events array
      for link in event_links:
        links_reg.append(link.get_attribute('href'))
    
    # generate a random index
    random_num = random.randint(0, len(list_m_events) + 1)
    print(len(list_m_events))
    print(random_num)

    if(random_num < len(list_m_events)):
      # send message from the bot
      await message.channel.send(">>> "  + '\n' + list_m_events[random_num] + '\n\n' + 'Registration Link: \n' + links_reg[random_num])

    else:
      await message.channel.send("Couldn't fetch it. Try Again !")

# Condition to get latest events from google
  if msg.startswith("!pdc get-google-eve"):

    # get the event div
    event_div_g = google_driver.find_elements(By.CLASS_NAME, 'devsite-landing-row-item')

    # creating empty arrays to store
    # 1. Events' banner image
    event_g_image = []  
    # 2. Registration link
    reg_link = []
    # 3. Events' titles
    event_g_title = []

    # looping the through the event_div_g array to get other reuired elements
    for e in event_div_g:
      # using NoSuchElementException
      try:
        # this is done to check whether the div has a register button or not 
        # if it has that means that the event is upcoming and not conducted
        e.find_element(By.CLASS_NAME, 'button-primary')
        linkreg_g = e.find_elements(By.CLASS_NAME, 'button-primary')

        # if it has a button then get the title, link and image
        event_image = e.find_elements(By.TAG_NAME, 'img')
        event_go_title = e.find_elements(By.TAG_NAME, 'h3')

        # store image link into event_g_image array
        for i_link in event_image:
          event_g_image.append(i_link.get_attribute('src'))
        
        # store registration links into reg_link array
        for r_link in linkreg_g:
          reg_link.append(r_link.get_attribute('href'))
        
        # store titles in event_g_title array
        for e_title in event_go_title:
          event_g_title.append(e_title.text)

      except NoSuchElementException:
        print('done')    

    # generate a random index
    random_num_g = random.randint(0, len(reg_link) + 1)

    # send message
    if(random_num_g < len(reg_link)):
      await message.channel.send(">>> " + "\n" + event_g_title[random_num_g] + "\n\n" + "Registration Link :\n" + reg_link[random_num_g] + "\n")
      
      await message.channel.send(event_g_image[random_num_g])

    else:
      await message.channel.send("Couldn't fetch it. Try Again !")

  
# Condition to get latest events from amazon (AWS)
  if msg.startswith("!pdc amazon-eve"):
    
    event_ama = amazon_driver.find_elements(By.CLASS_NAME, 'm-headline')

    # created empty arrays to store:
    # 1. Titles
    event_ama_title = []
    # 2. Links
    event_ama_link = []

    # looping the through the event_ama array to get other reuired elements
    for event in event_ama:
      event_links = event.find_elements(By.TAG_NAME, 'a')
      
      # get links and event titles
      for link in event_links:
        event_ama_link.append(link.get_attribute('href'))
        event_ama_title.append(link.text)

    # genrate a random index
    random_ama_eve = random.randint(0, len(event_ama_link) + 1)
    print(len(event_ama_link))
    print(random_ama_eve)

    # send message
    if(random_ama_eve < len(event_ama_link)):
      await message.channel.send(">>> " + event_ama_title[random_ama_eve] + "\n\n" + "Registration Link: \n" + event_ama_link[random_ama_eve])
    else:
      await message.channel.send("Couldn't fetch it. Try Again !")

# Condition to get latest tech news
  if msg.startswith("!pdc get-news"):

    # get the news div element
    event_news = tech_crunch_driver.find_elements(By.CLASS_NAME, 'post-block__title__link')

    # Created empty array to store:
    # 1. News title
    info_text = []
    # 2. News Link
    info_link = []

    
    # loop through event_news array to get the other reuired elements
    for info in event_news:
      info_text.append(info.text)
      info_link.append(info.get_attribute('href'))

    # generate a random index number
    random_info = random.randint(0, len(info_text) + 1)

    if(random_info < len(info_text)):
      # send message
      await message.channel.send(">>> " + info_text[random_info] + "\n\n To read more: \n" + info_link[random_info])

    else:
      await message.channel.send("Couldn't fetch it. Try Again !")

    
#Keep Alive
keep_alive()

client.run(os.getenv('botTOKEN'))

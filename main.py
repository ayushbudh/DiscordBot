import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


# Creating connection to discord
client = discord.Client()

sad_words = ["sad","depressed", "unhappy", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!", "Hang in there.", "Your are a great person! - bot :)"
]

if "responding" not in db.keys():
  db["responding"] = True


# function to return quote from the API
def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)

# for database 
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db ["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["enncouragements"] = encouragements

# registering an event 
# this is an asynchronous event (i.e. this task will run in the background)  
# 0 will be replaced by client
@client.event
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client))

# when the bit receives message

@client.event
async def on_message(message):
  # if the message received is from us do nothing
  if message.author == client.user: 
    return

  # if someone starts the statement with $hello bot responds with hello
  # if message.content.startswith('$hello'):
  #   await message.channel.send('Hello!')

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:

    options  = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

# lis encouraging messages

  if msg.startswith('$list'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

  if value.lower() == "true":
    db["responding"] = True
    await message.channel.send("Responding is on.")
  else :
    db["responding"] = False
    await message.channel.send("Responding is off.")

keep_alive()
# getting the environment variable TOKEN from .env  file
client.run(os.getenv('TOKEN'))
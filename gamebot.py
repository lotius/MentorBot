import os
import commands
import discord

import requests

from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('MY_DISCORD_GUILD')
NEWS_CHANNEL_NAME = os.getenv('NEWS_CHANNEL_NAME')

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

# URL to poll, and the search title to poll for
instruction_url = 'https://instructions.hasbro.com/en-us/all-instructions?search=heroquest'
titles = ['Against the Ogre Horde', 'The Jungles of Delthrak', 'First Light']  

@tasks.loop(minutes=5)
async def new_instructions_available():
    response = requests.get(instruction_url)
    response_text_lower = response.text.lower()  # Convert the response text to lowercase

    for title in titles:
        if response_text_lower.find(title.lower()) != -1:  # Convert title to lowercase before search
            filename = f"{title}.txt"  # Create a filename based on the title
            if not os.path.isfile('found_instructions/' + filename):  # Check if the file doesn't exist
                print(f'Found {title}!')
                channel = discord.utils.get(client.get_all_channels(), name=NEWS_CHANNEL_NAME)
                if channel:
                    await channel.send(f"Hey everyone! This is just to inform you that the new quest booklet for {title} is now available on the Hasbro Instructions webpage! https://instructions.hasbro.com")
                    # Write the filename to indicate the quest booklet has been processed
                    with open('found_instructions/' + filename, 'w') as file:
                        file.write(f"{title} processed")
                else:
                    print(f"Channel with name '{NEWS_CHANNEL_NAME}' not found.")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    guild = discord.utils.get(client.guilds, name=GUILD_NAME)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    new_instructions_available.start()

@client.event
async def on_message(message):
    command = ""
    params = ""

    if ((message.guild.id == int(os.getenv('MY_DISCORD_GUILD_ID'))) and message.author.bot == False and not message.attachments and not message.is_system()): 
        if (message.content[0] == '!' and len(message.content) > 1):

            space_position = message.content.find(' ')
            
            if (space_position != -1):
                command = message.content[1:space_position]
                params = message.content[space_position + 1:]
            else:
                command = message.content[1:]

            await commands.process_command(message, command, params)
    else:
        return

#@client.event
#async def on_member_join(member):
    # get general channel object here
#    if (int(member.guild.id) == int(os.getenv('MY_DISCORD_GUILD_ID'))):
#        welcome_message = 'Welcome, ' + member.name + '! If you\'d like access to the GM (Zargon/Morcar) channel please let us know.'
#        #await channel.send(welcome_message)

client.run(TOKEN)
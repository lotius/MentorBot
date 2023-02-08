import os
import commands
import discord

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('MY_DISCORD_GUILD')

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    guild = discord.utils.get(client.guilds, name=GUILD_NAME)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

@client.event
async def on_message(message):
    command = ""
    params = ""

    if ((not message.guild.id == int(os.getenv('MY_DISCORD_GUILD_ID'))) and message.author.bot == False and not message.attachments and not message.is_system()): 
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
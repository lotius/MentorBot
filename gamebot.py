import os
import requests
import commands
import discord

from bs4 import BeautifulSoup
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
instruction_url = "https://instructions.hasbro.com/en-us/all-instructions?search=heroquest&page=1&limit=50&sort=newest"
found_ids_dir = "found_instructions"
os.makedirs(found_ids_dir, exist_ok=True)

@tasks.loop(minutes=15)
async def new_instructions_available():
    """Checks for new HeroQuest instruction PDFs and posts them to Discord."""
    
    response = requests.get(instruction_url)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    instructions = []

    # Find all "View Details" links
    for view_details in soup.find_all("a", string=lambda s: s and "View Details" in s):
        # Extract the instruction page URL
        page_url = f"https://instructions.hasbro.com{view_details['href']}" if view_details.has_attr("href") else "No URL Found"

        # Move up the tree to find the containing div
        container = view_details.find_parent("div")
        if not container:
            continue  # Skip if no container found

        # Step back 3 <p> tags to find the Title
        title_tag = view_details.find_previous("p").find_previous("p").find_previous("p")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

        # Step back 2 <p> tags to find the Avalon Hill ID
        id_tag = view_details.find_previous("p").find_previous("p")
        avalon_id = "Unknown ID"
        if id_tag and "(" in id_tag.get_text() and ")" in id_tag.get_text():
            avalon_id = id_tag.get_text(strip=True).split("(")[-1].split(")")[0]

        instructions.append({"title": title, "id": avalon_id, "page_url": page_url})

    # Process new instructions
    for instruction in instructions:
        filename = os.path.join(found_ids_dir, f"{instruction['id']}.txt")

        if not os.path.isfile(filename):  # New entry found
            print(f"New instruction found: {instruction['title']} (ID: {instruction['id']})")

            # Send to Discord
            channel = discord.utils.get(client.get_all_channels(), name=NEWS_CHANNEL_NAME)
            if channel:
                await channel.send(
                     f"Hey everyone! A new PDF for **{instruction['title']}** is now available on the Hasbro Instructions webpage!\n"
                     f"🔗 [{instruction['title']}]({instruction['page_url']})"
                )

                # Save the ID to prevent duplicate notifications
                with open(filename, "w") as f:
                    f.write(f"{instruction['id']} processed")
                
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
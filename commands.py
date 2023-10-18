import random
import os
import re
import discord

from hqdice import checkHeroQuestCombatDiceParameters
from oqdice import checkOrcQuestDiceParameters
from scdice import checkSpaceCrusadeCombatDiceParameters

async def process_command(message, command, param):
    if (command == 'help'):
        await help(message, param)
    elif (command == 'roll'):
        await roll(message, param)
    elif (command == 'hqroll'):
        await heroquest_roll(message, param)
    elif (command == 'rollcolor'):
        await roll_color(message, param)
    elif (command == 'scroll' or command == 'sqroll'):
        await spacecrusade_roll(message, param)

def can_convert_to_int(string):
    try:
        int(string)

        return True
    except ValueError:
        return False

async def help(message, param):
    if (len(param) == 0):
        await message.channel.send(f'Command List:\n \
!roll - Roll a specified set of dice faces. For example, if you\'d like to roll a 2d6 type: !roll 2d6\n \
!hqroll - Roll the HeroQuest combat dice. For example, if you\'d like to roll 3 combat dice type: !hqroll 3\n \
!scroll or !sqroll - Roll the Space Crusade combat dice. For example, if you\'d like to roll 2 white \
combat dice type: !scroll 2 white\n \
Use !help _command_ to get more specific information about an available command.')
    elif (param == 'roll'):
        await message.channel.send(f'**Roll standard dice**:\n \
To roll standard dice use the _**!roll**_ command followed by the number of dice you wish to roll (up to 10), followed by \
how many sides each die will have (up to 100). If you leave off the number of dice you wish to roll and only input the \
number of sides for the die to have the bot will roll 1 die (ie !roll d100)\n \
_Examples: !roll 2d6, !roll d20, !roll 3d4, !roll d100_')
    elif (param == 'hqroll'):
        await message.channel.send(f'**Roll HeroQuest combat dice**:\n \
To roll HeroQuest dice use the _**!hqroll**_ command followed by the number of dice you wish \
to roll (up to 15). Optionally, you can include one of the 5 German variant dice colors \
in order to roll that set instead of standard dice, and even multiple colors at once.\n\n \
Available variant dice colors are blue, orange, green, purple, yellow, and black.\n \
**Examples:** _**!hqroll 2**, **!hqroll 5**, **!hqroll 6 orange**, **!hqroll 4 green**_\n \
You can also specify multiple dice colors in a single command\n \
**Examples:** _**!hqroll 2 white 2 orange**, **!hqroll 1 white 3 green 2 blue**_')
    elif (param == 'rollcolor'):
        await message.channel.send(f'**Generate random HeroQuest combat dice color**:\n \
Generates a random enhanced combat dice color for HeroQuest Fans Twitch rewards!\n \
Valid colors are: blue, orange, green, purple, yellow, and black.')
    elif (param == 'scroll' or param == 'sqroll'):
        await message.channel.send(f'**Roll Space Crusade combat dice**:\n \
To roll Space Crusade dice use the _**!scroll**_ or _**!sqroll**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In Space Crusade \
you can roll up to 4 white and up to 4 red dice.\n \
**Examples:** _**!scroll 2 white**, **!scroll 1 red 3 white**, **!sqroll 1 white 2 red**_')
    elif (param == 'oqroll'):
        await message.channel.send(f'**Roll OrcQuest combat dice**:\n \
To roll OrcQuest dice use the _**!oqroll**_ command followed by the number of dice you \
wish to roll, followed by the type of dice you wish to roll. In OrcQuest you can roll up \
to 3 of a single attack or defense dice and up to 2 badass dice of one single color.\n \
**Examples:** _**!oqroll 2 whiteattack 1 whitedefend**, **oqroll 1 blackattack 1 greydefend 1 whitedefend**, \n\
**!oqroll 1 whiteattack 1 greyattack 1 greenbadass 2 whitedefend**_')

async def roll(message, param):
    diceTotalDetail = []
    dice = []
    regex = re.compile(r'^(([1-9]|10)?[dD]([1-9][0-9]?$|100))$')

    # Guarantee either d#, D#, #d# or #D# was entered using the regex pattern.
    if (re.match(regex, param)):
        dice = param.lower().split('d', 1)

        # User entered a number after the d only, roll 1 die.
        if (dice[0] == ''):
            diceTotalDetail.append(random.randint(1, int(dice[1])))
        # User entered 1 to 10 dice, and 1 to 100 sides.
        else:
            for x in range(int(dice[0])):
                diceTotalDetail.append(random.randint(1, int(dice[1])))
    else:
        await message.channel.send('Proper roll format is #d or #d#! (Examples: !roll 2d6 or !roll d12). Maximum of 10 die and 100 sides.')
        return

    await message.channel.send(f'**{message.author.name}** rolled **{sum(diceTotalDetail)}** _{diceTotalDetail}_.')

async def heroquest_roll(message, param):
    # Determine if regex was matched. A digit can be matched by itself, or a combination of a digit followed by a
    # word can be matched. If a digit and word combination is matched it is allowed to be repeated.
    regex = re.compile(r'^(\d{1,2}|(\d{1,2}\s[a-zA-Z]+\b\s?)+)$')

    match = re.match(regex, param)
    if match:
        await checkHeroQuestCombatDiceParameters(message, param)
    else:
        await message.channel.send(f'**{message.author.name}** your input pattern is invalid! Please use _!help hqroll_ \
to review the proper usage of the _hqroll_ command.')
        return
    
async def orcquest_roll(message, param):
    # Determine if regex was matched. A digit can be matched by itself, or a combination of a digit followed by a
    # word can be matched. If a digit and word combination is matched it is allowed to be repeated.
    regex = re.compile(r'^((\d{1,2}\s[a-zA-Z]+\b\s?)+)$')

    match = re.match(regex, param)
    if match:
        await checkOrcQuestDiceParameters(message, param)
    else:
        await message.channel.send(f'**{message.author.name}** your input pattern is invalid! Please use _!help oqroll_ \
to review the proper usage of the _oqroll_ command.')
        return
    
async def roll_color(message, param):
    path = 'images/blankcolors'
    files = os.listdir(path)

    file_to_send = files[random.randint(0, len(files) - 1)]

    await message.channel.send(file=discord.File(f'images/blankcolors/{file_to_send}'))
    return

async def spacecrusade_roll(message, param):
    # Determine if regex was matched. A combination of a digit followed by a
    # word can be matched up to 2 times as there are only red and white dice in Space Crusade.
    regex = re.compile(r'^(\d{1}\s[a-zA-Z]+\b\s?){1,2}$')

    match = re.match(regex, param)
    if match:
        await checkSpaceCrusadeCombatDiceParameters(message, param)
    else:
        await message.channel.send(f'**{message.author.name}** your input pattern is invalid! Please use _!help scroll_ \
to review the proper usage of the _scroll_ command.')
        return
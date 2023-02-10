import random
import os
import re

from discord.ui import Select, View
from discord.ext import commands
from hqdice import checkHeroQuestCombatDiceParameters
from scdice import checkSpaceCrusadeCombatDiceParameters

async def process_command(message, command, param):
    if (command == 'help'):
        await help(message, param)
    elif (command == 'roll'):
        await roll(message, param)
    elif (command == 'hqroll'):
        await heroquest_roll(message, param)
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
how many sides each die will have (up to 100).\n_Examples: !roll 2d6, !roll 1d20, !roll 3d4_')
    elif (param == 'hqroll'):
        await message.channel.send(f'**Roll HeroQuest combat dice**:\n \
To roll HeroQuest dice use the _**!hqroll**_ command followed by the number of dice you wish \
to roll (up to 15). Optionally, you can include one of the 5 German variant dice colors \
in order to roll that set instead of standard dice, and even multiple colors at once.\n\n \
Available variant dice colors are blue, orange, green, purple, yellow, and black.\n \
**Examples:** _**!hqroll 2**, **!hqroll 5**, **!hqroll 6 orange**, **!hqroll 4 green**_\n \
You can also specify multiple dice colors in a single command\n \
**Examples:** _**!hqroll 2 white 2 orange**, **!hqroll 1 white 3 green 2 blue**_')
    elif (param == 'scroll' or param == 'sqroll'):
        await message.channel.send(f'**Roll Space Crusade combat dice**:\n \
To roll Space Crusade dice use the _**!scroll**_ or _**!sqroll**_ command followed by the \
number of dice you wish to roll, followed by the color you wish to roll. In Space Crusade \
you can roll up to 4 white and up to 4 red dice.\n \
**Examples:** _**!scroll 2 white**, **!scroll 1 red 3 white**, **!sqroll 1 white 2 red**_')

async def roll(message, param):
    dice = param.split('d', 1)
    diceTotalDetail = []

    if (len(dice) != 2 or not can_convert_to_int(dice[0]) or not can_convert_to_int(dice[1]) or int(dice[0]) > 10 or int(dice[1]) > 100):
        await message.channel.send('Proper roll format is #d#! (Example: !roll 2d6). Maximum of 10 die and 100 sides.')
        return

    for x in range(int(dice[0])):
        diceTotalDetail.append(random.randint(1, int(dice[1])))

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

async def spacecrusade_roll(message, param):
    print('Entered space crusade function.')
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
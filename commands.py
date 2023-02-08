import random
import os

from discord.ui import Select, View
from discord.ext import commands
from hqdice import rollHeroQuestCombatDice

async def process_command(message, command, param):
    if (command == 'help'):
        await help(message, param)
    elif (command == 'roll'):
        await roll(message, param)
    elif (command == 'hqroll'):
        await heroquest_roll(message, param)

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
!hqroll - Roll the HeroQuest combat dice. For example, if you\'d like to roll 3 combat dice type: !hqroll 3\n')
    elif (param == 'roll'):
        await message.channel.send(f'**Roll standard dice**:\n \
To roll standard dice use the _!roll_ command followed by the number of dice you wish to roll (up to 10), followed by \
how many sides each die will have (up to 100).\n_Examples: !roll 2d6, !roll 1d20, !roll 3d4_')
    elif (param == 'hqroll'):
        await message.channel.send(f'**Roll HeroQuest dice**:\n \
To roll HeroQuest dice use the _!hqroll_ command followed by the number of dice you wish to roll (up to 10), followed by \
how many sides each die will have (up to 100).\nOptionally, you can include one of the 5 German variant dice colors to \
roll that. Available variant dice colors are blue, orange, green, purple, and black.\n_Examples: !hqroll 2, !hqroll 6, !hqroll 4 green_')

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
    params = param.split(' ', 1)
    diceRolls = []
    color = 'white'

    # Determine if a valid number was entered.
    if (can_convert_to_int(params[0]) and int(params[0]) > 0 and int(params[0]) <= 15):
        for x in range(int(params[0])):
            diceRolls.append(random.randint(1, 6))
    else:
        await message.channel.send(f'HeroQuest combat roll command usage: !hqroll # _[color]_ (Example: !hqroll 3). Max roll of 15.\n \
Color is optional, but if included will roll the German variant dice.\n \
Color options are: blue, orange, green, purple, and black.')
        return
    
    # A possible optional color was requested.
    if (len(params) > 1):
        if (params[1] == 'blue'):
            await rollHeroQuestCombatDice(message, [{'face': 'skull-blue.png', 'numOfFaces': 3}, {'face': 'whiteshield-blue.png', 'numOfFaces': 1}, {'face': 'blackshield-blue.png', 'numOfFaces': 2}], len(diceRolls))
        elif (params[1] == 'orange'):
            await rollHeroQuestCombatDice(message, [{'face': 'skull-orange.png', 'numOfFaces': 1}, {'face': 'doubleskull-orange.png', 'numOfFaces': 2}, {'face': 'doublewhiteshield-orange.png', 'numOfFaces': 1}, {'face': 'blackshield-orange.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-orange.png', 'numOfFaces': 1}], len(diceRolls))
        elif (params[1] == 'green'):
            await rollHeroQuestCombatDice(message, [{'face': 'skull-green.png', 'numOfFaces': 2}, {'face': 'whiteshield-green.png', 'numOfFaces': 3}, {'face': 'blackshield-green.png', 'numOfFaces': 1}], len(diceRolls))
        elif (params[1] == 'purple'):
            await rollHeroQuestCombatDice(message, [{'face': 'skull-purple.png', 'numOfFaces': 2}, {'face': 'doubleskull-purple.png', 'numOfFaces': 1}, {'face': 'whiteshield-purple.png', 'numOfFaces': 1}, {'face': 'doublewhiteshield-purple.png', 'numOfFaces': 1}, {'face': 'blackshield-purple.png', 'numOfFaces': 1}], len(diceRolls))
        elif (params[1] == 'black'):
            await rollHeroQuestCombatDice(message, [{'face': 'skull-black.png', 'numOfFaces': 4}, {'face': 'whiteshield-black.png', 'numOfFaces': 1}, {'face': 'blackshield-black.png', 'numOfFaces': 1}], len(diceRolls))
        elif (params[1] == 'white'):
            await rollHeroQuestCombatDice(message, [{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 2}, {'face': 'blackshield.png', 'numOfFaces': 1}], len(diceRolls))
        else:
            await message.channel.send('That color dice set is not available. Available colors are blue, orange, green, purple, and black.')
    else:
        # Standard dice
        await rollHeroQuestCombatDice(message, [{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 2}, {'face': 'blackshield.png', 'numOfFaces': 1}], len(diceRolls))
    
import random
import os

from discord.ui import Select, View
from discord.ext import commands
from hqdice import rollHeroQuestCombatDice

async def process_command(message, command, param):
    if (command == 'help'):
        await help(message)
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

async def help(message):
    await message.channel.send(f'Command List:\n \
        !roll - Roll a specified set of dice faces. For example, if you\'d like to roll a 2d6 type: !roll 2d6\n \
        !hqroll - Roll the HeroQuest combat dice. For example, if you\'d like to roll 3 combat dice type: !hqroll 3\n')
        
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
    diceRolls = []

    if (can_convert_to_int(param) and int(param) > 0 and int(param) <= 15):
        for x in range(int(param)):
            diceRolls.append(random.randint(1, 6))
    else:
        await message.channel.send('HeroQuest combat roll command usage: !hqroll # (Example: !hqroll 3). Max roll of 15.')
        return
    
    # Call the roll function differently if user chose one of the German varieties of HeroQuest dice.
    await rollHeroQuestCombatDice(message, [{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 2}, {'face': 'blackshield.png', 'numOfFaces': 1}], len(diceRolls))
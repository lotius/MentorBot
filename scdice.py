import os
import random
import numpy as np
import cv2
import discord
import requests
from dotenv import load_dotenv

load_dotenv()

DDDICE_API_KEY = str(os.getenv('DDDICE_API_KEY'))
DDDICE_ROLL_API_ENDPOINT = str(os.getenv('DDDICE_ROLL_API_ENDPOINT'))
DDDICE_KURGAN_ROOM_ID = str(os.getenv('DDDICE_KURGAN_ROOM_ID'))
DDDICE_DISCORD_CHANNEL = str(os.getenv('DDDICE_DISCORD_CHANNEL'))

# Send the dice results to dddice.com website. Send the results to a specific room and only if
# it was rolled from a specific channel within the Discord server.
async def sendToDDDICE(message, dddRolledDice):
    if (message.channel.name == DDDICE_DISCORD_CHANNEL):
        raw_data = {
            'dice': dddRolledDice,
            'room': DDDICE_KURGAN_ROOM_ID
        }
    
        headers = {
            "Authorization": f"Bearer {DDDICE_API_KEY}", 
            "Content-Type": "application/json", 
            "Accept": "application/json"
        }

        response = requests.post(DDDICE_ROLL_API_ENDPOINT, json=raw_data, headers=headers)
        #print(response.status_code)
        #print(response.text)

async def checkSpaceCrusadeCombatDiceParameters(message, param):
    params = param.split(' ')
    totalDiceRolled = 0
    diceToRoll = []
    
    paramArray = np.array_split(params, len(params) / 2)

    # Iterate the sets of dice quantities and requested colors.
    for currentParam in paramArray:
        numToRoll = int(currentParam[0])
        currentColor = currentParam[1]
    
        totalDiceRolled = totalDiceRolled + numToRoll
        # Ensure both the current numToRoll and the cumulative total dice rolled do not exceed 8, and
        # each color can only be rolled up to 4 times.
        if (totalDiceRolled > 8 or numToRoll > 4):
            await message.channel.send('Sorry, but you cannot roll more than 4 of each color dice and/or up to 8 total combat dice in a single command.')
            return
        
        # Ensure that at least 1 die of each requested color is rolled.
        if (numToRoll < 1):
            await message.channel.send('Sorry, but for each die color specified you must roll at least 1 die.')
            return
        
        # Ensure that the colors requested are available.
        if (currentColor != 'white' and currentColor != 'red'):
            await message.channel.send('Sorry, but you\'ve included a die color that isn\'t available. Available colors \
are red and/or white.')
            return
        
        for existingDice in diceToRoll:
            for dieColor in existingDice.values():
                if (currentColor == dieColor):
                    await message.channel.send('Sorry, but each die color can only be specified once.')
                    return

        diceToRoll.append({'face': currentColor, 'numToRoll': int(numToRoll)})

    await rollSpaceCrusadeCombatDice(message, diceToRoll)
    
# Function takes 3 parameters:
# 1. An array describing the dice faces of a die to be rolled and how many of each face are on that die.
# Example: [{'face': 'white-1.png', 'numOfFaces': 1}, {'face': 'white-2.png', 'numOfFaces': 1}, {'face': 'white-0.png', 'numOfFaces': 4}]
# 2. The number of dice to be rolled.
async def rollSpaceCrusadeCombatDice(message, diceToRoll):
    white = [{'face': 'white-1.png', 'numOfFaces': 1}, {'face': 'white-2.png', 'numOfFaces': 1}, {'face': 'white-0.png', 'numOfFaces': 4}]
    red = [{'face': 'red-1.png', 'numOfFaces': 1}, {'face': 'red-2.png', 'numOfFaces': 1}, {'face': 'red-3.png', 'numOfFaces': 1}, {'face': 'red-0.png', 'numOfFaces': 3}]
    diceFaceCount = 0
    diceImages = {}
    rolledDice = []
    dddRolledDice = []
    dddiceTheme = ""

    # Assemble current dice's faces
    for currentRequestedFace in diceToRoll:

        # Color of current face
        currentFaceColor = currentRequestedFace['face']
        if (currentFaceColor == 'white'):
            currentFace = white
            dddiceTheme = "space-crusade-white-dice-lfgd1lnu"
        elif (currentFaceColor == 'red'):
            currentFace = red
            dddiceTheme = "space-crusade-red-dice-lfgczoch"
        
        # Assemble the current color's dice faces
        for coloredFace in currentFace:
            for x in range(0, coloredFace['numOfFaces']):
                diceFaceCount = diceFaceCount + 1
                diceImages[diceFaceCount] = cv2.imread('images/spacecrusade/' + coloredFace['face'], cv2.IMREAD_UNCHANGED)

        # Roll the dice and save the appropriate face to an array
        for x in range(int(currentRequestedFace['numToRoll'])):
            roll = random.randint(1, 6)
            rolledDice.append(diceImages[roll])
            dddRolledDice.append({'type': 'd6', 'theme': dddiceTheme, 'value': str(roll)})
                
        diceFaceCount = 0
        diceImages.clear()

    result_image = np.zeros((100, len(rolledDice) * 108, 4), np.uint8)
    result_image[:, :, 3] = 0
    
    x = 0
    for currentDiceFace in rolledDice:
        result_image[0 : 100, 108 * x : 108 * (x + 1), 0:3] = currentDiceFace[:, :, 0:3]
        result_image[0 : 100, 108 * x : 108 * (x + 1), 3] = currentDiceFace[:, :, 3]
        x = x + 1

    cv2.imwrite('images/spacecrusade/results.png', result_image)

    await message.channel.send(file=discord.File('images/spacecrusade/results.png'))

    await sendToDDDICE(message, dddRolledDice)
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

async def rollHeroQuestMovement(message, param):
    colorToRoll = ""
    dddiceTheme = ""
    rolledDice = []
    dddRolledDice = []
    diceImages = {}
    diceFaceCount = 0

    red = [{'face': '1-red.png', 'numOfFaces': 1}, {'face': '2-red.png', 'numOfFaces': 1}, {'face': '3-red.png', 'numOfFaces': 1}, {'face': '4-red.png', 'numOfFaces': 1}, {'face': '5-red.png', 'numOfFaces': 1}, {'face': '6-red.png', 'numOfFaces': 1}]
    blue = [{'face': '1-blue.png', 'numOfFaces': 1}, {'face': '2-blue.png', 'numOfFaces': 1}, {'face': '3-blue.png', 'numOfFaces': 1}, {'face': '4-blue.png', 'numOfFaces': 1}, {'face': '5-blue.png', 'numOfFaces': 1}, {'face': '6-blue.png', 'numOfFaces': 1}]

    params = param.split(' ')

    # Figure out color to roll
    if (len(params) == 1 or (len(params) == 2 and params[1].lower().strip() == 'red')):
        colorToRoll = red
        dddiceTheme = 'heroquest-red-movement-dice-lfhfjiff'
    elif (len(params) == 2 and params[1].lower().strip() == 'blue'):
        colorToRoll = blue
        dddiceTheme = 'heroquest-blue-movement-dice-lfhhootl'
    else:
        await message.channel.send('Sorry, but you can only roll red or blue movement dice.')

    # Assemble the current color's dice faces
    for currentFace in colorToRoll:
        for x in range(0, currentFace['numOfFaces']):
            diceFaceCount = diceFaceCount + 1
            diceImages[diceFaceCount] = cv2.imread('images/hqdice/transparent/' + currentFace['face'], cv2.IMREAD_UNCHANGED)

    # Roll the dice
    for x in range(int(params[0])):
        roll = random.randint(1, 6)
        rolledDice.append(diceImages[roll])
        dddRolledDice.append({'type': 'd6', 'theme': dddiceTheme, 'value': str(roll)})

    result_image = np.zeros((100, len(rolledDice) * 108, 4), np.uint8)
    result_image[:, :, 3] = 0
	
    x = 0
    for currentDiceFace in rolledDice:
        result_image[0 : 100, 108 * x : 108 * (x + 1), 0:3] = currentDiceFace[:, :, 0:3]
        result_image[0 : 100, 108 * x : 108 * (x + 1), 3] = currentDiceFace[:, :, 3]
        x = x + 1

    cv2.imwrite('images/hqdice/results.png', result_image)

    await message.channel.send(file=discord.File('images/hqdice/results.png'))

    await sendToDDDICE(message, dddRolledDice)

async def checkHeroQuestCombatDiceParameters(message, param):
    params = param.split(' ')
    totalDiceRolled = 0
    diceToRoll = []

    # Only a single number was entered. Make sure it's within range and process as a standard die.
    if (len(params) == 1 and int(params[0]) > 0 and int(params[0]) <= 15):
        await rollHeroQuestCombatDice(message, [{'face': 'white', 'numToRoll': int(params[0])}])
        return
    
    paramArray = np.array_split(params, len(params) / 2)


    # Iterate the sets of dice quantities and requested colors.
    for currentParam in paramArray:
        numToRoll = int(currentParam[0])
        currentColor = currentParam[1]
    
        totalDiceRolled = totalDiceRolled + numToRoll
        # Ensure both the current numToRoll and the cumulative total dice rolled do not exceed 15.
        if (totalDiceRolled > 15):
            await message.channel.send('Sorry, but you cannot roll more than 15 total combat dice in a single command.')
            return
        
        # Ensure that at least 1 die of each requested color is rolled.
        if (numToRoll < 1):
            await message.channel.send('Sorry, but for each die color specified you must roll at least 1 die.')
            return
        
        # Ensure that the colors requested are available.
        if (currentColor != 'blue' and currentColor != 'orange' and currentColor != 'green' and \
                currentColor != 'purple' and currentColor != 'black' and currentColor != 'yellow' \
                and currentColor != 'white' and currentColor != 'pink' and currentColor != 'red' \
                and currentColor != 'sqt' and currentColor != 'pot' and currentColor != 'fh' \
                and currentColor != 'gen' and currentColor != 'dread' and currentColor != 'gen24' \
                and currentColor != 'dew' and currentColor != 'jod' and currentColor != 'boss'):
            await message.channel.send('Sorry, but you\'ve included a die color that isn\'t available. Available colors \
are blue, orange, green, purple, black, red, yellow, pink, white, boss, sqt, pot, fh, gen, gen24 (or dew), dread, and jod.')
            return
        
        for existingDice in diceToRoll:
            for dieColor in existingDice.values():
                if (currentColor == dieColor):
                    await message.channel.send('Sorry, but each die color can only be specified once.')
                    return

        diceToRoll.append({'face': currentColor, 'numToRoll': int(numToRoll)})

    await rollHeroQuestCombatDice(message, diceToRoll)
    
async def rollHeroQuestCombatDice(message, diceToRoll):
    white = [{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 2}, {'face': 'blackshield.png', 'numOfFaces': 1}]
    red = [{'face': 'skull-red.png', 'numOfFaces': 3}, {'face': 'whiteshield-red.png', 'numOfFaces': 2}, {'face': 'blackshield-red.png', 'numOfFaces': 1}]
    blue = [{'face': 'skull-blue.png', 'numOfFaces': 3}, {'face': 'whiteshield-blue.png', 'numOfFaces': 1}, {'face': 'blackshield-blue.png', 'numOfFaces': 2}]
    orange = [{'face': 'doubleskull-orange.png', 'numOfFaces': 2}, {'face': 'doublewhiteshield-orange.png', 'numOfFaces': 2}, {'face': 'blackshield-orange.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-orange.png', 'numOfFaces': 1}]
    green = [{'face': 'skull-green.png', 'numOfFaces': 2}, {'face': 'whiteshield-green.png', 'numOfFaces': 3}, {'face': 'blackshield-green.png', 'numOfFaces': 1}]
    pink = [{'face': 'skull-pink.png', 'numOfFaces': 3}, {'face': 'whiteshield-pink.png', 'numOfFaces': 2}, {'face': 'blackshield-pink.png', 'numOfFaces': 1}]
    purple = [{'face': 'skull-purple.png', 'numOfFaces': 2}, {'face': 'doubleskull-purple.png', 'numOfFaces': 1}, {'face': 'whiteshield-purple.png', 'numOfFaces': 1}, {'face': 'doublewhiteshield-purple.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-purple.png', 'numOfFaces': 1}]
    black = [{'face': 'skull-black.png', 'numOfFaces': 4}, {'face': 'whiteshield-black.png', 'numOfFaces': 1}, {'face': 'blackshield-black.png', 'numOfFaces': 1}]
    yellow = [{'face': 'skull-yellow.png', 'numOfFaces': 1}, {'face': 'doubleskull-yellow.png', 'numOfFaces': 1}, {'face': 'whiteshield-yellow.png', 'numOfFaces': 1}, {'face': 'doublewhiteshield-yellow.png', 'numOfFaces': 1}, {'face': 'blackshield-yellow.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-yellow.png', 'numOfFaces': 1}]
    boss = [{'face': 'skull-redboss.png', 'numOfFaces': 1}, {'face': 'doubleskull-redboss.png', 'numOfFaces': 2}, {'face': 'doublewhiteshield-redboss.png', 'numOfFaces': 1}, {'face': 'blackshield-redboss.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-redboss.png', 'numOfFaces': 1}]
    sqt = [{'face': 'skull-sqt.png', 'numOfFaces': 3}, {'face': 'whiteshield-sqt.png', 'numOfFaces': 2}, {'face': 'blackshield-sqt.png', 'numOfFaces': 1}]
    pot = [{'face': 'skull-pot.png', 'numOfFaces': 3}, {'face': 'whiteshield-pot.png', 'numOfFaces': 2}, {'face': 'blackshield-pot.png', 'numOfFaces': 1}]
    fh = [{'face': 'skull-fh.png', 'numOfFaces': 3}, {'face': 'whiteshield-fh.png', 'numOfFaces': 2}, {'face': 'blackshield-fh.png', 'numOfFaces': 1}]
    gen = [{'face': 'skull-gen.png', 'numOfFaces': 3}, {'face': 'whiteshield-gen.png', 'numOfFaces': 2}, {'face': 'blackshield-gen.png', 'numOfFaces': 1}]
    gen24 = [{'face': 'skull-gen24.png', 'numOfFaces': 3}, {'face': 'whiteshield-gen24.png', 'numOfFaces': 2}, {'face': 'blackshield-gen24.png', 'numOfFaces': 1}]
    dread = [{'face': 'skull-dread.png', 'numOfFaces': 3}, {'face': 'whiteshield-dread.png', 'numOfFaces': 2}, {'face': 'blackshield-dread.png', 'numOfFaces': 1}]
    jod = [{'face': 'skull-jod.png', 'numOfFaces': 3}, {'face': 'whiteshield-jod.png', 'numOfFaces': 2}, {'face': 'blackshield-jod.png', 'numOfFaces': 1}]
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
            dddiceTheme = "heroquest-combat-dice-lfftlvf4"
        if (currentFaceColor == 'red'):
            currentFace = red
            dddiceTheme = "heroquest-red-combat-dice-lz1cecrn"
        elif (currentFaceColor == 'blue'):
            currentFace = blue
            dddiceTheme = "heroquest-blue-combat-dice-lffwvlt3"
        elif (currentFaceColor == 'orange'):
            currentFace = orange
            dddiceTheme = "heroquest-orange-combat-dice-lffxaqw1"
        elif (currentFaceColor == 'green'):
            currentFace = green
            dddiceTheme = "heroquest-green-combat-dice-lffz5gf7"
        elif (currentFaceColor == 'pink'):
            currentFace = pink
            dddiceTheme = "heroquest-pink-combat-dice-lz1clxi7"
        elif (currentFaceColor == 'purple'):
            currentFace = purple
            dddiceTheme = "heroquest-purple-combat-dice-lffzqsek"
        elif (currentFaceColor == 'black'):
            currentFace = black
            dddiceTheme = "heroquest-black-combat-dice-lffwqzve"
        elif (currentFaceColor == 'yellow'):
            currentFace = yellow
            dddiceTheme = "heroquest-yellow-combat-dice-lfg05rag"
        elif (currentFaceColor == 'boss'):
            currentFace = boss
            dddiceTheme = "heroquest-red-boss-combat-dice-m1qpq8k5"
        elif (currentFaceColor == 'sqt'):
            currentFace = sqt
            dddiceTheme = "heroquest-spirit-queen's-torment-combat-dice-lz1deske"
        elif (currentFaceColor == 'pot'):
            currentFace = pot
            dddiceTheme = "heroquest-prophecy-of-telor-combat-dice-lz1dmod3"
        elif (currentFaceColor == 'fh'):
            currentFace = fh
            dddiceTheme = "heroquest-frozen-horror-combat-dice-lz1d4ggg"
        elif (currentFaceColor == 'gen'):
            currentFace = gen
            dddiceTheme = "heroquest-gencon-combat-dice-lz1e930v"
        elif (currentFaceColor == 'gen24' or currentFaceColor == 'dew'):
            currentFace = gen24
            dddiceTheme = "heroquest-gencon-2024-combat-dice-m01rq6ia"
        elif (currentFaceColor == 'dread'):
            currentFace = dread
            dddiceTheme = "heroquest-dread-veil-combat-dice-lz1lyex4"
        elif (currentFaceColor == 'jod'):
            currentFace = jod
            dddiceTheme = "heroquest-jungles-of-delthrakk-combat-diceice-m01stff3"
        
        # Assemble the current color's dice faces
        for coloredFace in currentFace:
            for x in range(0, coloredFace['numOfFaces']):
                diceFaceCount = diceFaceCount + 1
                diceImages[diceFaceCount] = cv2.imread('images/hqdice/transparent/' + coloredFace['face'], cv2.IMREAD_UNCHANGED)

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

    cv2.imwrite('images/hqdice/results.png', result_image)

    await message.channel.send(file=discord.File('images/hqdice/results.png'))

    await sendToDDDICE(message, dddRolledDice)
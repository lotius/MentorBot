import random
import numpy as np
import cv2
import discord

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
                and currentColor != 'white'):
            await message.channel.send('Sorry, but you\'ve included a die color that isn\'t available. Available colors \
are blue, orange, green, purple, black, yellow or white.')
            return
        
        for existingDice in diceToRoll:
            for dieColor in existingDice.values():
                if (currentColor == dieColor):
                    await message.channel.send('Sorry, but each die color can only be specified once.')
                    return

        # Ensure that the same color was not requested more than once in a single roll command.
        #if (any(currentColor in dice for dice in diceToRoll)):
        #    await message.channel.send('Sorry, but each die color can only be specified once.')
        #    return
        #else:
        #    diceToRoll.append({'face': currentColor, 'numToRoll': int(numToRoll)})

        diceToRoll.append({'face': currentColor, 'numToRoll': int(numToRoll)})

    await rollHeroQuestCombatDice(message, diceToRoll)
    
# Function takes 3 parameters:
# 1. An array describing the dice faces of a die to be rolled and how many of each face are on that die.
# Example: [{'face': 'skull.png', 'numOfSides': 3}, {'face': 'whiteshield.png', 'numOfSides': 2}, {'face': 'blackshield.png', 'numOfSides': 1}]
# 2. The number of dice to be rolled.
# 3. The background color of the dice image, defaults to white.
async def rollHeroQuestCombatDice(message, diceToRoll):
    white = [{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 2}, {'face': 'blackshield.png', 'numOfFaces': 1}]
    blue = [{'face': 'skull-blue.png', 'numOfFaces': 3}, {'face': 'whiteshield-blue.png', 'numOfFaces': 1}, {'face': 'blackshield-blue.png', 'numOfFaces': 2}]
    orange = [{'face': 'skull-orange.png', 'numOfFaces': 1}, {'face': 'doubleskull-orange.png', 'numOfFaces': 2}, {'face': 'doublewhiteshield-orange.png', 'numOfFaces': 1}, {'face': 'blackshield-orange.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-orange.png', 'numOfFaces': 1}]
    green = [{'face': 'skull-green.png', 'numOfFaces': 2}, {'face': 'whiteshield-green.png', 'numOfFaces': 3}, {'face': 'blackshield-green.png', 'numOfFaces': 1}]
    purple = [{'face': 'skull-purple.png', 'numOfFaces': 2}, {'face': 'doubleskull-purple.png', 'numOfFaces': 1}, {'face': 'whiteshield-purple.png', 'numOfFaces': 1}, {'face': 'doublewhiteshield-purple.png', 'numOfFaces': 1}, {'face': 'blackshield-purple.png', 'numOfFaces': 1}]
    black = [{'face': 'skull-black.png', 'numOfFaces': 4}, {'face': 'whiteshield-black.png', 'numOfFaces': 1}, {'face': 'blackshield-black.png', 'numOfFaces': 1}]
    yellow = [{'face': 'skull-yellow.png', 'numOfFaces': 1}, {'face': 'doubleskull-yellow.png', 'numOfFaces': 1}, {'face': 'whiteshield-yellow.png', 'numOfFaces': 1}, {'face': 'doublewhiteshield-yellow.png', 'numOfFaces': 1}, {'face': 'blackshield-yellow.png', 'numOfFaces': 1}, {'face': 'doubleblackshield-yellow.png', 'numOfFaces': 1}]
    diceFaceCount = 0
    diceImages = {}
    rolledDice = []

    # Assemble current dice's faces
    for currentRequestedFace in diceToRoll:

        # Color of current face
        currentFaceColor = currentRequestedFace['face']
        if (currentFaceColor == 'white'):
            currentFace = white
        elif (currentFaceColor == 'blue'):
            currentFace = blue
        elif (currentFaceColor == 'orange'):
            currentFace = orange
        elif (currentFaceColor == 'green'):
            currentFace = green
        elif (currentFaceColor == 'purple'):
            currentFace = purple
        elif (currentFaceColor == 'black'):
            currentFace = black
        elif (currentFaceColor == 'yellow'):
            currentFace = yellow
        
        # Assemble the current color's dice faces
        for coloredFace in currentFace:
            for x in range(0, coloredFace['numOfFaces']):
                diceFaceCount = diceFaceCount + 1
                diceImages[diceFaceCount] = cv2.imread('images/hqdice/' + coloredFace['face'], cv2.IMREAD_COLOR)

        # Roll the dice and save the appropriate face to an array
        for x in range(int(currentRequestedFace['numToRoll'])):
            rolledDice.append(diceImages[random.randint(1, 6)])
                
        diceFaceCount = 0
        diceImages.clear()

    result_image = np.zeros((100, len(rolledDice) * 108, 3), np.uint8)
    x = 0
    for currentDiceFace in rolledDice:
        result_image[0 : 100, 108 * x : 108 * (x + 1)] = currentDiceFace
        x = x + 1

    cv2.imwrite('images/hqdice/results.png', result_image)

    await message.channel.send(file=discord.File('images/hqdice/results.png'))
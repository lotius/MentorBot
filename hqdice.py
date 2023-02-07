import random
import numpy as np
import cv2
import discord

# Function takes 3 parameters:
# 1. An array describing the dice faces of a die to be rolled and how many of each face are on that die.
# Example: [{'face': 'skull.png', 'numOfSides': 3}, {'face': 'whiteshield.png', 'numOfSides': 2}, {'face': 'blackshield.png', 'numOfSides': 1}]
# 2. The number of dice to be rolled.
# 3. The background color of the dice image, defaults to white.
async def rollHeroQuestCombatDice(message, diceFaces, totalDiceRolled):
    diceFaceCount = 0
    diceRolls = []
    diceArray = {}
    diceImages = {}

    # Assemble dice faces
    for currentFace in diceFaces:
        for x in range(0, int(currentFace['numOfFaces'])):
            diceFaceCount = diceFaceCount + 1
            diceArray[diceFaceCount] = currentFace['face']
            diceImages[diceFaceCount] = cv2.imread('images/hqdice/' + currentFace['face'], cv2.IMREAD_COLOR)

    # Roll the dice
    for x in range(int(totalDiceRolled)):
        diceRolls.append(random.randint(1, 6))

    result_image = np.zeros((100, len(diceRolls) * 108, 3), np.uint8)
    for x in range(len(diceRolls)):
        result_image[0 : 100, 108 * x : 108 * (x + 1)] = diceImages[diceRolls[x]]

    cv2.imwrite('images/hqdice/results.png', result_image)

    await message.channel.send(file=discord.File('images/hqdice/results.png'))

# Example rolls of different face types
# rollHeroQuestCombatDice([{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 2}, {'face': 'blackshield.png', 'numOfFaces': 1}], 3)
# rollHeroQuestCombatDice([{'face': 'skull.png', 'numOfFaces': 3}, {'face': 'whiteshield.png', 'numOfFaces': 1}, {'face': 'blackshield.png', 'numOfFaces': 2}], 3, 'darkpurple')
# rollHeroQuestCombatDice([{'face': 'skull.png', 'numOfFaces': 1}, {'face': 'doubleskull.png', 'numOfFaces': 2}, {'face': 'doublewhiteshield.png', 'numOfFaces': 1}, {'face': 'blackshield.png', 'numOfFaces': 1}, {'face': 'doubleblackshield.png', 'numOfFaces': 1}], 3, 'orange')
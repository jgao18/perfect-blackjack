import pyautogui as pag
import math, operator
import functools
import os
import random

from PIL import Image
from PIL import ImageChops
import imagehash
#pag.click()

#image = pag.screenshot(region=(1352,338,28,28))

#image.save(r"c:\temp\screenshot.png")

def clickDouble():
    pag.moveTo(1720, 350, duration = 1) 

def clickHit():
    pag.moveTo(1720, 525, duration = 1)
    pag.click()

def clickStand():
    pag.moveTo(1720, 700, duration = 1)
    pag.click()

def clickRebet():
    pag.moveTo(1720, 525, duration = 1)

def clickSplit():
    pag.moveTo(1360, 610, duration = 1)
    
def clickNoInsurance():
    pag.moveTo(1720, 770, duration = 1)
               
def screenshotFirstCard():
    image = pag.screenshot(region=(1048,405,14,19))
    return image

def screenshotSecondCard():
    image = pag.screenshot(region=(1078,405,14,19))
    return image

def screenshotThirdCard():
    image = pag.screenshot(region=(1093,405,14,19))
    return image

def screenshotFourthCard():
    image = pag.screenshot(region=(1108,405,14,19))
    return image

def screenshotDealerCard():
    image = pag.screenshot(region=(1360,342,14,19))
    return image

def getImageDifference(image1, image2):
    h1 = image1.histogram()
    h2 = image2.histogram()
    rms = math.sqrt(functools.reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    return rms

def getImageDifferenceHash(image1, image2):
    hash = imagehash.average_hash(image1)
    otherhash = imagehash.average_hash(image2)

    return hash - otherhash

def getCardValue(currentCardImage, cardNumber):
    rootPath = ""
    
    if cardNumber == 0:
        rootPath = "C:\\git\\bj\\dealer_cards"
    if cardNumber == 1:
        rootPath = "C:\\git\\bj\\first_cards"
    elif cardNumber == 2:
        rootPath = "C:\\git\\bj\\second_cards"
    elif cardNumber == 3:
        rootPath = "C:\\git\\bj\\third_cards"
    elif cardNumber == 4:
        rootPath = "C:\\git\\bj\\fourth_cards"
        
    bestGuessCard = ""
    bestGuessDiff = 1000
    
    for fileName in os.listdir(rootPath):
        fullPath = os.path.join(rootPath, fileName)
        
        checkCardImage = Image.open(fullPath)
        imageDifference = getImageDifferenceHash(currentCardImage, checkCardImage)

        if imageDifference < bestGuessDiff:
            bestGuessCard = os.path.splitext(fileName)[0]
            bestGuessDiff = imageDifference
            
    print(bestGuessCard + " - " + str(bestGuessDiff))
    return bestGuessDiff

def getDealerCardValue():
    currentCardImage = screenshotDealerCard()
    rootPath = "C:\\git\\bj\\dealer_cards"
    
    for fileName in os.listdir(rootPath):
        fullPath = os.path.join(rootPath, fileName)
        
        checkCardImage = Image.open(fullPath)
        imageDifference = getImageDifference(currentCardImage, checkCardImage)

        if imageDifference == 0:
            cardString = os.path.splitext(fileName)[0]
            print(cardString)


#getCardValue(screenshotDealerCard(), 0)
#getCardValue(screenshotFirstCard(), 1)
#getCardValue(screenshotSecondCard(), 2)
#if getCardValue(screenshotThirdCard(), 3) != 0.0:
    #screenshotThirdCard().save("C:\\git\\bj\\third_cards\\" + str(random.randint(1,200)) + ".png")
if getCardValue(screenshotFourthCard(), 4) != 0:
    screenshotFourthCard().save("C:\\git\\bj\\fourth_cards\\" + str(random.randint(1,999)) + ".png")
    print("saving fourth")

#print("First Card: " + getImageDifference(screenshotSecondCard(), Image.open("C:\\git\\bj\\second_cards\\8black_tent.png")))

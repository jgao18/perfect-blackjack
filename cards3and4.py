import math, operator
import functools
import os
import random
import time

from PIL import Image
import imagehash

from PagCommands import PagCommands
Pag = PagCommands()

def sleepRandom(low, high):
    time.sleep(random.uniform(low, high))
    
def getImageDifferenceHash(image1, image2):
    hash = imagehash.average_hash(image1)
    otherhash = imagehash.average_hash(image2)

    return hash - otherhash

def getCardValue(currentCardImage, cardNumber):
    rootPath = ""
    printString = ""
    
    if cardNumber == 0:
        rootPath = "C:\\git\\bj\\dealer_cards"
        printString += "D1: "
    if cardNumber == 1:
        rootPath = "C:\\git\\bj\\first_cards"
        printString += "C1: "
    elif cardNumber == 2:
        rootPath = "C:\\git\\bj\\second_cards"
        printString += "C2: "
    elif cardNumber == 3:
        rootPath = "C:\\git\\bj\\third_cards"
        printString += "C3: "
    elif cardNumber == 4:
        rootPath = "C:\\git\\bj\\fourth_cards"
        printString += "C4: "
        
    bestGuessCard = ""
    bestGuessDiff = 1000
    
    for fileName in os.listdir(rootPath):
        fullPath = os.path.join(rootPath, fileName)
        
        checkCardImage = Image.open(fullPath)
        imageDifference = getImageDifferenceHash(currentCardImage, checkCardImage)

        if imageDifference < bestGuessDiff:
            bestGuessCard = os.path.splitext(fileName)[0][:1]
            bestGuessDiff = imageDifference
            
    return bestGuessCard, bestGuessDiff

def CalculateMove(currentHand, dealerCard):
    turnNumber = len(currentHand) - 1
    
    firstCard = currentHand[0]
    secondCard = currentHand[1]
    thirdCard = None
    fourthCard = None
    
    if len(currentHand) == 3:
        thirdCard = currentHand[2]
    if len(currentHand) == 4:
        fourthCard = currentHand[3]
    
    hardHand = True
    splitHand = False
    pocketAces = False
    
    dealerCardInt = 0
    firstCardInt = 0
    secondCardInt = 0
    thirdCardInt = 0
    fourthCardInt = 0

    acesCount = 0
    
    cardsTotalInt = 0

    if (dealerCard == "T") or (dealerCard == "J") or (dealerCard == "Q") or (dealerCard == "K"):
        dealerCardInt = 10
    elif (dealerCard == "1"):
        dealerCardInt = 11
    else:
        dealerCardInt = int(dealerCard)
    
    if (firstCard == "T") or (firstCard == "J") or (firstCard == "Q") or (firstCard == "K"):
        firstCardInt = 10
    elif (firstCard == "1"):
        hardHand = False
        firstCardInt = 11
        acesCount += 1
    else:
        firstCardInt = int(firstCard)

    if (secondCard == "T") or (secondCard == "J") or (secondCard == "Q") or (secondCard == "K"):
        secondCardInt = 10
    elif (secondCard == "1"):
        hardHand = False
        secondCardInt = 11
        acesCount += 1
    else:
        secondCardInt = int(secondCard)

    if thirdCard:
        if (thirdCard == "T") or (thirdCard == "J") or (thirdCard == "Q") or (thirdCard == "K"):
            thirdCardInt = 10
        elif (thirdCard == "1"):
            thirdCardInt = 11
            acesCount += 1
        else:
            thirdCardInt = int(thirdCard)

    if fourthCard:
        if (fourthCard == "T") or (fourthCard == "J") or (fourthCard == "Q") or (fourthCard == "K"):
            fourthCard = 10
        elif (thirdCard == "1"):
            fourthCard = 11
            acesCount += 1
        else:
            fourthCard = int(fourthCard)
        
    cardsTotalInt = firstCardInt + secondCardInt + thirdCardInt + fourthCardInt

    if (cardsTotalInt > 21):
        cardsTotalInt = firstCardInt + secondCardInt + thirdCardInt + fourthCardInt - (10*acesCount)
        
    if (firstCardInt == secondCardInt) and (len(currentHand) == 2):
        splitHand = True

    if pocketAces == True:
        return "SPLIT"

    # Split/Pair
    if splitHand == True:
        if (firstCardInt == 2) or (firstCardInt == 3):
            if (dealerCardInt == 2) or (dealerCardInt == 3):
                return "SPLIT"
            elif (dealerCardInt >= 4) and (dealerCardInt <= 7):
                return "SPLIT"
            else:
                return "HIT"
        elif (firstCardInt == 4):
            if (dealerCardInt == 5) or (dealerCardInt == 6):
                return "SPLIT"
            else:
                return "HIT"
        elif (firstCardInt == 5):
            if (dealerCardInt == 10) or (dealerCardInt == 11):
                return "HIT"
            else:
                return "DOUBLE"
        elif (firstCardInt == 6):
            if (dealerCardInt == 2):
                return "SPLIT"
            elif (dealerCardInt >= 3) and (dealerCardInt <= 6):
                return "SPLIT"
            else:
                return "HIT"
        elif (firstCardInt == 7):
            if (dealerCardInt >= 2) and (dealerCardInt <= 7):
                return "SPLIT"
            else:
                return "HIT"
        elif (firstCardInt == 8):
            if (dealerCardInt == 11):
                return "SURRENDER"
            else:
                return "SPLIT"
        elif (firstCardInt == 9):
            if (dealerCardInt == 7) or (dealerCardInt == 10) or (dealerCardInt == 11):
                return "STAND"
            else:
                return "SPLIT"
            
        
    # Hard
    elif hardHand == True:
        if cardsTotalInt <= 8:
            return "HIT"
        elif cardsTotalInt == 9:
            if (dealerCardInt == 3) or (dealerCardInt == 4) or (dealerCardInt == 5) or (dealerCardInt == 6):
                if turnNumber == 1:
                    return "DOUBLE"
                else:
                    return "HIT"
            else:
                return "HIT"
        elif cardsTotalInt == 10:
            if (dealerCardInt == 10) or (dealerCardInt == 11):
                return "HIT"
            else:
                if turnNumber == 1:
                    return "DOUBLE"
                else:
                    return "HIT"
        elif cardsTotalInt == 11:
            if turnNumber == 1:
                return "DOUBLE"
            else:
                return "HIT"
        elif cardsTotalInt == 12:
            if (dealerCardInt == 4) or (dealerCardInt == 5) or (dealerCardInt == 6):
                return "STAND"
            else:
                return "HIT"
        elif (cardsTotalInt == 13) or (cardsTotalInt == 14):
            if (dealerCardInt >= 7):
                return "HIT"
            else:
                return "STAND"
        elif (cardsTotalInt == 15):
            if (dealerCardInt <=6):
                return "STAND"
            elif (dealerCardInt == 7) or (dealerCardInt == 8) or (dealerCardInt == 9):
                return "HIT"
            elif (dealerCardInt >=10):
                if (turnNumber == 1):
                    return "SURRENDER"
                else:
                    return "HIT"
        elif (cardsTotalInt == 16):
            if (dealerCardInt <=6):
                return "STAND"
            elif (dealerCardInt == 7) or (dealerCardInt == 8):
                return "HIT"
            elif (dealerCardInt >=9):
                if (turnNumber == 1):
                    return "SURRENDER"
                else:
                    return "HIT"
        elif (cardsTotalInt == 17):
            if (dealerCardInt == 11) and (turnNumber == 1):
                return "SURRENDER"
            else:
                return "STAND"
        elif (cardsTotalInt >= 18):
            return "STAND"

    # Soft
    elif hardHand == False:
        if (cardsTotalInt == 13) or (cardsTotalInt == 14):
            if (turnNumber == 1) and ( (dealerCardInt == 5) or (dealerCardInt == 6)  ):
                return "DOUBLE"
            else:
                return "HIT"
        elif (cardsTotalInt == 15) or (cardsTotalInt == 16):
            if (turnNumber == 1) and ( (dealerCardInt == 4) or (dealerCardInt == 5) or (dealerCardInt == 6)  ):
                return "DOUBLE"
            else:
                return "HIT"
        elif (cardsTotalInt == 17):
            if (turnNumber == 1) and ( (dealerCardInt == 3) or (dealerCardInt == 4) or (dealerCardInt == 5) or (dealerCardInt == 6)  ):
                return "DOUBLE"
            else:
                return "HIT"
        elif (cardsTotalInt == 18):
            if (dealerCardInt >= 2) and (dealerCardInt <= 6):
                if (turnNumber == 1):
                    return "DOUBLE"
                else:
                    return "STAND"
            elif (dealerCardInt == 7) or (dealerCardInt == 8):
                return "STAND"
            else:
                return "HIT"
        elif (cardsTotalInt == 19):
            if (dealerCardInt == 6):
                if (turnNumber == 1):
                    return "DOUBLE"
                else:
                    return "STAND"
            else:
                return "STAND"
        elif (cardsTotalInt >= 20):
            return "STAND"

            
def main():
    play = True
    handNumber = 1
    currentHand = []

    while play:
        #Pag.clickRebet()
        #handNumber = 1
        #turnNumber = 1
        #sleepRandom(10, 15)
        
        dealerCardImage = Pag.screenshotAndReturnDealerCard()
        dealerCard, imageDiff = getCardValue(dealerCardImage, 0)
        if imageDiff != 0:
            os._exit(0)

        firstCardImage = Pag.screenshotAndReturnFirstCard()
        firstCard, imageDiff = getCardValue(firstCardImage, 1)
        currentHand.append(firstCard)
        if imageDiff != 0:
            os._exit(0)

        secondCardImage = Pag.screenshotAndReturnSecondCard()
        secondCard, imageDiff = getCardValue(secondCardImage, 1)
        currentHand.append(secondCard)
        if imageDiff != 0:
            os._exit(0)

        correctMove = CalculateMove(currentHand, dealerCard)
        
        os._exit(0)


dealerCard = getCardValue(Pag.screenshotAndReturnDealerCard(), 0)[0]
card1 = getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[0]
card3 = getCardValue(Pag.screenshotAndReturnSecondCard(), 2)[0]

print("D: " + dealerCard)
print("C1: " + card1)
print("C2: " + card2)
print(CalculateMove([card1, card2], dealerCard))
print("____________________")


if getCardValue(screenshotThirdCard(), 3) != 0:
    screenshotThirdCard().save("C:\\git\\bj\\third_cards\\" + str(random.randint(1,200)) + ".png")
    print("saving third")


def testMove(card1, card2, dealerCard, expected):
    if (card1 == 11):
        card1 = "1"
    if (card2 == 11):
        card2 = "1"
    arr = []
    arr.append(str(card1))
    arr.append(str(card2))
    actual = CalculateMove(arr, dealerCard)

    if (actual is not expected):
        print(str(card1) + ", " + str(card2) + ", " + str(dealerCard) + "  - A:" + actual + " VS E:" + expected)
        
def test():
    #hard
    for card1 in range(2, 11):
        for card2 in range(2, 11):
            if card1 is not card2:
                cardSum = card1 + card2

                if cardSum == 11:
                    testMove(card1, card2, 11, "DOUBLE")
                elif cardSum <= 14:
                    testMove(card1, card2, 11, "HIT")
                elif cardSum <= 17:
                    testMove(card1, card2, 11, "SURRENDER")
                else:
                    testMove(card1, card2, 11, "STAND")
                    
                for dealerCard in range(2, 11):
                    if cardSum <= 8:
                        testMove(card1, card2, dealerCard, "HIT")
                    elif cardSum == 9:
                        if dealerCard >= 3 and dealerCard <=6:
                            testMove(card1, card2, dealerCard, "DOUBLE")
                        else:
                            testMove(card1, card2, dealerCard, "HIT")
                    elif cardSum == 10:
                        if dealerCard <= 9:
                            testMove(card1, card2, dealerCard, "DOUBLE")
                        else:
                            testMove(card1, card2, dealerCard, "HIT")
                    elif cardSum == 11:
                        testMove(card1, card2, dealerCard, "DOUBLE")
                    elif cardSum == 12:
                        if dealerCard >=4 and dealerCard <= 6:
                            testMove(card1, card2, dealerCard, "STAND")
                        else:
                            testMove(card1, card2, dealerCard, "HIT")
                    elif cardSum == 13 or cardSum == 14:
                        if dealerCard <= 6:
                            testMove(card1, card2, dealerCard, "STAND")
                        else:
                            testMove(card1, card2, dealerCard, "HIT")
                    elif cardSum == 15:
                        if dealerCard <= 6:
                            testMove(card1, card2, dealerCard, "STAND")
                        elif dealerCard >= 7 and dealerCard <= 9:
                            testMove(card1, card2, dealerCard, "HIT")
                        else:
                            testMove(card1, card2, dealerCard, "SURRENDER")
                    elif cardSum == 16:
                        if dealerCard <= 6:
                            testMove(card1, card2, dealerCard, "STAND")
                        elif dealerCard >= 7 and dealerCard <= 8:
                            testMove(card1, card2, dealerCard, "HIT")
                        else:
                            testMove(card1, card2, dealerCard, "SURRENDER")
                    elif cardSum >= 17:
                        testMove(card1, card2, dealerCard, "STAND")

    #soft1
    card1 = 11
    for card2 in range(2, 10):
        cardSum = card1 + card2

        if cardSum <= 18:
            testMove(card1, card2, 11, "HIT")
        else:
            testMove(card1, card2, 11, "STAND")
        
        for dealerCard in range(2, 11):
            if cardSum == 13 or cardSum == 14:
                if dealerCard == 5 or dealerCard == 6:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                else:
                    testMove(card1, card2, dealerCard, "HIT")
            elif cardSum == 15 or cardSum == 16:
                if dealerCard == 5 or dealerCard == 6 or dealerCard == 4:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                else:
                    testMove(card1, card2, dealerCard, "HIT")
            elif cardSum == 17:
                if dealerCard == 5 or dealerCard == 6 or dealerCard == 4 or dealerCard == 3:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                else:
                    testMove(card1, card2, dealerCard, "HIT")
            elif cardSum == 18:
                if dealerCard <=6:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                elif dealerCard <=8:
                    testMove(card1, card2, dealerCard, "STAND")
                else:
                    testMove(card1, card2, dealerCard, "HIT")
            elif cardSum == 19:
                if dealerCard == 6:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                else:
                    testMove(card1, card2, dealerCard, "STAND")
            elif cardSum == 20:
                testMove(card1, card2, dealerCard, "STAND")

    #soft2
    card2 = 11
    for card1 in range(2, 10):
        cardSum = card1 + card2

        if cardSum <= 18:
            testMove(card1, card2, 11, "HIT")
        else:
            testMove(card1, card2, 11, "STAND")
            
        for dealerCard in range(2, 11):
            if cardSum == 13 or cardSum == 14:
                if dealerCard == 5 or dealerCard == 6:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                else:
                    testMove(card1, card2, dealerCard, "HIT")
            elif cardSum == 15 or cardSum == 16:
                if dealerCard == 5 or dealerCard == 6 or dealerCard == 4:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                else:
                    testMove(card1, card2, dealerCard, "HIT")
            elif cardSum == 17:
                if dealerCard == 5 or dealerCard == 6 or dealerCard == 4 or dealerCard == 3:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                else:
                    testMove(card1, card2, dealerCard, "HIT")
            elif cardSum == 18:
                if dealerCard <=6:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                elif dealerCard <=8:
                    testMove(card1, card2, dealerCard, "STAND")
                else:
                    testMove(card1, card2, dealerCard, "HIT")
            elif cardSum == 19:
                if dealerCard == 6:
                    testMove(card1, card2, dealerCard, "DOUBLE")
                else:
                    testMove(card1, card2, dealerCard, "STAND")
            elif cardSum == 20:
                testMove(card1, card2, dealerCard, "STAND")

    #splits
    for card in range(2, 11):
        
        if cardSum <= 14:
            testMove(card1, card2, 11, "HIT")
        elif cardSum <= 16:
            testMove(card1, card2, 11, "SURRENDER")
        elif cardSum <= 18:
            testMove(card1, card2, 11, "SURRENDER")
        else:
            testMove(card1, card2, 11, "STAND")
            
        for dealerCard in range(2, 11):
            if card == 2 or card == 3:
                if dealerCard <= 3:
                    testMove(card, card, dealerCard, "SPLIT")
                elif dealerCard <= 7:
                    testMove(card, card, dealerCard, "SPLIT")
                else:
                    testMove(card, card, dealerCard, "HIT")
            elif card == 4:
                if dealerCard <= 4:
                    testMove(card, card, dealerCard, "HIT")
                elif dealerCard <= 6:
                    testMove(card, card, dealerCard, "SPLIT")
                else:
                    testMove(card, card, dealerCard, "HIT")
            elif card == 5:
                if dealerCard == 10:
                    testMove(card, card, dealerCard, "HIT")
                else:
                    testMove(card, card, dealerCard, "DOUBLE")
            elif card == 6:
                if dealerCard == 2:
                    testMove(card, card, dealerCard, "SPLIT")
                elif dealerCard <= 6:
                    testMove(card, card, dealerCard, "SPLIT")
                else:
                    testMove(card, card, dealerCard, "HIT")
            elif card == 7:
                if dealerCard <= 7:
                    testMove(card, card, dealerCard, "SPLIT")
                else:
                    testMove(card, card, dealerCard, "HIT")
            elif card == 8:
                testMove(card, card, dealerCard, "SPLIT")
            elif card == 9:
                if dealerCard == 7 or dealerCard == 10:
                    testMove(card, card, dealerCard, "STAND")
                else:
                    testMove(card, card, dealerCard, "SPLIT")


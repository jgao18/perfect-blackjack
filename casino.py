import math, operator
import functools
import os
import random
import time
import datetime

from PIL import Image
import imagehash
import string

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

def CalculateMove(currentHand, dealerCard, doNotSplit):
    turnNumber = len(currentHand) - 1
    
    firstCard = currentHand[0]
    secondCard = currentHand[1]
    thirdCard = None
    fourthCard = None
    
    if len(currentHand) >= 3:
        thirdCard = currentHand[2]
    if len(currentHand) >= 4:
        fourthCard = currentHand[3]
    
    hardHand = True
    splitHand = False
    
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
        if turnNumber == 1:
            hardHand = False
        firstCardInt = 11
        acesCount += 1
    else:
        firstCardInt = int(firstCard)

    if (secondCard == "T") or (secondCard == "J") or (secondCard == "Q") or (secondCard == "K"):
        secondCardInt = 10
    elif (secondCard == "1"):
        if turnNumber == 1:
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
        elif (fourthCard == "1"):
            fourthCard = 11
            acesCount += 1
        else:
            fourthCardInt = int(fourthCard)

    if (firstCardInt + secondCardInt == 22):
        return "SPLIT"
        
    cardsTotalInt = firstCardInt + secondCardInt + thirdCardInt + fourthCardInt

    if (cardsTotalInt > 21):
        cardsTotalInt = firstCardInt + secondCardInt + thirdCardInt + fourthCardInt - (10*acesCount)
        
    if (firstCardInt == secondCardInt) and (len(currentHand) == 2) and (not doNotSplit):
        splitHand = True

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
        elif (firstCardInt == 10):
            return "STAND"
            
        
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

def checkAndLogInitialCards():

    dealerCard = getCardValue(Pag.screenshotAndReturnDealerCard(), 0)[0]
    card1 = getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[0]
    card2 = getCardValue(Pag.screenshotAndReturnSecondCard(), 2)[0]

    N = 8
    if getCardValue(Pag.screenshotAndReturnDealerCard(), 0)[1] != 0:
        Pag.screenshotAndReturnDealerCard().save("C:\\git\\bj\\newfound\\dealer\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
        print("Found a new dealer card with a diff of " + str(getCardValue(Pag.screenshotAndReturnDealerCard(), 0)[1]) + ", exiting.")
        os._exit(0)

    if getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0:
        Pag.screenshotAndReturnFirstCard().save("C:\\git\\bj\\newfound\\first\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
        print("Found a new first card with a diff of " + getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] + ", exiting.")
        os._exit(0)

    if getCardValue(Pag.screenshotAndReturnSecondCard(), 2)[1] != 0:
        Pag.screenshotAndReturnSecondCard().save("C:\\git\\bj\\newfound\\second\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
        print("Found a new second card, exiting.")
        os._exit(0)

def clickBasedOnCards(currentHand, dealerCard, doNotSplit):
    correctMove = CalculateMove(currentHand, dealerCard, doNotSplit)
    
    if correctMove == "HIT":
        Pag.clickHit()      
    elif correctMove == "STAND":
        Pag.clickStand()
    elif correctMove == "DOUBLE":
        Pag.clickDouble()
    elif correctMove == "SPLIT":
        Pag.clickSplit()
    elif correctMove == "SURRENDER":
        Pag.clickSurrender()
    else:
        print("Exiting because correct move was None")
        os._exit(0)

    return correctMove

def atMainMenu():
    sleepRandom(2.0, 2.5)
    testMainMenu = Pag.screenshotAndReturnMainMenu()
    realMainMenu = Image.open("C:\\git\\bj\\menu.png")
    imageDifference = getImageDifferenceHash(testMainMenu, realMainMenu)
    if imageDifference == 0:
        return True
    else:
        return False

def areThreeCards():
    testThree = Pag.screenshotAndReturnThreeCardLines()
    realThree = Image.open("C:\\git\\bj\\three_cards.png")
    imageDifference = getImageDifferenceHash(testThree, realThree)
    if imageDifference == 0:
        return True
    else:
        return False

def areFourCards():
    testFour = Pag.screenshotAndReturnFourCardLines()
    realFour = Image.open("C:\\git\\bj\\four_cards.png")
    imageDifference = getImageDifferenceHash(testFour, realFour)
    if imageDifference == 0:
        return True
    else:
        return False

def areFiveCards():
    testFive = Pag.screenshotAndReturnFiveCardLines()
    realFive = Image.open("C:\\git\\bj\\five_cards.png")
    imageDifference = getImageDifferenceHash(testFive, realFive)
    if imageDifference == 0:
        return True
    else:
        return False

def main():
    play = True
    roundCount = 1
    handNumber = 1
    N=8
    now = datetime.datetime.now()
    print("Ran at " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
    while play:
        print("----------- STARTING NEW ROUND: " + str(roundCount) + " --------------")
        currentHand = []
        handNumber = 1

        Pag.clickRebet()
        sleepRandom(4.5, 5.5)
        Pag.clickNoInsurance()
        sleepRandom(6.5,7.5)
        
        while handNumber <= 3:
            print("  Playing hand: " + str(handNumber))
            # See if we're back at the main menu
            if atMainMenu():
                print("  Found that we're at the main menu")
                break

            checkAndLogInitialCards()
            
            dealerCardImage = Pag.screenshotAndReturnDealerCard()
            dealerCard, imageDiff = getCardValue(dealerCardImage, 0)

            firstCardImage = Pag.screenshotAndReturnFirstCard()
            firstCard, imageDiff = getCardValue(firstCardImage, 1)
            currentHand.append(firstCard)

            secondCardImage = Pag.screenshotAndReturnSecondCard()
            secondCard, imageDiff = getCardValue(secondCardImage, 2)
            currentHand.append(secondCard)

            print("    D: " + dealerCard + " | C1: " + firstCard + " | C2: " + secondCard)

            action = clickBasedOnCards(currentHand, dealerCard, False)
            print("    Performing " + action)
            sleepRandom(3.5, 4.5)
            
            if (action == "HIT") and (not atMainMenu()):
                if areThreeCards(): #getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0:
                    #need a second action
                    thirdCardImage = Pag.screenshotAndReturnThirdCard()
                    thirdCard, imageDiff = getCardValue(thirdCardImage, 3)
                    currentHand.append(thirdCard)

                    print("    C3: " + thirdCard)

                    if imageDiff > 1.5:
                        Pag.screenshotAndReturnThirdCard().save("C:\\git\\bj\\newfound\\third\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
                        print("    Found a new third card with a diff of " + str(imageDiff) + ", exiting.")
                        os._exit(0)

                    action = clickBasedOnCards(currentHand, dealerCard, False)
                    print("    Performing " + action)
                    sleepRandom(3.5, 4.5)
                    
                    if areFourCards(): #(getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0) and (not atMainMenu()):
                        #need a third action
                        fourthCardImage = Pag.screenshotAndReturnFourthCard()
                        fourthCard, imageDiff = getCardValue(fourthCardImage, 4)
                        currentHand.append(fourthCard)

                        print("    C4: " + fourthCard)

                        if imageDiff > 1.5:
                            Pag.screenshotAndReturnFourthCard().save("C:\\git\\bj\\newfound\\fourth\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
                            print("    Found a new fourth card with a diff of " + str(imageDiff) + ", exiting.")
                            os._exit(0)
                            
                        action = clickBasedOnCards(currentHand, dealerCard, False)
                        print("    Performing " + action)
                        sleepRandom(3.5, 4.5)
                        
                        if areFiveCards(): #"(getCardValue(Pag.screenshotAndReturnSecondCard(), 2)[1] != 0.0) and (not atMainMenu()):
                            # for the fourth action, just stand
                            print("    Performing STAND for last action")
                            Pag.clickStand()
                            sleepRandom(3.5, 4.5)
                        
            elif (action == "SPLIT") and (not atMainMenu()):
                currentHand.pop()

                # if we get pocket aces the round might be over or the next hand comes up
                if (firstCard == "1"):
                    sleepRandom(3.5, 4.5)
                    del currentHand[:]
                    handNumber += 1
                    sleepRandom(7, 9)
                    continue

                secondCardImage = Pag.screenshotAndReturnSecondCard()
                secondCard, imageDiff = getCardValue(secondCardImage, 2)
                currentHand.append(secondCard)

                print("    C2: " + secondCard)

                if imageDiff > 1.5:
                    Pag.screenshotAndReturnSecondCard().save("C:\\git\\bj\\newfound\\split\\second\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
                    print("    Found a new split second card with a diff of " + str(imageDiff) + ", exiting.")
                    os._exit(0)

                action = clickBasedOnCards(currentHand, dealerCard, True)
                print("    Performing " + action)
                sleepRandom(3.5, 4.5)

                if (action == "HIT") and (not atMainMenu()):
                    if areThreeCards():  # getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0:
                        # need a second action
                        thirdCardImage = Pag.screenshotAndReturnThirdCard()
                        thirdCard, imageDiff = getCardValue(thirdCardImage, 3)
                        currentHand.append(thirdCard)

                        print("    C3: " + thirdCard)

                        if imageDiff > 1.5:
                            Pag.screenshotAndReturnThirdCard().save("C:\\git\\bj\\newfound\\split\\third\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
                            print("    Found a new split third card with a diff of " + str(imageDiff) + ", exiting.")
                            os._exit(0)

                        action = clickBasedOnCards(currentHand, dealerCard, False)
                        print("    Performing " + action)
                        sleepRandom(3.5, 4.5)

                        if areFourCards():  # (getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0) and (not atMainMenu()):
                            # need a third action
                            fourthCardImage = Pag.screenshotAndReturnFourthCard()
                            fourthCard, imageDiff = getCardValue(fourthCardImage, 4)
                            currentHand.append(fourthCard)

                            print("    C4: " + fourthCard)

                            if imageDiff > 1.5:
                                Pag.screenshotAndReturnFourthCard().save("C:\\git\\bj\\newfound\\split\\fourth\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
                                print("    Found a new split fourth card with a diff of " + str(imageDiff) + ", exiting.")
                                os._exit(0)

                            action = clickBasedOnCards(currentHand, dealerCard, False)
                            print("    Performing " + action)
                            sleepRandom(3.5, 4.5)

                            if areFiveCards:  # "(getCardValue(Pag.screenshotAndReturnSecondCard(), 2)[1] != 0.0) and (not atMainMenu()):
                                # for the fourth action, just stand
                                print("    Performing STAND for last action")
                                Pag.clickStand()
                                sleepRandom(9,12)

                del currentHand[:]
                currentHand.append(firstCard)

                secondCardImage = Pag.screenshotAndReturnSecondCard()
                secondCard, imageDiff = getCardValue(secondCardImage, 2)
                currentHand.append(secondCard)

                print("    C2: " + secondCard)

                if imageDiff > 1.5:
                    Pag.screenshotAndReturnSecondCard().save("C:\\git\\bj\\newfound\\split\\second\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
                    print("    Found a new split second card with a diff of " + str(imageDiff) + ", exiting.")
                    os._exit(0)

                action = clickBasedOnCards(currentHand, dealerCard, True)
                print("    Performing " + action)
                sleepRandom(3.5, 4.5)

                if (action == "HIT") and (not atMainMenu()):
                    if areThreeCards():  # getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0:
                        # need a second action
                        print("Executing second action")
                        thirdCardImage = Pag.screenshotAndReturnThirdCard()
                        thirdCard, imageDiff = getCardValue(thirdCardImage, 3)
                        currentHand.append(thirdCard)

                        print("    C3: " + thirdCard)

                        if imageDiff > 1.5:
                            Pag.screenshotAndReturnThirdCard().save("C:\\git\\bj\\newfound\\split\\third\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
                            print("    Found a new split third card with a diff of " + str(imageDiff) + ", exiting.")
                            os._exit(0)

                        action = clickBasedOnCards(currentHand, dealerCard, False)
                        print("    Performing " + action)
                        sleepRandom(3.5, 4.5)

                        if areFourCards():  # (getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0) and (not atMainMenu()):
                            # need a third action
                            fourthCardImage = Pag.screenshotAndReturnFourthCard()
                            fourthCard, imageDiff = getCardValue(fourthCardImage, 4)
                            currentHand.append(fourthCard)

                            print("    C4: " + fourthCard)

                            if imageDiff > 1.5:
                                Pag.screenshotAndReturnFourthCard().save("C:\\git\\bj\\newfound\\split\\fourth\\" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + ".png")
                                print("    Found a new split fourth card with a diff of " + str(imageDiff) + ", exiting.")
                                os._exit(0)

                            action = clickBasedOnCards(currentHand, dealerCard, False)
                            print("    Performing " + action)
                            sleepRandom(3.5, 4.5)

                            if areFiveCards:  # "(getCardValue(Pag.screenshotAndReturnSecondCard(), 2)[1] != 0.0) and (not atMainMenu()):
                                # for the fourth action, just stand
                                print("    Performing STAND for last action")
                                Pag.clickStand()
                                sleepRandom(3.5, 4.5)

            del currentHand[:]
            handNumber += 1
            sleepRandom(7, 9)

        roundCount += 1

main()

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

def Split():
    dealerCard = "3"
    currentHand = ["3", "3"]
    currentHand.pop()

    #secondCardImage = Pag.screenshotAndReturnSecondCard()
    #secondCard, imageDiff = getCardValue(secondCardImage, 2)
    currentHand.append("9")
    #if imageDiff > 1.5:
        #print("exiting beacuse second imageDiff was " + str(imageDiff))
        #os._exit(0)

    action = clickBasedOnCards(currentHand, dealerCard, True)
    sleepRandom(3.5, 4.5)

    if (action == "HIT") and (not atMainMenu()):
        if areThreeCards():  # getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0:
            # need a second action
            print("Executing second action")
            thirdCardImage = Pag.screenshotAndReturnThirdCard()
            thirdCard, imageDiff = getCardValue(thirdCardImage, 3)
            currentHand.append(thirdCard)
            if imageDiff > 1.5:
                print("exiting beacuse third imageDiff was " + str(imageDiff))
                os._exit(0)
            action = clickBasedOnCards(currentHand, dealerCard, False)
            sleepRandom(3.5, 4.5)

            if areFourCards():  # (getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0) and (not atMainMenu()):
                # need a third action
                fourthCardImage = Pag.screenshotAndReturnFourthCard()
                fourthCard, imageDiff = getCardValue(fourthCardImage, 4)
                currentHand.append(fourthCard)
                if imageDiff > 1.5:
                    print("exiting beacuse fourth imageDiff was " + str(imageDiff))
                    os._exit(0)

                action = clickBasedOnCards(currentHand, dealerCard, False)
                sleepRandom(3.5, 4.5)

                if areFiveCards:  # "(getCardValue(Pag.screenshotAndReturnSecondCard(), 2)[1] != 0.0) and (not atMainMenu()):
                    # for the fourth action, just stand
                    print("Executing fourth action")
                    Pag.clickStand()
                    # sleepRandom(9,12)

    sleepRandom(3.5, 4.5)
    del currentHand[:]
    currentHand.append(secondCard)

    secondCardImage = Pag.screenshotAndReturnSecondCard()
    secondCard, imageDiff = getCardValue(secondCardImage, 2)
    currentHand.append(secondCard)
    if imageDiff > 1.5:
        print("exiting beacuse second imageDiff was " + str(imageDiff))
        os._exit(0)

    action = clickBasedOnCards(currentHand, dealerCard, True)
    sleepRandom(3.5, 4.5)

    if (action == "HIT") and (not atMainMenu()):
        if areThreeCards():  # getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0:
            # need a second action
            print("Executing second action")
            thirdCardImage = Pag.screenshotAndReturnThirdCard()
            thirdCard, imageDiff = getCardValue(thirdCardImage, 3)
            currentHand.append(thirdCard)
            if imageDiff > 1.5:
                print("exiting beacuse third imageDiff was " + str(imageDiff))
                os._exit(0)
            action = clickBasedOnCards(currentHand, dealerCard, False)
            sleepRandom(3.5, 4.5)

            if areFourCards():  # (getCardValue(Pag.screenshotAndReturnFirstCard(), 1)[1] != 0.0) and (not atMainMenu()):
                # need a third action
                fourthCardImage = Pag.screenshotAndReturnFourthCard()
                fourthCard, imageDiff = getCardValue(fourthCardImage, 4)
                currentHand.append(fourthCard)
                if imageDiff > 1.5:
                    print("exiting beacuse fourth imageDiff was " + str(imageDiff))
                    os._exit(0)

                action = clickBasedOnCards(currentHand, dealerCard, False)
                sleepRandom(3.5, 4.5)

                if areFiveCards:  # "(getCardValue(Pag.screenshotAndReturnSecondCard(), 2)[1] != 0.0) and (not atMainMenu()):
                    # for the fourth action, just stand
                    print("Executing fourth action")
                    Pag.clickStand()
                    sleepRandom(3.5, 4.5)


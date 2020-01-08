#hard
for card1 in range(2, 11):
    for card2 in range(2, 11):
        if card1 is not card2:
            cardSum = card1 + card2

            # check when dealerCard is Ace
            
            for dealerCard in range(2, 11):
                if cardSum <= 8:
                    print("HIT")
                elif cardSum == 9:
                    if dealerCard >= 3 and dealerCard <=6:
                        print("DOUBLE")
                    else:
                        print("HIT")
                elif cardSum == 10:
                    if dealerCard <= 9:
                        print("DOUBLE")
                    else:
                        print("HIT")
                elif cardSum == 11:
                    print("DOUBLE")
                elif cardSum == 12:
                    if dealerCard >=4 and dealerCard <= 6:
                        print("STAND")
                    else:
                        print("HIT")
                elif cardSum == 13 or cardSum == 14:
                    if dealerCard <= 6:
                        print("STAND")
                    else:
                        print("HIT")
                elif cardSum == 15:
                    if dealerCard <= 6:
                        print("STAND")
                    elif dealerCard >= 7 and dealerCard <= 9:
                        print("HIT")
                    else:
                        print("SURRENDER")
                elif cardSum == 16:
                    if dealerCard <= 6:
                        print("STAND")
                    elif dealerCard >= 7 and dealerCard <= 8:
                        print("HIT")
                    else:
                        print("SURRENDER")
                elif cardSum >= 17:
                    print("STAND")

#soft1
card1 = 11
for card2 in range(2, 11):
    cardSum = card1 + card2
    for dealerCard in range(2, 11):
        if cardSum == 13 or cardSum == 14:
            if dealerCard == 5 or dealerCard == 6:
                print("DOUBLE")
            else:
                print("HIT")
        elif cardSum == 15 or cardsum == 16:
            if dealerCard == 5 or dealerCard == 6 or dealerCard == 4:
                print("DOUBLE")
            else:
                print("HIT")
        elif cardSum == 17:
            if dealerCard == 5 or dealerCard == 6 or dealerCard == 4 or dealerCard == 3:
                print("DOUBLE")
            else:
                print("HIT")
        elif cardSum == 18:
            if dealerCard <=6:
                return("DOUBLE")
            elif dealerCard <=8:
                return "STAND"
            else:
                return "HIT"
        elif cardSum == 19:
            if dealerCard == 6:
                return "DOUBLE"
            else:
                return "STAND"
        elif cardSum == 20:
            return "STAND"

#soft2
card2 = 11
for card1 in range(2, 11):
    cardSum = card1 + card2
    for dealerCard in range(2, 11):
        if cardSum == 13 or cardSum == 14:
            if dealerCard == 5 or dealerCard == 6:
                print("DOUBLE")
            else:
                print("HIT")
        elif cardSum == 15 or cardsum == 16:
            if dealerCard == 5 or dealerCard == 6 or dealerCard == 4:
                print("DOUBLE")
            else:
                print("HIT")
        elif cardSum == 17:
            if dealerCard == 5 or dealerCard == 6 or dealerCard == 4 or dealerCard == 3:
                print("DOUBLE")
            else:
                print("HIT")
        elif cardSum == 18:
            if dealerCard <=6:
                return("DOUBLE")
            elif dealerCard <=8:
                return "STAND"
            else:
                return "HIT"
        elif cardSum == 19:
            if dealerCard == 6:
                return "DOUBLE"
            else:
                return "STAND"
        elif cardSum == 20:
            return "STAND"

#splits
for card in range(2, 11):
    for dealerCard in range(2, 11):
        if card ==2 or card == 3:
            if dealerCard <= 3:
                return "SPLIT"
            elif dealerCard < =7:
                return "SPLIT"
            else:
                return "HIT"
        elif card == 4:
            if dealerCard <= 4:
                return "HIT"
            elif dealerCard <= 6:
                return "SPLIT"
            else:
                return "HIT"
        elif card == 5:
            if dealerCard == 10:
                return "HIT"
            else:
                return "DOUBLE"
        elif card == 6:
            if dealerCard == 2:
                return "SPLIT"
            elif dealerCard <= 6:
                return "SPLIT"
            else:
                return "HIT"
        elif card == 7:
            if dealerCard <= 7:
                return "SPLIT"
            else:
                return "HIT"
        elif card == 8:
            return "SPLIT"
        elif card == 9:
            if dealerCard == 7 or dealerCard == 10:
                return "STAND"
            else:
                return "SPLIT"

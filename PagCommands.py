import pyautogui as pag

class PagCommands:
    def __init__(self):
        pass

    def clickDouble(self):
        pag.moveTo(1720, 350, duration = 1)
        pag.click()

    def clickHit(self):
        pag.moveTo(1720, 525, duration = 1)
        pag.click()

    def clickStand(self):
        pag.moveTo(1720, 700, duration = 1)
        pag.click()

    def clickSurrender(self):
        pag.moveTo(1720,900, duration = 1)
        pag.click()

    def clickRebet(self):
        pag.moveTo(1720, 525, duration = 1)
        pag.click()

    def clickSplit(self):
        pag.moveTo(1360, 610, duration = 1)
        pag.click()
        
    def clickNoInsurance(self):
        pag.moveTo(1720, 770, duration = 1)
        pag.click()
               
    def screenshotAndReturnFirstCard(self):
        image = pag.screenshot(region=(1048,405,14,19))
        return image

    def screenshotAndReturnSecondCard(self):
        image = pag.screenshot(region=(1078,405,14,19))
        return image

    def screenshotAndReturnThirdCard(self):
        image = pag.screenshot(region=(1093,405,14,19))
        return image

    def screenshotAndReturnFourthCard(self):
        image = pag.screenshot(region=(1108,405,14,19))
        return image

    def screenshotAndReturnDealerCard(self):
        image = pag.screenshot(region=(1360,342,14,19))
        return image

    def screenshotAndReturnMainMenu(self):
        image = pag.screenshot(region=(1048,405,200,300))
        return image

    def screenshotAndReturnThreeCardLines(self):
        image = pag.screenshot(region=(1025,505,70,10))
        return image
    
    def screenshotAndReturnFourCardLines(self):
        image = pag.screenshot(region=(1010,505,100,10))
        return image

    def screenshotAndReturnFiveCardLines(self):
        image = pag.screenshot(region=(1010,505,105,10))
        return image


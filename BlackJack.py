from random import randint
from os import system
system('cls')
CARD_ARRAY = ("Ace","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King")
SUIT_ARRAY = ("Hearts","Clubs","Spades","Diamonds")

class Card():
    def __init__(self,suitNum,cardNum):
        self.name = self.getName(cardNum)
        self.value = self.getValue(cardNum)
        self.suit = self.getSuit(suitNum)
        self.isAce = type(self.value) == tuple

    def getName(self,num):
        return CARD_ARRAY[num-1]
    def getSuit(self,num):
        return SUIT_ARRAY[num]
    def getValue(self,num):
        if num == 1:
            return (1,11)
        elif num > 10:
            return 10
        else:
            return num
    def rCard(self):
        print("{} of {}".format(self.name,self.suit))

class Game():
    def __init__(self):
        self.deck = self.makeDeck()
        self.playerHand = []
        self.playerHand2 = []
        self.dealerHand = []
        self.discardPile = []
        self.twoHands = False
        self.dealBlackJack = ""
        self.losses = 0 # TO BE IMPLEMENTED
        self.wins = 0

    def makeDeck(self):
        deck = []
        for i in range(4):
            for j in range(13):
                deck.append(Card(i,j+1))
        return deck

    def resetDeck(self):
        for card in self.discardPile:
            self.deck.append(self.discardPile.pop(-1))
    
    def firstDeal(self):
        for i in range(4):
            if len(self.deck) == 0:
                self.resetDeck() # Add cards back so it can draw them
            randNum = randint(0,(len(self.deck)-1))
            if i > 1:
                self.playerHand.append(self.deck.pop(randNum))
            else:
                self.dealerHand.append(self.deck.pop(randNum))
        system('cls')

    def checkHand(self, array):
        if array[0].name == array[1].name and len(array) == 2 and not self.twoHands:
            self.printHand(self.playerHand)
            print("Do you want to split your hand? (Y/N)")
            if inputYesNo():
                self.twoHands = True
                self.playerHand2.append(self.playerHand.pop(1))
            return True
        else:
            if self.checkHandValue(array) > 21:
                system('cls')
                self.printHand(array)
                self.bust(array)
                return True
            return False

    def draw(self, array):
        system('cls')
        while True:
            self.printHand(array)
            print("Would you like to twist(or stick)? (Y/N)")
            if inputYesNo():
                if len(self.deck) == 0:
                    self.resetDeck() # Add cards back so it can draw them
                randNum = randint(0,(len(self.deck)-1))
                array.append(self.deck.pop(randNum))
                if self.checkHand(array):
                    return False
            else:
                return True
            system('cls')

    def dealerDraw(self,array):
        aceValue = 0
        otherAceValue = 0
        value = 0
        tempArray = []
        while True:
            if aceValue == 0 and not len(array) == 5:
                for i in range(len(array)):
                    if array[i].isAce:
                        aceValue = 11
                        otherAceValue = 1
                        tempArray.append(array.pop(i))
                        break

            value = self.checkHandValue(array)
            if (value + aceValue) == 21 and aceValue == 11:
                array.append(tempArray.pop(0))
                print("Dealer got:")
                for card in array:
                    card.rCard()
                return False
            elif aceValue == 11:
                array.append(tempArray.pop(0))
                aceValue = 0
            if value + otherAceValue > 21:
                print("Dealer got:")
                for card in array:
                    card.rCard()
                print("\nDealer bust! You won")
                self.wins +=1
                print("Do you want to play another round? (Y/N)")
                if not inputYesNo():
                    quit()
                else:
                    self.handsToDiscard()
                    return True
            elif len(array) == 5:
                print("Dealer got:")
                for card in array:
                    card.rCard()
                print("\nDealer won with 5 card trick! You lost - unlucky")
                self.losses += 1
                print("Do you want to play another round? (Y/N)")
                if not inputYesNo():
                    quit()
                else:
                    self.handsToDiscard()
                    return True
            elif value + otherAceValue > 16:
                print("Dealer got:")
                for card in array:
                    card.rCard()
                return False
                
            else:
                if len(self.deck) == 0:
                    self.resetDeck() # Add cards back so it can draw them
                randNum = randint(0,(len(self.deck)-1))
                array.append(self.deck.pop(randNum))
        
    def checkWinner(self,handArray,dealArray):
        handAce = 0
        dealScore = 0

        if not len(handArray) > 4:
            for i in range(len(handArray)):
                if handArray[i].isAce:
                    handAce = 11
                    handArray.pop(i)
                    break
        for i in range(len(dealArray)):
           if dealArray[i].isAce:
                if len(dealArray) == 2:
                    dealScore = 21
                break

        if len(handArray) > 4:
            print("\nYou won with 5 card trick!")
            self.wins +=1
            print("Do you want to play another round? (Y/N)")
            if not inputYesNo():
                quit()
            else:
                self.handsToDiscard()
                return True
        elif dealScore == 21:
            if len(dealArray) == 2:
                self.dealBlackJack = " with blackjack"
            return False
        elif self.checkHandValue(handArray) > self.checkHandValue(dealArray):
            print("\nYou beat the dealer's total! You won!")
            self.wins +=1
            print("Do you want to play another round? (Y/N)")
            if not inputYesNo():
                quit()
            else:
                self.handsToDiscard()
                return True
        elif handAce > 0:
            if (handAce + self.checkHandValue(handArray)) > self.checkHandValue(dealArray) or ((handAce + self.checkHandValue(handArray)) == 21 and len(dealArray) > 2):
                if (self.checkHandValue(handArray) + handAce) == 21 and len(handArray) == 1:
                    print("\nYou won with blackjack!")
                else:
                    if handAce + self.checkHandValue(handArray) > 21:
                        if 1 +  self.checkHandValue(handArray) > self.checkHandValue(dealArray):
                            print("\nYou beat the dealer's total! You won!")
                        else:
                            return False
                    else:
                        print("\nYou beat the dealer's total! You won!")
                self.wins +=1
                print("Do you want to play another round? (Y/N)")
                if not inputYesNo():
                    quit()
                else:
                    self.handsToDiscard()
                    return True
            else:
                return False
        else:
            return False

    def handsToDiscard(self):
        for i in range(len(self.dealerHand)):
            self.discardPile.append(self.dealerHand.pop(-1))
        for i in range(len(self.playerHand2)):
            self.discardPile.append(self.playerHand2.pop(-1))
        for i in range(len(self.playerHand)):
            self.discardPile.append(self.playerHand.pop(-1))

    def checkHandValue(self, array):
        total = 0
        for card in array:
            if card.isAce:
                total += card.value[0]
            else:
                total += card.value
        return total

    def bust(self,array):
        print("\nYou went bust!")
        if not self.twoHands or len(self.playerHand) == 0:
            print("You lost! Do you want to play another round? (Y/N)")
            self.losses += 1
            if not inputYesNo():
                quit()
            else:
                self.handsToDiscard()
                return
        else:
            for i in range(len(array)):
                self.discardPile.append(array.pop(-1))
            print("Press enter to continue...")
            input()

        
            
        
            

    def printHand(self, array):
        print("Wins: {}   Losses: {}\n".format(self.wins,self.losses))
        print("The dealer has: ")
        self.dealerHand[0].rCard()
        print("Unknown")
        print("\nYour hand consists of:")
        for card in array:
            card.rCard()

    def printDeck(self):
        for card in self.deck:
            card.rCard()

def start():
    game = Game()
    balance = 100
    losses = 0
    bet = 0
    while True:
        system('cls')
        game.twoHands = False
        game.dealBlackJack = ""
        game.firstDeal()
        
        values = placeBet(balance,game,losses, bet)
        if values[0] == 0:
            break
        bet = values[0]
        balance = values[1]
        losses = game.losses
        
        game.checkHand(game.playerHand)
        playRound(game)

def placeBet(bal,game,losses,oldBet):
    if losses < game.losses:
        bal -= oldBet
    else:
        bal += oldBet

    print("You have £{}".format(str(bal)))
    if bal == 0:
        print("You ran out of money!")
        input("Press X to end game or enter to restart")
        return [0,0]
    else:
        while True:
            try:
                bet = int(input("What is your bet:\n£"))
                if bet > 0 and not bet > bal:
                    break
                else:
                    print("Must have valid bet\n")
            except(ValueError):
                print("You didn't place an integer bet\n")
    return [bet,bal]

def playRound(game): # TOO MANY IFS NOT ENOUGH SLEEP
    if game.twoHands:
        firstNotBust = game.draw(game.playerHand)
        if game.draw(game.playerHand2):
            system('cls')
            if not game.dealerDraw(game.dealerHand): # returns false if dealer won
                if firstNotBust: # if stuck on hand 2 and 1
                    if not game.checkWinner(game.playerHand,game.dealerHand): # returns false if dealer won
                        if not game.checkWinner(game.playerHand2,game.dealerHand):
                            print("\nDealer beat your score{}! You lost".format(game.dealBlackJack))
                            game.losses += 1
                            print("Do you want to play another round? (Y/N)")
                            if not inputYesNo():
                                quit()
                            else:
                                game.handsToDiscard()
                else:
                    if not game.checkWinner(game.playerHand2,game.dealerHand):
                        print("\nDealer beat your score{}! You lost".format(game.dealBlackJack))
                        game.losses += 1
                        print("Do you want to play another round? (Y/N)")
                        if not inputYesNo():
                            quit()
                        else:
                            game.handsToDiscard()
        elif firstNotBust:
            system('cls')
            if not game.dealerDraw(game.dealerHand):
                if not game.checkWinner(game.playerHand,game.dealerHand):
                    print("\nDealer beat your score{}! You lost".format(game.dealBlackJack))
                    game.losses += 1
                    print("Do you want to play another round? (Y/N)")
                    if not inputYesNo():
                        quit()
                    else:
                        game.handsToDiscard()
    else:
        if game.draw(game.playerHand): # returns true if stick
            system('cls')
            if not game.dealerDraw(game.dealerHand):
                if not game.checkWinner(game.playerHand,game.dealerHand):
                    print("\nDealer beat your score{}! You lost".format(game.dealBlackJack))
                    game.losses += 1
                    print("Do you want to play another round? (Y/N)")
                    if not inputYesNo():
                        quit()
                    else:
                        game.handsToDiscard()
    
def inputYesNo():
    while True:
        uInput = input(">> ")
        uInput = uInput.upper()
        if uInput == "Y":
            return True
        elif uInput == "N": 
            return False
        else:
            print("\nPlease enter Y or N")

while True:
    start()
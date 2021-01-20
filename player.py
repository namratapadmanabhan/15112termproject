#This class defines a player. We will use this for both the human and the 
#computer, so that both players have the same functionalities. 

#template for this class taken from
# https://github.com/CodingEZ/Scrabble-AI/blob/master/computerRuleChecker.py

class player():
    def __init__(self):
        self.score = 0
        self.hand = ''
    
    def playFromHand(self, letters):
        for letter in letters:
            letterPosition = self.hand.find(letter)
            self.hand = self.hand[:letterPosition] + self.hand[letterPosition+1:]

    def changeScore(self, add):
        self.score += add

    def addLetters(self, char):
        self.hand += char

#The main purpose of this file is to create our "bag of tiles" like in the 
#actual Scrabble game. We determine how many letters are actually in the bag, 
#and after each time the human player/computer player plays a turn, we add
#the correct number of letters back to their hand, removing them from our bag.

import random
class scrabbleTiles():
    def __init__(self):
        self.scrabbleTiles = []
        charCounts = {'A' : 9, 'B' : 2, 'C' : 2, 'D' : 3, 'E' : 12, 
                    'F' : 2, 'G' : 3, 'H' : 2,
                      'I' : 9, 'J' : 1, 'K' : 1, 
                      'L' : 4, 'M' : 2, 'N' : 6, 
                      'O' : 8, 'P' : 2, 'Q' : 1, 'R' : 6, 'S' : 4, 
                    'T' : 6, 'U' : 3, 'V' : 2, 'W' : 2, 'X' : 1,
                      'Y' : 2, 'Z' : 1}
        for char in charCounts:
            for _ in range(charCounts[char]):
                self.scrabbleTiles.append(char)

    def moveLettersToHand(self, numInHand):
        movedToHand = ''
        if numInHand < len(self.scrabbleTiles):
            for _ in range(numInHand):
                bagLength = len(self.scrabbleTiles)
                randLetter = random.random()
                letterPosition = int(randLetter*bagLength)
                movedToHand += self.scrabbleTiles[letterPosition]
                self.scrabbleTiles.pop(letterPosition)
        else:
            for letter in self.scrabbleTiles:
                movedToHand += letter
            self.scrabbleTiles = []
        return movedToHand
            

import itertools
import computerRuleChecker as CRC
import searchingFunctions

###############################################################################
#A comment about how this file works:
# the first class checks the words that can possibly be made. There is a function 
# which gets all possible letter permutations of all lengths from the computer's
# hand. Another function gets all the possible directions on the board currently
# that are open to having letters placed there.
# Another function goes through all these open spots on the board and tries
# all possible combinations of the letter permutations we got in each position.
# then we check each possible word in our dictionary.
# then there are a few functions which check some things we had also checked for
# the player: the word is valid, the letters are connected on board, they are in 
# a row, etc.
# then we are taking the word which uses the most letters and uses the highest scoring
# letters it can, and placing that word in its position on the board (this is 
# called the final word).
###############################################################################

class aiPlayerCheck():
    def updateHand(self, newLetters):
        self.newLetters = newLetters

    def getWordDirections(self, currBoard, filledCells, connectedToLetters, letters):
        letterPermutations = self.getAllLetterPermutations()
        cellPositions = self.allPossibleLetterPlacements(currBoard, filledCells, connectedToLetters)
        lettersThatPass = []
        for (possibleLetterPositions, possibleCellCombinations) in zip(letterPermutations, cellPositions):
            for position in possibleLetterPositions:
                for cell in possibleCellCombinations[0]:
                    if self.checkCombination(position, cell, currBoard, filledCells, letters, True):
                        lettersThatPass.append([position, cell, self.allPossibleWords])
                for cell in possibleCellCombinations[1]:
                    if self.checkCombination(position, cell, currBoard, filledCells, letters, False):
                        lettersThatPass.append([position, cell, self.allPossibleWords])
        return lettersThatPass

    def getAllLetterPermutations(self):
        newLetters = self.newLetters
        possibleLetterPermutations = []
        numLetters = len(newLetters)
        for numLetters in range(1, numLetters+1):
            possibleWords = list(itertools.permutations(list(newLetters),numLetters))
            possibleLetterPermutations.append(set(possibleWords))
        return possibleLetterPermutations  

    def checkCombination(self, possibleCombination, cellCombination, currBoard, filledCells, letters, possibleWord):
        self.allPossibleWords = CRC.allPossibleWords(cellCombination, filledCells, possibleWord)
        for letterCombination in self.allPossibleWords:
            potentialWord = '' 
            for char in letterCombination:
                if char in cellCombination:
                    potentialWord += possibleCombination[cellCombination.index(char)]
                else:
                    potentialWord += currBoard[char]
            if potentialWord.lower() not in letters:
                return False
        return True

    def allPossibleLetterPlacements(self, currBoard, filledCells, connectedToLetters):
        newLetters = self.newLetters
        cellPositions = []
        numLetters = len(newLetters)
        for numLetters in range(1, numLetters + 1):
            rows = []
            cols = []
            for cell in range(len(currBoard)):
                if cell not in filledCells:
                    row = cell//15
                    col = cell%15 + 1  
                    numCells = 1
                    boardRows = row*15
                    cellCombination = [cell]    
                    while numCells != numLetters:
                        if col != 15:
                            if (boardRows + col) not in filledCells:
                                numCells += 1
                                cellCombination.append(boardRows + col)
                            col += 1
                        else:
                            numCells = numLetters     
                    if len(cellCombination) == numLetters and CRC.checkWordConnected(cellCombination, connectedToLetters):
                        rows.append(cellCombination)
            if numLetters != 1:
                for cell in range(len(currBoard)):
                    if cell not in filledCells:
                        row = cell//15 + 1
                        col = cell%15
                        numCells = 1
                        cellCombination = [cell]
                        while numCells != numLetters:
                            if row != 15:
                                if (row*15 + col) not in filledCells:
                                    numCells += 1
                                    cellCombination.append(row*15 + col)
                                row += 1
                            else:
                                numCells = numLetters
                        if len(cellCombination) == numLetters and CRC.checkWordConnected(cellCombination, connectedToLetters):
                            cols.append(cellCombination)

            cellPositions.append([rows, cols]) 

        return cellPositions

def allPossibleWords(currBoard, filledCells, possibleWord):
    allLetterCombinations = []
    finalWord = determineFinalWord(possibleWord, currBoard[0], filledCells, currBoard)
    if len(allLetterCombinations) != 1: 
        allLetterCombinations.append(finalWord)
    for cell in currBoard:
        anotherCombination = determineOtherWords(possibleWord, cell, filledCells)
        if anotherCombination != []: 
            allLetterCombinations.append(anotherCombination)
    if len(allLetterCombinations) == 0:
        allLetterCombinations.append(finalWord)    
    return allLetterCombinations

def determineFinalWord(possibleWord, cell, filledCells, currBoard):
    boardPositions = [cell]
    currPos = cell
    boardLength = 15
    beginningBoard = 0
    endBoard = 14
    if possibleWord:
        nextCell = currPos + 1
        while ((currPos + 1 in filledCells) or (currPos + 1 in currBoard)) and (currPos % boardLength != endBoard):
            currPos += 1
            boardPositions.append(currPos)
        currPos = cell 
        prevCell = currPos - 1
        while (currPos - 1 in filledCells) and (currPos % boardLength != beginningBoard):
            currPos -= 1
            boardPositions.insert(beginningBoard, currPos)
    else:
        nextRow = currPos + boardLength
        while (currPos + boardLength in filledCells) or (currPos + boardLength in currBoard):
            currPos += boardLength
            boardPositions.append(currPos)
        currPos = cell
        prevRow = currPos - boardLength
        while currPos - boardLength in filledCells:
            currPos -= boardLength
            boardPositions.insert(beginningBoard, currPos)
    return boardPositions

def checkWordConnected(currBoard, connectedToLetters):
    for cell in currBoard:
        if cell in connectedToLetters:
            return True 
        else: return False


def determineOtherWords(possibleWord, cell, filledCells):
    boardPositions = [cell]
    currPos = cell
    boardLength = 15
    beginningBoard = 0
    endBoard = 14
    if possibleWord:
        while (currPos + boardLength) in filledCells:
            currPos += boardLength
            boardPositions.append(currPos)
        currPos = cell
        while (currPos - boardLength) in filledCells:
            currPos -= boardLength
            boardPositions.insert(beginningBoard, currPos)
    else:
        while ((currPos + 1) in filledCells) and (currPos % boardLength != endBoard):
            currPos += 1
            boardPositions.append(currPos)
        currPos = cell
        while ((currPos - 1) in filledCells) and (currPos % boardLength != beginningBoard):
            currPos -= 1
            boardPositions.insert(beginningBoard, currPos)
    if boardPositions == [cell]:
        return []
    return boardPositions


        

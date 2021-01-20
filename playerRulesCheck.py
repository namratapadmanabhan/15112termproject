#The main purpose of this file and the classes within it is to check each move
#made by the person player with the Scrabble rules. For example, we make sure
#after each move, that the letters are in either the same row or column, that
#they are attached to each other, and that the letters 
# actually make a word when put together.

import itertools
import searchingFunctions
import string

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

class playerRulesCheck():
    def __init__(self):
        text = open('scrabbleDictionary.txt', 'r')
        finalDoc = text.read().lower()
        self.dictionary = set(finalDoc.split('\n'))

    def mkAlphabet(self, chars):       
        allLetters = {'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0,
                       'E' : 0, 'F' : 0, 'G' : 0, 'H' : 0,
                       'I' : 0, 'J' : 0, 'K' : 0, 'L' : 0,
                       'M' : 0, 'N' : 0, 'O' : 0, 'P' : 0,
                       'Q' : 0, 'R' : 0, 'S' : 0, 'T' : 0,
                       'U' : 0, 'V' : 0, 'W' : 0, 'X' : 0,
                       'Y' : 0, 'Z' : 0, '$' : 0}
        for letter in chars:
            if letter in """1234567890!@#$%^&*()[]{}:;"'<>,.?/|~`\\ """:
                return 'Error: not in alphabet'
            else:
                allLetters[letter] += 1
        return allLetters

    def letterCombinationWorks(self, letters, allCells, currBoard, filledCells, charsDict, letterCombinations):
        for combination in letterCombinations:
            potentialCombination = ''
            for cell in combination:
                if cell in allCells:
                    potentialCombination += letters[allCells.index(cell)]
                else:
                    potentialCombination += currBoard[cell]
            if potentialCombination.lower() not in charsDict:
                printStatement = 'That is not a word!'
                return (False, printStatement)
        return (True, '')

    def updateHand(self, newLetters):
        self.newLetters = newLetters

    def checkFinalCombination(self, newLetters, allCells, currBoard, filledCells, connected, letters):
        if self.checkLetterCount(newLetters):
            printStatement = 'All letters are in hand.'
            if checkIfFilled(allCells, filledCells):
                printStatement = 'Spaces chosen are empty!'
                verifyLine = lineConnected(allCells, filledCells, connected)
                if verifyLine[0]:
                    printStatement = 'Letters are connected.'
                    if connectedToLetters(allCells, filledCells, connected)[0]:
                        printStatement = 'Letters all attached to board!'
                        permutations = getAllLetterPermutations(allCells, filledCells, verifyLine[1])
                        combinationWorks = self.letterCombinationWorks(newLetters, allCells, currBoard, filledCells, letters, permutations)
                        if combinationWorks[0]:
                            printStatement = 'Your word follows all the rules!'
                            return (True, permutations, printStatement)
                        else:
                            printStatement = combinationWorks[1]
                    else:
                        printStatement = 'Letters are not attached to the board!'
                else:
                    printStatement = verifyLine[1]
            else:
                printStatement = 'That space is occupied. Try again!'
        else:
            printStatement = 'Your hand does not have those letters. Try again!'

        return (False, [], printStatement)

    def checkLetterCount(self, givenWord):
        if '$' in givenWord:
            return False
        alphaLetter = self.mkAlphabet(self.newLetters)
        alphaWord = self.mkAlphabet(givenWord)
        for char in alphaLetter:
            if alphaWord[char] > alphaLetter[char]: return False
            else: return True
###############################################################################

def checkIfFilled(currBoard, filled):
    for cell in currBoard:
        if cell in filled:
            return False
        else: return True

def checkCurrRow(currBoard):
    length = len(currBoard)
    row = currBoard[0]//15
    for cell in range(length):
        currCell = currBoard[cell]
        if row != currCell//15:
            return (False, 0)
    return (True, row)

def checkCurrCol(currBoard):
    col = currBoard[0]%15
    length = len(currBoard)
    for cell in range(1, length):
        currCell = currBoard[cell]
        if col != currCell%15:
            return (False, 0)
    return (True, col)

def horizLetters(cell, filledCells):
    col = cell % 15
    if col != 0:
        if (cell - 1) in filledCells:
            return True
    if col != 14:
        if (cell + 1) in filledCells:
            return True
    else: return False

def vertLetters(cell, filledCells):
    row = cell//15
    if row != 0:
        if (cell - 15) in filledCells:
            return True
    if row != 14:
        if (cell + 15) in filledCells:
            return True
    return False

def lineConnected(currBoard, filledCells, connectedToLetters):    
    if len(currBoard) == 0:
        return (False, 'These are not letters!')
    verifyRow = checkCurrRow(currBoard)
    verifyCol = checkCurrCol(currBoard)
    if verifyRow[0]:
        cols = []   
        row = currBoard[0]//15
        for cell in currBoard:
            cols.append(cell % 15)
        currCol = 0
        while currCol != len(cols)-1:
            numOfCurrCol = cols[currCol]
            if (((row*15 + numOfCurrCol + 1) in filledCells) and (currCol != 14)):
                cols = cols[:currCol+1] + [numOfCurrCol + 1] + cols[currCol+1:]
            if numOfCurrCol + 1 != cols[currCol+1]:
                return (False, 'Not consecutive columns')
            currCol += 1
        return (True, True)    
    elif verifyCol[0]:
        rows = []
        col = currBoard[0]%15
        for cell in currBoard:
            rows.append(cell//15)
        currRow = 0
        while currRow != len(rows)-1:
            numOfCurrRow = rows[currRow]
            if (((numOfCurrRow*15 + col + 15) in filledCells) and (currRow != 14)):
                rows = rows[:currRow+1] + [numOfCurrRow + 1] + rows[currRow+1:]
            if numOfCurrRow + 1 != rows[currRow+1]:
                return (False, 'Rows not consecutive')
            currRow += 1
        return (True, False)
        
    else:
        return (False, 'Place the letters in the same line!')
    
def connectedToLetters(currBoard, filledCells, connected):
    wordIsConnected = lineConnected(currBoard, filledCells, connected)[1]
    for cell in currBoard:
        if cell in connected:
            return (True, wordIsConnected) 
    return (False, 'Please connect your letters to current letters on board!')

def getFinalWord(isConnectedToLetters, filledCells, currBoard):
    cell = currBoard[0]
    boardPositions = [cell]
    currPos = cell
    if isConnectedToLetters:
        newPos = currPos + 1
        while (((currPos + 1) in filledCells) or ((currPos + 1) in currBoard)) and (currPos%15 != 14):
            currPos += 1
            boardPositions.append(currPos)
        currPos = cell  
        prevPos = currPos - 1 
        while (((currPos - 1) in filledCells) or ((currPos - 1) in currBoard)) and (currPos%15 != 0):
            currPos -= 1
            boardPositions.append(currPos)
    else:
        nextRow = currPos + 15
        while ((currPos + 15) in filledCells) or ((currPos + 15) in currBoard):
            currPos += 15
            boardPositions.append(currPos)
        currPos = cell  
        prevRow = currPos - 15
        while ((currPos - 15) in filledCells) or ((currPos - 15) in currBoard):
            currPos -= 15
            boardPositions.append(currPos)
    return sorted(boardPositions)

def determineOtherWords(isConnectedToLetters, cell, filledCells):
    boardPositions = [cell]
    currPos = cell
    if isConnectedToLetters:
        newRow = currPos + 15
        while (currPos + 15) in filledCells:
            currPos += 15
            boardPositions.append(currPos)
        currPos = cell
        prevRow = currPos - 15
        while (currPos - 15) in filledCells:
            currPos -= 15
            boardPositions.append(currPos)
    else:
        newCell = currPos + 1
        while ((currPos + 1) in filledCells) and (currPos%15 != 14):
            currPos += 1
            boardPositions.append(currPos)
        currPos = cell
        prevCell = currPos - 1
        while ((currPos - 1) in filledCells) and (currPos%15 != 0):
            currPos -= 1
            boardPositions.append(currPos)
    return sorted(boardPositions)

def getAllLetterPermutations(currBoard, filledCells, isConnectedToLetters):
    currPermutationsList = []
    finalWord = getFinalWord(isConnectedToLetters, filledCells, currBoard)
    if len(finalWord) != 1:
        currPermutationsList.append(finalWord)
    for cell in currBoard:
        if (isConnectedToLetters) and (vertLetters(cell, filledCells)):
            currPermutationsList.append(determineOtherWords(isConnectedToLetters, cell, filledCells))
        if (not isConnectedToLetters) and (horizLetters(cell, filledCells)):
            currPermutationsList.append(determineOtherWords(isConnectedToLetters, cell, filledCells))
    if len(currPermutationsList) == 0:
        currPermutationsList.append(finalWord)  
    return currPermutationsList 

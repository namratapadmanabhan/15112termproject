#The main purpose of this file is to check the rules for the AI player based
#on the rules of Scrabble. This is very similar to the file which checks rules
#for the human player, and many of the functions are almost identical. We just
#have to do a few checks that the computer is playing the optimal word that it can.

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

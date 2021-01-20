#The main purpose of this file is to run all the other files in the program.
#Instances of all classes in the other files are created, as well as wrapper
#functions which allow the key, mouse, and redraw functions from other classes
#to run.

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import scrabbleInformation as dataImport
import aiPlayerCheck as checkAI
import playerRulesCheck as playerCheck
import player as player
import scoreCalculations as scoreCalc
import createBoard as board
import scrabbleTiles as tiles
import searchingFunctions

#Some references/small portions of functions in these files
# are from the following link:
# https://github.com/CodingEZ/Scrabble-AI/blob/master/computerRuleChecker.py

createBoard = board.createBoard()
personPlayer = player.player()
aiPlayer = player.player()
humanCheck = playerCheck.playerRulesCheck()
checkAI = checkAI.aiPlayerCheck()
scrabbleTiles = tiles.scrabbleTiles()

#the dictionary, 'scrabbleDictionary.txt' was taken from 
# https://github.com/CodingEZ/Scrabble-AI/blob/master/computerRuleChecker.py
doc = open('scrabbleDictionary.txt', 'r')
document = doc.read().lower()
dictionary = set(document.split('\n'))
doc.close()

#the template for this function was taken from the following website
#belonging to the 112 course:
# http://www.krivers.net/15112-s19/notes/notes-animations-part2.html
def run(width=1000, height=600):  
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height, fill='white', width=0)
        scrabbleInfo.redrawAll(canvas)
        canvas.update()

    def keyPressedWrapper(event, canvas, data):
        scrabbleInfo.keyPressed(event, data)
        redrawAllWrapper(canvas, data)  

    def mousePressedWrapper(event, canvas, data):
        if scrabbleInfo.data.gameOver:
            if personPlayer.score > aiPlayer.score:
                scrabbleInfo.data.printStatement = 'You win!'
            elif personPlayer.score < aiPlayer.score:
                scrabbleInfo.data.printStatement = 'Computer wins :('
            else:
                scrabbleInfo.data.printStatement = "It's a tie!"
        elif scrabbleInfo.data.computerTurn:
            negVal = -1
            redrawAllWrapper(canvas, data)
            canvas.create_rectangle(100, 100, 150, 150, outline = "gold", width = 30)

            connectedToLetters = set(createBoard.findNewStartingPositions())
            filledCells = set(createBoard.findFilledCells())
            checkAI.updateHand(aiPlayer.hand)
            checkAI.getAllLetterPermutations()
            possibleCombinations = checkAI.getWordDirections(createBoard.board, filledCells, connectedToLetters, dictionary)
            bestCombination = scoreCalc.bestPossibleWord(possibleCombinations, createBoard.board)
            if bestCombination[0] != negVal:
                scrabbleInfo.resetExtraTiles(scoreCalc.tripleWord, scoreCalc.doubleWord, scoreCalc.doubleLetter, scoreCalc.tripleLetter)
                createBoard.update(bestCombination[1], bestCombination[2])
                scrabbleInfo.computerResetBoard(createBoard.board, bestCombination[1], bestCombination[2])
                aiPlayer.changeScore(bestCombination[0])
                scrabbleInfo.changeScore(aiPlayer.score, False)
                aiPlayer.playFromHand(bestCombination[1])
                lettersToHand = scrabbleTiles.moveLettersToHand(len(bestCombination[1]))
                scrabbleInfo.changeLetterBagSize(len(scrabbleTiles.scrabbleTiles))
                aiPlayer.addLetters(lettersToHand)
                data.printStatement1 = "Score: " + str(bestCombination[0]) + ", Letters used: " + str(bestCombination[1])
            else:
                scrabbleInfo.data.printStatement1 = "Computer can't play a word!"
            scrabbleInfo.data.computerTurn = False
            scrabbleInfo.data.humanTurn = False
            if len(aiPlayer.hand) == 0:
                scrabbleInfo.data.gameOver == True 
        elif scrabbleInfo.data.humanTurn:
            filledCells = set(createBoard.findFilledCells())
            connectedToLetters = set(createBoard.findNewStartingPositions())
            scrabbleInfo.mousePressed(event)
            if scrabbleInfo.data.canSearch:
                scrabbleInfo.data.canSearch = False
                element = Entry()
                element.pack()
                element.delete(0, END)
                element.insert(0, " ")
            elif scrabbleInfo.data.canSwitchTurns:
                scrabbleInfo.data.canSwitchTurns = False
                scrabbleInfo.tempLettersBack()         
            elif scrabbleInfo.data.canPassOnTurn:
                scrabbleInfo.data.canPassOnTurn = False
                scrabbleInfo.tempLettersBack()
                scrabbleInfo.data.humanTurn = False
                scrabbleInfo.data.computerTurn = True  
            elif scrabbleInfo.data.doTurn:
                scrabbleInfo.data.doTurn = False
                humanCheck.updateHand(personPlayer.hand)
                cellLocations = sorted(scrabbleInfo.data.tempCells)
                alphas = []
                charsDict = {}
                for (location, character) in zip(scrabbleInfo.data.tempCells, scrabbleInfo.data.tempLetters):
                    charsDict[location] = character
                for cell in cellLocations:
                    alphas.append(charsDict[cell])
                if len(alphas) != len(cellLocations):
                    cellLocations = []
                    alphas = []
                elif not searchingFunctions.isPossibleChar(alphas):
                    alphas = ['$']
                elif not searchingFunctions.canPlaceInCell(cellLocations):
                    cellLocations = []
                else:
                    cellPlaces = []
                    for cell in cellLocations:
                        cellPlaces.append(int(cell))
                    cellLocations = cellPlaces
                finalCombinations = humanCheck.checkFinalCombination(alphas, cellLocations, createBoard.board, filledCells, connectedToLetters, dictionary)
                scrabbleInfo.data.printStatement1 += finalCombinations[2]
                if finalCombinations[0]:
                    possibleCombinations = [[alphas, cellLocations, finalCombinations[1]]]
                    bestCombination = scoreCalc.bestPossibleWord(possibleCombinations, createBoard.board)
                    scrabbleInfo.resetExtraTiles(scoreCalc.tripleWord, scoreCalc.doubleWord, scoreCalc.doubleLetter, scoreCalc.tripleLetter)
                    score = bestCombination[0]
                    playedHand = bestCombination[1]
                    combos = bestCombination[2]
                    scrabbleInfo.data.printStatement3 = "Click anywhere to start the computer's turn."
                    createBoard.update(playedHand, combos)
                    personPlayer.changeScore(score)
                    scrabbleInfo.changeScore(personPlayer.score, True)
                    personPlayer.playFromHand(playedHand)
                    lettersToHand = scrabbleTiles.moveLettersToHand(len(playedHand))
                    personPlayer.addLetters(lettersToHand)
                    scrabbleInfo.updateHand(personPlayer.hand)
                    scrabbleInfo.changeLetterBagSize(len(scrabbleTiles.scrabbleTiles))
                    scrabbleInfo.alphaReset(personPlayer.hand)
                    scrabbleInfo.newPlayerBoard(createBoard.board)
                    scrabbleInfo.resetData()
                    scrabbleInfo.data.humanTurn = False
                    scrabbleInfo.data.computerTurn = True
                    if len(personPlayer.hand) == 0:
                        scrabbleInfo.data.gameOver == True
                else:
                    scrabbleInfo.data.printStatement2 = "Invalid move! Click a tile or button!"

        else:
            scrabbleInfo.data.printStatement1 = "Your turn!"
            scrabbleInfo.data.humanTurn = True
            scrabbleInfo.data.computerTurn = False

        redrawAllWrapper(canvas, data)

# the template for this function comes from
# http://www.krivers.net/15112-s19/notes/notes-animations-part2.html
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.gameOver = False
    scrabbleInfo = dataImport.scrabbleInformation(data)
    scrabbleInfo.resetExtraTiles(scoreCalc.tripleWord, scoreCalc.doubleWord, scoreCalc.doubleLetter, scoreCalc.tripleLetter)
    
    lettersToHand = scrabbleTiles.moveLettersToHand(7)
    personPlayer.addLetters(lettersToHand)
    
    scrabbleInfo.data.letterHand = personPlayer.hand
    lettersToHand = scrabbleTiles.moveLettersToHand(7)
    
    aiPlayer.addLetters(lettersToHand)
    scrabbleInfo.changeLetterBagSize(len(scrabbleTiles.scrabbleTiles))
    
    root = Tk()
    frame = Frame(root)
    canvas = Canvas(root, width=scrabbleInfo.data.width, height=scrabbleInfo.data.height)
    canvas.pack()
    redrawAllWrapper(canvas, scrabbleInfo.data)
    root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas, scrabbleInfo.data))
    root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, scrabbleInfo.data))
    while not scrabbleInfo.data.gameOver:
        root.mainloop()
    print("it's the end!")

run(1000, 600)

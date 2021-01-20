#This file encompasses many purposes. First, there are the main draw functions
#which draw each of the modes in the game, and much of the UI. This is also where
#there are functions to control and check when we have clicked and placed a piece
#from the hand to the board, vice versa, switching the order of tiles around, etc.
#Finally, this file also keeps track of all the buttons, etc and checks pressing
#in different areas of the screen.

#Some references/small portions of functions in this file
# are from the following link:
# https://github.com/CodingEZ/Scrabble-AI/blob/master/computerRuleChecker.py

from tkinter import messagebox
import time
from tkinter import *
import playerRulesCheck as playerCheck
humanCheck = playerCheck.playerRulesCheck()

class scrabbleInformation():
    def __init__(self, data):
        self.data = data
        self.data.highlightedCells = []
        self.data.scoreBoosterCells = []
        self.data.infoMid = 750
        self.data.squareLeft = 140
        self.data.squareTop = 60
        self.data.canSearch = False
        self.data.doTurn = False
        self.data.backgroundFill = "PaleVioletRed1"
        self.data.instructionFill = "DarkSlateGray3"
        self.data.emptySquareFill = "floral white"
        self.data.tripleWordFill = "orange"
        self.data.doubleWordFill = "pink"
        self.data.doubleLetterFill = "deep sky blue"
        self.data.tripleLetterFill = "RoyalBlue1"
        self.data.occupiedSquareFill = "DeepPink2"
        self.data.handSquareFill = "orange3"
        self.data.centerSquareFill = "dark green"
        self.data.highlightFill = "yellow"
        self.data.squareSize = 32
        self.data.letterHand = 'abcdefg'
        self.data.unoccupiedHandPositions = []
        self.data.playerScore = 0
        self.data.computerScore = 0
        self.data.tripleWord = []
        self.data.doubleWord = []
        self.data.invalidTurn = True
        self.data.searchIsPossible = False
        self.data.timerDelay = 50
        self.data.handSquareSize = 40
        self.data.blankBoard = []
        self.data.board = ''
        for i in range(225):
            self.data.blankBoard.append(i)  
            self.data.board += '-'   
        self.data.filledBoardLocations = []
        self.data.filledBoardLetters = []
        self.data.numLettersInBag = 0
        self.data.humanTurn = False
        self.data.computerTurn = False
        self.data.canPassOnTurn = False
        self.data.canPlayPersonTurn = False
        self.data.canSwitchTurns = False
        self.data.tempCells = []
        self.data.tempLetters = []
        self.data.printStatement1 = 'Welcome to Scrabble!'
        self.data.printStatement2 = 'Click anywhere to start.'
        self.data.printStatement3 = ''
        self.data.doubleLetter = []
        self.data.tripleLetter = []
        self.data.filledHandSpots = [0, 1, 2, 3, 4, 5, 6]
        self.data.readyHandToBoard = False
        self.data.readyBoardToHand = False
        self.data.beginningClick = -1
        self.data.beginningClickLetter = '_'
        self.data.mode = "splashscreen"

    def keyPressed(self, event, data):
        if event.keysym == "m":
            self.data.mode = "game2screen"
        elif event.keysym == "h":
            self.data.mode = "helpscreen"
        else:
            self.data.mode = "gamescreen"

    def updateHand(self, letterHand):
        self.data.letterHand = letterHand

    def changeLetterBagSize(self, numLettersInBag):
        self.data.numLettersInBag = numLettersInBag

    def newPlayerBoard(self, board):
        allCells = len(self.data.tempCells)
        for cell in range(allCells):
            self.data.filledBoardLocations.append(self.data.tempCells[cell])
            self.data.filledBoardLetters.append(self.data.tempLetters[cell])
        self.data.tempCells = []
        self.data.tempLetters = []

    def alphaReset(self, letterHand):
        self.data.filledHandSpots = []
        numLetters = len(letterHand)
        for letter in range(numLetters):
            self.data.filledHandSpots.append(letter)
        self.data.unoccupiedHandPositions = []

    def computerResetBoard(self, board, chars, cells):
        self.data.board = board
        for (alpha, cell) in zip(chars, cells):
            self.data.blankBoard.remove(cell)
            self.data.filledBoardLocations.append(cell)
            self.data.filledBoardLetters.append(alpha)

    def resetData(self):
        self.data.readyHandToBoard = False
        self.data.readyBoardToHand = False
        self.data.beginningClick = -1
        self.data.beginningClickLetter = '_'
        self.data.invalidTurn = True

    def handToBoardTemp(self, cell):     
        colOfTile = self.data.beginningClick
        numCell = self.data.tempCells.index(cell)
        letterCopy = self.data.letterHand[colOfTile]
        self.data.tempLetters = self.data.tempLetters[:numCell] + [letterCopy] + self.data.tempLetters[numCell+1:]
        self.data.letterHand = self.data.letterHand[:colOfTile] + self.data.board[cell] + self.data.letterHand[colOfTile+1:]
        self.data.board = self.data.board[:cell] + letterCopy + self.data.board[cell+1:]

    def handToBoardEmpty(self, spot):
        colOfTile = self.data.beginningClick
        newLetters = self.data.letterHand[colOfTile]
        self.data.letterHand = self.data.letterHand[:colOfTile] + self.data.board[spot] + self.data.letterHand[colOfTile+1:]
        self.data.board = self.data.board[:spot] + newLetters + self.data.board[spot+1:]
        self.data.blankBoard.remove(spot)    
        self.data.tempCells.append(spot)
        self.data.tempLetters.append(self.data.board[spot])
        self.data.filledHandSpots.remove(colOfTile)      
        self.data.unoccupiedHandPositions.append(colOfTile)
        self.data.highlightedCells.remove(colOfTile) 

    def resetExtraTiles(self, tripWord, dubWord, dubLetter, tripLetter):
        self.data.tripleWord = tripWord
        self.data.doubleWord = dubWord
        self.data.doubleLetter = dubLetter
        self.data.tripleLetter = tripLetter    

    def handToHandFilled(self, colOfTile):       
        col1 = self.data.beginningClick
        col2 = colOfTile
        char1 = self.data.letterHand[col1]
        char2 = self.data.letterHand[col2]
        self.data.letterHand = self.data.letterHand[:col1] + char2 + self.data.letterHand[col1+1:]
        self.data.letterHand = self.data.letterHand[:col2] + char1 + self.data.letterHand[col2+1:]

    def boardToHandFilled(self, currTileCol):     
        cell = self.data.beginningClick
        numCell = self.data.tempCells.index(cell)
        newLetter = self.data.letterHand[currTileCol]
        self.data.tempLetters = self.data.tempLetters[:numCell] + [newLetter] + self.data.tempLetters[numCell+1:]
        self.data.letterHand = self.data.letterHand[:currTileCol] + self.data.board[cell] + self.data.letterHand[currTileCol+1:]
        self.data.board = self.data.board[:cell] + newLetter + self.data.board[cell+1:]

    def boardToHandEmpty(self, currTileCol):    
        cell = self.data.beginningClick
        numCell = self.data.tempCells.index(cell)   
        self.data.tempCells.pop(numCell)       
        self.data.tempLetters.pop(numCell)
        self.data.blankBoard.append(cell)
        self.data.filledHandSpots.append(currTileCol)     
        self.data.unoccupiedHandPositions.remove(currTileCol)       
        newLetter = self.data.letterHand[currTileCol]
        self.data.letterHand = self.data.letterHand[:currTileCol] + self.data.board[cell] + self.data.letterHand[currTileCol+1:]
        self.data.board = self.data.board[:cell] + newLetter + self.data.board[cell+1:]

    def handToHandEmpty(self, currTileCol):     
        col1 = self.data.beginningClick
        col2 = currTileCol
        char1 = self.data.letterHand[col1]
        char2 = self.data.letterHand[col2]
        self.data.letterHand = self.data.letterHand[:col1] + char2 + self.data.letterHand[col1+1:]
        self.data.letterHand = self.data.letterHand[:col2] + char1 + self.data.letterHand[col2+1:]
        self.data.filledHandSpots.remove(col1)
        self.data.unoccupiedHandPositions.remove(col2)
        self.data.filledHandSpots.append(col2)
        self.data.unoccupiedHandPositions.append(col1)

    def boardToBoardTemp(self, spot):    
        cell1 = self.data.beginningClick
        cell2 = spot
        char1 = self.data.board[cell1]
        char2 = self.data.board[cell2]
        self.data.board = self.data.board[:cell1] + char2 + self.data.board[cell1+1:]
        self.data.board = self.data.board[:cell2] + char1 + self.data.board[cell2+1:]
        numCell1 = self.data.tempCells.index(cell1)
        numCell2 = self.data.tempCells.index(cell2)
        self.data.tempCells[numCell1] = cell2
        self.data.tempCells[numCell2] = cell1

    def drawCell(self, canvas, row, col, char, fill):
        data = self.data
        midHeight = col + 0.5
        midWidth = row + 0.5
        canvas.create_rectangle(data.squareLeft + col*data.squareSize,
                    data.squareTop + row*data.squareSize,
                    data.squareLeft + col*data.squareSize + data.squareSize,
                    data.squareTop + row*data.squareSize + data.squareSize,
                    fill=fill)
        canvas.create_text(data.squareLeft + (midHeight)*data.squareSize,
                    data.squareTop + (midWidth)*data.squareSize,
                    text=char, font="Arial 10")

    def changeScore(self, score, forPlayer):
        if forPlayer:
            self.data.playerScore = score
        else:
            self.data.computerScore = score

    def boardToBoardEmpty(self, cell):    
        cell1 = self.data.beginningClick
        cell2 = cell
        char1 = self.data.board[cell1]
        char2 = self.data.board[cell2]
        self.data.board = self.data.board[:cell1] + char2 + self.data.board[cell1+1:]
        self.data.board = self.data.board[:cell2] + char1 + self.data.board[cell2+1:]
        numCell1 = self.data.tempCells.index(cell1)
        numCell2 = self.data.blankBoard.index(cell2)
        self.data.tempCells[numCell1] = cell2
        self.data.blankBoard[numCell2] = cell1

    def tempLettersBack(self):
        for char in self.data.tempLetters:
            self.data.letterHand += char
        numLetters = len(self.data.letterHand)
        for i in range(numLetters-1, 0, -1):
            if self.data.letterHand[i] == '-':
                self.data.letterHand = self.data.letterHand[:i] + self.data.letterHand[i+1:]
        self.data.blankBoard += self.data.tempCells
        for cell in self.data.tempCells:
            self.data.board = self.data.board[:cell] + '-' + self.data.board[cell+1:]
        numLetters = len(self.data.tempCells)+len(self.data.filledHandSpots)
        self.data.filledHandSpots = []
        for letter in range(numLetters):
            self.data.filledHandSpots.append(letter)
        self.data.tempCells = []
        self.data.tempLetters = []

    def handPress1(self, colOfTile):
        self.data.highlightedCells.append(colOfTile)
        self.data.readyHandToBoard = True
        self.data.beginningClick = colOfTile

    def boardPress1(self, cell):
        self.data.readyBoardToHand = True
        self.data.beginningClick = cell

    def redrawAll(self, canvas):
        #splashscreen mode
        if self.data.mode == "splashscreen":
            height1 = 325
            height2 = 400
            height3 = 475
            canvas.create_text(500, 250, text = "Welcome to Millennial Scrabble!", font = "Helvetica 50 bold")
            canvas.create_text(500, 320, text = "The only game of Scrabble with all your favorite slang words", font = "Helvetica 30 ")
            canvas.create_rectangle(180, 450, 420, 500, fill = "green3", outline = "green4")
            canvas.create_text(300, 475, text = "Instructions")
            canvas.create_rectangle(580, 450, 820, 500, fill = "orange red", outline = "firebrick3")
            canvas.create_text(700, 475, text = "Start Game")

        #help mode
        elif self.data.mode == "helpscreen":
            canvas.create_text(500, 50, text = "Instructions", font = "Helvetica 30 bold")
            font = 'Arial 19 bold'
            canvas.create_text(500, 100, 
                        text="Press the green button labeled 'Your Turn' to begin", font=font)
            canvas.create_text(500, 150, 
                        text='Click any letter in your hand, and then the space you want to place it in.', font=font)
            canvas.create_text(500, 200, 
                text="Make sure to start in the center square!", font=font)
            canvas.create_text(500, 250, 
            text='When your word has been made, play your turn.', font=font)
            canvas.create_text(500, 300, 
            text="Click to start the computer's turn whenever you're ready.",font=font)
            canvas.create_text(500, 350, 
            text='Press any key to get back to the game.', font=font)
            canvas.create_text(500, 400, 
            text="You'll automatically start off in regular mode, but", font=font)
            canvas.create_text(500, 450, 
            text="press 'm' at any time to change to slang mode, and any key to go back", font=font)
            canvas.create_text(500, 500, 
            text='Enjoy!', font=font)

        #game mode
        elif self.data.mode == "gamescreen":
            data = self.data
            spotList = []  
            buttonH1 = 400
            buttonH2 = 430 
            level1 = 408
            level2 = 420
            for i in range(225):
                spotList.append(i)
            for (letter, cell) in zip(data.board, spotList):
                row = cell//15
                column = cell%15
                letter = data.board[cell]
                cellSize = int(len(data.board)//15)
                if cell in data.blankBoard:
                    if cell in data.tripleWord:
                        self.drawCell(canvas, row, column, letter, data.tripleWordFill)
                    elif row == 7 and column == 7:
                        self.drawCell(canvas, row, column, letter, "DeepPink2")
                    elif cell in data.doubleWord:
                        self.drawCell(canvas, row, column, letter, data.doubleWordFill)
                    elif cell in data.doubleLetter:
                        self.drawCell(canvas, row, column, letter, data.doubleLetterFill)
                    elif cell in data.tripleLetter:
                        self.drawCell(canvas, row, column, letter, data.tripleLetterFill)
                    else:
                        self.drawCell(canvas, row, column, letter, data.emptySquareFill)
                elif cell in data.tempCells:
                    self.drawCell(canvas, row, column, letter, "orange3")
                else:
                    self.drawCell(canvas, row, column, letter, data.occupiedSquareFill)
            canvas.create_text(data.infoMid-60, 325, text="Your Hand", font="Arial 14")

            indexList = []
            for i in range(len(data.letterHand)):
                indexList.append(i)
                    
            for (letter, boardCol) in zip(data.letterHand, indexList):
                if letter == '-':
                    canvas.create_rectangle(data.infoMid-115 + data.squareSize *boardCol,
                                            360,
                                            data.infoMid-115 + data.squareSize *boardCol + data.squareSize ,
                                            360 + data.squareSize ,
                                            fill="floral white")
                else:
                    if boardCol in data.highlightedCells:
                        canvas.create_rectangle(data.infoMid-115 + data.squareSize *boardCol,
                                            360,
                                            data.infoMid-115 + data.squareSize *boardCol + data.squareSize ,
                                            360 + data.squareSize,
                                            fill="yellow")
                    else:
                        canvas.create_rectangle(data.infoMid-115 + data.squareSize *boardCol,
                                                360,
                                                data.infoMid-115 + data.squareSize *boardCol + data.squareSize ,
                                                360 + data.squareSize,
                                                fill="orange3")
                canvas.create_text(data.infoMid-115 + data.squareSize *(boardCol+0.5),
                                        360 + data.squareSize/2,
                                        text=letter,
                                        font="Arial 10")
            canvas.create_rectangle(650, buttonH1, 700, buttonH2, fill="antique white")
            canvas.create_rectangle(700, buttonH1, 750, buttonH2, fill="VioletRed1")
            canvas.create_rectangle(750, buttonH1, 800, buttonH2, fill="antique white")
            canvas.create_rectangle(800, buttonH1, 850, buttonH2, fill="antique white")
            canvas.create_text(675, level1, text="Skip", font="Arial 10")
            canvas.create_text(675, level2, text="Turn", font="Arial 10")
            canvas.create_text(725, level1, text="Play", font="Arial 10")
            canvas.create_text(725, level2, text="Turn", font="Arial 10")
            canvas.create_text(775, level1, text="Swap", font="Arial 10")
            canvas.create_text(775, level2, text="Tiles", font="Arial 10")
            canvas.create_text(825, level1, text="Check", font="Arial 10")
            canvas.create_text(825, level2, text="Word", font="Arial 10")
            canvas.create_rectangle(data.infoMid-100, 280, data.infoMid+100, 330, fill="gold")
            canvas.create_text(data.infoMid, 290, text=("Scores"), font="Arial 20")
            canvas.create_text(data.infoMid, 315, text=("You: " + str(data.playerScore) + "      Computer: " + str(data.computerScore)), font="Arial 15")
            canvas.create_rectangle(data.infoMid-100, 100, data.infoMid+100, 150, fill="SpringGreen4")
            canvas.create_text(data.infoMid, 123, text= "Start Your Turn", font="Arial 20")
            canvas.create_rectangle(data.infoMid-100, 190, data.infoMid+100, 240, fill="PeachPuff3")
            canvas.create_text(data.infoMid, 213, text="Start Computer Turn", font="Arial 16")

            canvas.create_text(500, 30, text="Scrabble: Normal Mode", font="Helvetica 30")
            canvas.create_text(70, 220, text="Board Key:", font="Arial 16 bold")
            canvas.create_text(70, 240, text="Orange: Triple Word")
            canvas.create_text(70, 260, text="Pink: Double Word")
            canvas.create_text(70, 280, text="Blue: Triple Letter")
            canvas.create_text(70, 300, text="Cyan: Double Letter")
            canvas.create_text(data.infoMid + 180, 220, text="Letter Values:", font="Arial 16 bold")
            canvas.create_text(data.infoMid + 180, 245, text="A: 1, B: 3, C: 3", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 270, text="D: 2, E: 1, F: 4", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 295, text="G: 2, H: 4, I: 1", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 320, text="J: 8, K: 5, L: 1", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 345, text="M: 3, N: 1, O: 1", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 370, text="P: 3, Q: 10, R: 1", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 395, text="S: 1, T: 1, U: 4", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 420, text="V: 4, W: 4, X: 8", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 445, text="Y: 4, Z: 10", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 470, text="Blank: 0", font="Arial 16")
########################################################################################################           
        elif self.data.mode == "game2screen":
            data = self.data
            spotList = []   
            for i in range(225):
                spotList.append(i)
            for (letter, cell) in zip(data.board, spotList):
                row = cell//15
                column = cell%15
                letter = data.board[cell]
                cellSize = int(len(data.board)//15)
                if cell in data.blankBoard:
                    if cell in data.tripleWord:
                        self.drawCell(canvas, row, column, letter, data.tripleWordFill)
                    elif row == 7 and column == 7:
                        self.drawCell(canvas, row, column, letter, "DeepPink2")
                    elif cell in data.doubleWord:
                        self.drawCell(canvas, row, column, letter, data.doubleWordFill)
                    elif cell in data.doubleLetter:
                        self.drawCell(canvas, row, column, letter, data.doubleLetterFill)
                    elif cell in data.tripleLetter:
                        self.drawCell(canvas, row, column, letter, data.tripleLetterFill)
                    else:
                        self.drawCell(canvas, row, column, letter, data.emptySquareFill)
                elif cell in data.tempCells:
                    self.drawCell(canvas, row, column, letter, "orange3")
                else:
                    self.drawCell(canvas, row, column, letter, data.occupiedSquareFill)
            canvas.create_text(data.infoMid-60, 325, text="Your Hand", font="Arial 14")

            indexList = []
            for i in range(len(data.letterHand)):
                indexList.append(i)
                    
            for (letter, column) in zip(data.letterHand, indexList):
                if letter == '-':
                    canvas.create_rectangle(data.infoMid-115 + data.squareSize *column,
                                            360,
                                            data.infoMid-115 + data.squareSize *column + data.squareSize ,
                                            360 + data.squareSize ,
                                            fill=data.emptySquareFill)
                else:
                    if column in data.highlightedCells:
                        canvas.create_rectangle(data.infoMid-115 + data.squareSize *column,
                                            360,
                                            data.infoMid-115 + data.squareSize *column + data.squareSize ,
                                            360 + data.squareSize,
                                            fill="yellow")
                    if column in data.scoreBoosterCells:
                        canvas.create_rectangle(data.infoMid-115 + data.squareSize *column,
                                            360,
                                            data.infoMid-115 + data.squareSize *column + data.squareSize ,
                                            360 + data.squareSize,
                                            fill="magenta")
                    else:
                        canvas.create_rectangle(data.infoMid-115 + data.squareSize *column,
                                                360,
                                                data.infoMid-115 + data.squareSize *column + data.squareSize ,
                                                360 + data.squareSize,
                                                fill="orange3")
                canvas.create_text(data.infoMid-115 + data.squareSize *(column+0.5),
                                        360 + data.squareSize/2,
                                        text=letter,
                                        font="Arial 10")
            #drawing most of the buttons and features in the GUI
            canvas.create_rectangle(650, 400, 700, 430, fill="antique white")
            canvas.create_rectangle(700, 400, 750, 430, fill="antique white")
            canvas.create_rectangle(750, 400, 800, 430, fill="antique white")
            canvas.create_rectangle(800, 400, 850, 430, fill="antique white")
            canvas.create_text(675, 408, text="Skip", font="Arial 10")
            canvas.create_text(675, 420, text="Turn", font="Arial 10")
            canvas.create_text(725, 408, text="Play", font="Arial 10")
            canvas.create_text(725, 420, text="Turn", font="Arial 10")
            canvas.create_text(775, 408, text="Swap", font="Arial 10")
            canvas.create_text(775, 420, text="Tiles", font="Arial 10")
            canvas.create_text(825, 408, text="Check", font="Arial 10")
            canvas.create_text(825, 420, text="Word", font="Arial 10")
            canvas.create_rectangle(data.infoMid-100, 280, data.infoMid+100, 330, fill="brown3")
            canvas.create_text(data.infoMid, 290, text=("Score"), font="Arial 20")
            canvas.create_text(data.infoMid, 315, text=("You: " + str(data.playerScore) + "      Computer: " + str(data.computerScore)), font="Arial 15")
            canvas.create_rectangle(data.infoMid-100, 100, data.infoMid+100, 150, fill="SpringGreen4")
            canvas.create_text(data.infoMid, 123, text= "Start Your Turn", font="Arial 20")
            canvas.create_rectangle(data.infoMid-100, 190, data.infoMid+100, 240, fill="PeachPuff3")
            canvas.create_text(data.infoMid, 213, text="Start Computer Turn", font="Arial 16")

            canvas.create_text(500, 30, text="Scrabble: Slang Mode", font="Helvetica 30")
            canvas.create_text(70, 220, text="Board Key:", font="Arial 16 bold")
            canvas.create_text(70, 240, text="Orange: Triple Word")
            canvas.create_text(70, 260, text="Pink: Double Word")
            canvas.create_text(70, 280, text="Blue: Triple Letter")
            canvas.create_text(70, 300, text="Cyan: Double Letter")
            canvas.create_text(data.infoMid + 180, 220, text="Letter Values:", font="Arial 16 bold")
            canvas.create_text(data.infoMid + 180, 245, text="A: 1, B: 3, C: 3", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 270, text="D: 2, E: 1, F: 4", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 295, text="G: 2, H: 4, I: 1", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 320, text="J: 8, K: 5, L: 1", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 345, text="M: 3, N: 1, O: 1", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 370, text="P: 3, Q: 10, R: 1", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 395, text="S: 1, T: 1, U: 4", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 420, text="V: 4, W: 4, X: 8", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 445, text="Y: 4, Z: 10", font="Arial 16")
            canvas.create_text(data.infoMid + 180, 470, text="Blank: 0", font="Arial 16")


    def mousePressed(self, event):
        if self.data.mode == "splashscreen":
            if (event.y >= 450 and event.y < 500) and (event.x >= 180 and event.x < 420):
                self.data.mode = "helpscreen"
            if (event.y >= 450 and event.y < 500) and (event.x >= 580 and event.x < 820):
                self.data.mode = "gamescreen"
        col = ((event.x - self.data.squareLeft) // self.data.squareSize)
        if (col > 14 or col < 0):
            col = 225        
        row = ((event.y - self.data.squareTop) // self.data.squareSize)
        cell = row*15 + col     
        currInTemp = cell in self.data.tempCells
        currInEmpty = cell in self.data.blankBoard

        currTileRow = (event.y - 360)//self.data.squareSize
        currTileCol = ((event.x - (self.data.infoMid-115))//self.data.squareSize)  
        currSelectedHandTile = ((currTileRow == 0) and (currTileCol in self.data.filledHandSpots))
        blankHandSpaces = ((currTileRow == 0) and (currTileCol in self.data.unoccupiedHandPositions))

        currOnSkip = (event.y >= 400 and event.y < 430) and (event.x >= 650 and event.x < 700)
        currOnPlay = (event.y >= 400 and event.y < 430) and (event.x >= 700 and event.x < 750)
        currOnSwitch = (event.y >= 400 and event.y < 430) and (event.x >= 750 and event.x < 800)
        currOnSearch = (event.y >= 400 and event.y < 430) and (event.x >= 800 and event.x < 850)
        
        if self.data.readyHandToBoard:
            if currInEmpty: self.handToBoardEmpty(cell)  
            elif currInTemp: self.handToBoardTemp(cell)
            elif currSelectedHandTile: self.handToHandFilled(currTileCol)
            elif blankHandSpaces: self.handToHandEmpty(currTileCol)
            else:
                self.data.printStatement1 = "Error, you must click the board or hand."
            self.data.beginningClick = -1      
            self.data.readyHandToBoard = False   
        elif self.data.readyBoardToHand:
            if currSelectedHandTile: self.boardToHandFilled(currTileCol)   
            elif blankHandSpaces: self.boardToHandEmpty(currTileCol)
            elif currInEmpty: self.boardToBoardEmpty(cell)
            elif currInTemp: self.boardToBoardTemp(cell)
            else:
                self.data.printStatement1 = "Error, you must click the board or the hand."
            self.data.beginningClick = -1 
            self.data.readyBoardToHand = False
        else:
            if currSelectedHandTile: self.handPress1(currTileCol)
            elif currInTemp: self.boardPress1(cell)
            elif currInEmpty:
                self.data.printStatement2 = "Try to click a blue box."
            elif currOnSkip:
                self.data.canPassOnTurn = True
            elif currOnPlay:
                self.data.doTurn = True
            elif currOnSwitch:
                self.data.canSwitchTurns = True
            elif currOnSearch:
                self.data.canSearch = True
            else:
                self.data.printStatement1 = "Please click a blue letter or orange button."
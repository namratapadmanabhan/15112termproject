#The purpose of this file is to draw the board. There are functions to find
#all the locations which would be needed, as well as the various colors and 
#whether or not a cell is filled with a letter, so that the board can be 
#redrawn after every turn. 

class createBoard():
    def __init__(self):
        row = "---------------"
        self.board = row*15

    def findNewStartingPositions(self):
        board = self.board
        startingPositions = set([])
        checkpoint = '-23@#'
        length = len(board)
        for position in range(length):
            if board[position] not in checkpoint:
                currRow = position//15
                currCol = position%15
                fullRow = currRow*15
                newRow = currRow + 1
                newCol = currCol + 1
                lPos = fullRow + (currCol-1)
                rPos = fullRow + (currCol+1)
                uPos = (currRow+1)*15 + currCol
                dPos = (currRow-1)*15 + currCol
                colLength = 15
                secondToLast = 14
                beginningPos = 0
                if currRow != beginningPos and dPos not in startingPositions:
                    startingPositions.add(dPos)
                if currRow != secondToLast and uPos not in startingPositions:
                    startingPositions.add(uPos)
                if currCol != beginningPos and lPos not in startingPositions:
                    startingPositions.add(lPos)
                if newCol != colLength and rPos not in startingPositions:
                    startingPositions.add(rPos)
        beginningPos = 0
        numToAdd = 112
        if len(startingPositions) == beginningPos:
            startingPositions.add(numToAdd)
        return startingPositions

    def update(self, boardValues, positions):
        for (boardValue, position) in zip(boardValues, positions):
            self.board = self.board[:position] + boardValue + self.board[position+1:]

    def findFilledCells(self):
        board = self.board
        length = len(board)
        filledCells = []
        checkpoint = '-23@#'
        for cell in range(length):
            if board[cell] not in checkpoint:
                filledCells.append(cell)
        return filledCells

    def drawBoard(self):
        board = self.board
        width = len(board)
        cellWidth = int(width//15)
        for row in range(cellWidth):
            for col in range(15):
                print(board[(15*row) + col])

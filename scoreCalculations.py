#The main purpose of this file is to determine the best word using the spaces
#on the board, and to calculate what the score would be for a specific 
#word placement on a certain part of the board, after we define the specific
#spaces on the board that correspond to "special" tiles, and the scores we would
#get for each letter. This lets us calculate the optimal score.

tripleWord = [0, 7, 14, 105, 119, 210, 217, 224]
doubleWord = [16, 28, 32, 42, 48, 56, 64, 70, 154, 160, 168, 176, 182, 192, 196, 208]
doubleLetter = [3, 11, 36, 38, 45, 52, 59, 92, 96, 98, 102, 108, 116, 122, 126, 128, 132, 165, 172, 179, 186, 188, 213, 221]
tripleLetter = [20, 24, 76, 80, 84, 88, 136, 140, 144, 148, 200, 204]

scoresForTiles = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
                  'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
                  'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
                  'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

def bestPossibleWord(letterCombinations, currBoard):
    bestWord = [-1, [], []]
    bestPlacementLocations = []
    for combination in letterCombinations:
        wordVal = 0
        letters = {}
        for (char, cell) in zip(combination[0], combination[1]):
            letters[cell] = char
        for combo in combination[2]:
            wordVal += calculateWordScore(combo, letters, currBoard)
        if len(combination[1]) == 7: #full hand!
            wordVal += 50
        if wordVal > bestWord[0]:
            bestWord = [wordVal, combination[0], combination[1]]
            bestPlacementLocations = combination[1]

    for cell in bestPlacementLocations:
        if cell in tripleWord:
            tripleWord.remove(cell)
        elif cell in doubleWord:
            doubleWord.remove(cell)
        elif cell in doubleLetter:
            doubleLetter.remove(cell)
        elif cell in tripleLetter:
            tripleLetter.remove(cell)

    return bestWord

def calculateWordScore(wordPossible, lettersDict, currBoard):
    thisTileScore = 0
    dubscore = 0
    tripscore = 0
    scoreAdd = 1
    dub = 2
    trip = 3
    for cell in wordPossible:
        if cell in doubleWord:
            dubscore += scoreAdd
        elif cell in tripleWord:
            tripscore += scoreAdd
        if cell in doubleLetter:
            if cell in lettersDict:
                thisTileScore += dub*scoresForTiles[lettersDict[cell]]
            else:
                thisTileScore += dub*scoresForTiles[currBoard[cell]]
        elif cell in tripleLetter:
            if cell in lettersDict:
                thisTileScore += trip*scoresForTiles[lettersDict[cell]]
            else:
                thisTileScore += trip*scoresForTiles[currBoard[cell]]
        else:
            if cell in lettersDict:
                thisTileScore += scoresForTiles[lettersDict[cell]]
            else:
                thisTileScore += scoresForTiles[currBoard[cell]]
                
    return thisTileScore * (dub**dubscore) * (trip**tripscore)

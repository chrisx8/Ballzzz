import random

from gameObjects.block import generateBlocks

def createBoard(canvasWidth, canvasHeight, margin):
    newBoard = []
    # each cell is 40px*40px
    cellDimention = 40
    cols = (canvasWidth-margin) // cellDimention
    rows = (canvasHeight-margin) // cellDimention
    for row in range(rows):
        newRow = []
        for col in range(cols):
            newRow.append(None)
        newBoard.append(newRow)
    return newBoard


def moveBoard(data):
    newRow = [None] * len(data.board[0])
    data.board.insert(0, newRow)
    # generate random blocks
    countNewBlocks = random.randint(2, len(data.board[0])-1)
    generateBlocks(countNewBlocks, data)
    # add random blocks on top row
    # remove bottom row
    data.board.pop()
    # game over if current bottom row isn't empty
    for cell in data.board[len(data.board)-1]:
        if cell is not None:
            data.gameOver = True

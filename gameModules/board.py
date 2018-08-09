import random

from gameModules.block import generateBlocks, Block


def createEmptyBoard(data):
    newBoard = []
    # each cell is 40px*40px
    cellDimention = 40
    cols = (data.width-data.margin) // cellDimention
    rows = (data.height-data.margin) // cellDimention
    for row in range(rows):
        newRow = []
        for col in range(cols):
            newRow.append(None)
        newBoard.append(newRow)
    return newBoard


def createRandomBoard(data):
    data.board = createEmptyBoard(data)
    # generate between 2 and 4 blocks on the top row initially
    countInitialBlocks = random.randint(2, 4)
    generateBlocks(countInitialBlocks, data)


def createBoardFromDrawing(data):
    data.board = createEmptyBoard(data)
    # each cell is 40px*40px
    cellDimention = 40
    # look each line segment
    for segment in data.segments:
        if None not in segment:
            # only use real mouse pos. ignore stored previous pos
            x1, y1 = segment[2], segment[3]
            # calculate row/col
            col = x1 // cellDimention
            row = y1 // cellDimention
            # create a block in row/col
            data.board[row][col] = Block(row, col, data.margin,
                                         data.ballCount, data.difficulty)


def moveBoard(data):
    newRow = [None] * len(data.board[0])
    data.board.insert(0, newRow)
    # generate random blocks
    countNewBlocks = random.randint(2, len(data.board[0])-1)
    generateBlocks(countNewBlocks, data)
    # add random blocks on top row
    # remove bottom row
    data.board.pop()
    # score+1 on each move
    data.score += 1
    # increment shots
    data.shots += 1
    # if score is a multiple of 50, increase difficulty (up to 9)
    if data.difficulty < 9 and data.score % 50 == 0:
        data.difficulty += 1

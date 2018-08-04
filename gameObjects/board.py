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


def moveBoard(board, data):
    # add random blocks on top row
    board.insert(0, [None] * len(board[0]))
    # remove bottom row
    board.pop()
    # game over if current bottom row isn't empty
    for cell in board[len(board)-1]:
        if cell is not None:
            data.gameOver = True

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

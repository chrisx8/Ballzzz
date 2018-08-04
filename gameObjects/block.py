import random

class Block(object):
    def __init__(self, row, col, margin):
        colors = ('green2', 'hotPink')
        self.dimension = 40
        self.margin = margin
        self.row = row
        self.col = col
        self.updatePos(margin, row, col)
        self.color = random.choice(colors)

    def updatePos(self, margin, row, col):
        self.topLeft = (margin+col*self.dimension, margin+row*self.dimension)
        self.bottomRight = (margin + (col+1) * self.dimension,
                            margin + (row+1) * self.dimension)

    def draw(self, canvas):
        canvas.create_rectangle(self.topLeft, self.bottomRight, fill=self.color)

    def moveDown(self):
        self.row += 1
        self.updatePos(self.margin, self.row, self.col)


def generateBlocks(countBlocks, canvasWidth, margin, dimension, board):
    while countBlocks > 0:
        cols = (canvasWidth-margin)//dimension-1
        randomCol = random.randint(0, cols)
        if not board[0][randomCol]:
            board[0][randomCol] = Block(0, randomCol, margin)
            countBlocks -= 1

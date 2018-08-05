import random

from gameObjects.ball import SuperBall


class Block(object):
    def __init__(self, row, col, margin, countBalls):
        colors = ('green2', 'hotPink')
        self.dimension = 40
        self.margin = margin
        self.row = row
        self.col = col
        self.updatePos()
        self.color = random.choice(colors)
        self.number = random.randint(countBalls, countBalls*3)

    def updatePos(self):
        self.topLeft = (self.margin+self.col*self.dimension,
                        self.margin+self.row*self.dimension)
        self.bottomRight = (self.margin + (self.col+1) * self.dimension,
                            self.margin + (self.row+1) * self.dimension)

    def draw(self, canvas):
        canvas.create_rectangle(self.topLeft, self.bottomRight, fill=self.color)
        canvas.create_text(self.topLeft[0]+self.dimension//2,
                           self.topLeft[1]+self.dimension//2, text=self.number)

    def moveDown(self):
        self.row += 1
        self.updatePos()

    def onCollision(self, ball):
        if isinstance(ball, SuperBall):
            self.number = 0
        else:
            self.number -= 1


def generateBlocks(countBlocks, data):
    while countBlocks > 0:
        cols = (data.width-data.margin)//data.dimension-1
        randomCol = random.randint(0, cols)
        if not data.board[0][randomCol]:
            data.board[0][randomCol] = Block(0, randomCol,
                                             data.margin, data.countBalls)
            countBlocks -= 1

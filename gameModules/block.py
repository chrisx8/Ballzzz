import random

from gameModules.ball import SuperBall


class Block(object):
    def __init__(self, row, col, margin, countBalls=None,
                 difficulty=None, number=None):
        colors = ('green2', 'hotPink', 'dodgerblue')
        self.dimension = 40
        self.margin = margin
        self.row = row
        self.col = col
        self.updatePos()
        self.color = random.choice(colors)
        if number is None:
            self.number = random.randint(countBalls, countBalls*3*difficulty)
        else:
            self.number = number

    # return a evaluable string for recreating the object
    def __repr__(self):
        return "%s(%d, %d, %d, number=%d)" % (type(self).__name__, self.row,
                                              self.col, self.margin,
                                              self.number)

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
    # increase difficulty every 50 points earned
    if data.score % 50 == 0:
        data.difficulty += 1
    generateTarget = random.choice([True, False])
    if generateTarget:
        cols = (data.width-data.margin)//data.dimension-1
        randomCol = random.randint(0, cols)
        data.board[0][randomCol] = Target(data.margin, 0, randomCol)
    while countBlocks > 0:
        cols = (data.width-data.margin)//data.dimension-1
        randomCol = random.randint(0, cols)
        if not data.board[0][randomCol]:
            data.board[0][randomCol] = Block(0, randomCol, data.margin,
                                             data.ballCount, data.difficulty)
            countBlocks -= 1


class Target(object):
    def __init__(self, margin, row, col):
        self.color = "dodger blue"
        self.dimension = 40
        self.radius = 10
        self.margin = margin
        self.row = row
        self.col = col
        self.updatePos()

    # return a evaluable string for recreating the object
    def __repr__(self):
        return "%s(%d, %d, %d)" % (type(self).__name__, self.margin,
                                   self.row, self.col)

    def updatePos(self):
        self.cx = self.margin + self.col*self.dimension + self.dimension//2
        self.cy = self.margin + self.row*self.dimension + self.dimension//2
        self.topLeft = (self.cx-self.radius, self.cy-self.radius)
        self.bottomRight = (self.cx+self.radius, self.cy+self.radius)

    def draw(self, canvas):
        canvas.create_oval(self.topLeft, self.bottomRight,
                           outline=self.color, width=2)
        canvas.create_text(self.cx, self.cy, text="+1", fill="white")

    def moveDown(self):
        self.row += 1
        self.updatePos()

import random

class Block(object):
    def __init__(self, row, col, margin):
        colors = ('green2', 'hotPink')
        self.dimension = 40
        self.topLeft = (margin+col*self.dimension, margin+row*self.dimension)
        self.bottomRight = (margin + (col+1) * self.dimension,
                            margin + (row+1) * self.dimension)
        self.color = random.choice(colors)

    def draw(self, canvas):
        canvas.create_rectangle(self.topLeft, self.bottomRight, fill=self.color)

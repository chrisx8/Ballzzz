class UserInterface(object):
    def __init__(self, canvasWidth, canvasHeight):
        self.width = canvasWidth
        self.height = canvasHeight

    def drawStart(self, canvas):
        print('press S to start')

    def drawGameOver(self, canvas):
        print('press R to restart')

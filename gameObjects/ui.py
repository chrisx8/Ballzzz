class UserInterface(object):
    def __init__(self, canvasWidth, canvasHeight):
        self.width = canvasWidth
        self.height = canvasHeight

    def drawGameOver(self, canvas):
        canvas.create_text()
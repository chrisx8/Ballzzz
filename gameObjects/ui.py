class UserInterface(object):
    def __init__(self, canvasWidth, canvasHeight):
        self.width = canvasWidth
        self.height = canvasHeight

    def drawStart(self, canvas, width, height):
        canvas.create_text(width//2, height//2,
                           text="press S to start", fill="red")

    def drawGameOver(self, canvas, width, height):
        boxHeight = 50
        canvas.create_rectangle(0, height//2-boxHeight//2,
                                width, height//2+boxHeight//2, fill="white")
        canvas.create_text(width//2, height//2,
                           text="press R to restart", fill="red")

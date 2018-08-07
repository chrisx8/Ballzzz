class UserInterface(object):
    def __init__(self, canvasWidth, canvasHeight):
        self.width = canvasWidth
        self.height = canvasHeight

    def drawStart(self, canvas, width, height):
        canvas.create_text(width//2, height//2,
                           text="press S to start", fill="red")

    def drawGameOver(self, canvas, data):
        boxHeight = 100
        # center box
        canvas.create_rectangle(0, data.height//2-boxHeight//2, data.width,
                                data.height//2+boxHeight//2, fill="white")
        canvas.create_text(data.width//2, data.height//2-20, text="Game Over",
                           fill="red", font="Verdana 24 bold")
        canvas.create_text(data.width//2, data.height//2+10,
                           text="Your score: %d" % data.score, fill="red")
        canvas.create_text(data.width//2, data.height//2+30,
                           text="Your ranking: %d" % data.rank, fill="red")
        # bottom box
        canvas.create_rectangle(0, data.height//2+boxHeight//2+20, data.width,
                                data.height//2+boxHeight, fill="white")
        canvas.create_text(data.width//2, data.height//2+boxHeight//2+35,
                           text="Press R to restart", fill="red")

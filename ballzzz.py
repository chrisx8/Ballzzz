from tkinter import *
from gameObjects.ball import Ball, SuperBall
from gameObjects.block import Block, generateBlocks
from gameObjects.ui import UserInterface
from gameObjects.board import createBoard, moveBoard
import random
import os


def init(data):
    data.margin = 20
    # dimension of blocks
    data.dimension = 40
    # UI object
    data.ui = UserInterface(data.width, data.height)
    # number of available balls
    data.countBalls = 1
    data.balls = [Ball("green2", 42, data.height, data.margin)]
    data.board = createBoard(data.width, data.height, data.margin)
    data.startGame = False
    data.gameOver = False
    data.score = 0
    # generate between 2 and 4 blocks on the top row initially
    countInitialBlocks = random.randint(2, 4)
    generateBlocks(countInitialBlocks, data)


def mousePressed(event, data):
    if data.gameOver or not data.startGame: return
    for row in data.board:
        for block in row:
            if block: block.moveDown()
    moveBoard(data)
    print(len(data.board))


def keyPressed(event, data):
    if not data.startGame and event.keysym == 's':
        data.startGame = True
        return
    if event.keysym == 'r':
        init(data)


def timerFired(data):
    pass


def redrawAll(canvas, data):
    if not data.startGame:
        data.ui.drawStart(canvas)
        return
    if data.gameOver:
        data.ui.drawGameOver(canvas)
        return
    # draw black background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    # draw margin
    canvas.create_rectangle(0, 0, data.width, data.margin, fill="gray")
    for row in data.board:
        for block in row:
            if block: block.draw(canvas)
    for ball in data.balls:
        ball.draw(canvas)


####################################
# run functions
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    """
    Change title of Tkinter windows
    cited from https://stackoverflow.com/questions/2395431/
                using-tkinter-in-python-to-edit-the-title-bar
    """
    root.title("Ballzzz")
    """
    Change Tkinter window icon
    cited from https://stackoverflow.com/questions/18537918/set-window-icon
    Get current path
    cited from https://stackoverflow.com/questions/3430372/
                how-to-get-full-path-of-current-files-directory-in-python
    """
    # Get absolute directory of icon
    root.iconbitmap(os.path.dirname(os.path.abspath(__file__))
                    + os.sep + 'ballzzz_icon.ico')
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(400, 600)

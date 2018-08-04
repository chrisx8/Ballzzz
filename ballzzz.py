from tkinter import *
from gameObjects.ball import Ball, SuperBall
from gameObjects.block import Block
from gameObjects.ui import UserInterface
from gameObjects.board import createBoard
import random
import os

def init(data):
    data.margin = 10
    # dimension of blocks
    data.dimension = 40
    data.balls = [Ball("green2", 42, data.height, data.margin)]
    data.board = createBoard(data.width, data.height, data.margin)
    data.startGame = False
    data.gameOver = False
    # generate between 2 and 4 blocks on the top row initially
    countInitialBlocks = random.randint(2, 4)
    while countInitialBlocks > 0:
        cols = (data.width-data.margin)//data.dimension-1
        randomCol = random.randint(0, cols)
        if not data.board[0][randomCol]:
            data.board[0][randomCol] = Block(0, randomCol, data.margin)
            countInitialBlocks -= 1


def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if event.keysym == 'r':
        init(data)

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # if not startGame:
    # draw black background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
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
import math
import os
from tkinter import *

from gameObjects.ball import Ball
from gameObjects.board import *
from gameObjects.ui import UserInterface


def init(data):
    data.margin = 20
    # dimension of blocks
    data.dimension = 40
    # UI object
    data.ui = UserInterface(data.width, data.height)
    # number of available balls
    data.countBalls = 1
    data.ball = Ball("green2", 66, data.height, data.margin)
    data.board = createBoard(data.width, data.height, data.margin)
    data.startGame = False
    data.gameOver = False
    data.score = 1
    # generate between 2 and 4 blocks on the top row initially
    countInitialBlocks = random.randint(2, 4)
    generateBlocks(countInitialBlocks, data)


def mousePressed(event, data):
    if data.gameOver or not data.startGame: return
    ballX, ballY = data.ball.cx, data.ball.cy
    distanceToClick = math.sqrt((ballX-event.x)**2 + (ballY-event.y)**2)
    # formula = distanceToClick / sin(pi/2) = (e.y-ballY) / sin(angle)
    sinAngle = abs(event.y-ballY) / distanceToClick
    angle = math.asin(sinAngle)
    if event.x >= ballX:
        data.ball.move(angle, 1)
    else:
        data.ball.move(angle, 2)


def keyPressed(event, data):
    # press R to restart at any time after game started
    if data.startGame and event.keysym == 'r':
        init(data)
        data.startGame = True
    # start game
    if not data.startGame and event.keysym == 's':
        data.startGame = True
    # ignore rest when game is over or when game isn't started
    if data.gameOver or not data.startGame: return
    # TODO: TESTING CODE BELOW. REMOVE AFTER TESTING
    if event.keysym == 'c':
        for row in data.board:
            for block in row:
                if block: block.onCollision(data.ball)
    if event.keysym == 'm':
        for row in data.board:
            for block in row:
                if block: block.moveDown()
        moveBoard(data)


def timerFired(data):
    # update ball movement
    data.ball.updatePos()
    collisionStatus = data.ball.collisionWithBorder(data.width,
                                                    data.height, data.margin)
    if not collisionStatus:
        data.ball = Ball("hotPink", 66, data.height, data.margin)
    for row in range(len(data.board)):
        for col in range(len(data.board[0])):
            if data.board[row][col]:
                # process collision
                if data.ball.isCollisionWithBlock(data.board[row][col]):
                    pass
                    # data.ball.onCollision()
                    # data.board[row][col].onCollision(data.ball)
                # remove empty blocks
                if data.board[row][col].number == 0:
                    data.board[row][col] = None


def redrawAll(canvas, data):
    # draw start screen
    if not data.startGame:
        data.ui.drawStart(canvas, data.width, data.height)
        return
    # draw black background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    # draw margin
    drawMargin(canvas, data)
    # draw blocks
    for row in data.board:
        for block in row:
            if block: block.draw(canvas)
    # draw game over screen
    if data.gameOver:
        data.ui.drawGameOver(canvas, data.width, data.height)
        return
    # draw score
    canvas.create_text(data.width//2, data.margin//2,
                       text="Score: %d" % data.score, fill="white")
    # draw balls
    data.ball.draw(canvas)


def drawMargin(canvas, data):
    # top
    canvas.create_rectangle(0, 0, data.width, data.margin,
                            fill="gray", outline="")
    # left
    canvas.create_rectangle(0, 0, data.margin, data.height,
                            fill="gray", outline="")
    # bottom
    canvas.create_rectangle(0, data.height-data.margin, data.width, data.height,
                            fill="gray", outline="")
    # right
    canvas.create_rectangle(data.width-data.margin, 0, data.width, data.height,
                            fill="gray", outline="")

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
    data.timerDelay = 33   # milliseconds (about 30fps)
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

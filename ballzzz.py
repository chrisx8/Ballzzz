import copy
import math
import os
from tkinter import *

from gameObjects.api import API
from gameObjects.ball import Ball
from gameObjects.block import Block, Target
from gameObjects.board import *
from gameObjects.ui import UserInterface


def init(data):
    # current asset path
    data.assetPath = os.path.dirname(os.path.abspath(__file__)) + \
                     os.sep + 'assets' + os.sep
    data.timerDelay = 30
    data.margin = 20
    # dimension of blocks
    data.dimension = 40
    # UI object
    data.ui = UserInterface()
    # Ball object that stays on the bottom.
    randomBallPos = random.randint(data.margin+10, data.width-data.margin-10)
    data.ball = Ball("green2", randomBallPos, data.height, data.margin)
    # number of available balls; number of unreleased balls
    data.ballCount, data.remainingBalls = 1, 1
    # Moving balls
    data.movingBalls = []
    # number of bounces in each shot and average hit per ball
    data.bounces, data.averageHitsPerBall = 0, 0
    # Where to display ball count depends on ball pos
    data.ballCountPos = (data.ball.cx, data.ball.cy-data.ball.radius-10)
    # Create a board
    data.board = createBoard(data.width, data.height, data.margin)
    # Scoring and game state
    data.startGame, data.gameOver = False, False
    data.score = 1
    data.bestScore = None
    data.rank = None
    # current shot timer
    data.timer = 0
    # Define api connection
    data.api = API('haha')
    # generate between 2 and 4 blocks on the top row initially
    countInitialBlocks = random.randint(2, 4)
    generateBlocks(countInitialBlocks, data)


def mousePressed(event, data):
    # TODO: MOUSE-NAVIGABLE UI
    # mouse navigation on game over screen, and ignore rest
    if data.gameOver and data.width//2-60 <= event.x <= data.width//2+60:
        init(data)
        data.startGame = True
        return
    # ignore rest when game isn't started or there are moving balls
    if not data.startGame or data.movingBalls != []: return
    # copy initial ball and add to moving ball list
    # copyBall = Ball(data.ball.color, data.ball.cx, data.height, data.margin)
    while data.remainingBalls > 0:
        data.movingBalls.append(copy.copy(data.ball))
        data.remainingBalls -= 1
    for ball in data.movingBalls:
        ballX, ballY = ball.cx, ball.cy
        distanceToClick = math.sqrt((ballX-event.x)**2 + (ballY-event.y)**2)
        # angle of ball movement
        # formula = distanceToClick / sin(pi/2) = (e.y-ballY) / sin(angle)
        angle = math.asin(abs(event.y-ballY) / distanceToClick)
        if event.x >= ballX:
            ball.move(angle, 1)
        else:
            ball.move(angle, 2)


def keyPressed(event, data):
    # TODO: REMOVE TESING CODE
    if event.keysym == 'g':
        data.gameOver = True
        apiResp = data.api.uploadScore(data.score)
        data.rank = apiResp['ranking']
        data.bestScore = apiResp['score']
    if event.keysym == 'h':
        data.score += 10
    # press R to restart at any time after game started
    # if data.startGame and event.keysym == 'r':
    #     init(data)
    #     data.startGame = True
    # start game
    if not data.startGame and event.keysym == 's':
        data.startGame = True
    # ignore rest when game is over or when game isn't started
    if data.gameOver or not data.startGame: return
    # Speed up ball if user presses A
    if data.timer >= 10000 and event.keysym == 'a':
        data.timerDelay = 5


def timerFired(data):
    # ignore all if game isn't started
    if data.gameOver or not data.startGame: return
    # increment timer of current shot if balls are moving
    if len(data.movingBalls) != 0: data.timer += data.timerDelay
    print(data.timer)
    # game over if current bottom row isn't empty
    for cell in data.board[len(data.board)-1]:
        if isinstance(cell, Block):
            data.gameOver = True
            apiResp = data.api.uploadScore(data.score)
            data.rank = apiResp['ranking']
            data.bestScore = apiResp['score']
    # update ball movement
    for ball in data.movingBalls:
        if isinstance(ball, Ball):
            ball.updatePos()
            # handle border collisions
            processBorderCollision(data, ball)
            # handling target/block collisions
            processBoardObjectCollision(data, ball)


def redrawAll(canvas, data):
    # draw start screen
    if not data.startGame:
        data.ui.drawStart(canvas, data)
        return
    # draw game over screen
    if data.gameOver:
        data.ui.drawGameOver(canvas, data)
        return
    # draw black background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    # draw margin
    drawMargin(canvas, data)
    # draw blocks
    for row in data.board:
        for block in row:
            if block: block.draw(canvas)
    if data.remainingBalls > 0:
        canvas.create_text(data.ballCountPos,
                           text="x%d" % data.remainingBalls, fill="white")
    # draw score
    canvas.create_text(data.width//2, data.margin//2,
                       text="Score: %d" % data.score, fill="white")
    # draw initial ball
    data.ball.draw(canvas)
    # draw moving balls
    for ball in data.movingBalls:
        if isinstance(ball, Ball):
            ball.draw(canvas)


# Handling ball hitting borders
def processBorderCollision(data, ball):
    # call border collision function. Returns last x pos when hitting bottom
    lastXPos = ball.collisionWithBorder(data.width,
                                                data.height, data.margin)
    # ball landed on the bottom border
    if lastXPos is not None:
        data.movingBalls.remove(ball)
    # if last ball reaches the bottom
    if lastXPos is not None and len(data.movingBalls) == 0:
        for row in data.board:
            for block in row:
                # shift down every block
                if block: block.moveDown()
        # Create new row on top of board
        moveBoard(data)
        # create a new ball
        data.ball = Ball(data.ball.color, lastXPos, data.height, data.margin)
        data.movingBalls = []
        data.remainingBalls = data.ballCount
        data.ballCountPos = (data.ball.cx, data.ball.cy-data.ball.radius-10)
        # reset bounces and average hits per ball
        data.bounces, data.averageHitsPerBall = 0, 0
        # reset timer and speed
        data.timerDelay = 30
        data.timer = 0


# handling target/block collisions
def processBoardObjectCollision(data, ball):
    for row in range(len(data.board)):
        for col in range(len(data.board[0])):
            # process collision with target
            if isinstance(data.board[row][col], Target) and \
                    ball.isCollisionWithBlock(data.board[row][col]):
                data.ballCount += 1
                data.board[row][col] = None
            # process collision with block
            if isinstance(data.board[row][col], Block) and \
                    ball.isCollisionWithBlock(data.board[row][col]):
                data.bounces += 1
                # ball bouncing
                ball.collisionWithBlock(data.board[row][col])
                # block number change
                data.board[row][col].onCollision(ball)
                # remove empty blocks
                if data.board[row][col].number == 0:
                    data.board[row][col] = None


def drawMargin(canvas, data):
    # top
    canvas.create_rectangle(0, 0, data.width, data.margin,
                            fill="gray25", outline="")
    # left
    canvas.create_rectangle(0, 0, data.margin, data.height,
                            fill="gray25", outline="")
    # bottom
    canvas.create_rectangle(0, data.height-data.margin, data.width,
                            data.height, fill="gray25", outline="")
    # right
    canvas.create_rectangle(data.width-data.margin, 0, data.width,
                            data.height, fill="gray25", outline="")


########################################################################
# run functions
# https://www.cs.cmu.edu/~112n18/notes/notes-animations-part1.html
########################################################################

def run(width=300, height=300):
    print('Welcome!')

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
    data.timerDelay = 30   # milliseconds (about 30fps)
    root = Tk()
    init(data)
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
    root.iconbitmap(data.assetPath + 'ballzzz_icon.ico')
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

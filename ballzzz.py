import copy
import math
import os
import random
import string
from tkinter import *

from gameModules import board
from gameModules import drawboard
from gameModules import ui
from gameModules.api import API
from gameModules.ball import Ball, SuperBall
from gameModules.block import Block, Target


########################################################################
# animation template adopted from course note
# https://www.cs.cmu.edu/~112n18/notes/notes-animations-part1.html
########################################################################

def init(data):
    """
    Get current paths cited from
    https://stackoverflow.com/questions/3430372/
            how-to-get-full-path-of-current-files-directory-in-python
    """
    data.assetPath = os.path.dirname(os.path.abspath(__file__)) + \
                     os.sep + 'assets' + os.sep
    data.timerDelay = 30
    data.margin = 20
    # dimension of blocks
    data.dimension = 40
    # Moving balls
    data.movingBalls = []
    # number of bounces in each shot
    data.bounces = 0
    # Scoring and game state
    data.startGame, data.gameOver = False, False
    data.drawLeaderboard = False
    data.drawCustomizations = False
    data.ballColorBoxSelected = False
    data.superBallColorBoxSelected = False
    data.bestScore = None
    data.rank = None
    # points of the user-drawn pattern
    data.segments = set()
    # X pos for bottom margin scroll text
    data.bottomScrollX = data.width
    # try to get user-defined color. default to green2 if it doesn't exist
    try: data.ballColor
    except: data.ballColor = "green2"
    data.superBallColor = "hotPink"
    data.allowSaveCustomization = True
    # try to load saved game
    try:
        import savedGame
        """
        Explicitly reload an imported module
        https://emacs.stackexchange.com/questions/13476/how-to-force-a-python-
            shell-to-re-import-modules-when-running-a-buffer
        """
        import importlib
        importlib.reload(savedGame)
        # load ball
        data.ball = eval(savedGame.ball)
        # load board
        data.board = eval(savedGame.board)
        # eval everything in board
        tempBoard = eval(savedGame.board)
        data.board = board.createEmptyBoard(data)
        # eval everything in board
        for row in range(len(tempBoard)):
            for col in range(len(tempBoard[0])):
                data.board[row][col] = eval(tempBoard[row][col])
        # number of available balls; number of unreleased balls
        data.ballCount = savedGame.ballCount
        data.remainingBalls = savedGame.remainingBalls
        # number of shots
        data.shots = savedGame.shots
        # difficulty 1-9. 1=easy
        data.difficulty = savedGame.difficulty
        data.score = savedGame.score
        # current shot timer
        data.timer = savedGame.timer
        data.paused = savedGame.paused
        # load username and url
        data.username = savedGame.username
        data.url = savedGame.url
    # start as new game if saved game doesn't exist
    except: startNewGame(data)
    # try to read username and url
    try: data.username, data.url
    # if url and username aren't defined, get from console
    except AttributeError: data.username, data.url = getUserInput()
    # # customized colors
    # data.ball.color = data.ballColor
    # Where to display ball count depends on ball pos
    data.ballCountPos = (data.ball.cx, data.ball.cy - data.ball.radius - 10)
    # Define api connection
    data.api = API(data.username, data.url)


def mousePressed(event, data):
    # mouse navigation on game over screen, and ignore rest
    # drawboard button
    if data.width // 2 - 60 <= event.x <= data.width // 2 + 60 and \
            data.height // 2 + 80 <= event.y <= data.height // 2 + 120 and \
            not data.drawCustomizations and \
            not data.drawLeaderboard and not data.startGame:
        # open drawboard
        print('Please ignore Tkinter errors, as they don\'t affect the '
              'functionality of the game.')
        drawboard.run(data)
        return
    # settings button
    if data.width // 2 - 20 <= event.x <= data.width // 2 + 20 and \
            data.height // 2 + 250 <= event.y <= data.height // 2 + 290 and \
            not data.drawCustomizations and not data.startGame:
        data.drawCustomizations = True
        return
    if data.drawCustomizations:
        # click in ball color box to activate input
        # deactivate the other text box
        if 70 < event.x < data.width - 70 and 260 < event.y < 300:
            data.ballColorBoxSelected = True
            data.superBallColorBoxSelected = False
        # click in super ball color box to activate input
        # deactivate the other text box
        elif 70 < event.x < data.width - 70 and 360 < event.y < 400:
            data.superBallColorBoxSelected = True
            data.ballColorBoxSelected = False
        # click outside the text boxes to deactivate all
        else:
            data.ballColorBoxSelected = False
            data.superBallColorBoxSelected = False
    # play/restart button
    if data.width//2-60 <= event.x <= data.width//2+60 and \
            data.height//2+140 <= event.y <= data.height//2+180 and \
            not data.drawCustomizations and \
            not data.drawLeaderboard and (data.gameOver or not data.startGame):
        if not data.startGame and len(data.segments) != 0:
                # create a board from drawing
                startNewGame(data)
                board.createBoardFromDrawing(data)
        if data.gameOver:
            init(data)
            # create random board
            board.createRandomBoard(data)
        data.startGame = True
        return
    # leaderboard (start screen)/exit (game over)/save (settings) button
    if data.width//2-60 <= event.x <= data.width//2+60 and \
            data.height//2+200 <= event.y <= data.height//2+240:
        if data.drawLeaderboard:
            data.drawLeaderboard = False
        elif data.drawCustomizations and data.allowSaveCustomization:
            data.drawCustomizations = False
            data.ball.color = data.ballColor
        elif not data.startGame:
            data.topTen = data.api.getTopTen()['response']
            data.drawLeaderboard = True
        elif data.gameOver:
            init(data)
        return
    # ignore rest when game isn't started or there are moving balls
    if not data.startGame or data.movingBalls != [] or data.paused: return
    # copy initial ball and add to moving ball list
    while data.remainingBalls > 0 and not isinstance(data.ball, SuperBall):
        data.movingBalls.append(copy.copy(data.ball))
        data.remainingBalls -= 1
    # one super ball
    if isinstance(data.ball, SuperBall):
        data.movingBalls.append(data.ball)
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
    # when paused, press any key to resume game and ignore rest
    if data.paused:
        data.bottomScrollX = data.width
        data.paused = False
        return
    # in settings, accept input
    if data.drawCustomizations:
        if data.ballColorBoxSelected:
            # allow letters and numbers
            if event.keysym in string.ascii_lowercase+string.digits:
                data.ballColor += event.keysym
            # backspace to delete one character
            if event.keysym == "BackSpace":
                data.ballColor = data.ballColor[:len(data.ballColor)-1]
        elif data.superBallColorBoxSelected:
            # allow letters and numbers
            if event.keysym in string.ascii_lowercase+string.digits:
                data.superBallColor += event.keysym
            # backspace to delete one character
            if event.keysym == "BackSpace":
                data.superBallColor = \
                    data.superBallColor[:len(data.superBallColor)-1]
    # only check when playing
    if data.startGame and not data.gameOver and not data.paused:
        # press ESC to go home when there's no moving balls
        if data.movingBalls == [] and event.keysym == "Escape":
            saveGame(data)
            init(data)
        # Speed up ball if user presses A
        if data.timer >= 10000 and event.keysym == 'a':
            data.timerDelay = 5
        # press P to pause during game play
        elif event.keysym == 'p':
            data.paused = True
        # press R to restart during game play
        elif event.keysym == 'r':
            init(data)
            startNewGame(data)
            board.createRandomBoard(data)
            data.startGame = True
        # press D to increase difficulty (up to 9)
        elif event.keysym == 'd' and data.difficulty < 9:
            data.difficulty += 1


def timerFired(data):
    # ignore all if game isn't started
    if data.gameOver or not data.startGame or data.paused: return
    # increment timer of current shot if balls are moving
    if len(data.movingBalls) != 0: data.timer += data.timerDelay
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
    # draw customizations page
    if data.drawCustomizations:
        ui.drawCustomizations(canvas, data)
        return
    # draw leaderboard
    if data.drawLeaderboard:
        ui.drawLeaderboard(canvas, data)
        return
    # draw start screen
    if not data.startGame:
        ui.drawStart(canvas, data)
        return
    # draw game over screen
    if data.gameOver:
        ui.drawGameOver(canvas, data)
        return
    # draw black background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    # draw margin
    ui.drawMargin(canvas, data)
    # draw blocks
    for row in data.board:
        for block in row:
            if block: block.draw(canvas)
    # draw ball counter
    if data.remainingBalls > 0 and not isinstance(data.ball, SuperBall):
        canvas.create_text(data.ballCountPos,
                           text="x%d" % data.remainingBalls, fill="white")
    # draw initial ball
    data.ball.draw(canvas)
    # draw moving balls
    for ball in data.movingBalls:
        if isinstance(ball, Ball):
            ball.draw(canvas)
    # draw paused banner
    if data.paused:
        ui.drawPaused(canvas, data)


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
        shotComplete(data, lastXPos)


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
                # ball bouncing. True if colliding with SuperBall
                if ball.collisionWithBlock(data.board[row][col]):
                    # block number change to 0
                    data.board[row][col].onCollision(ball)
                    # remove empty block
                    data.board[row][col] = None
                    # create new ball
                    shotComplete(data, data.ball.cx)
                    return
                # block number change
                data.board[row][col].onCollision(ball)
                # remove empty blocks
                if data.board[row][col].number == 0:
                    data.board[row][col] = None


def shotComplete(data, lastXPos):
    for row in data.board:
        for block in row:
            # shift down every block
            if block: block.moveDown()
    # Create new row on top of board
    board.moveBoard(data)
    # create a new ball
    createNewBall(data, lastXPos)
    data.movingBalls = []
    data.remainingBalls = data.ballCount
    data.ballCountPos = (data.ball.cx, data.ball.cy - data.ball.radius - 10)
    # reset bounces and average hits per ball
    data.bounces, data.averageHitsPerBall = 0, 0
    # reset timer and speed
    data.timerDelay = 30
    data.timer = 0


def createNewBall(data, lastXPos):
    averageHitsPerBall = data.bounces // data.ballCount
    """
    generate super ball if
    - previous ball isn't a super ball
    - average hits per ball > 10
    - every 10 shots in easy mode
    """
    if not isinstance(data.ball, SuperBall) and \
            (averageHitsPerBall > 10 or
             (data.shots % 10 == 0 and data.difficulty == 1)):
        data.ball = SuperBall(data.superBallColor, lastXPos,
                              data.height, data.margin)
    else:
        data.ball = Ball(data.ballColor, lastXPos, data.height, data.margin)


def saveGame(data):
    # write stuff to file with trailing newline
    def writeToSavedGameFile(content):
        data.savedGameFile.write(content+'\n')

    print('Saving game......', end='')
    # open saved game file for editing
    data.savedGameFile = open('savedGame.py', 'w+')
    # parse everything on board to string
    parsedBoard = board.createEmptyBoard(data)
    for row in range(len(data.board)):
        for col in range(len(data.board[0])):
            parsedBoard[row][col] = str(data.board[row][col])
    writeToSavedGameFile('board = "%s"' % str(parsedBoard))
    writeToSavedGameFile('ball = "%s"' % str(data.ball))
    writeToSavedGameFile('ballCount = %d' % data.ballCount)
    writeToSavedGameFile('remainingBalls = %d' % data.remainingBalls)
    writeToSavedGameFile('shots = %d' % data.shots)
    writeToSavedGameFile('paused = %s' % data.paused)
    writeToSavedGameFile('difficulty = %d' % data.difficulty)
    writeToSavedGameFile('score = %d' % data.score)
    writeToSavedGameFile('timer = %d' % data.timer)
    writeToSavedGameFile('username = "%s"' % data.username)
    writeToSavedGameFile('url = "%s"' % data.url)
    data.savedGameFile.close()
    print('Game saved!')



def getUserInput():
    url = input("Enter your scoreboard server URL \n "
                "(start with HTTP/HTTPS and no trailing slashes. "
                "LEAVE BLANK to use default): ")
    # blank for default
    if url == '':
        url = "https://ballzzz.chrisx.tk"
    usernameRegex = re.compile('^[a-zA-Z0-9._-]{4,50}$')
    username = input("Enter your username: ")
    # validate username
    while not usernameRegex.match(username):
        print('\nInvalid username! \n'
              'Your username should contain 4-50 characters, '
              'with only letters and numbers.\n')
        username = input("Enter your username: ")
    return username, url


def loadGame(data):
    import savedGame
    """
    Explicitly reload an imported module
    https://emacs.stackexchange.com/questions/13476/how-to-force-a-python-
        shell-to-re-import-modules-when-running-a-buffer
    """
    import importlib
    importlib.reload(savedGame)
    # load ball
    data.ball = eval(savedGame.ball)
    # load board
    data.board = eval(savedGame.board)
    # eval everything in board
    tempBoard = eval(savedGame.board)
    data.board = board.createEmptyBoard(data)
    # eval everything in board
    for row in range(len(tempBoard)):
        for col in range(len(tempBoard[0])):
            data.board[row][col] = eval(tempBoard[row][col])
    # number of available balls; number of unreleased balls
    data.ballCount = savedGame.ballCount
    data.remainingBalls = savedGame.remainingBalls
    # number of shots
    data.shots = savedGame.shots
    # difficulty 1-9. 1=easy
    data.difficulty = savedGame.difficulty
    data.score = savedGame.score
    # current shot timer
    data.timer = savedGame.timer
    data.paused = savedGame.paused
    # load username and url
    data.username = savedGame.username
    data.url = savedGame.url


def startNewGame(data):
    # Ball object that stays on the bottom.
    randomBallPos = random.randint(data.margin + 10,
                                   data.width - data.margin - 10)
    data.ball = Ball(data.ballColor, randomBallPos, data.height, data.margin)
    # Where to display ball count depends on ball pos
    data.ballCountPos = (data.ball.cx, data.ball.cy - data.ball.radius - 10)
    # number of available balls; number of unreleased balls
    data.ballCount, data.remainingBalls = 1, 1
    # number of shots
    data.shots = 0
    # difficulty 1-9. 1=easy
    data.difficulty = 1
    data.score = 1
    # current shot timer
    data.timer = 0
    data.paused = False
    # create a new random board
    board.createRandomBoard(data)


########################################################################
# run functions from course notes
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

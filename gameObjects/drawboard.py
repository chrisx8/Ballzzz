from tkinter import *


########################################################################
# animation template adopted from course website
# https://www.cs.cmu.edu/~112n18/notes/notes-animations-part1.html
# modified for the draw function
########################################################################


def init(data):
    data.margin = 20
    # points of the line
    data.segments = set()
    # previous mouse position
    data.prevMouseX = None
    data.prevMouseY = None
    # if mouse is down
    data.mouseDown = False
    # text alternation timer
    data.textTimer = 0


def mousePressed(event, data):
    pass


def mouseUp(event, data):
    data.mouseDown = False
    # stop current draw by clearing previous positions
    data.prevMouseX, data.prevMouseY = None, None


def mouseDown(event, data):
    # only register mouse down within margin
    if mouseInMargin(event.x, event.y, data):
       data.mouseDown = True


def mouseMove(event, data):
    # only draw in margin
    if data.mouseDown and mouseInMargin(event.x, event.y, data):
        # treat draw as segments between last mouse pos and current pos
        data.segments.add((data.prevMouseX, data.prevMouseY, event.x, event.y))
        data.prevMouseX = event.x
        data.prevMouseY = event.y
    # treat mouse out-of-margin as mouse up
    elif not mouseInMargin(event.x, event.y, data):
        mouseUp(event, data)


# pass root in so window can close completely
def keyPressed(event, data):
    if event.keysym == "e":
        data.segments = set()


def timerFired(data):
    data.textTimer += data.timerDelay


def redrawAll(canvas, data):
    # draw black background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    # draw margin
    drawMargin(canvas, data)
    for segment in data.segments:
        # only draw legal segments
        if None not in segment: canvas.create_line(segment, fill="green")


def drawMargin(canvas, data):
    # top
    canvas.create_rectangle(0, 0, data.width, data.margin,
                            fill="gray25", outline="")
    # top text alternates every 3 seconds
    if data.textTimer % 6000 <= 3000:
        canvas.create_text(data.width//2, data.margin//2,
                           fill="white", text="Draw a pattern, and a board "
                                              "will be created based on it!")
    else:
        canvas.create_text(data.width//2, data.margin // 2,
                           text="Close this window when you finished drawing.",
                           fill="white")
    # left
    canvas.create_rectangle(0, 0, data.margin, data.height,
                            fill="gray25", outline="")
    # bottom
    canvas.create_rectangle(0, data.height - data.margin, data.width,
                            data.height, fill="gray25", outline="")
    canvas.create_text(data.width // 2, data.height - data.margin // 2,
                       text="Press E to start over",
                       fill="white")
    # right
    canvas.create_rectangle(data.width - data.margin, 0, data.width,
                            data.height, fill="gray25", outline="")


# check if current mouse pos is in margin
def mouseInMargin(mouseX, mouseY, data):
    return data.margin <= mouseX <= data.width - data.margin and \
           data.margin <= mouseY <= data.height - data.margin


########################################################################
# run functions from course notes
# https://www.cs.cmu.edu/~112n18/notes/notes-animations-part1.html
########################################################################

# use data from game
def run(data):
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

    # custom wrappers for mouse up/down
    def mouseDownWrapper(event, canvas, data):
        mouseDown(event, data)
        redrawAllWrapper(canvas, data)

    def mouseUpWrapper(event, canvas, data):
        mouseUp(event, data)
        redrawAllWrapper(canvas, data)

    def mouseMoveWrapper(event, canvas, data):
        mouseMove(event, data)
        redrawAllWrapper(canvas, data)

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
    # get asset path from call
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
    """
    Mouse up/down/motion event bindings. Adopted from
    https://svn.python.org/projects/python/trunk/Demo/tkinter/guido/paint.py
    Modified to comply with MVC and fit animation template from course website
    https://www.cs.cmu.edu/~112n18/notes/notes-animations-part1.html
    """
    canvas.bind("<Motion>", lambda event:
                                        mouseMoveWrapper(event, canvas, data))
    canvas.bind("<ButtonPress-1>", lambda event:
                                        mouseDownWrapper(event, canvas, data))
    canvas.bind("<ButtonRelease-1>", lambda event:
                                        mouseUpWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)

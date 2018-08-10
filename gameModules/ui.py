from tkinter import PhotoImage, Label


def drawPaused(canvas, data):
    canvas.create_rectangle(0, data.height//2-40, data.width,
                            data.height//2+40, fill="purple", outline="")
    canvas.create_text(data.width//2, data.height//2, text="Paused",
                       fill="White", font=('Century Gothic', 30, 'bold'))


def drawMargin(canvas, data):
    # top
    canvas.create_rectangle(0, 0, data.width, data.margin,
                            fill="gray25", outline="")
    # left
    canvas.create_rectangle(0, 0, data.margin, data.height,
                            fill="gray25", outline="")
    # bottom
    canvas.create_rectangle(0, data.height - data.margin, data.width,
                            data.height, fill="gray25", outline="")
    # right
    canvas.create_rectangle(data.width - data.margin, 0, data.width,
                            data.height, fill="gray25", outline="")
    # draw score
    canvas.create_text(data.width//2, data.margin//2,
                       text="Score: %d" % data.score, fill="white")
    # draw resume instruction when paused and ignore rest
    if data.paused:
        canvas.create_text(data.width // 2, data.height - data.margin // 2,
                           text="Press any key to resume", fill="white")
        return
    # draw speedup instruction
    if data.timer > 10000 and data.timerDelay == 30:
        # alternating color
        if data.timer % 600 <= 300:
            canvas.create_text(data.width//2, data.height-data.margin//2,
                               text="Press A to speed up", fill="red")
        else:
            canvas.create_text(data.width//2, data.height-data.margin//2,
                               text="Press A to speed up", fill="white")
    # draw current difficulty, restart and difficulty change instruction
    else:
        if data.bottomScrollX <= -700:
            data.bottomScrollX = data.width
        else:
            data.bottomScrollX -= 3
        canvas.create_text(data.bottomScrollX, data.height-data.margin//2,
                           text="Current Difficulty: %d                 "
                                % data.difficulty +
                                "Press D to increase difficulty          "
                                "Press P to pause         "
                                "Press R to restart         "
                                "Press ESC to save and quit", fill="white",
                           anchor="w")


def drawStart(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="gray18")
    """
    Displaying image in Tkinter
    https://stackoverflow.com/questions/35024118/
        how-to-load-an-image-into-a-python-3-4-tkinter-window
    http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    """
    # logo
    imgPath = data.assetPath + 'ballzzz.png'
    img = PhotoImage(file=imgPath)
    label = Label(image=img)
    label.image = img
    canvas.create_image(data.width//2, data.height//4, image=img)
    # warning
    canvas.create_text(data.width//2, data.height//2+50, fill="white",
                       text='"Draw a board" always creates a new game!',
                       font=('Century Gothic', 12, 'bold'))
    # draw board button
    canvas.create_rectangle(data.width//2-60, data.height//2+80,
                            data.width//2+60, data.height//2+120,
                            outline="", fill="turquoise4")
    canvas.create_text(data.width//2, data.height//2+100, fill="white",
                       text="Draw a board", font=('Century Gothic', 12, 'bold'))
    # play button
    canvas.create_rectangle(data.width//2-60, data.height//2+140,
                            data.width//2+60, data.height//2+180,
                            outline="", fill="green")
    canvas.create_text(data.width//2, data.height//2+160, fill="white",
                       text="Play", font=('Century Gothic', 14, 'bold'))
    # Leaderboard button
    canvas.create_rectangle(data.width//2-60, data.height//2+200,
                            data.width//2+60, data.height//2+240,
                            outline="", fill="purple")
    canvas.create_text(data.width//2, data.height//2+220, fill="white",
                       text="Leaderboard", font=('Century Gothic', 13, 'bold'))


def drawGameOver(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="gray18")
    """
    Displaying image in Tkinter
    https://stackoverflow.com/questions/35024118/
        how-to-load-an-image-into-a-python-3-4-tkinter-window
    http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    """
    # logo
    # imgPath =
    img = PhotoImage(file=data.assetPath+'ballzzz.png')
    label = Label(image=img)
    label.image = img
    canvas.create_image(data.width//2, data.height//4, image=img)
    # game over
    canvas.create_text(data.width//2, data.height//2-40, text="Game Over",
                       fill="gray90", font=('Century Gothic', 28, 'bold'))
    # score
    canvas.create_text(data.width//2, data.height//2+20, fill="gray90",
                       text="Score: ", font=('Century Gothic', 14, 'bold'),
                       anchor='e')
    canvas.create_text(data.width//2, data.height//2+20, fill="white",
                       font=('Century Gothic', 24, 'bold'),
                       text=str(data.score), anchor='w')
    # best score
    canvas.create_text(data.width//2, data.height//2+55, fill="gray90",
                       text="Best Score: ", font=('Century Gothic', 14, 'bold'),
                       anchor='e')
    canvas.create_text(data.width//2, data.height//2+55, fill="white",
                       font=('Century Gothic', 22, 'bold'),
                       text=str(data.bestScore), anchor='w')
    # rank
    canvas.create_text(data.width//2, data.height//2+90, fill="gray90",
                       text="Rank: ", font=('Century Gothic', 14, 'bold'),
                       anchor='e')
    canvas.create_text(data.width//2, data.height//2+90, fill="white",
                       font=('Century Gothic', 24, 'bold'),
                       text=str(data.rank), anchor='w')
    # restart button
    canvas.create_rectangle(data.width//2-60, data.height//2+140,
                            data.width//2+60, data.height//2+180,
                            outline="", fill="green")
    canvas.create_text(data.width//2, data.height//2+160, fill="white",
                       text="Restart", font=('Century Gothic', 14, 'bold'))
    # exit button
    canvas.create_rectangle(data.width//2-60, data.height//2+200,
                            data.width//2+60, data.height//2+240,
                            outline="", fill="red4")
    canvas.create_text(data.width//2, data.height//2+220, fill="white",
                       text="Exit", font=('Century Gothic', 14, 'bold'))


def drawLeaderboard(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="gray25")
    """
    Displaying image in Tkinter
    https://stackoverflow.com/questions/35024118/
        how-to-load-an-image-into-a-python-3-4-tkinter-window
    http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    """
    # logo
    imgPath = data.assetPath + 'ballzzz.png'
    img = PhotoImage(file=imgPath)
    label = Label(image=img)
    label.image = img
    canvas.create_image(data.width//2, 60, image=img)
    yPos = 150
    canvas.create_text(50, yPos, fill="white",
                       text="Rank", anchor="n",
                       font=('Century Gothic', 14, 'bold'))
    canvas.create_text(data.width // 2, yPos, fill="white",
                       text="Username", anchor="n",
                       font=('Century Gothic', 14, 'bold'))
    canvas.create_text(data.width-50, yPos, fill="white",
                       text="Score", anchor="n",
                       font=('Century Gothic', 14, 'bold'))
    yPos += 30
    for entry in data.topTen:
        canvas.create_text(50, yPos, fill="white",
                           text=data.topTen[entry]['ranking'], anchor="n",
                           font=('Century Gothic', 12))
        canvas.create_text(data.width//2, yPos, fill="white",
                           text=data.topTen[entry]['username'], anchor="n",
                           font=('Century Gothic', 12))
        canvas.create_text(data.width-50, yPos, fill="white",
                           text=data.topTen[entry]['score'], anchor="n",
                           font=('Century Gothic', 12))
        yPos += 25
    # back button
    canvas.create_rectangle(data.width//2-60, data.height//2+200,
                            data.width//2+60, data.height//2+240,
                            outline="", fill="red4")
    canvas.create_text(data.width//2, data.height//2+220, fill="white",
                       text="Back", font=('Century Gothic', 14, 'bold'))

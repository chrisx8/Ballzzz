from tkinter import PhotoImage, Label


class UserInterface(object):
    def drawMargin(self, canvas, data):
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
        # draw instruction
        canvas.create_text(data.width//2, data.height-data.margin//2,
                           text="Press R to restart game", fill="white")

    def drawStart(self, canvas, data):
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
        # play button
        canvas.create_rectangle(data.width//2-60, data.height//2+140,
                                data.width//2+60, data.height//2+180,
                                outline="", fill="green")
        canvas.create_text(data.width//2, data.height//2+160, fill="white",
                           text="Play", font="Verdana 14")
        # Leaderboard button
        canvas.create_rectangle(data.width//2-60, data.height//2+200,
                                data.width//2+60, data.height//2+240,
                                outline="", fill="purple")
        canvas.create_text(data.width//2, data.height//2+220, fill="white",
                           text="Leaderboard", font="Verdana 13")

    def drawGameOver(self, canvas, data):
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
        # game over
        canvas.create_text(data.width//2, data.height//2-40, text="Game Over",
                           fill="gray90", font="Verdana 28 bold")
        # score
        canvas.create_text(data.width//2, data.height//2+20, fill="gray90",
                           text="Score: ", font="Verdana 14", anchor='e')
        canvas.create_text(data.width//2, data.height//2+20, fill="white",
                           font="Verdana 22 bold",
                           text=str(data.score), anchor='w')
        # best score
        canvas.create_text(data.width//2, data.height//2+55, fill="gray90",
                           text="Best Score: ", font="Verdana 14", anchor='e')
        canvas.create_text(data.width//2, data.height//2+55, fill="white",
                           font="Verdana 22 bold",
                           text=str(data.bestScore), anchor='w')
        # rank
        canvas.create_text(data.width//2, data.height//2+90, fill="gray90",
                           text="Rank: ", font="Verdana 14", anchor='e')
        canvas.create_text(data.width//2, data.height//2+90, fill="white",
                           font="Verdana 22 bold",
                           text=str(data.rank), anchor='w')
        # restart button
        canvas.create_rectangle(data.width//2-60, data.height//2+140,
                                data.width//2+60, data.height//2+180,
                                outline="", fill="green")
        canvas.create_text(data.width//2, data.height//2+160, fill="white",
                           text="Restart", font="Verdana 14")
        # exit button
        canvas.create_rectangle(data.width//2-60, data.height//2+200,
                                data.width//2+60, data.height//2+240,
                                outline="", fill="red4")
        canvas.create_text(data.width//2, data.height//2+220, fill="white",
                           text="Exit", font="Verdana 14")

    def drawLeaderboard(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill="green2")
        canvas.create_text(100, 100, text='leaderboard')
        # back button
        canvas.create_rectangle(data.width//2-60, data.height//2+200,
                                data.width//2+60, data.height//2+240,
                                outline="", fill="red4")
        canvas.create_text(data.width//2, data.height//2+220, fill="white",
                           text="Back", font="Verdana 14")

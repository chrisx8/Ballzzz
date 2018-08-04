class Ball(object):
    def __init__(self, color, startX, canvasHeight, canvasMargin):
        # user-defined color in customization
        self.color = color
        # radius is always 5px
        self.radius = 5
        # balls start at where the last ball landed, at the bottom of canvas
        self.cx = startX
        self.cy = canvasHeight - canvasMargin - self.radius

    def draw(self, canvas):
        canvas.create_oval(self.cx-self.radius, self.cy-self.radius,
                           self.cx+self.radius, self.cy+self.radius,
                           fill=self.color)


class SuperBall(Ball):
    def __init__(self, color, startX, canvasHeight, canvasMargin):
        super().__init__(color, startX, canvasHeight, canvasMargin)
        # super balls are twice as big as normal
        self.radius = 10

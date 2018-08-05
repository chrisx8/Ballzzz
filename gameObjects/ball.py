import math

class Ball(object):
    def __init__(self, color, startX, canvasHeight, canvasMargin):
        # user-defined color in customization
        self.color = color
        # radius is always 5px
        self.radius = 5
        # balls start at where the last ball landed, at the bottom of canvas
        self.cx = startX
        self.cy = canvasHeight - canvasMargin - self.radius - 2
        # change
        self.dx = 0
        self.dy = 0
        self.quadrant = 0
        self.speed = 5

    def draw(self, canvas):
        canvas.create_oval(self.cx-self.radius, self.cy-self.radius,
                           self.cx+self.radius, self.cy+self.radius,
                           fill=self.color)

    def move(self, angle, quadrant):
        self.angle = angle
        self.quadrant = quadrant
        self.dx = self.radius * math.cos(angle)
        self.dy = self.radius * math.sin(angle)
        if quadrant == 2:
            self.dx *= -1

    def updatePos(self):
        self.cx += self.dx * self.speed
        self.cy -= self.dy * self.speed

    def collisionWithBorder(self, canvasWidth, canvasHeight, canvasMargin):
        # top border: reverse vertical direction
        if self.cy-self.radius <= canvasMargin:
            self.dy *= -1
        # left border: change quadrant
        elif self.cx-self.radius <= canvasMargin:
            self.move(self.angle, 1)
        # right border: change quadrant
        elif self.cx+self.radius >= canvasWidth-2*canvasMargin:
            self.move(self.angle, 2)
        # bottom border: remove ball by returning False
        elif self.cy+self.radius >= canvasHeight-2*canvasMargin:
            return False
        # otherwise keep ball by returning True
        return True

    def isCollisionWithBlock(self, block):
        return self.cx+self.radius >= block.topLeft[0] or \
               self.cx-self.radius <= block.bottomRight[0] or \
               self.cy+self.radius >= block.topLeft[1] or \
               self.cy-self.radius <= block.bottomRight[1]

    def onCollision(self):
        if self.quadrant == 1:
            self.move(self.angle, 2)
        elif self.quadrant == 2:
            self.move(self.angle, 1)


class SuperBall(Ball):
    def __init__(self, color, startX, canvasHeight, canvasMargin):
        super().__init__(color, startX, canvasHeight, canvasMargin)
        # super balls are twice as big as normal
        self.radius = 10
        self.cy = canvasHeight - canvasMargin - self.radius

    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_text(self.cx, self.cy, text="S")

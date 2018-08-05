import math


class Ball(object):
    def __init__(self, color, startX, canvasHeight, canvasMargin):
        # user-defined color in customization
        self.color = color
        # radius is always 5px
        self.radius = 5
        # balls start at where the last ball landed, at the bottom of canvas
        self.cx = startX
        self.cy = canvasHeight - canvasMargin - self.radius - 5
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
        self.dy = self.radius * math.sin(angle) * -1
        if quadrant == 2:
            self.dx *= -1
        elif quadrant == 3:
            self.dx *= -1
            self.dy *= -1
        elif quadrant == 4:
            self.dy *= -1

    def updatePos(self):
        self.cx += self.dx * self.speed
        self.cy += self.dy * self.speed

    def isMoving(self):
        return self.dx != 0 or self.dy != 0

    def collisionWithBorder(self, canvasWidth, canvasHeight, canvasMargin):
        # top border: reverse vertical direction
        if self.cy-self.radius <= canvasMargin:
            self.dy *= -1
        # left border: change quadrant
        if self.cx-self.radius <= canvasMargin:
            # go to quadrant 1 when going up
            if self.dy < 0:
                self.move(self.angle, 1)
            # go to quadrant 4 when going up
            elif self.dy > 0:
                self.move(self.angle, 4)
        # right border: change quadrant
        elif self.cx+self.radius >= canvasWidth-2*canvasMargin:
            # go to quadrant 2 when going up
            if self.dy < 0:
                self.move(self.angle, 2)
            # go to quadrant 3 when going up
            elif self.dy > 0:
                self.move(self.angle, 3)
        # bottom border: return True to remove ball
        elif self.cy+self.radius >= canvasHeight-canvasMargin:
            return True

    def isCollisionWithBlock(self, block):
        return self.cx + self.radius >= block.topLeft[0] and \
               self.cx - self.radius <= block.bottomRight[0] and \
               self.cy + self.radius >= block.topLeft[1] and \
               self.cy - self.radius <= block.bottomRight[1]

    def collisionWithBlock(self, block):
        # top/bottom border: reverse vertical direction
        if self.cy-self.radius <= block.bottomRight[1] or \
           self.cy + self.radius >= block.topLeft[1]:
            self.dy *= -1
        # left border: change quadrant
        if self.cx+self.radius >= block.topLeft[0]:
            # go to quadrant 1 when going up
            if self.dy < 0:
                self.move(self.angle, 1)
            # go to quadrant 4 when going up
            elif self.dy > 0:
                self.move(self.angle, 4)
        # right border: change quadrant
        elif self.cx-self.radius <= block.bottomRight[0]:
            # go to quadrant 2 when going up
            if self.dy < 0:
                self.move(self.angle, 2)
            # go to quadrant 3 when going up
            elif self.dy > 0:
                self.move(self.angle, 3)

    def onCollision(self):
        if self.quadrant == 1:
            self.move(self.angle, 2)
        elif self.quadrant == 2:
            self.move(self.angle, 1)
        elif self.quadrant == 3:
            self.move(self.angle, 4)
        elif self.quadrant == 4:
            self.move(self.angle, 3)


class SuperBall(Ball):
    def __init__(self, color, startX, canvasHeight, canvasMargin):
        super().__init__(color, startX, canvasHeight, canvasMargin)
        # super balls are twice as big as normal
        self.radius = 10
        self.cy = canvasHeight - canvasMargin - self.radius

    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_text(self.cx, self.cy, text="S")

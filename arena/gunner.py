from basics import Entity, Screen, Color, Point, Polygon, Softbody
import pygame

class Gunner(Entity):

    def __init__(self, x=0, y=0):
        Entity.__init__(self, x, y)
        self.maxV = 3

        self.splitTimer = 0
        self.splitTimerMax = 0.5

        self.radius = 10

    def Update(self):
        self.input()
        self.x += self.v.x
        self.y += self.v.y

        self.splitTimer = max(self.splitTimer - Screen.DeltaTime(), 0)

    def Render(self):
        Screen.DrawCircle(self, self.radius, Color.light_green)
        shotVectors = self.shotVectors(Screen.MousePosition())
        if self.splitTimer > 0:
            thickness = int((self.splitTimer * 4)**8 / 8)
            for shotVector in shotVectors:
                Screen.DrawRay(shotVector[0], shotVector[1], Color.red, thickness)

    def shotVectors(self, targetPosition, dAngle=5):
        diff = targetPosition - self
        angle = diff.degrees
        ptLeft = Point.Clone(diff)
        ptRight = Point.Clone(diff)
        ptLeft.degrees = angle + dAngle
        ptRight.degrees = angle - dAngle
        return [[self, self + ptLeft], [self, self + ptRight], [self, Point.Clone(targetPosition)]]

    def input(self):
        acc = 1
        if Screen.KeyDown(pygame.K_a):
            self.v.x -= acc
        if Screen.KeyDown(pygame.K_d):
            self.v.x += acc
        if Screen.KeyDown(pygame.K_w):
            self.v.y -= acc
        if Screen.KeyDown(pygame.K_s):
            self.v.y += acc

        if self.v.lengthSq > self.maxV**2:
            self.v.length = self.maxV

        self.v *= 0.9

        if Screen.LeftMousePressed():
            self.splitTimer = self.splitTimerMax
            softbodies = Entity.GetAllEntitiesOfType("Softbody")
            shotVectors = self.shotVectors(Screen.MousePosition())
            for softbody in softbodies:
                softbody.split(shotVectors)

        if Screen.RightMouseReleased():
            diff = Screen.MousePosition() - self
            angle = diff.degrees
            ptLeft = Point(0, self.radius)
            ptRight = Point(0, -self.radius)
            ptLeft.degrees = angle
            ptRight.degrees = angle
            vertices = [
                self + ptRight,
                self + ptLeft,
                self + diff.normalized * self.radius * 3
            ]
            polygon = Polygon.NewFromAbsolutePositions(vertices)
            softbodies = Entity.GetAllEntitiesOfType("Softbody")
            for softbody in softbodies:
                Softbody.Subtract(softbody, polygon)


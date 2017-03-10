from basics import Entity, Screen, Color
import pygame

class Gunner(Entity):

    def __init__(self, x=0, y=0):
        Entity.__init__(self, x, y)
        self.maxV = 3

        self.splitTimer = 0
        self.splitTimerMax = 0.5

    def Update(self):
        self.input()
        self.x += self.v.x
        self.y += self.v.y

        self.splitTimer = max(self.splitTimer - Screen.DeltaTime(), 0)

    def Render(self):
        Screen.DrawCircle(self, 10, Color.light_green)
        if self.splitTimer > 0:
            thickness = int((self.splitTimer * 4)**8 / 8)
            Screen.DrawRay(self, Screen.MousePosition(), Color.red, thickness)

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
            for softbody in softbodies:
                softbody.splitOnceAndDestroy(self, Screen.MousePosition())


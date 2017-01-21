from screen import Screen
import pygame
from utils import *
import math
from entity import Entity

class Gladiator(Entity):

    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.color = (255, 255, 255)
        self.radius = 12
        
        self.AddState("normal", self.UpdateNormal)
        self.SetState("normal")

    def UpdateVelocity(self):
        self.v.x = self.v.y = 0

    def UpdateNormal(self):
        self.UpdateVelocity()
        
        self.x += self.v.x
        self.y += self.v.y

        self.x = min(max(self.x, 0), Screen.Instance.width)
        self.y = min(max(self.y, 0), Screen.Instance.height)

    def Render(self):
        Screen.DrawCircle(self, self.radius, self.color)


class Player(Gladiator):

    def __init__(self, x, y):
        Gladiator.__init__(self, x, y)
        self.color = (0, 255, 0)

    def UpdateVelocity(self):
        self.v.x = self.v.y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.v.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.v.x += 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.v.y -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.v.y += 5

class AI(Gladiator):

    def __init__(self, x, y):
        Gladiator.__init__(self, x, y)
        self.color = (255, 0, 0)
        
        self.v.x = 5
        self.v.y = 0

    def UpdateVelocity(self):
        self.v.degrees += 10
    
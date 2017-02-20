from basics import Screen, PolygonEntity, Point
import pygame
from time import time
from math import pi
from random import random
import random

def PreGame():
    random.seed(5)
    pygame.display.set_caption("Polygon Intersection Test")

def GeneratePolygon():
    vertices = []
    angle = 0
    while angle < 2 * pi:
        length = random.random() * 250 + 50
        angle = min(angle + random.random() * 0.5, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return vertices

merge = True
A = None
B = None
C = None
def BeginGame():
    global A, B, C, D, E
    A = PolygonEntity(400, 400, GeneratePolygon(), (128, 255, 128))
    B = PolygonEntity(400, 400, GeneratePolygon(), (128, 128, 255))
    C = PolygonEntity(400, 400, GeneratePolygon(), (255, 128, 128))
    D = PolygonEntity(400, 400, GeneratePolygon(), (255, 128, 255))
    E = PolygonEntity(400, 400, GeneratePolygon(), (128, 255, 255))

firstFrameTriggered = False
angle = 0
def UpdateGame():
    global firstFrameTriggered, A, B, C, D, E, angle, merge
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

    p = Point(100, 0)
    if Screen.KeyReleased(pygame.K_SPACE):
        A.visible = not A.visible
        B.visible = not B.visible
    if Screen.KeyReleased(pygame.K_x):
        merge = not merge
    if Screen.KeyReleased(pygame.K_z):
        if merge:
            PolygonEntity.Merge(A, B, C, D, E)
        else:
            PolygonEntity.IntersectionPolygon(A, B, C)

    #angle -= 0.05
    #p.radians = angle
    #A.rotateRadians(0.03)
    B.x = 300 + p.x
    B.y = 400 + p.y

def RenderGame():
    global A, B, C, merge
    #input("Waiting")
    #B.IntersectionPolygon(A, (255, 0, 0))

def StartGame():
    Screen(800, 800)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
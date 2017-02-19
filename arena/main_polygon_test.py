from basics import Screen, PolygonEntity, Point
import pygame
from time import time


def PreGame():
    pygame.display.set_caption("Polygon Intersection Test")

A = None
B = None
def BeginGame():
    global A, B
    verticesA = [
        Point(300, 400, True),
        Point(100, 100, True),
        Point(380, 300, True)
    ]

    verticesB = [
        Point(400, 300, True),
        Point(240, 380, True),
        Point(300, 280, True),
        Point(140, 280, True),
        Point(140, 260, True),
        Point(200, 200, True),
        Point(220, 100, True)
    ]

    A = PolygonEntity(50, 20, verticesA, (128, 255, 128))
    B = PolygonEntity(50, 20, verticesB, (128, 128, 255))

firstFrameTriggered = False
angle = 0
def UpdateGame():
    global firstFrameTriggered, B, angle
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

    p = Point(100, 0)
    if Screen.KeyDown(pygame.K_SPACE):
        angle += 0.02
    p.radians = angle
    B.x = 50 + p.x
    B.y = 20 + p.y

def RenderGame():
    global A, B
    A.IntersectionPolygon(B, (255, 255, 0))
    #B.IntersectionPolygon(A, (255, 0, 0))

def StartGame():
    Screen(640, 480)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
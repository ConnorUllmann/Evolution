from basics import Screen, PolygonEntity, Point
import pygame
from time import time
from math import pi
from random import random


def PreGame():
    pygame.display.set_caption("Polygon Intersection Test")

A = None
B = None
def BeginGame():
    global A, B
    # verticesA = [
    #     # Point(100, 100, True),
    #     # Point(300, 100, True),
    #     # Point(200, 300, True)
    #     Point(300, 400, True),
    #     Point(100, 100, True),
    #     Point(380, 300, True)
    # ]
    # verticesB = [
    #     # Point(200, 50, True),
    #     # Point(300, 400, True),
    #     # Point(100, 400, True)
    #     Point(400, 300, True),
    #     Point(240, 380, True),
    #     Point(300, 280, True),
    #     Point(140, 280, True),
    #     Point(140, 260, True),
    #     Point(200, 200, True),
    #     Point(220, 100, True)
    # ]

    verticesA = []
    angle = 0
    while angle < 2 * pi:
        length = random() * 250 + 50
        angle += random() * 0.5
        point = Point(length, 0)
        point.radians = angle
        verticesA.append(point)

    verticesB = []
    angle = 0
    while angle < 2 * pi:
        length = random() * 290 + 10
        angle += random() * 0.5
        point = Point(length, 0)
        point.radians = angle
        verticesB.append(point)

    A = PolygonEntity(400, 400, verticesA, (128, 255, 128))
    B = PolygonEntity(400, 400, verticesB, (128, 128, 255))

firstFrameTriggered = False
angle = 0
def UpdateGame():
    global firstFrameTriggered, A, B, angle
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

    p = Point(100, 0)
    #if Screen.KeyDown(pygame.K_SPACE):
    angle -= 0.05
    p.radians = angle

    midPt = Point()
    for pt in A.vertices:
        midPt += pt
    midPt /= len(A.vertices)
    for pt in A.vertices:
        pt.rotateRadians(0.03, midPt)
    B.x = 300 + p.x
    B.y = 400 + p.y

def RenderGame():
    global A, B
    A.IntersectionPolygon(B, (255, 255, 0))
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
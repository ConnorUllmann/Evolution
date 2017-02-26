from basics import Screen, Polygon, PolygonEntity, Point, Color
import pygame
from time import time
from math import pi
from random import random
import random

def PreGame():
    random.seed(5)
    pygame.display.set_caption("Polygon Intersection Test")

def GeneratePolygon(x, y):
    vertices = []
    angle = 0
    while angle < 2 * pi:
        length = random.random() * 200 + 50
        angle = min(angle + random.random() * 0.2 + 0.1, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return Polygon(x, y, vertices)

merge = True
polygons = []
combinePolygons = []
def BeginGame():
    global polygons, debugPoints
    colors = [
        Color.light_green,
        Color.light_blue,
        Color.light_red,
        Color.light_magenta,
        Color.light_cyan
    ]

    #polygons.append(PolygonEntity(Polygon(200, 200, [Point(-100, 0), Point(100, 0), Point(200, 200)])))
    #polygons.append(PolygonEntity(Polygon(400, 200, [Point(-100, 0), Point(100, 0), Point(200, 200)])))
    for i in range(2):
        polygons.append(PolygonEntity(GeneratePolygon(300 + 200 * random.random(), 300 + 200 * random.random()), colors[i%len(colors)]))

def RotatePolygons(amount, polygons):
    for i in range(len(polygons)):
        polygons[i].rotateRadians(amount * (i+1))

firstFrameTriggered = False
def UpdateGame():
    global firstFrameTriggered, polygons, combinePolygons, merge
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

    if Screen.KeyReleased(pygame.K_c):
        RotatePolygons(0.5, polygons)

    if Screen.KeyDown(pygame.K_v):
        RotatePolygons(0.025, polygons)

    if Screen.KeyReleased(pygame.K_SPACE):
        for polygon in polygons:
            polygon.visible = not polygon.visible

    if Screen.KeyReleased(pygame.K_x):
        merge = not merge
        print("Merge" if merge else "Intersect")

    if Screen.KeyReleased(pygame.K_1) or Screen.KeyDown(pygame.K_0):
        combinePolygons = Polygon.Merge(polygons[0], polygons[1]) if merge else Polygon.Intersect(polygons[0], polygons[1])

def RenderGame():
    global combinePolygons
    for polygon in combinePolygons:
        polygon.renderPolygon(Color.white, 4)

def StartGame():
    Screen(800, 800)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
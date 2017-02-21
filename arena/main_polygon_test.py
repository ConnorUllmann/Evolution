from basics import Screen, Polygon, PolygonEntity, Point
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
        length = random.random() * 250 + 50
        angle = min(angle + random.random() * 0.5, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return Polygon(x, y, vertices)

merge = True
polygons = []
combinePolygons = []
def BeginGame():
    global polygons
    colors = [
        (128, 255, 128),
        (128, 128, 255),
        (255, 128, 128),
        (255, 128, 255),
        (128, 255, 255)
    ]
    polygons = []
    for i in range(3):
        polygons.append(PolygonEntity(GeneratePolygon(300 + 200 * random.random(), 300 + 200 * random.random()), colors[i%len(colors)]))

firstFrameTriggered = False
angle = 0
def UpdateGame():
    global firstFrameTriggered, polygons, combinePolygons, angle, merge
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

    if Screen.KeyDown(pygame.K_c):
        for i in range(len(polygons)):
            polygons[i].rotateRadians(i / 100)

    if Screen.KeyReleased(pygame.K_SPACE):
        for polygon in polygons:
            polygon.visible = not polygon.visible
    if Screen.KeyReleased(pygame.K_x):
        merge = not merge
    if True:#Screen.KeyReleased(pygame.K_z):
        if merge:
            combinePolygons = Polygon.Merge(*polygons)
        else:
            combinePolygons = Polygon.Intersect(*polygons)

def RenderGame():
    global combinePolygons
    for polygon in combinePolygons:
        polygon.RenderPolygon((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 3)

def StartGame():
    Screen(800, 800)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
from basics import Screen, Polygon, PolygonEntity, Point, Color, RectanglesCollide
import pygame
from time import time
from math import pi
from random import random
import random
from time import time

def PreGame():
    random.seed(5)
    pygame.display.set_caption("Polygon Intersection Test")

def GeneratePolygon(x, y):
    vertices = []
    angle = 0
    while angle < 2 * pi:
        length = random.random() * 50 + 100
        angle = min(angle + random.random() * 0.3, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return Polygon(x, y, vertices)

merge = True
polygons = []
mergePolygons = []
intersectPolygons = []
def BeginGame():
    global polygons, debugPoints
    colors = [
        Color.light_green,
        Color.light_blue,
        Color.light_red,
        Color.light_magenta,
        Color.light_cyan
    ]

    # polygons.append(PolygonEntity(Polygon(200, 200, [Point(-100, 0), Point(100, 0), Point(0, 200)]), Color.green))
    # polygons.append(PolygonEntity(Polygon(500, 200, [Point(-100, 0), Point(100, 0), Point(0, 200)]), Color.blue))
    for i in range(2):
        polygons.append(PolygonEntity(GeneratePolygon(300 + 200 * random.random(), 300 + 200 * random.random()), colors[i%len(colors)]))

def RotatePolygons(amount, polygons):
    for i in range(len(polygons)):
        polygons[i].rotateRadians(amount * (i+1) * (1 if i % 2 else -1))

firstFrameTriggered = False
def UpdateGame():
    global firstFrameTriggered, polygons, mergePolygons, intersectPolygons, merge
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
        mergeStart = time()
        mergePolygons = Polygon.Merge(polygons[0], polygons[1])
        intersectPolygons = Polygon.Intersect(polygons[0], polygons[1])
        mergeDuration = time() - mergeStart
        print("Merge/intersect duration: {}s = {} frames at 60FPS".format(int(mergeDuration*100)/100, int(mergeDuration*60)))

    polygons[0].x = Screen.Instance.MousePosition().x
    polygons[0].y = Screen.Instance.MousePosition().y

def RenderGame():
    global mergePolygons, intersectPolygons
    for polygon in mergePolygons:
        polygon.renderPolygon(Color.cyan, 4)
    for polygon in intersectPolygons:
        polygon.renderPolygon(Color.yellow, 4)
    if polygons[0].boundingRectsCollide(polygons[1]):
        polygons[1].renderBoundingRect(Color.red, 6, False)

def StartGame():
    Screen(800, 800)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
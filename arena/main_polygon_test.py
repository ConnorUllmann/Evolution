from basics import Screen, Polygon, PolygonEntity, Point, Color, RectanglesCollide, PointOnLineAtX, PointOnLineAtY, PointOnLineClosestToPoint
import pygame
from time import time
from math import pi, sin
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
        length = random.random() * 250 + 20
        angle = min(angle + random.random() * 0.1 + 0.05, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return Polygon(x, y, vertices)

merge = True
polygons = []
mergePolygons = []
intersectPolygons = []
cuttingLines = [
    [Point(200, 200), Point(300, 300)],
    [Point(600, 200), Point(500, 500)],
    [Point(350, 100), Point(350, 200)],
    [Point(0, 300), Point(100, 300)]
]
def BeginGame():
    global polygons, debugPoints

    for i in range(1):
        polygons.append(PolygonEntity(GeneratePolygon(300 + 200 * random.random(), 300 + 200 * random.random()), Color.all[i%len(Color.all)]))

def RotatePolygons(amount, polygons):
    for i in range(len(polygons)):
        polygons[i].rotateRadians(amount * (i+1) * (1 if i % 2 else -1))

firstFrameTriggered = False
def UpdateGame():
    global firstFrameTriggered, polygons, mergePolygons, intersectPolygons, merge, cuttingLines
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

    if Screen.KeyReleased(pygame.K_v):
        RotatePolygons(0.5, polygons)

    if Screen.KeyDown(pygame.K_b):
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

    if Screen.KeyReleased(pygame.K_c):
        mergePolygons = polygons[0].split(cuttingLines)

    if Screen.KeyReleased(pygame.K_n):
        for polygon in mergePolygons:
            polygon.Destroy()
        mergePolygons = polygons[0].splitWithVelocity(cuttingLines)

    polygons[0].x = Screen.Instance.MousePosition().x
    polygons[0].y = Screen.Instance.MousePosition().y

def RenderGame():
    global mergePolygons, intersectPolygons, cuttingLines
    for i in range(len(mergePolygons)):
        mergePolygons[i].renderPolygon(Color.all[i%len(Color.all)], 1)
    for polygon in intersectPolygons:
        polygon.renderPolygon(Color.yellow, 4)

    for pair in cuttingLines:
        Screen.DrawLine(PointOnLineAtX(pair[0], pair[1], 0),
                        PointOnLineAtX(pair[0], pair[1], Screen.Width()), Color.red, 1)
        Screen.DrawLine(PointOnLineAtY(pair[0], pair[1], 0),
                        PointOnLineAtY(pair[0], pair[1], Screen.Height()), Color.red, 1)

def StartGame():
    Screen(800, 600)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
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
        angle = min(angle + random.random() * 0.3 + 0.15, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return Polygon(x, y, vertices)

merge = True
polygons = []
mergePolygons = []
intersectPolygons = []
cuttingLines = [
    # [Point(200, 200), Point(300, 300)],
    # [Point(600, 200), Point(500, 500)],
    # [Point(350, 100), Point(350, 200)],
    # [Point(0, 300), Point(100, 300)]
]
def BeginGame():
    global polygons, debugPoints

    for i in range(5):
        polygons.append(PolygonEntity(GeneratePolygon(100 + 400 * random.random(), 100 + 400 * random.random()), Color.all[i%len(Color.all)]))

    # vertices = [Point(318, 556), Point(304, 510), Point(251, 439), Point(219, 399), Point(219, 353), Point(236, 312),
    #             Point(305, 249), Point(330, 212), Point(399, 138), Point(501, 170), Point(505, 171), Point(473, 130),
    #             Point(389, 117), Point(328, 91), Point(252, 161), Point(198, 218), Point(174, 304), Point(154, 337),
    #             Point(183, 401), Point(195, 491), Point(267, 558), Point(307, 559)]
    # vertices = [Point(318, 556),Point(307, 559),Point(267, 558),Point(195, 491),Point(183, 401),Point(154, 337),Point(174, 304),Point(198, 218),Point(252, 161),Point(328, 91),Point(389, 117),Point(473, 130),Point(505, 171),Point(501, 170),Point(399, 138),Point(330, 212),Point(305, 249),Point(236, 312),Point(219, 353),Point(219, 399),Point(251, 439),Point(304, 510)]
    # polygon = Polygon.NewFromAbsolutePositions(vertices)
    # polygons.append(PolygonEntity(polygon, Color.yellow, 3))

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
        polygons[0].visible = not polygons[0].visible
        polygons[1].visible = not polygons[1].visible
        #RotatePolygons(0.5, polygons)

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
        if len(mergePolygons) > 0:
            for polygon in polygons:
                polygon.visible = True
            for polygon in mergePolygons:
                polygon.Destroy()
            mergePolygons = []
        else:
            mergePolygons = polygons[0].splitWithVelocity(cuttingLines)
            for polygon in polygons:
                polygon.visible = False

    if Screen.LeftMouseReleased() or Screen.KeyDown(pygame.K_y):
        mergePolygons = Polygon.Subtract(polygons[0], *polygons[1:])


    polygons[0].x = Screen.MousePosition().x
    polygons[0].y = Screen.MousePosition().y

def RenderGame():
    global mergePolygons, intersectPolygons, cuttingLines
    for i in range(len(mergePolygons)):
        mergePolygons[i].renderPolygon(Color.all[i%len(Color.all)], 3)
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
    Screen.AddUpdateFunction("main", UpdateGame)
    Screen.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
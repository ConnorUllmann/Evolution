from basics import Screen, Point, Color, QuadTree, RectanglesCollide
from random import random, seed
from time import time
from math import sin, cos, pi

rects = []
quadtree = None
leafNodes = []
debugRectInfo = None
debugRect = [Point(220, 320), Point(200, 150)]

def Begin():
    global rects, quadtree, debugRectInfo
    #seed(15)
    w = 1000
    h = 1000
    for i in range(w):
        for j in range(h):
            if random() < 0.999:
                continue
            width = max(20 * random(), 1)
            height = max(20 * random(), 1)
            x = Screen.Width() * i / (w - 1.0) - width / 2.0
            y = Screen.Height() * j / (h - 1.0) - height / 2.0
            rects.append([Point(x, y), Point(width, height), Color.light_red])
    debugRectInfo = rects[47]
    debugRectInfo[2] = Color.yellow

    quadtree = QuadTree(0, 0, Screen.Width(), Screen.Height())
    for rect in rects:
        quadtree.insertObjectWithBoundingBox(rect, rect[0].x, rect[0].y, rect[1].x, rect[1].y)


def Update():
    global rects, quadtree, leafNodes, debugRectInfo, debugRect

    # startTime = time()
    for rect in rects:
        rect[2] = Color.light_red
    #     objects = quadtree.collidingObjects(rect[0].x, rect[0].y, rect[1].x, rect[1].y)
    #     objects.remove(rect)
    # print("Quad tree: {}s".format(time() - startTime))

    # startTime = time()
    # for rectA in rects:
    #     for rectB in rects:
    #         if rectA != rectB:
    #             if RectanglesCollide(rectA[0].x, rectA[0].y, rectA[1].x, rectA[1].y, rectB[0].x, rectB[0].y, rectB[1].x, rectB[1].y):
    #                 pass
    # print("Brute force: {}s".format(time() - startTime))

    startTime = time()
    debugRect[0] = Screen.MousePosition() - debugRect[1] * 0.5
    debugRectCollidingObjects = quadtree.collidingObjects(debugRect[0].x, debugRect[0].y, debugRect[1].x, debugRect[1].y)
    for obj in debugRectCollidingObjects:
        obj[2] = Color.light_blue
    print("Quad tree: {}s".format(time() - startTime))

def Render():
    global rects, quadtree, leafNodes, debugRect
    for rect in rects:
        Screen.DrawRect(rect[0], rect[1], rect[2])

    Screen.DrawRect(debugRectInfo[0], debugRectInfo[1], debugRectInfo[2])
    Screen.DrawRect(debugRect[0], debugRect[1], Color.cyan, 3, filled=False)

    nodes = quadtree.collidingLeafNodes(debugRect[0].x, debugRect[0].y, debugRect[1].x, debugRect[1].y)
    for node in nodes:
        node.render()

    # quadtree.render()

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render)

from basics import Screen, Point, Color, QuadTree, RectanglesCollide
from random import random, seed
from time import time

rects = []
quadtree = None
leafNodes = []
debugRectInfo = None
debugRect = [Point(220, 320), Point(200, 150)]

def Begin():
    global rects, quadtree, debugRectInfo
    seed(15)
    for i in range(10000):
        width = max(8 * random(), 1)
        height = max(8 * random(), 1)
        x = Screen.Width() * random() - width / 2
        y = Screen.Height() * random() - height / 2
        rects.append([Point(x, y), Point(width, height), Color.light_red])
    debugRectInfo = rects[47]
    debugRectInfo[2] = Color.yellow

def Update():
    global rects, quadtree, leafNodes, debugRectInfo

    print("--")

    startTime = time()
    quadtree = QuadTree(0, 0, Screen.Width(), Screen.Height())
    for rect in rects:
        quadtree.insertObjectWithBoundingBox(rect, rect[0].x, rect[0].y, rect[1].x, rect[1].y)
    print("Insertion: {}s".format(time() - startTime))

    # leafNodes = quadtree.getLeafNodesCollidingObject(debugRectInfo)
    # for leafNode in leafNodes:
    #     leafNode.color = Color.blue

    startTime = time()
    collidingObjects = []
    for rect in rects:
        objects = quadtree.collidingObjects(rect[0].x, rect[0].y, rect[1].x, rect[1].y)
        objects.remove(rect)
        collidingObjects.append(objects)
    print("Quad tree: {}s".format(time() - startTime))
    sQuadTree = ""
    for collidingObject in collidingObjects:
        sQuadTree += str(len(collidingObject))
    # for collidingObject in collidingObjects:
    #     collidingObject[2] = Color.light_blue

    # startTime = time()
    # collidingObjects = []
    # for rectA in rects:
    #     collidingObjects.append([])
    #     for rectB in rects:
    #         if rectA != rectB:
    #             if RectanglesCollide(rectA[0].x, rectA[0].y, rectA[1].x, rectA[1].y, rectB[0].x, rectB[0].y, rectB[1].x, rectB[1].y):
    #                 collidingObjects[-1].append(rectB)
    # print("Brute force: {}s".format(time() - startTime))
    # sBruteForce = ""
    # for collidingObject in collidingObjects:
    #     sBruteForce += str(len(collidingObject))
    #
    # print("Same results: {}".format(sQuadTree == sBruteForce))

def Render():
    global rects, quadtree, leafNodes, debugRect
    for rect in rects:
        Screen.DrawRect(rect[0], rect[1], rect[2])

    Screen.DrawRect(debugRectInfo[0], debugRectInfo[1], debugRectInfo[2])
    Screen.DrawRect(debugRect[0], debugRect[1], Color.cyan, 3, filled=False)

    quadtree.render()
    # for node in leafNodes:
    #     node.render()

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render)

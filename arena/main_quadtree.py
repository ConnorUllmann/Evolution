from basics import Screen, Point, Color, QuadTree
from random import random

rects = []
quadtree = None
leafNodes = []
debugRectInfo = None
debugRect = [Point(200, 300), Point(200, 150)]

def Begin():
    global rects, quadtree, debugRectInfo
    for i in range(100):
        width = max(80 * random(), 10)
        height = max(80 * random(), 10)
        x = Screen.Width() * random() - width / 2
        y = Screen.Height() * random() - height / 2
        rects.append([Point(x, y), Point(width, height), Color.light_red])
    debugRectInfo = rects[47]
    debugRectInfo[2] = Color.yellow

def Update():
    global rects, quadtree, leafNodes, debugRectInfo
    quadtree = QuadTree(0, 0, Screen.Width(), Screen.Height())
    for rect in rects:
        quadtree.insertObjectWithBoundingBox(rect, rect[0].x, rect[0].y, rect[1].x, rect[1].y)

    collidingObjects = quadtree.collidingObjects(debugRect[0].x, debugRect[0].y, debugRect[1].x, debugRect[1].y)
    for collidingObject in collidingObjects:
        collidingObject[2] = Color.light_blue

    leafNodes = quadtree.collidingLeafNodes(debugRectInfo)
    for leafNode in leafNodes:
        leafNode.color = Color.blue

def Render():
    global rects, quadtree, leafNodes, debugRect
    for rect in rects:
        Screen.DrawRect(rect[0], rect[1], rect[2])

    Screen.DrawRect(debugRectInfo[0], debugRectInfo[1], debugRectInfo[2])
    Screen.DrawRect(debugRect[0], debugRect[1], Color.cyan, 3, filled=False)

    #quadtree.render()
    for node in leafNodes:
        node.render()

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render)

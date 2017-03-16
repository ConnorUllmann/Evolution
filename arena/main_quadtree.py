from basics import Screen, Point, Color, QuadTree
from random import random

rects = []
quadtree = None


def Begin():
    global rects, quadtree
    for i in range(100):
        rects.append([Point(Screen.Width() * random(), Screen.Height() * random()), Point(30, 30)])


def Update():
    global rects, quadtree
    quadtree = QuadTree(0, 0, Screen.Width(), Screen.Height())
    for rect in rects:
        quadtree.insertObjectWithBoundingBox(rect[0].x, rect[0].y, rect[1].x, rect[1].y, rect)
    #quadtree.printContentLengths()

def Render():
    global rects, quadtree
    for rect in rects:
        Screen.DrawRect(rect[0], rect[1], Color.light_blue)
    quadtree.render()

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render)

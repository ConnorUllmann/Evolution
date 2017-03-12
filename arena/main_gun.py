from basics import Screen, Point, Softbody
from gunner import Gunner
import random
from math import pi

def GeneratePolygonVertices():
    vertices = []
    angle = 0
    while angle < 2 * pi:
        length = random.random() * 20 + 100
        angle = min(angle + random.random() * 0.2 + 0.1, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return vertices

def Begin():
    vertices = GeneratePolygonVertices()
    softbody = Softbody(Screen.Width() / 2, Screen.Height() / 2, vertices)
    #softbody.addRandomSupportRods(20)

    gunner = Gunner(Screen.Width() / 4, Screen.Height() / 4)

def Update():
    pass

def Render():
    pass

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render)
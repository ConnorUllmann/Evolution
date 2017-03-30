from basics import Screen, Point, Softbody, Color
from gunner import Gunner
import random
from time import time
from math import pi, sin

random.seed(15)

def GeneratePolygonVertices():
    vertices = []
    angle = 0
    while angle < 2 * pi:
        length = random.random() * 40 + 50
        angle = min(angle + random.random() * 0.6 + 0.2, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return vertices

def GenerateSoftbody(x, y):
    softbody = Softbody(x, y, GeneratePolygonVertices())
    softbody.addStandardSupportRods()
    return softbody

softbodies = []
mousePositionClick = None

def Begin():
    global softbodies
    A = GenerateSoftbody(Screen.Width()/4, Screen.Height()*3/4)
    B = GenerateSoftbody(Screen.Width()*3/4, Screen.Height()*3/4)

    A.v = Point(7.5, -5)
    B.v = Point(-1, -5)

    softbodies = [A, B]

    #gunner = Gunner(Screen.Width() / 2, Screen.Height() / 4)

def Update():
    global softbodies, mousePositionClick

    softbodiesTemp = []
    softbodiesCount = len(softbodies)
    for i in range(softbodiesCount):
        A = softbodies[i]
        for j in range(i+1, softbodiesCount):
            B = softbodies[j]

            if not A.destroyed and not B.destroyed and A.collide(B):
                A.v *= 0.5
                B.v *= 0.5

                if A.v.lengthSq < 1 and B.v.lengthSq < 1:
                    mergeSoftbodies = A.merge(B)
                    for softbody in mergeSoftbodies:
                        softbody.addRandomSupportRods((len(softbody.vertices) - len(softbody.rodsSupport)) / 2)
                        softbodiesTemp.append(softbody)
                    A.Destroy()
                    B.Destroy()
        if not A.destroyed:
            softbodiesTemp.append(A)
    softbodies = softbodiesTemp

    if Screen.LeftMousePressed():
        mousePositionClick = Screen.MousePosition()
    if Screen.LeftMouseReleased():
        mousePosition = Screen.MousePosition()
        softbody = GenerateSoftbody(*mousePositionClick)
        softbody.v = (mousePosition - mousePositionClick) / 35
        softbodies.append(softbody)
        mousePositionClick = None

def Render():
    if mousePositionClick is not None:
        Screen.DrawLine(mousePositionClick, Screen.MousePosition(), Color.white)
        Screen.DrawCircle(mousePositionClick, 3 + sin(time()), Color.white)

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render)
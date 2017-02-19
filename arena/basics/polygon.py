from .point import Point
from .entity import Entity
from .screen import Screen
from .utils import *


def Drawable(vertices, offset=Point()):
    verticesTemp = []
    if len(vertices) > 0:
        for vertex in vertices:
            verticesTemp.append((offset.x + vertex.x, offset.y + vertex.y))
        verticesTemp.append(verticesTemp[0])
    return verticesTemp

class Polygon:

    def __init__(self, vertices=[]):
        self.vertices = list(vertices)

class PolygonEntity(Polygon, Entity):

    def contains(self, point):
        start = Point(-10**9, -10**9)
        intersectionPoints = []
        for i in range(len(self.vertices)):
            a = self + self.vertices[i]
            b = self + self.vertices[(i+1)%len(self.vertices)]
            p = LinesIntersectionPoint(a, b, start, point, True)
            if p is not None:
                intersectionPoints.append(p)
        return len(intersectionPoints) % 2

    def contains2(self, point):
        total = 0
        for i in range(len(self.vertices)):
            a = self + self.vertices[i] - point
            b = self + self.vertices[(i+1)%len(self.vertices)] - point
            total += AngleDiff(a.radians, b.radians)
        return abs(total) > 0.001

    def VerticesWithIntersectionPoints(self, other):
        allIntersectionPoints = []
        for i in range(len(self.vertices)):
            a = self + self.vertices[i]
            b = self + self.vertices[(i+1)%len(self.vertices)]
            intersectionPoints = []
            for j in range(len(other.vertices)):
                m = other + other.vertices[j]
                n = other + other.vertices[(j+1)%len(other.vertices)]
                p = LinesIntersectionPoint(a, b, m, n, True)
                if p is not None:
                    intersectionPoints.append(p)
            intersectionPoints.sort(key = lambda x: (x - a).lengthSq)
            allIntersectionPoints.append(a)
            allIntersectionPoints.extend(intersectionPoints)
        return allIntersectionPoints

    def Traverse(self, other):
        return self.TraverseHandoff(other, 0, self.VerticesWithIntersectionPoints(other), other.VerticesWithIntersectionPoints(self), [[]], None, Drawable(self.vertices, self), Drawable(other.vertices, other))

    def TraverseHandoff(self, other, index, verticesA, verticesB, polygonPoints, nowInside, uncheckedA, uncheckedB):
        i = index
        while True:
            a = verticesA[i%len(verticesA)]
            b = verticesA[(i+1)%len(verticesA)]
            c = (a + b)/2

            if a in uncheckedA:
                uncheckedA.remove(a)
            if a in uncheckedB:
                uncheckedB.remove(a)

            if nowInside is None:
                nowInside = other.contains(a)
                if nowInside:
                    polygonPoints[-1].append(a)
            else:
                finishedPolygon = len(polygonPoints[-1]) > 0 and a == polygonPoints[-1][0]
                if finishedPolygon:
                    if len(uncheckedA) > 0:
                        return self.TraverseHandoff(other, verticesA.index(uncheckedA.pop(0)), verticesA, verticesB, polygonPoints+[[]], None, uncheckedA, uncheckedB)
                    if len(uncheckedB) > 0:
                        return other.TraverseHandoff(self, verticesB.index(uncheckedB.pop(0)), verticesB, verticesA, polygonPoints+[[]], None, uncheckedB, uncheckedA)
                    return polygonPoints

                wasInside = nowInside
                nowInside = other.contains(c)
                if nowInside:
                    polygonPoints[-1].append(a)
                elif wasInside:
                    if a in verticesB:
                        return other.TraverseHandoff(self, verticesB.index(a), verticesB, verticesA, polygonPoints, False, uncheckedB, uncheckedA)
            i += 1
        return polygonPoints

    def IntersectionPolygon(self, other, color):

        polygonsPoints = self.Traverse(other)

        s = ""
        for polygonPoints in polygonsPoints:
            s += "points[{}]: ".format(len(polygonPoints))
            for pt in polygonPoints:
                s += "(" + str(int(pt.x)) + ", " + str(int(pt.y)) + ")"
            s += "\n"
        print("intersectionPolygon[{}] poly points={}".format(len(polygonPoints), s))

        print(len(polygonsPoints))
        for polygonVertices in polygonsPoints:
            if len(polygonVertices) > 1:
                Screen.DrawLines(Drawable(polygonVertices), color, 4)

    def __init__(self, x, y, vertices=[], color=(255, 255, 255), thickness=1):
        Polygon.__init__(self, vertices)
        Entity.__init__(self, x, y)
        self.color = color
        self.thickness = thickness
        self.angle = 0

    def Render(self):
        if len(self.vertices) > 1:
            Screen.DrawLines(Drawable(self.vertices, self), self.color, self.thickness)
        for i in range(len(self.vertices)):
            vertex = self.vertices[i]
            Screen.DrawCircle(self + vertex, 2+i, (255, 255, 255))
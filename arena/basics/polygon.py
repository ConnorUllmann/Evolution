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
        self.vertices = vertices

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

    def Traverse(self, other, verticesA, verticesB):
        return self.TraverseHandoff(other, 0, verticesA, verticesB, [[]], None)

    def TraverseHandoff(self, other, index, verticesA, verticesB, polygonPoints, nowInside):
        i = index
        while True:
            a = verticesA[i%len(verticesA)]
            b = verticesA[(i+1)%len(verticesA)]
            c = (a + b)/2

            if nowInside is None:
                nowInside = other.contains(a)
                if nowInside:
                    polygonPoints[-1].append(a)
                i += 1
                continue

            wasInside = nowInside
            nowInside = other.contains(c)
            if nowInside:
                if len(polygonPoints[-1]) > 0 and a in polygonPoints[-1]:
                    polygonPoints.append([])
                    break
                else:
                    polygonPoints[-1].append(a)
            elif wasInside:
                if a in verticesB:
                    other.TraverseHandoff(self, verticesB.index(a), verticesB, verticesA, polygonPoints, False)
                    break
            i += 1
        return polygonPoints

class PolygonEntity(Polygon, Entity):

    def IntersectionPolygon(self, other, color):
        verticesA = self.VerticesWithIntersectionPoints(other)
        verticesB = other.VerticesWithIntersectionPoints(self)

        polygonsPoints = self.Traverse(other, verticesA, verticesB)

        for polygonVertices in polygonsPoints:
            if len(polygonVertices) > 1:
                Screen.DrawLines(Drawable(polygonVertices), color, 2)

    def __init__(self, x, y, vertices=[], color=(255, 255, 255), thickness=1):
        Polygon.__init__(self, vertices)
        Entity.__init__(self, x, y)
        self.color = color
        self.thickness = thickness

    def Render(self):
        if len(self.vertices) > 1:
            Screen.DrawLines(Drawable(self.vertices, self), self.color, self.thickness)
        for i in range(len(self.vertices)):
            vertex = self.vertices[i]
            Screen.DrawCircle(self + vertex, 2+i, (255, 255, 255))
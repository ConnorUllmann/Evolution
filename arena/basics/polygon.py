from .point import Point
from .entity import Entity
from .screen import Screen
from .utils import *
from random import randint


def Drawable(vertices, offset=Point()):
    verticesTemp = []
    if len(vertices) > 0:
        for vertex in vertices:
            verticesTemp.append((offset.x + vertex.x, offset.y + vertex.y))
        verticesTemp.append(verticesTemp[0])
    return verticesTemp

class Polygon:

    def __init__(self, vertices = []):
        self.vertices = list(vertices)

    def centerOfMassRelative(self):
        midPoint = Point()
        for vertex in self.vertices:
            midPoint += vertex
        return midPoint / len(self.vertices)

    def centerVertices(self):
        centerOfMass = self.centerOfMassRelative()
        for vertex in self.vertices:
            vertex -= centerOfMass

    def rotateRadians(self, radians):
        centerOfMass = self.centerOfMassRelative()
        for vertex in self.vertices:
            vertex.rotateRadians(radians, centerOfMass)


class PolygonEntity(Polygon, Entity):

    def contains(self, point, offset):
        total = 0
        for i in range(len(self.vertices)):
            a = offset + self.vertices[i] - point
            b = offset + self.vertices[(i+1)%len(self.vertices)] - point
            total += AngleDiff(a.radians, b.radians)
        return abs(total) > 0.001

    def AbsolutePolygonPointPositionsWithIntersections(self, other, offsetA, offsetB):
        allIntersectionPoints = []
        for i in range(len(self.vertices)):
            a = offsetA + self.vertices[i]
            b = offsetA + self.vertices[(i+1)%len(self.vertices)]
            intersectionPoints = []
            for j in range(len(other.vertices)):
                m = offsetB + other.vertices[j]
                n = offsetB + other.vertices[(j+1)%len(other.vertices)]
                p = LinesIntersectionPoint(a, b, m, n, True)
                if p is not None:
                    intersectionPoints.append(p)
            intersectionPoints.sort(key = lambda x: (x - a).lengthSq)
            allIntersectionPoints.append(a)
            allIntersectionPoints.extend(intersectionPoints)
        return allIntersectionPoints

    #Returns list of polygon point sets formed by the intersection or the merging of two polygons (depending on the boolean "merge" property)
    @staticmethod
    def Traverse(merge, A, B):
        polygonPoints = PolygonEntity.TraverseHandoff(merge, A, B, A.AbsolutePolygonPointPositionsWithIntersections(B, A, B), B.AbsolutePolygonPointPositionsWithIntersections(A, B, A), Drawable(A.vertices, A)[:-1], Drawable(B.vertices, B)[:-1], [], 0, [[]], None)
        if len(polygonPoints) > 0 and len(polygonPoints[-1]) <= 0:
            polygonPoints = polygonPoints[:-1]
        return polygonPoints

    @staticmethod
    def TraverseHandoff(merge, A, B, verticesA, verticesB, uncheckedA, uncheckedB, addedIntersections, index, polygonPoints, nowInside):
        if len(verticesA) <= 0 or len(verticesB) <= 0:
            return polygonPoints
        i = index
        polygon = polygonPoints[-1]
        while True:
            a = verticesA[i%len(verticesA)]
            b = verticesA[(i+1)%len(verticesA)]
            c = (a + b)/2

            if a in uncheckedA:
                uncheckedA.remove(a)
            if a in uncheckedB:
                uncheckedB.remove(a)

            if nowInside is None:
                if B.contains(a, B) ^ merge:
                    polygon.append(a)
                nowInside = B.contains(c, B) ^ merge
            else:
                finishedPolygon = len(polygon) > 0 and a == polygon[0]
                if finishedPolygon:
                    polygonPoints += [[]]
                    break

                wasInside = nowInside
                nowInside = B.contains(c, B) ^ merge
                if nowInside:
                    if a in addedIntersections:
                        break
                    elif a in verticesA and a in verticesB:
                        addedIntersections.append(a)
                    polygon.append(a)
                elif wasInside:
                    if a in verticesB:
                        return PolygonEntity.TraverseHandoff(merge, B, A, verticesB, verticesA, uncheckedB, uncheckedA, addedIntersections, verticesB.index(a), polygonPoints, nowInside)
                elif len(polygon) <= 0:
                    break

            i += 1

        if len(uncheckedA) > 0:
            return PolygonEntity.TraverseHandoff(merge, A, B, verticesA, verticesB, uncheckedA, uncheckedB, addedIntersections, verticesA.index(uncheckedA[0]), polygonPoints, None)
        if len(uncheckedB) > 0:
            return PolygonEntity.TraverseHandoff(merge, B, A, verticesB, verticesA, uncheckedB, uncheckedA, addedIntersections, verticesB.index(uncheckedB[0]), polygonPoints, None)
        return polygonPoints

    @staticmethod
    def CombineTwo(merge, A, B):
        polygonsPoints = PolygonEntity.Traverse(merge, A, B)
        polygons = []
        for polygonPoints in polygonsPoints:
            polygons.append(PolygonEntity.FromAbsoluteCoordinates(polygonPoints, (randint(0, 255), randint(0, 255), randint(0, 255)), 5))
        return polygons

    @staticmethod
    def Combine(merge, *args):
        polygons = PolygonEntity.CombineTwo(merge, args[0], args[1])
        for i in range(2, len(args)):
            C = args[i]
            polygonsTemp = []
            for polygon in polygons:
                polygon.Destroy()
            for polygon in polygons:
                temp = PolygonEntity.CombineTwo(merge, C, polygon)
                polygonsTemp.extend(temp)
            polygons = polygonsTemp
        return polygons

    #Returns the merging of all polygon arguments
    @staticmethod
    def Merge(*args):
        return PolygonEntity.Combine(True, *args)

    #Returns the instersection of all polygon arguments
    @staticmethod
    def Intersect(*args):
        return PolygonEntity.Combine(False, *args)

    def __init__(self, x, y, vertices=[], color=(255, 255, 255), thickness=1):
        Polygon.__init__(self, vertices)
        Entity.__init__(self, x, y)
        self.color = color
        self.thickness = thickness
        self.angle = 0
        self.visible = True

    @staticmethod
    def FromAbsoluteCoordinates(vertices, color=(255, 255, 255), thickness=1):
        p = PolygonEntity(0, 0, vertices, color, thickness)
        p.position = p.centerOfMassRelative()
        p.centerVertices()
        return p

    def Render(self):
        if self.visible:
            if len(self.vertices) > 1:
                Screen.DrawLines(Drawable(self.vertices, self), self.color, self.thickness)
            for i in range(len(self.vertices)):
                vertex = self.vertices[i]
                Screen.DrawCircle(self + vertex, 2, (255, 255, 255))
from .entity import Entity
from .screen import Screen
from .utils import *
from .color import Color

class Polygon(Point):

    @staticmethod
    def NewFromPolygon(polygon):
        v = []
        for vertex in polygon.vertices:
            v.append(Point(vertex.x, vertex.y))
        p = Polygon(polygon.x, polygon.y, v)
        return p

    @staticmethod
    def NewFromAbsolutePositions(vertices):
        p = Polygon(0, 0, vertices)
        p.position = p.centerOfMassRelative()
        p.centerVertices()
        return p

    def __str__(self):
        s = "["
        for v in self.vertices:
            s += str(Point(self.x + v.x, self.y + v.y, True))+","
        s = s[:-1]
        s += "]"
        return s

    def __init__(self, x=0, y=0, vertices=[]):
        Point.__init__(self, x, y)
        self.vertices = vertices

    def renderPolygon(self, color, thickness):
        if len(self.vertices) > 1:
            verticesTemp = []
            for vertex in self.vertices:
                verticesTemp.append((self.x + vertex.x, self.y + vertex.y))
            verticesTemp.append(verticesTemp[0])
            Screen.DrawLines(verticesTemp, color, thickness)
            count = len(self.vertices)
            for i in range(count):
                Screen.DrawCircle(self + self.vertices[i], 2+3 * (i/(count-1)), color)

    def verticesAbsolute(self):
        vertices = []
        for vertex in self.vertices:
            vertices.append(self + vertex)
        return vertices

    def centerOfMassRelative(self):
        midPoint = Point()
        for vertex in self.vertices:
            midPoint += vertex
        return midPoint / max(1, len(self.vertices))

    def centerOfMassAbsolute(self):
        return self + self.centerOfMassRelative()

    def centerVertices(self):
        centerOfMass = self.centerOfMassRelative()
        for vertex in self.vertices:
            vertex -= centerOfMass

    def rotateRadians(self, radians, center=None):
        centerOfMass = self.centerOfMassRelative() if center is None else (center - self)
        for vertex in self.vertices:
            vertex.rotateRadians(radians, centerOfMass)

    def contains(self, point):
        total = 0
        for i in range(len(self.vertices)):
            a = self + self.vertices[i] - point
            b = self + self.vertices[(i + 1) % len(self.vertices)] - point
            total += AngleDiff(a.radians, b.radians)
        return abs(total) > 0.001

    @property
    def empty(self):
        return len(self.vertices) <= 0

    @staticmethod
    def AbsolutePolygonPointPositionsAndIntersections(A, B, merge, withIncomingIntersections):
        allPoints = []
        allIntersectionIndices = []
        verticesA = A.verticesAbsolute()
        verticesB = B.verticesAbsolute()
        for i in range(len(verticesA)):
            a = verticesA[i]
            b = verticesA[(i + 1) % len(verticesA)]
            intersectionPoints = []
            for j in range(len(verticesB)):
                m = verticesB[j]
                n = verticesB[(j + 1) % len(verticesB)]
                p = LinesIntersectionPoint(a, b, m, n, True)
                if p is not None:
                    intersectionPoints.append(p)
            intersectionPoints.sort(key=lambda x: (x - a).lengthSq)

            allPoints.append(a)
            for intersection in intersectionPoints:
                if withIncomingIntersections:
                    allIntersectionIndices.append(len(allPoints))
                allPoints.append(intersection)

        if not withIncomingIntersections:
            return allPoints

        count = len(allPoints)
        incomingIntersections = []
        for index in allIntersectionIndices:
            intersection = allPoints[index]
            intersectionP = allPoints[(index - 1 + count) % count]
            intersectionN = allPoints[(index + 1) % count]
            insideP = B.contains((intersection + intersectionP) / 2)
            insideN = B.contains((intersection + intersectionN) / 2)
            if (insideN and not insideP) ^ merge:
                incomingIntersections.append(intersection)

        return [allPoints, incomingIntersections]

    @staticmethod
    def TraverseHandoff(merge, A, B, verticesA, verticesB, intersections, startPolygon, index, polygonPoints):
        i = index
        polygon = polygonPoints[-1]
        while True:
            a = verticesA[i%len(verticesA)]
            b = verticesA[(i+1)%len(verticesA)]

            if a in intersections:
                intersections.remove(a)

            if len(polygon) > 0 and a == polygon[0]:
                if len(intersections) > 0:
                    if startPolygon == A:
                        return Polygon.TraverseHandoff(merge, A, B, verticesA, verticesB, intersections, startPolygon, verticesA.index(intersections[0]), polygonPoints+[[]])
                    else:
                        return Polygon.TraverseHandoff(merge, B, A, verticesB, verticesA, intersections, startPolygon, verticesB.index(intersections[0]), polygonPoints+[[]])
                return polygonPoints

            if B.contains((a + b)/2) ^ merge:
                polygon.append(a)
            else:
                if a in verticesB:
                    return Polygon.TraverseHandoff(merge, B, A, verticesB, verticesA, intersections, startPolygon, verticesB.index(a), polygonPoints)
            i += 1

    #Returns list of polygon point sets formed by the intersection or the merging of two polygons (depending on the boolean "merge" property)
    @staticmethod
    def Traverse(merge, A, B):
        #Return case where one of the polygons is empty
        Aempty = A.empty
        Bempty = B.empty
        if merge:
            if Aempty and Bempty:
                return []
            elif Aempty:
                return [B.verticesAbsolute()]
            elif Bempty:
                return [A.verticesAbsolute()]
        else:
            if Aempty or Bempty:
                return []

        verticesA, incomingIntersectionsA = Polygon.AbsolutePolygonPointPositionsAndIntersections(A, B, merge, True)
        verticesB = Polygon.AbsolutePolygonPointPositionsAndIntersections(B, A, merge, False)

        #Return case where the polygons are identical
        ABsame = True
        if len(verticesA) == len(verticesB):
            for vertex in verticesA:
                if vertex not in verticesB:
                    ABsame = False
                    break
        else:
            ABsame = False
        if ABsame:
            return [A.verticesAbsolute()]

        #Return case where one polygon is inside the other or they do not touch
        if len(incomingIntersectionsA) <= 0:
            for vertex in verticesB:
                if vertex not in verticesA and A.contains(vertex):
                    return [A.verticesAbsolute()] if merge else [B.verticesAbsolute()]
            for vertex in verticesA:
                if vertex not in verticesB and B.contains(vertex):
                    return [B.verticesAbsolute()] if merge else [A.verticesAbsolute()]
            return [A.verticesAbsolute(), B.verticesAbsolute()] if merge else []

        polygonPoints = Polygon.TraverseHandoff(merge, A, B, verticesA, verticesB, incomingIntersectionsA, A, verticesA.index(incomingIntersectionsA[0]), [[]])

        #If we started a polygon but didn't finish it, chop it off
        if len(polygonPoints) > 0 and len(polygonPoints[-1]) <= 0:
            polygonPoints = polygonPoints[:-1]
        return polygonPoints

    @staticmethod
    def CombineTwo(merge, A, B):
        polygonsPoints = Polygon.Traverse(merge, A, B)
        polygons = []
        for polygonPoints in polygonsPoints:
            polygons.append(Polygon.NewFromAbsolutePositions(polygonPoints))
        return polygons

    @staticmethod
    def Merge(A, B):
        return Polygon.CombineTwo(True, A, B)

    @staticmethod
    def Intersect(A, B):
        return Polygon.CombineTwo(False, A, B)


class PolygonEntity(Polygon, Entity):

    def __init__(self, polygon, color=(255, 255, 255), thickness=1):
        Polygon.__init__(self, polygon.x, polygon.y, polygon.vertices)
        Entity.__init__(self, polygon.x, polygon.y)
        self.color = color
        self.thickness = thickness
        self.angle = 0
        self.visible = True

    def __str__(self):
        return Entity.__str__(self) + Polygon.__str__(self)

    def Render(self):
        if self.visible:
            self.renderPolygon(self.color, self.thickness)
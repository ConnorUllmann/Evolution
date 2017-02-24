from .entity import Entity
from .screen import Screen
from .utils import *

class Polygon(Point):

    def __init__(self, x=0, y=0, vertices = []):
        Point.__init__(self, x, y)
        self.vertices = list(vertices)

    @staticmethod
    def NewFromAbsolutePositions(vertices):
        p = Polygon(0, 0, vertices)
        p.position = p.centerOfMassRelative()
        p.centerVertices()
        return p

    def centerOfMassRelative(self):
        midPoint = Point()
        for vertex in self.vertices:
            midPoint += vertex
        return midPoint / max(1, len(self.vertices))

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

    def AbsolutePolygonPointPositionsWithIntersections(self, other, merge):
        allPoints = []
        for i in range(len(self.vertices)):
            a = self + self.vertices[i]
            b = self + self.vertices[(i + 1) % len(self.vertices)]
            intersectionPoints = []
            for j in range(len(other.vertices)):
                m = other + other.vertices[j]
                n = other + other.vertices[(j + 1) % len(other.vertices)]
                p = LinesIntersectionPoint(a, b, m, n, True)
                if p is not None:
                    intersectionPoints.append(p)
            intersectionPoints.sort(key = lambda x: (x - a).lengthSq)

            allPoints.append([a, False])
            for intersection in intersectionPoints:
                allPoints.append([intersection, True])

        count = len(allPoints)
        for i in range(count):
            if allPoints[i][1]:
                insideP = other.contains(0.5 * (allPoints[i][0] + allPoints[(i - 1 + count)%count][0]))
                insideN = other.contains(0.5 * (allPoints[i][0] + allPoints[(i + 1) % count][0]))
                allPoints[i][1] = insideN and not insideP
        return allPoints

    #Returns list of polygon point sets formed by the intersection or the merging of two polygons (depending on the boolean "merge" property)
    @staticmethod
    def Traverse(merge, A, B):
        allPointsA = A.AbsolutePolygonPointPositionsWithIntersections(B, merge)
        allPointsB = B.AbsolutePolygonPointPositionsWithIntersections(A, merge)

        if len(allPointsA) <= 0:
            return [[]]

        verticesA = []
        for point in allPointsA:
            verticesA.append(point[0])
        verticesB = []
        for point in allPointsB:
            verticesB.append(point[0])

        intersectionsA = []
        for point in allPointsA:
            if point[1]:
                intersectionsA.append((point[0], A))

        if len(intersectionsA) <= 0:
            return [[]]

        index = verticesA.index(intersectionsA.pop(0)[0])
        polygonPoints = Polygon.TraverseHandoff(merge, A, B, verticesA, verticesB, intersectionsA, index, [[]], merge)

        if len(polygonPoints) > 0 and len(polygonPoints[-1]) <= 0:
            polygonPoints = polygonPoints[:-1]
        return polygonPoints


    @staticmethod
    def TraverseHandoff(merge, A, B, verticesA, verticesB, intersections, index, polygonPoints, nowInside):
        i = index
        polygon = polygonPoints[-1]
        while True:
            a = verticesA[i%len(verticesA)]
            b = verticesA[(i+1)%len(verticesA)]

            jRemove = None
            for j in range(len(intersections)):
                if intersections[j][0] == a:
                    jRemove = j
                    break
            if jRemove is not None:
                intersections.pop(j)

            if len(polygon) > 0 and a == polygon[0]:
                break

            wasInside = nowInside
            nowInside = B.contains((a + b)/2) ^ merge
            if nowInside:
                polygon.append(a)
            elif wasInside:
                if a in verticesB:
                    return Polygon.TraverseHandoff(merge, B, A, verticesB, verticesA, intersections, verticesB.index(a), polygonPoints, False)
            i += 1

        if len(intersections) > 0:
            intersection = intersections.pop(0)
            if intersection[1] == A:
                return Polygon.TraverseHandoff(merge, A, B, verticesA, verticesB, intersections, verticesA.index(intersection[0]), polygonPoints+[[]], False)
            else:
                return Polygon.TraverseHandoff(merge, B, A, verticesB, verticesA, intersections, verticesB.index(intersection[0]), polygonPoints+[[]], False)
        return polygonPoints

    @staticmethod
    def CombineTwo(merge, A, B):
        polygonsPoints = Polygon.Traverse(merge, A, B)
        polygons = []
        for polygonPoints in polygonsPoints:
            polygons.append(Polygon.NewFromAbsolutePositions(polygonPoints))
        return polygons

    @staticmethod
    def Combine(merge, *args):
        polygons = Polygon.CombineTwo(merge, args[0], args[1])
        for i in range(2, len(args)):
            C = args[i]
            polygonsTemp = []
            for polygon in polygons:
                polygonsTemp.extend(Polygon.CombineTwo(merge, C, polygon))
            polygons = polygonsTemp
        return polygons

    #Returns the merging of all polygon arguments
    @staticmethod
    def Merge(*args):
        return Polygon.Combine(True, *args)

    #Returns the instersection of all polygon arguments
    @staticmethod
    def Intersect(*args):
        return Polygon.Combine(False, *args)

    def RenderPolygon(self, color, thickness):
        if len(self.vertices) > 1:
            verticesTemp = []
            for vertex in self.vertices:
                verticesTemp.append((self.x + vertex.x, self.y + vertex.y))
            verticesTemp.append(verticesTemp[0])
            Screen.DrawLines(verticesTemp, color, thickness)
        #for i in range(len(self.vertices)):
        #    Screen.DrawCircle(self + self.vertices[i], 2, color)


class PolygonEntity(Polygon, Entity):

    def __init__(self, polygon, color=(255, 255, 255), thickness=1):
        Polygon.__init__(self, polygon.x, polygon.y, polygon.vertices)
        Entity.__init__(self, polygon.x, polygon.y)
        self.color = color
        self.thickness = thickness
        self.angle = 0
        self.visible = True


    def Render(self):
        if self.visible:
            self.RenderPolygon(self.color, self.thickness)
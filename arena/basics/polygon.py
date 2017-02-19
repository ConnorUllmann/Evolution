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

    def Traverse(self, other, verticesA, verticesB):
        polygonPoints = self.TraverseHandoff(other, 0, verticesA, verticesB, [[]], None, Drawable(self.vertices, self)[:-1], Drawable(other.vertices, other)[:-1], [])
        if len(polygonPoints) > 0 and len(polygonPoints[-1]) <= 0:
            polygonPoints = polygonPoints[:-1]
        return polygonPoints

    def TraverseHandoff(self, other, index, verticesA, verticesB, polygonPoints, nowInside, uncheckedA, uncheckedB, addedIntersections):
        debug = False
        nameA = "A" if self.color==(128, 255, 128) else "B"
        nameB = "B" if nameA == "A" else "A"
        i = index
        polygon = polygonPoints[-1]
        while True:
            a = verticesA[i%len(verticesA)]
            b = verticesA[(i+1)%len(verticesA)]
            c = (a + b)/2

            if debug:
                print("{}{}".format(nameA, i%len(verticesA)))

            if a in uncheckedA:
                if debug:
                    print("{}{} removed from unchecked{} index:{}".format(nameA, i%len(verticesA), nameA, uncheckedA.index(a)))
                uncheckedA.remove(a)
            if a in uncheckedB:
                if debug:
                    print("{}{} removed from unchecked{} index:{}".format(nameA, i%len(verticesA), nameB, uncheckedB.index(a)))
                uncheckedB.remove(a)

            if nowInside is None:
                if other.contains(a):
                    if debug:
                        print("added {}{} to polygon {}".format(nameA, i%len(verticesA), polygonPoints.index(polygon)))
                    polygon.append(a)
                nowInside = other.contains(c)
            else:
                finishedPolygon = len(polygon) > 0 and a == polygon[0]
                if finishedPolygon:
                    if debug:
                        print("(new polygon) unchecked ([{}]{} [{}]{})".format(len(uncheckedA), nameA, len(uncheckedB), nameB))
                        for ptA in uncheckedA:
                            print(" {}{}".format(nameA, verticesA.index(ptA)))
                        print(" --- ")
                        for ptB in uncheckedB:
                            print(" {}{}".format(nameB, verticesB.index(ptB)))
                    if len(uncheckedA) > 0:
                        return self.TraverseHandoff(other, verticesA.index(uncheckedA[0]), verticesA, verticesB, polygonPoints+[[]], None, uncheckedA, uncheckedB, addedIntersections)
                    if len(uncheckedB) > 0:
                        return other.TraverseHandoff(self, verticesB.index(uncheckedB[0]), verticesB, verticesA, polygonPoints+[[]], None, uncheckedB, uncheckedA, addedIntersections)
                    return polygonPoints

                wasInside = nowInside
                nowInside = other.contains(c)
                if nowInside:
                    if debug:
                        print("added {}{} to polygon {}".format(nameA, i%len(verticesA), polygonPoints.index(polygon)))
                    if a in addedIntersections:
                        if debug:
                            print("unchecked ([{}]{} [{}]{})".format(len(uncheckedA), nameA, len(uncheckedB), nameB))
                            for ptA in uncheckedA:
                                print(" {}{}".format(nameA, verticesA.index(ptA)))
                            print(" --- ")
                            for ptB in uncheckedB:
                                print(" {}{}".format(nameB, verticesB.index(ptB)))
                        if len(uncheckedA) > 0:
                            return self.TraverseHandoff(other, verticesA.index(uncheckedA[0]), verticesA, verticesB, polygonPoints, None, uncheckedA, uncheckedB, addedIntersections)
                        if len(uncheckedB) > 0:
                            return other.TraverseHandoff(self, verticesB.index(uncheckedB[0]), verticesB, verticesA, polygonPoints, None, uncheckedB, uncheckedA, addedIntersections)
                        return polygonPoints
                    elif a in verticesA and a in verticesB:
                        addedIntersections.append(a)
                    polygon.append(a)
                elif wasInside:
                    if a in verticesB:
                        if debug:
                            print("handoff to other")
                        return other.TraverseHandoff(self, verticesB.index(a), verticesB, verticesA, polygonPoints, nowInside, uncheckedB, uncheckedA, addedIntersections)
                elif len(polygon) <= 0:
                    if debug:
                        print("unchecked ([{}]{} [{}]{})".format(len(uncheckedA), nameA, len(uncheckedB), nameB))
                        for ptA in uncheckedA:
                            print(" {}{}".format(nameA, verticesA.index(ptA)))
                        print(" --- ")
                        for ptB in uncheckedB:
                            print(" {}{}".format(nameB, verticesB.index(ptB)))
                    if len(uncheckedA) > 0:
                        return self.TraverseHandoff(other, verticesA.index(uncheckedA[0]), verticesA, verticesB, polygonPoints, None, uncheckedA, uncheckedB, addedIntersections)
                    if len(uncheckedB) > 0:
                        return other.TraverseHandoff(self, verticesB.index(uncheckedB[0]), verticesB, verticesA, polygonPoints, None, uncheckedB, uncheckedA, addedIntersections)
                    return polygonPoints

            i += 1

    def IntersectionPolygon(self, other, color):
        verticesA = self.VerticesWithIntersectionPoints(other)
        verticesB = other.VerticesWithIntersectionPoints(self)

        # print("verticesA:")
        # for i in range(len(verticesA)):
        #     print("A{} = {}".format(i, verticesA[i]))
        # print("verticesB:")
        # for i in range(len(verticesB)):
        #     print("B{} = {}".format(i, verticesB[i]))

        polygonsPoints = self.Traverse(other, verticesA, verticesB)

        s = ""
        # for polygonPoints in polygonsPoints:
        #     s += "points[{}]:\n".format(len(polygonPoints))
        #     for pt in polygonPoints:
        #         inA = pt in verticesA
        #         inB = pt in verticesB
        #
        #         if inA and inB:
        #             s += " A{} == B{}\n".format(verticesA.index(pt), verticesB.index(pt))#"(" + str(int(pt.x)) + ", " + str(int(pt.y)) + ")"
        #         elif inA:
        #             s += " A{}\n".format(verticesA.index(pt))
        #         elif inB:
        #             s += " B{}\n".format(verticesB.index(pt))
        print("Number of polygons: {}\n{}---".format(len(polygonsPoints), s))
        for polygonVertices in polygonsPoints:
            if len(polygonVertices) > 1:
                Screen.DrawLines(Drawable(polygonVertices), color, 2)

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
            Screen.DrawCircle(self + vertex, 2, (255, 255, 255))
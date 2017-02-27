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
        p.centerVertices()
        return p

    def __str__(self):
        s = "["
        for v in self.vertices:
            s += str(Point(self.x + v.x, self.y + v.y, True))+","
        s = s[:-1]
        s += "]"
        return s

    def __len__(self):
        return len(self.vertices)

    def __init__(self, x=0, y=0, vertices=[]):
        Point.__init__(self, x, y)
        self.vertices = vertices

    def renderPolygon(self, color, thickness):
        Screen.DrawCircle(self, 3, color)
        if len(self.vertices) > 1:
            verticesTemp = []
            for vertex in self.vertices:
                verticesTemp.append((self.x + vertex.x, self.y + vertex.y))
            verticesTemp.append(verticesTemp[0])
            Screen.DrawLines(verticesTemp, color, thickness)
            #count = len(self)
            #for i in range(count):
            #    Screen.DrawCircle(self + self.vertices[i], 2+3 * (i/(count-1)), color)

    def renderBoundingRect(self, color=Color.white, thickness=1, filled=True):
        selfMinX = self.minX
        selfMinY = self.minY
        Screen.DrawRect((selfMinX, selfMinY), (self.maxX - selfMinX, self.maxY - selfMinY), color, thickness, filled)

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
        self.x += centerOfMass.x
        self.y += centerOfMass.y
        for i in range(len(self.vertices)):
            self.vertices[i].x -= centerOfMass.x
            self.vertices[i].y -= centerOfMass.y

    def rotateRadians(self, radians, center=None):
        centerOfMass = self.centerOfMassRelative() if center is None else (center - self)
        for vertex in self.vertices:
            vertex.rotateRadians(radians, centerOfMass)

    def contains(self, point):
        total = 0
        for i in range(len(self)):
            a = self + self.vertices[i] - point
            b = self + self.vertices[(i + 1) % len(self)] - point
            total += AngleDiff(a.radians, b.radians)
        return abs(total) > 0.001
    
    def boundingRectsCollide(self, other):
        selfMinX = self.minX
        selfMinY = self.minY
        otherMinX = other.minX
        otherMinY = other.minY
        return RectanglesCollide(selfMinX, selfMinY, self.maxX - selfMinX, self.maxY - selfMinY,
                                 otherMinX, otherMinY, other.maxX - otherMinX, other.maxY - otherMinY)

    def scale(self, multiplier, center=None):
        if center is None:
            center = self.centerOfMassRelative()
        for i in range(len(self.vertices)):
            self.vertices[i].x = multiplier * (self.vertices[i].x - center.x) + center.x
            self.vertices[i].y = multiplier * (self.vertices[i].y - center.y) + center.y

    @property
    def minX(self):
        if len(self) <= 0:
            return None
        minX = self.vertices[0].x
        for i in range(1, len(self)):
            minX = min(minX, self.vertices[i].x)
        return minX + self.x
    
    @property
    def maxX(self):
        if len(self) <= 0:
            return None
        maxX = self.vertices[0].x
        for i in range(1, len(self)):
            maxX = max(maxX, self.vertices[i].x)
        return maxX + self.x

    @property
    def minY(self):
        if len(self) <= 0:
            return None
        minY = self.vertices[0].y
        for i in range(1, len(self)):
            minY = min(minY, self.vertices[i].y)
        return minY + self.y
    
    @property
    def maxY(self):
        if len(self) <= 0:
            return None
        maxY = self.vertices[0].y
        for i in range(1, len(self)):
            maxY = max(maxY, self.vertices[i].y)
        return maxY + self.y

    @property
    def empty(self):
        return len(self.vertices) <= 0

    @staticmethod
    def SplitTraverse(polygon, lineA, lineB):
        if len(polygon) <= 0:
            return []

        if lineA.y == lineB.y:
            xmin = polygon.minX - 10
            xmax = polygon.maxX + 10
            m = PointOnLineAtX(lineA, lineB, xmin)
            n = PointOnLineAtX(lineA, lineB, xmax)
        else:
            ymin = polygon.minY - 10
            ymax = polygon.maxY + 10
            m = PointOnLineAtY(lineA, lineB, ymin)
            n = PointOnLineAtY(lineA, lineB, ymax)

        vertices = polygon.verticesAbsolute()

        points = []
        intersections = []
        unchecked = []
        count = len(vertices)
        for j in range(count):
            a = vertices[j]
            b = vertices[(j + 1) % count]
            p = LinesIntersectionPoint(m, n, a, b, True)
            unchecked.append(len(points))
            points.append(a)
            if p is not None:
                intersections.append([p, b])
                points.append(p)
        intersections.sort(key=lambda x: (x[0] - m).lengthSq)

        count = len(intersections)
        for i in range(0, count, 2):
            c = intersections[i]
            if i+1 >= count:
                c.append(c[0])
                break
            d = intersections[i+1]
            c.append(d[0])
            d.append(c[0])

        polygonsPoints = [[]]
        i = unchecked[0]
        while True:
            if i in unchecked:
                unchecked.remove(i)

            if len(polygonsPoints[-1]) > 0 and polygonsPoints[-1][0] == points[i]:
                polygonsPoints.append([])
                if len(unchecked) > 0:
                    i = unchecked[0]
                    continue
                return polygonsPoints

            polygonsPoints[-1].append(Point.Clone(points[i]))
            j = (i+1)%len(points)
            for intersectionInfo in intersections:
                if intersectionInfo[0] == points[i]:
                    for intersectionInfoOther in intersections:
                        if intersectionInfo[2] == intersectionInfoOther[0]:
                            j = points.index(intersectionInfoOther[1])
                            break
                    polygonsPoints[-1].append(Point.Clone(intersectionInfo[2]))
                    break
            i = j

    @staticmethod
    def SplitOnce(polygon, lineA, lineB):
        polygonsPoints = Polygon.SplitTraverse(polygon, lineA, lineB)
        polygons = []
        for polygonPoints in polygonsPoints:
            polygons.append(Polygon.NewFromAbsolutePositions(polygonPoints))
        return polygons

    @staticmethod
    def Split(polygon, linePoints):
        polygons = [polygon]
        for pair in linePoints:
            polygonsNew = []
            for _polygon in polygons:
                polygonsNew.extend(Polygon.SplitOnce(_polygon, pair[0], pair[1]))
            polygons = polygonsNew
        return polygons

    @staticmethod
    def AbsolutePolygonPointPositionsAndIntersections(A, B, merge, withIncomingIntersections):
        allPoints = []
        allIntersectionIndices = []
        verticesB = B.verticesAbsolute()
        for i in range(len(A.vertices)):
            a = A + A.vertices[i]
            b = A + A.vertices[(i + 1) % len(A)]
            intersectionPoints = []
            for j in range(len(verticesB)):
                p = LinesIntersectionPoint(a, b, verticesB[j], verticesB[(j + 1) % len(verticesB)], True)
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
            insideP = B.contains((intersection + allPoints[(index - 1 + count) % count]) / 2)
            insideN = B.contains((intersection + allPoints[(index + 1) % count]) / 2)
            if (insideN and not insideP) ^ merge:
                incomingIntersections.append(intersection)

        return [allPoints, incomingIntersections]

    @staticmethod
    def TraverseHandoff(merge, A, B, verticesA, verticesB, intersections, startPolygon, i, polygonPoints):
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
            elif a in verticesB:
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

        if not A.boundingRectsCollide(B):
            return [A.verticesAbsolute(), B.verticesAbsolute()] if merge else []

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
            #self.renderBoundingRect(filled=False)
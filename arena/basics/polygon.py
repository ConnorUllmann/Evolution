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
        return Polygon(polygon.x, polygon.y, v)

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

    def perimeter(self):
        perimeter = 0
        count = len(self.vertices)
        for i in range(count):
            j = (i+1)%count
            a = self.vertices[i]
            b = self.vertices[j]
            perimeter += (a - b).length
        return perimeter

    def renderPolygon(self, color, thickness):
        Screen.DrawCircle(self, 3, color)
        if len(self.vertices) > 1:
            verticesTemp = []
            for vertex in self.vertices:
                verticesTemp.append((self.x + vertex.x, self.y + vertex.y))
            Screen.DrawPolygon(verticesTemp, color, thickness)
            count = len(self)
            for i in range(count):
                Screen.DrawCircle(self + self.vertices[i], 2+3 * (i/(count-1)), color)

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

    def containsLineSegment(self, a, b):
        # a and b are points in absolute space

        if not self.contains((a + b) / 2):
            return False

        count = len(self.vertices)
        for i in range(count):
            m = self + self.vertices[i]
            n = self + self.vertices[(i + 1) % count]
            if LinesIntersectionPoint(a, b, m, n, True) is not None:
                return False

        return True

    def insideScreen(self):
        return self.collideWithRectangle(0, 0, Screen.Width(), Screen.Height())

    def collideWithRectangle(self, ax, ay, aw, ah):
        rect = Polygon(ax, ay, [Point(0, 0), Point(0, ah), Point(aw, ah), Point(aw, 0)])
        return self.collide(rect)

    def boundingRectCollideWithRectangle(self, ax, ay, aw, ah):
        selfMinX = self.minX
        selfMinY = self.minY
        return RectanglesCollide(selfMinX, selfMinY, self.maxX - selfMinX, self.maxY - selfMinY, ax, ay, aw, ah)

    def boundingRectsCollide(self, other):
        otherMinX = other.minX
        otherMinY = other.minY
        return self.boundingRectCollideWithRectangle(otherMinX, otherMinY, other.maxX - otherMinX, other.maxY - otherMinY)

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

    def splitTraverse(self, lineA, lineB):
        if len(self) <= 0:
            return []

        if lineA.y == lineB.y:
            xmin = self.minX - 10
            xmax = self.maxX + 10
            m = PointOnLineAtX(lineA, lineB, xmin)
            n = PointOnLineAtX(lineA, lineB, xmax)
        else:
            ymin = self.minY - 10
            ymax = self.maxY + 10
            m = PointOnLineAtY(lineA, lineB, ymin)
            n = PointOnLineAtY(lineA, lineB, ymax)

        vertices = self.verticesAbsolute()

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

        if len(intersections) <= 0:
            return [vertices]

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

    def splitOnceWithVelocity(self, lineA, lineB, velocities):
        #velocities is an implicitly returned dictionary
        parentVelocity = Point() if self not in velocities else velocities[self]
        polygonsPoints = self.splitTraverse(lineA, lineB)
        if len(polygonsPoints) > 0 and len(polygonsPoints[-1]) <= 0:
            polygonsPoints = polygonsPoints[:-1]
        shouldPush = len(polygonsPoints) != 1 or len(polygonsPoints[0]) != len(self.vertices)
        polygons = []
        for polygonPoints in polygonsPoints:
            polygon = Polygon.NewFromAbsolutePositions(polygonPoints)
            polygons.append(polygon)
            diff = polygon - PointOnLineClosestToPoint(lineA, lineB, polygon, False)
            #If we're not on the same side as the center of mass of the parent, make us move away
            if diff.lengthSq < (self - polygon).lengthSq:
                push = diff.normalized * 10 if shouldPush else Point()
            else:
                push = Point()
            velocities[polygon] = parentVelocity + push
        return polygons

    def splitOnce(self, lineA, lineB):
        polygonsPoints = self.splitTraverse(lineA, lineB)
        polygons = []
        for polygonPoints in polygonsPoints:
            polygons.append(Polygon.NewFromAbsolutePositions(polygonPoints))
        return polygons

    def split(self, linePoints):
        #linePoints is a list of point pairs that define the lines to be cut
        polygons = [self]
        for pair in linePoints:
            polygonsNew = []
            for polygon in polygons:
                polygonsNew.extend(polygon.splitOnce(pair[0], pair[1]))
            polygons = polygonsNew
        return polygons

    def removeVertexAt(self, i):
        return self.vertices.pop(i)

    def collide(self, other):
        return Polygon.Collide(self, other)

    @staticmethod
    def Collide(A, B):
        #Return case where one of the polygons is empty
        if A.empty or B.empty:
            return False

        #Bounding boxes don't overlap
        if not A.boundingRectsCollide(B):
            return False

        #Return case where they intersect
        lenA = len(A.vertices)
        lenB = len(B.vertices)
        for i in range(lenA):
            a = A + A.vertices[i]
            b = A + A.vertices[(i + 1) % lenA]
            for j in range(lenB):
                c = B + B.vertices[j]
                d = B + B.vertices[(j + 1) % lenB]
                if LinesIntersectionPoint(a, b, c, d, True) is not None:
                    return True

        #Return case where one is inside the other
        if A.contains(B + B.vertices[0]):
            return True
        if B.contains(A + A.vertices[0]):
            return True

        #Return case where bounding boxes collide,
        #but they never intersect and are outside one another
        return False

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

    @staticmethod
    def Traverse(merge, A, B):
        # Returns list of polygon point sets formed by the intersection or the merging of two polygons (depending on the boolean "merge" property)

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

    @staticmethod
    def Subtract(A, *polygons):
        polygonsReturn = [A]
        for polygon in polygons:
            polygonsReturnTemp = []
            for Asubpolygon in polygonsReturn:
                polygonsReturnTemp.extend(Polygon.SubtractTwo(Asubpolygon, polygon))
            polygonsReturn = polygonsReturnTemp
        return polygonsReturn

    @staticmethod
    def SubtractTwo(A, B):
        polygonsPoints = Polygon.SubtractTraverse(A, B)
        polygons = []
        for polygonPoints in polygonsPoints:
            polygons.append(Polygon.NewFromAbsolutePositions(polygonPoints))
        return polygons

    @staticmethod
    def SubtractTraverseHandoff(A, B, verticesA, verticesB, intersections, startPolygon, i, polygonPoints):
        polygon = polygonPoints[-1]
        while True:
            next = 1 if startPolygon == A else -1
            a = verticesA[i%len(verticesA)]
            b = verticesA[(i+len(verticesA)+next)%len(verticesA)]

            if a in intersections:
                intersections.remove(a)

            if len(polygon) > 0 and a == polygon[0]:
                if len(intersections) > 0:
                    if startPolygon == A:
                        return Polygon.SubtractTraverseHandoff(A, B, verticesA, verticesB, intersections, startPolygon, verticesA.index(intersections[0]), polygonPoints+[[]])
                    else:
                        return Polygon.SubtractTraverseHandoff(B, A, verticesB, verticesA, intersections, startPolygon, verticesB.index(intersections[0]), polygonPoints+[[]])
                return polygonPoints

            if (not B.contains((a + b)/2)) ^ (startPolygon == A):
                if a in verticesB:
                    return Polygon.SubtractTraverseHandoff(B, A, verticesB, verticesA, intersections, startPolygon, verticesB.index(a), polygonPoints)
            else:
                polygon.append(a)
            i += next

    @staticmethod
    def SubtractTraverse(A, B):
        #Return case where one of the polygons is empty
        Aempty = A.empty
        Bempty = B.empty
        if Aempty and Bempty:
            return []
        elif Aempty:
            return []
        elif Bempty:
            return [A.verticesAbsolute()]

        if not A.boundingRectsCollide(B):
            return [A.verticesAbsolute()]

        verticesA, incomingIntersectionsA = Polygon.AbsolutePolygonPointPositionsAndIntersections(A, B, True, True)
        verticesB = Polygon.AbsolutePolygonPointPositionsAndIntersections(B, A, None, False)

        #Return case where one polygon is inside the other or they do not touch
        if len(incomingIntersectionsA) <= 0:
            for vertex in verticesB:
                if vertex not in verticesA and A.contains(vertex):
                    return [A.verticesAbsolute()]
            for vertex in verticesA:
                if vertex not in verticesB and B.contains(vertex):
                    return []
            return [A.verticesAbsolute()]

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
            return []

        polygonPoints = Polygon.SubtractTraverseHandoff(A, B, verticesA, verticesB, incomingIntersectionsA, A, verticesA.index(incomingIntersectionsA[0]), [[]])

        #If we started a polygon but didn't finish it, chop it off
        if len(polygonPoints) > 0 and len(polygonPoints[-1]) <= 0:
            polygonPoints = polygonPoints[:-1]
        return polygonPoints


class PolygonEntity(Polygon, Entity):

    def __init__(self, polygon, color=None, thickness=1):
        Polygon.__init__(self, polygon.x, polygon.y, polygon.vertices)
        Entity.__init__(self, polygon.x, polygon.y)
        self.color = color if color is not None else Color.all[self.id%len(Color.all)]
        self.thickness = thickness
        self.angle = 0
        self.visible = True

    def __str__(self):
        #Not including the Polygon string because it is expensive to calculate and we only
        #need this string to uniquely identify this polygon among all entities
        return Entity.__str__(self)# + Polygon.__str__(self)

    def Render(self):
        if self.visible:
            self.renderPolygon(self.color, self.thickness)

    def Update(self):
        Entity.Update(self)
        self.v *= 0.5
        self.x += self.v.x
        self.y += self.v.y

    def splitWithVelocity(self, linePoints):
        polygons = [self]
        velocities = {}
        for pair in linePoints:
            polygonsNew = []
            for _polygon in polygons:
                polygonsNew.extend(_polygon.splitOnceWithVelocity(pair[0], pair[1], velocities))
            polygons = polygonsNew

        polygonEntities = []
        for polygon in polygons:
            polygonEntity = PolygonEntity(polygon)
            polygonEntities.append(polygonEntity)
            polygonEntity.v = velocities[polygon]
        return polygonEntities

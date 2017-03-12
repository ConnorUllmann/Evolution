from .polygon import Polygon
from .point import Point
from .screen import Screen
from .color import Color
from .entity import Entity
from .utils import PointOnLineAtX, PointOnLineAtY, LinesIntersectionPoint, PointOnLineClosestToPoint, RectanglesCollide, Sigmoid
from random import random
from math import exp

class ViscoElasticNode(Point):

    dampener = 0.9
    maxMomentum = 100

    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.mass = 10
        self.momentum = Point()
        self.rods = []

    def update(self):
        self.contract()

        #self.momentum.y += ViscoElasticNode.gravity * self.mass

        self.momentum *= ViscoElasticNode.dampener

        if self.momentum.length > ViscoElasticNode.maxMomentum:
            self.momentum = self.momentum.normalized * ViscoElasticNode.maxMomentum

        self.x += self.momentum.x / self.mass
        self.y += self.momentum.y / self.mass

        # if self.x < 0:
        #     self.momentum.x = abs(self.momentum.x)
        # if self.x > Screen.Width():
        #     self.momentum.x = -abs(self.momentum.x)
        # if self.y < 0:
        #     self.momentum.y = abs(self.momentum.y)
        # if self.y > Screen.Height():
        #     self.momentum.y = -abs(self.momentum.y)

    def render(self, offset):
        Screen.DrawCircle(self + offset, 2, Color.yellow)

    def contract(self):
        for rod in self.rods:
            delta_momentum = (self - rod).normalized * rod.force
            self.momentum += delta_momentum

class ViscoElasticRod(Point):

    coeffPull = 25

    def __init__(self, nodeA, nodeB, color, spanMin=5):
        position = (nodeA + nodeB) / 2
        Point.__init__(self, position.x, position.y)

        self.color = color
        self.spanMin = spanMin

        nodeA.rods.append(self)
        nodeB.rods.append(self)

        self.force = 0
        self.nodes = [nodeA, nodeB]
        self.resetSpan()

    def resetSpan(self):
        #Having a minimum on the span helps with the vertices that freak out when they're too close together
        self.span = max(self.spanMin, (self.nodes[0] - self.nodes[1]).length)

    def destroy(self):
        for node in self.nodes:
            if self in node.rods:
                node.rods.remove(self)

    def update(self):
        v = 1 - (self.nodes[0] - self.nodes[1]).length / self.span
        #v = 2.0 / (1.0 + exp(-min(max(v, -1), 1)*5)) - 1

        #if abs(v) > 0.9:
        #    print(v)

        self.force = ViscoElasticRod.coeffPull * v

        self.center()

    def render(self, offset):
        Screen.DrawLine(self.nodes[0] + offset, self.nodes[1] + offset, self.color)

    def center(self):
        p = Point()
        totalMass = 0
        for node in self.nodes:
            p += node * node.mass
            totalMass += node.mass
        p /= totalMass
        self.x = p.x
        self.y = p.y

class Softbody(Entity, Polygon):

    friction = 0.95
    gravity = 1

    @staticmethod
    def NewFromPolygon(polygon):
        v = []
        for vertex in polygon.vertices:
            v.append(Point(vertex.x, vertex.y))
        return Softbody(polygon.x, polygon.y, v)

    @staticmethod
    def NewFromAbsolutePositions(vertices):
        s = Softbody(0, 0, vertices)
        s.centerVertices()
        return s

    @staticmethod
    def GetVerticesAsNodes(vertices):
        nodes = []
        for vertex in vertices:
            nodes.append(ViscoElasticNode(vertex.x, vertex.y))
        return nodes

    def __init__(self, x, y, vertices):
        Entity.__init__(self, x, y)
        Polygon.__init__(self, x, y, Softbody.GetVerticesAsNodes(vertices))

        self.rodsSupport = []
        self.rods = []
        for i in range(len(self.vertices)):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % len(self.vertices)]
            self.addRod(a, b)

    def Update(self):

        if not self.insideScreen():
            self.Destroy()
            return

        #self.v.y += Softbody.gravity

        self.x += self.v.x
        self.y += self.v.y

        self.v *= Softbody.friction

        for rod in self.rods:
            rod.update()
        for rod in self.rodsSupport:
            rod.update()
        for node in self.vertices:
            node.update()
        # self.moveNodesAroundMouse()
        # self.putVerticesInsideScreen()

    def Render(self):
        for rod in self.rods:
            rod.render(self)
        for rod in self.rodsSupport:
            rod.render(self)
        for node in self.vertices:
            node.render(self)

    def scale(self, multiplier, center=None):
        Polygon.scale(self, multiplier, center)
        for rod in self.rods:
            rod.span *= multiplier
        for rod in self.rodsSupport:
            rod.span *= multiplier

    def addSupportRod(self, a, b):
        # a and b are nodes on the Softbody
        if a in self.vertices and b in self.vertices:
            rod = ViscoElasticRod(a, b, Color.cyan)
            self.rodsSupport.append(rod)
            return rod
        return None

    def addStandardSupportRods(self):
        self.rodsSupport = []
        for i in range(int(len(self.vertices)/2)):
            a = self.vertices[i]
            b = self.vertices[(i+int(len(self.vertices)/2))%len(self.vertices)]
            self.addSupportRod(a, b)

    def addRandomSupportRods(self, count=20):
        newSupportRods = 0
        while newSupportRods < count:
            aIndex = int(random() * len(self.vertices))
            bIndex = int(random() * len(self.vertices))
            if abs(bIndex - aIndex) > 2:
                a = self.vertices[aIndex]
                b = self.vertices[bIndex]
                ab = (b - a).normalized * 0.00001
                aTemp = self + a + ab
                bTemp = self + b - ab
                if self.containsLineSegment(aTemp, bTemp):
                    self.addSupportRod(a, b)
                    newSupportRods += 1

    def putVerticesInsideScreen(self):
        for vertex in self.vertices:
            vertex.x = min(max(vertex.x + self.x, 0), Screen.Width()) - self.x
            vertex.y = min(max(vertex.y + self.y, 0), Screen.Height()) - self.y

    def moveNodesAroundMouse(self):
        for node in self.vertices:
            mouseRelative = Screen.MousePosition() - self
            nodeToMouse = mouseRelative - node
            if nodeToMouse.length < 60:
                pt = node - max(1 - nodeToMouse.length / 60, 0) * nodeToMouse.normalized * 10
                node.x = pt.x
                node.y = pt.y

    def addRod(self, a, b):
        self.rods.append(ViscoElasticRod(a, b, Color.orange))

    def removeRod(self, rod):
        if rod in self.rods:
            self.rods.remove(rod)
        elif rod in self.rodsSupport:
            self.rodsSupport.remove(rod)

    def removeVertexAt(self, i):
        ai = (i+len(self.vertices)-1)%len(self.vertices)
        bi = (i+1)%len(self.vertices)
        a = self.vertices[ai]
        b = self.vertices[bi]
        vertex = Polygon.removeVertexAt(self, i)
        rodsToRemove = []
        for rod in self.rods:
            for i in range(len(rod.nodes)):
                j = (i + 1) % len(rod.nodes)
                if vertex == rod.nodes[i]:
                    if rod.nodes[i] != a and rod.nodes[j] != a and abs(self.vertices.index(rod.nodes[j]) - ai) > 1:
                        rod.nodes[i] = a
                        rod.resetSpan()
                    elif rod.nodes[i] != b and rod.nodes[j] != b and abs(self.vertices.index(rod.nodes[j]) - bi) > 1:
                        rod.nodes[i] = b
                        rod.resetSpan()
                    else:
                        rodsToRemove.append(rod)
        for rod in self.rodsSupport:
            for i in range(len(rod.nodes)):
                if vertex == rod.nodes[i]:
                    j = (i + 1) % len(rod.nodes)
                    if rod.nodes[i] != a and rod.nodes[j] != a and abs(self.vertices.index(rod.nodes[j]) - ai) > 1:
                        rod.nodes[i] = a
                        rod.resetSpan()
                    elif rod.nodes[i] != b and rod.nodes[j] != b and abs(self.vertices.index(rod.nodes[j]) - bi) > 1:
                        rod.nodes[i] = b
                        rod.resetSpan()
                    else:
                        rodsToRemove.append(rod)
        for rod in rodsToRemove:
            self.removeRod(rod)

    def splitTraverse(self, lineA, lineB):
        # Returns list of lists of vertices and a list of rods whose first element is a point that lies on one of the new polygons

        if len(self) <= 0:
            #print("EXIT - No vertices!")
            return [[[]], []]

        type = "RAY"
        if type == "LINE":
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
        elif type == "RAY":
            if self.contains(lineA):
                m = lineA
                if lineA.x == lineB.x:
                    n = PointOnLineAtY(lineA, lineB, self.maxY + 10)
                else:
                    n = PointOnLineAtX(lineA, lineB, self.maxX + 10)
            else:
                if lineA.y == lineB.y:
                    xmin = self.minX - 10
                    xmax = self.maxX + 10
                    if lineA.x < lineB.x:
                        m = lineA
                        n = PointOnLineAtX(lineA, lineB, xmax)
                    else:
                        m = lineA
                        n = PointOnLineAtX(lineA, lineB, xmin)
                else:
                    ymin = self.minY - 10
                    ymax = self.maxY + 10
                    pmin = PointOnLineAtY(lineA, lineB, ymin)
                    pmax = PointOnLineAtY(lineA, lineB, ymax)
                    if lineA.y < lineB.y:
                        m = lineA
                        n = pmax
                    else:
                        m = lineA
                        n = pmin

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
            # print("EXIT - No intersections; vertices: {}".format(len(self.vertices)))
            return [None, None]

        rodsSupportEnds = []
        pointsToInsert = {}
        count = len(intersections)
        for i in range(0, count, 2):
            c = intersections[i]
            if i+1 >= count:
                c.append(c[0])
                break
            d = intersections[i+1]
            c.append(d[0])
            d.append(c[0])
            rodIntersections = []
            for rod in self.rodsSupport:
                intersectionPoint = LinesIntersectionPoint(self + rod.nodes[0], self + rod.nodes[1], c[0], d[0], True)
                if intersectionPoint is not None:
                    rodIntersections.append(intersectionPoint)
                    rodsSupportEnds.append([self + rod.nodes[0], intersectionPoint])
                    rodsSupportEnds.append([self + rod.nodes[1], intersectionPoint])

            rodIntersections.sort(key=lambda x: (x - c[0]).lengthSq)
            rodIntersectionsReverseCopy = list(Point.Clone(pt) for pt in rodIntersections)
            rodIntersectionsReverseCopy.reverse()

            pointsToInsert[str(c[0])+str(d[0])] = rodIntersections
            pointsToInsert[str(d[0])+str(c[0])] = rodIntersectionsReverseCopy

        polygonsPoints = [[]]
        i = unchecked[0]
        while True:
            if i in unchecked:
                unchecked.remove(i)

            if len(polygonsPoints[-1]) > 0 and polygonsPoints[-1][0] == points[i]:
                if len(unchecked) > 0:
                    polygonsPoints.append([])
                    i = unchecked[0]
                    continue
                return [polygonsPoints, rodsSupportEnds]

            j = (i+1)%len(points)

            polygonsPoints[-1].append(Point.Clone(points[i]))

            for intersectionInfo in intersections:
                if intersectionInfo[0] == points[i]:
                    for intersectionInfoOther in intersections:
                        if intersectionInfo[2] == intersectionInfoOther[0]:
                            j = points.index(intersectionInfoOther[1])
                            break

                    key = str(points[i]) + str(intersectionInfo[2])
                    if key in pointsToInsert:
                        #print("key = {}".format(key))
                        for pointToInsert in pointsToInsert[key]:
                            #print(pointToInsert)
                            polygonsPoints[-1].append(pointToInsert)
                    polygonsPoints[-1].append(Point.Clone(intersectionInfo[2]))
                    break
            i = j

    def splitOnce(self, lineA, lineB):
        polygonsPoints, rodsSupportEnds = self.splitTraverse(lineA, lineB)
        softbodies = []

        if polygonsPoints == None:
            return [self]

        for polygonPoints in polygonsPoints:
            softbodies.append(Softbody.NewFromAbsolutePositions(polygonPoints))

        for rodEnds in rodsSupportEnds:
            for softbody in softbodies:
                rodNodeA = None
                rodNodeB = None
                for vertex in softbody.vertices:
                    vertPoint = vertex + softbody
                    if rodNodeA is None:
                        if rodEnds[0] == vertPoint:
                            rodNodeA = vertex
                    if rodNodeB is None:
                        if rodEnds[1] == vertPoint:
                            rodNodeB = vertex
                    if rodNodeA is not None and rodNodeB is not None:
                        break

                if rodNodeA is not None and rodNodeB is not None:
                    softbody.rodsSupport.append(ViscoElasticRod(rodNodeA, rodNodeB, Color.cyan))
                    break

        for rod in self.rodsSupport:
            for softbody in softbodies:
                rodNodeA = None
                rodNodeB = None
                for vertex in softbody.vertices:
                    if rodNodeA is None:
                        if self + rod.nodes[0] == vertex + softbody:
                            rodNodeA = vertex
                    if rodNodeB is None:
                        if self + rod.nodes[1] == vertex + softbody:
                            rodNodeB = vertex
                    if rodNodeA is not None and rodNodeB is not None:
                        break
                if rodNodeA is not None and rodNodeB is not None:
                    softbody.rodsSupport.append(ViscoElasticRod(rodNodeA, rodNodeB, Color.cyan))
                    break

        for softbody in softbodies:
            totalMass = 0
            centerOfMass = softbody.centerOfMassAbsolute()
            direction = (centerOfMass - PointOnLineClosestToPoint(lineA, lineB, centerOfMass)).normalized
            for vertex in softbody.vertices:
                totalMass += vertex.mass
                vertex.momentum = 1000 * max(0, 25 - (PointOnLineClosestToPoint(lineA, lineB, vertex) - vertex).lengthSq) * direction

            softbody.v = self.v + 400 / totalMass * direction

        return softbodies

    def splitOnceAndDestroy(self, lineA, lineB):
        softbodies = self.splitOnce(lineA, lineB)
        if len(softbodies) == 1 and softbodies[0] == self:
            return softbodies
        self.Destroy()
        return softbodies

    def splitAndDestroy(self, linePoints):
        softbodies = self.split(linePoints)
        if len(softbodies) == 1 and softbodies[0] == self:
            return softbodies
        self.Destroy()
        return softbodies

    def split(self, linePoints):
        polygons = [self]
        for pair in linePoints:
            polygonsNew = []
            for polygon in polygons:
                polygonsNew.extend(polygon.splitOnceAndDestroy(pair[0], pair[1]))
            polygons = polygonsNew
        return polygons
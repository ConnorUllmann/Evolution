from .polygon import Polygon
from .point import Point
from .screen import Screen
from .color import Color
from .entity import Entity

class ViscoElasticNode(Point):
    gravity = 0.01
    dampener = 1
    maxMomentum = 100
    conRadius = 20

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

        if self.x > Screen.Width():
            self.momentum.x = -abs(self.momentum.x)
        if self.x < 0:
            self.momentum.x = abs(self.momentum.x)
        if self.y > Screen.Height():
            self.momentum.y = -abs(self.momentum.y)
        if self.y < 0:
            self.momentum.y = abs(self.momentum.y)

    def render(self, offset):
        Screen.DrawCircle(self + offset, 3, Color.yellow)

    def contract(self):
        for rod in self.rods:
            delta_momentum = Point(rod.force, 0)
            delta_momentum.radians = (self - rod).radians
            self.momentum += delta_momentum



class ViscoElasticRod(Point):
    coeffPull = 100

    def __init__(self, nodeA, nodeB):
        position = (nodeA + nodeB) / 2
        Point.__init__(self, position.x, position.y)

        nodeA.rods.append(self)
        nodeB.rods.append(self)
        self.nodes = [nodeA, nodeB]
        self.span = (nodeA - nodeB).length
        self.force = 0

    def update(self):
        self.force = ViscoElasticRod.coeffPull * (1 - (self.nodes[0] - self.nodes[1]).length / self.span)
        self.center()

    def render(self, offset):
        Screen.DrawLine(self.nodes[0] + offset, self.nodes[1] + offset, Color.orange)

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
    def __init__(self, x, y, vertices):
        Entity.__init__(self, x, y)
        Polygon.__init__(self, x, y, vertices)

        self.nodes = []
        for vertex in self.vertices:
            self.nodes.append(ViscoElasticNode(vertex.x, vertex.y))
        self.rods = []
        for i in range(len(self.nodes)):
            a = self.nodes[i]
            b = self.nodes[(i+1)%len(self.nodes)]
            rod = ViscoElasticRod(a, b)
            self.rods.append(rod)

    def Update(self):
        for rod in self.rods:
            rod.update()
        for node in self.nodes:
            node.update()
        for node in self.nodes:
            mouseRelative = Screen.Instance.MousePosition() - self
            nodeToMouse = mouseRelative - node
            if nodeToMouse.length < 25:
                pt = node - max(1 - nodeToMouse.length / 25, 0) * nodeToMouse.normalized * 5
                node.x = pt.x
                node.y = pt.y

    def Render(self):
        for rod in self.rods:
            rod.render(self)
        for node in self.nodes:
            node.render(self)
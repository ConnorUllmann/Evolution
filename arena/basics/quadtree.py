from .point import Point
from .screen import Screen
from .color import Color
from .utils import RectanglesCollide


class QuadTree(Point):

    def __init__(self, x, y, width, height, minCellWidth=40, minCellHeight=40):
        Point.__init__(self, x, y)
        self.maxObjectsPerCell = 2
        self.minCellWidth = minCellWidth
        self.minCellHeight = minCellHeight
        self.root = QuadTreeNode(0, 0, width, height, self)

    def insertObjectWithBoundingBox(self, x, y, width, height, obj):
        self.root.insertObjectWithBoundingBox(x, y, width, height, obj)

    def render(self):
        self.root.render()

class QuadTreeNode(Point):

    def __init__(self, x, y, width, height, quadTree):
        Point.__init__(self, x, y)
        self.width = width
        self.height = height
        self.quadTree = quadTree
        self.childTrees = []
        self.objectData = []

    def split(self):
        halfWidth = self.width / 2
        halfHeight = self.width / 2
        points = [
            Point(self.x, self.y),
            Point(self.x + halfWidth, self.y),
            Point(self.x, self.y + halfHeight),
            Point(self.x + halfWidth, self.y + halfHeight)
        ]
        for point in points:
            self.childTrees.append(QuadTreeNode(point.x, point.y, halfWidth, halfHeight, self.quadTree))

    @property
    def hasSplit(self):
        return len(self.childTrees) > 0

    @property
    def shouldSplit(self):
        return len(self.objectData) > self.quadTree.maxObjectsPerCell

    @property
    def canSplit(self):
        return self.width > self.quadTree.minCellWidth and \
               self.height > self.quadTree.minCellHeight and \
               len(self.childTrees) <= 0

    def insertObjectWithBoundingBox(self, x, y, width, height, obj):
        if obj not in self.objectData and RectanglesCollide(self.x, self.y, self.width, self.height, x, y, width, height):
            self.objectData.append((x, y, width, height, obj))
            if self.hasSplit:
                for child in self.childTrees:
                    child.insertObjectWithBoundingBox(x, y, width, height, obj)
            elif self.shouldSplit and self.canSplit:
                self.split()
                for objectData in self.objectData:
                    for child in self.childTrees:
                        child.insertObjectWithBoundingBox(*objectData)

    def render(self):
        Screen.DrawRect(self, Point(self.width, self.height), Color.green, filled=False)
        Screen.DrawText(self + Point(self.width/2, self.height/2), "{}".format(len(self.objectData)))
        for child in self.childTrees:
            child.render()

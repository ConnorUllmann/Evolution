from .point import Point
from .screen import Screen
from .color import Color
from .utils import RectanglesCollide


class QuadTree(Point):

    def __init__(self, x, y, width, height, minCellWidth=20, minCellHeight=20):
        Point.__init__(self, x, y)
        self.maxObjectsPerCell = 2
        self.minCellWidth = minCellWidth
        self.minCellHeight = minCellHeight
        self.root = QuadTreeNode(0, 0, width, height, self)

    def getAllObjectsInTree(self):
        return list(x[0] for x in self.root.objectData)

    def insertObjectAtPoint(self, obj, x, y):
        self.root.insertObjectWithBoundingBox(obj, x, y, 0, 0)

    def insertObjectWithBoundingBox(self, obj, x, y, width, height):
        self.root.insertObjectWithBoundingBox(obj, x, y, width, height)

    def collidingObjects(self, x, y, width, height):
        return self.root.findCollidingObjects(x, y, width, height)

    def collidingLeafNodes(self, x, y, width, height):
        leafNodes = []
        self.root.findCollidingLeafNodes(x, y, width, height, leafNodes)
        return leafNodes

    def findNodeByPositionAndSize(self, x, y, width, height):
        return self.root.findNodeByPositionAndSize(x, y, width, height)

    def render(self):
        self.root.render()


class QuadTreeNode(Point):

    def __str__(self):
        return "(x={}, y={}, w={}, h={}, objs={})".format(self.x, self.y, self.width, self.height, len(self.objectData))

    def __init__(self, x, y, width, height, quadTree):
        Point.__init__(self, x, y)
        self.width = width
        self.height = height
        self.quadTree = quadTree
        self.childTrees = []
        self.objectData = []
        self.color = Color.green

    def split(self):
        halfWidth = self.width / 2.0
        halfHeight = self.height / 2.0
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

    def collideRect(self, x, y, width, height):
        return RectanglesCollide(self.x, self.y, self.width, self.height, x, y, width, height)

    def insertObjectWithBoundingBox(self, obj, x, y, width, height):
        for objectData in self.objectData:
            if objectData[0] == obj:
                return

        if self.collideRect(x, y, width, height):
            self.objectData.append((obj, x, y, width, height))

            if self.hasSplit:
                for child in self.childTrees:
                    child.insertObjectWithBoundingBox(obj, x, y, width, height)
            elif self.shouldSplit and self.canSplit:
                self.split()
                for objectData in self.objectData:
                    for child in self.childTrees:
                        child.insertObjectWithBoundingBox(*objectData)

    def findCollidingObjects(self, x, y, width, height):
        collidingObjects = []
        potentialCollidingObjectDatas = []
        self.findPotentialCollidingObjects(x, y, width, height, potentialCollidingObjectDatas)
        for pcod in potentialCollidingObjectDatas:
            if RectanglesCollide(x, y, width, height, pcod[1], pcod[2], pcod[3], pcod[4]):
                collidingObjects.append(pcod[0])
        return collidingObjects

    def findPotentialCollidingObjects(self, x, y, width, height, objectDatas=[]):
        if self.collideRect(x, y, width, height):
            if self.hasSplit:
                for child in self.childTrees:
                    child.findPotentialCollidingObjects(x, y, width, height, objectDatas)
            else:
                for objectData in self.objectData:
                    alreadyContainsObjectData = False
                    for tempObjectData in objectDatas:
                        if objectData[0] == tempObjectData[0]:
                            alreadyContainsObjectData = True
                            break
                    if not alreadyContainsObjectData:
                        objectDatas.append(objectData)

    def findCollidingLeafNodes(self, x, y, width, height, leafNodes=[]):
        if self.collideRect(x, y, width, height):
            if self.hasSplit:
                for child in self.childTrees:
                    child.findCollidingLeafNodes(x, y, width, height, leafNodes)
            else:
                leafNodes.append(self)

    def findNodeByPositionAndSize(self, x, y, width, height):
        if self.x == x and self.y == y and self.width == width and self.height == height:
            return self
        if self.hasSplit:
            for child in self.childTrees:
                result = child.findNodeByPositionAndSize(x, y, width, height)
                if result is not None:
                    return result
        return None

    def render(self):
        Screen.DrawRect(self, Point(self.width, self.height), self.color, filled=False)
        #Screen.DrawText(self + Point(self.width/2, self.height/2), "{}".format(len(self.objectData)))
        for child in self.childTrees:
            child.render()

from .point import Point
from .screen import Screen
from .color import Color
from .utils import RectanglesCollide


class QuadTree(Point):

    #Weird problem when minCellWidth and minCellHeight are set to 10 or 20; error message
    # "C:/Users/Connor/Desktop/Development/Python/Evolution/arena/main_quadtree.py", line 79, in < module >
    # Screen.StartGame(Begin, Update, Render)
    # "C:\Users\Connor\Desktop\Development\Python\Evolution\arena\basics\screen.py", line 100, in StartGame
    # Screen.Start()
    # "C:\Users\Connor\Desktop\Development\Python\Evolution\arena\basics\screen.py", line 80, in Start
    # Screen.Instance.StartHelper()
    # "C:\Users\Connor\Desktop\Development\Python\Evolution\arena\basics\screen.py", line 86, in StartHelper
    # self.Update()
    # "C:\Users\Connor\Desktop\Development\Python\Evolution\arena\basics\screen.py", line 170, in Update
    # updateFunction()
    # "C:/Users/Connor/Desktop/Development/Python/Evolution/arena/main_quadtree.py", line 42, in Update
    # objects.remove(rect)
    # ValueError: list.remove(x): x not in list
    def __init__(self, x, y, width, height, minCellWidth=20, minCellHeight=20):
        Point.__init__(self, x, y)
        self.maxObjectsPerCell = 5
        self.minCellWidth = minCellWidth
        self.minCellHeight = minCellHeight
        self.nodesByObject = {}
        self.root = QuadTreeNode(0, 0, width, height, self)

    def getAllObjectsInTree(self):
        return list(x[0] for x in self.root.objectData)

    def getNodesCollidingObject(self, obj):
        objStr = str(obj)
        if objStr not in self.nodesByObject:
            return []
        return self.nodesByObject[objStr]

    def getLeafNodesCollidingObject(self, obj):
        return list(filter(lambda x: not x.hasSplit, self.getNodesCollidingObject(obj)))

    def insertObjectAtPoint(self, obj, x, y):
        self.root.insertObjectWithBoundingBox(obj, x, y, 0, 0)

    def insertObjectWithBoundingBox(self, obj, x, y, width, height):
        self.root.insertObjectWithBoundingBox(obj, x, y, width, height)

    def collidingObjects(self, x, y, width, height):
        return self.root.findCollidingObjects(x, y, width, height)

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
        self.color = Color.green

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

    def collideRect(self, x, y, width, height):
        return RectanglesCollide(self.x, self.y, self.width, self.height, x, y, width, height)

    def insertObjectWithBoundingBox(self, obj, x, y, width, height):
        if obj not in self.objectData and self.collideRect(x, y, width, height):
            self.objectData.append((obj, x, y, width, height))

            objStr = str(obj)
            if objStr not in self.quadTree.nodesByObject:
                self.quadTree.nodesByObject[objStr] = []
            self.quadTree.nodesByObject[objStr].append(self)

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

    def render(self):
        Screen.DrawRect(self, Point(self.width, self.height), self.color, filled=False)
        Screen.DrawText(self + Point(self.width/2, self.height/2), "{}".format(len(self.objectData)))
        for child in self.childTrees:
            child.render()

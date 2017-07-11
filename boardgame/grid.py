from basics import Point, Entity, Screen, Color

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.values = [[0]*height for x in range(width)] if width > 0 and height > 0 else None
        self.cellWidth = len(self.values) / self.width if self.width > 0 else 0
        self.cellHeight = len(self.values[0]) / self.height if len(self.values) > 0 and self.height > 0 else 0
        print(self.values)

    def Add(self, x, y, value):
        if 0 <= x < len(self.values):
            if 0 <= y < len(self.values[x]):
                self.values[x][y] = value
                return True
        return False

    def Get(self, x, y, value):
        if 0 <= x < len(self.values):
            if 0 <= y < len(self.values[x]):
                return self.values[x][y]
        return None

    def Remove(self, x, y):
        if 0 <= x < len(self.values):
            if 0 <= y < len(self.values[x]):
                self.values[x][y] = 0
                return True
        return False

class PlayGrid(Entity, Grid):
    def __init__(self, width, height):
        Grid.__init__(self, width, height)
        Entity.__init__(self, 0, 0)
        self.colorFill = Color.white
        self.colorOutline = Color.black
        self.colorText = Color.blue

    def Render(self):
        for x in range(len(self.values)):
            for y in range(len(self.values[x])):
                value = self.values[x][y]
                position = self + Point(self.cellWidth * x, self.cellHeight * y)
                dimensions = Point(self.cellWidth, self.cellHeight)
                Screen.DrawRect(position, dimensions, self.colorFill)
                Screen.DrawText(position + dimensions / 2, value, self.colorText)
                Screen.DrawRect(position, dimensions, self.colorOutline, filled=False)

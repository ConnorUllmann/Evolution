from basics import Point, Entity, Screen, Color
import math, random

class Grid:
    def __init__(self, width, height, cellWidth, cellHeight):
        self.width = width
        self.height = height
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.columns = math.ceil(width/cellWidth)
        self.rows = math.ceil(height/cellHeight)
        self.values = []
        for i in range(self.columns):
            self.values.append([])
            for j in range(self.rows):
                self.values[i].append(None)

    def i(self, x):
        return math.floor(x / self.width * self.columns)

    def j(self, y):
        return math.floor(y / self.height * self.rows)

    def X(self, i):
        return i / self.columns * self.width

    def Y(self, j):
        return j / self.rows * self.height

    def InGrid(self, x=None, y=None, i=None, j=None):
        if self.values is None:
            return False
        if i is not None and j is not None:
            return 0 <= i < self.columns and 0 <= j < self.rows
        if x is not None and y is not None:
            return 0 <= x < self.width and 0 <= y < self.height
        return False

    def Set(self, value, x=None, y=None, i=None, j=None):
        if self.values is None:
            return False
        if i is not None and j is not None:
            if self.InGrid(i=i, j=j):
                self.values[i][j] = value
                return True
        if x is not None and y is not None:
            if self.InGrid(x=x, y=y):
                self.values[self.i(x)][self.j(y)] = value
                return True
        return False

    def Get(self, x=None, y=None, i=None, j=None):
        if self.values is None:
            return None
        if i is not None and j is not None and self.InGrid(i=i, j=j):
            return self.values[i][j]
        if x is not None and y is not None and self.InGrid(x=x, y=y):
            return self.values[self.i(x)][self.j(y)]
        return None

class Tile:
    def __init__(self, value, grid, i, j):
        self.value = value
        self.grid = grid
        self.width = self.grid.cellWidth
        self.height = self.grid.cellHeight
        self.i = i
        self.j = j
        self.x = grid.X(i) + grid.x
        self.y = grid.Y(j) + grid.y

    def UpdateValue(self):
        l = self.grid.Get(i=self.i - 1, j=self.j)
        r = self.grid.Get(i=self.i + 1, j=self.j)
        u = self.grid.Get(i=self.i, j=self.j - 1)
        d = self.grid.Get(i=self.i, j=self.j + 1)
        self.value = ((0 if l is None else l.value) +
                      (0 if r is None else r.value) +
                      (0 if u is None else u.value) +
                      (0 if d is None else d.value)) % self.grid.max

    def Render(self):
        if self.value == 0:
            return

        position = Point(self.x, self.y)
        dimensions = Point(self.width, self.height)
        dotDimensions = Point(4, 4)

        imouseCurrent, jmouseCurrent = self.grid.iMouseCurrent, self.grid.jMouseCurrent

        highlightedByMouse = imouseCurrent == self.i and jmouseCurrent == self.j
        highlightedInRange = (imouseCurrent == self.i and self.j - 1 <= jmouseCurrent <= self.j + 1) or (self.i - 1 <= imouseCurrent <= self.i + 1 and jmouseCurrent == self.j)
        selectedByMouse = self.grid.imouse is not None and self.grid.jmouse is not None and self.grid.imouse == self.i and self.grid.jmouse == self.j
        selectedAndPressed = selectedByMouse and Screen.LeftMouseDown()
        drawDots = (not highlightedByMouse or selectedByMouse) and not selectedAndPressed

        color = self.grid.colorsNormal[self.value]
        if highlightedInRange:
            if not highlightedByMouse:
                color = self.grid.colorsHighlighted[self.value]
        # if not drawDots:
        #    color = Color.black
        if selectedAndPressed:
            color = self.grid.colorsOutline[self.value]

        dotColor = Color.black
        if selectedByMouse:
            dotColor = self.grid.colorsNormal[0]

        Screen.DrawRect(position, dimensions, color)

        thickness = 4
        showOutline = highlightedInRange and not highlightedByMouse
        shift = Point(0, -thickness) / 2 if showOutline else Point()
        if drawDots:
            if self.value == 1:
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 2, dotDimensions, dotColor)
            elif self.value == 2:
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, 0),
                                dotDimensions, dotColor)
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, 0),
                                dotDimensions, dotColor)
            elif self.value == 3:
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, dotDimensions.y * 0.9),
                                dotDimensions, dotColor)
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, dotDimensions.y * 0.9),
                                dotDimensions, dotColor)
                Screen.DrawRect(
                    position + shift + dimensions / 2 - dotDimensions / 3 + Point(0, -dotDimensions.y * 0.9),
                    dotDimensions, dotColor)
            elif self.value == 4:
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, -dotDimensions.y),
                                dotDimensions, dotColor)
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, -dotDimensions.y),
                                dotDimensions, dotColor)
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, + dotDimensions.y),
                                dotDimensions, dotColor)
                Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, + dotDimensions.y),
                                dotDimensions, dotColor)
        # Screen.DrawText(position + dimensions / 2 + Point(0, 2), str(self.value), self.colorText, self.fontSize, "center", "center")
        if showOutline:
            Screen.DrawRect(position + shift + Point(0, dimensions.y - thickness),
                            Point(dimensions.x, thickness - shift.y), self.grid.colorsNormal[self.value], filled=True)
            Screen.DrawLine(position, position + Point(0, dimensions.y + 1) + shift, self.grid.colorsOutline[self.value],
                            thickness=thickness)
            Screen.DrawLine(position + Point(dimensions.x - thickness + 1),
                            position + Point(dimensions.x - thickness + 1, dimensions.y + 1) + shift,
                            self.grid.colorsOutline[self.value], thickness=thickness)
            Screen.DrawLine(position + Point(0, dimensions.y - 1), position + Point(dimensions.x - 1, dimensions.y - 1),
                            self.grid.colorsOutline[self.value], thickness=1)
            Screen.DrawRect(position + Point(thickness / 2 - 1, 0) + shift,
                            dimensions - Point(thickness - 1, thickness), self.grid.colorsOutline[self.value], filled=False,
                            thickness=thickness)

class PlayGrid(Entity, Grid):
    def __init__(self, x, y, width, height, cellWidth, cellHeight):
        Grid.__init__(self, width, height, cellWidth, cellHeight)
        Entity.__init__(self, x, y)
        self.fontSize = 32
        self.colorText = Color.white
        self.colorOutline = Color.black
        self.colorsNormal = [(220, 128, 80), (128, 220, 80), (80, 160, 220), (220, 220, 80), (220, 80, 220)]
        self.colorsHighlighted = [(255, 220, 180), (220, 255, 180), (180, 230, 255), (255, 255, 180), (255, 180, 255)]
        self.colorsOutline = [(180, 96, 64), (96, 180, 64), (64, 105, 180), (180, 180, 64), (180, 64, 180)]
        self.max = len(self.colorsNormal)

        self.imouse = None
        self.jmouse = None

        for j in range(self.rows):
            for i in range(self.columns):
                self.Set(Tile(random.randint(0, self.max-1), self, i, j), i=i, j=j)

    @property
    def iMouseCurrent(self):
        return self.i((Screen.MousePosition() - self).x)

    @property
    def jMouseCurrent(self):
        return self.j((Screen.MousePosition() - self).y)

    def Update(self):
        if Screen.LeftMouseDown():
            x, y = Screen.MousePosition() - self
            self.imouse, self.jmouse = self.i(x), self.j(y)

        if Screen.LeftMouseReleased():
            i, j = self.imouse, self.jmouse
            tile = self.Get(i=i, j=j)
            if tile is not None:
                tile.UpdateValue()

    def Render(self):
        for j in range(self.rows):
            for i in range(self.columns):
                self.Get(i=i, j=j).Render()
        Screen.DrawText(Screen.MousePosition(), str(Screen.DeltaTime()))

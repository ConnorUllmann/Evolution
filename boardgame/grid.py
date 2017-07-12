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
        self.values = [[None]*self.rows for _ in range(self.columns)] if self.columns > 0 and self.rows > 0 else None

    def i(self, x):
        return math.floor(x / self.width * self.columns)

    def j(self, y):
        return math.floor(y / self.height * self.rows)

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

class PlayGrid(Entity, Grid):
    def __init__(self, width, height, cellWidth, cellHeight):
        Grid.__init__(self, width, height, cellWidth, cellHeight)
        Entity.__init__(self, 0, 0)
        self.fontSize = 32
        self.colorText = Color.white
        self.colorOutline = Color.black
        self.colorsNormal = [(220, 128, 80), (128, 220, 80), (80, 160, 220), (220, 220, 80)]
        self.colorsHighlighted = [(255, 220, 180), (220, 255, 180), (180, 230, 255), (255, 255, 180)]
        self.colorsOutline = [(180, 96, 64), (96, 180, 64), (64, 105, 180), (180, 180, 64)]
        self.max = len(self.colorsNormal)

        self.imouse = None
        self.jmouse = None

        for i in range(self.columns):
            for j in range(self.rows):
                self.Set(random.randint(0, self.max-1), i=i, j=j)

    def Update(self):
        if Screen.LeftMouseDown():
            x, y = Screen.MousePosition() - self
            self.imouse, self.jmouse = self.i(x), self.j(y)

        if Screen.LeftMouseReleased():
            i, j = self.imouse, self.jmouse
            l = self.Get(i=i-1, j=j)
            r = self.Get(i=i+1, j=j)
            u = self.Get(i=i, j=j-1)
            d = self.Get(i=i, j=j+1)
            value = ((0 if l is None else l) +
                     (0 if r is None else r) +
                     (0 if u is None else u) +
                     (0 if d is None else d)) % self.max
            self.Set(value, i=i, j=j)

    def Render(self):
        for i in range(self.columns):
            for j in range(self.rows):
                value = self.Get(i=i, j=j)

                if value == 0:
                    continue

                position = self + Point(self.cellWidth * i, self.cellHeight * j)
                dimensions = Point(self.cellWidth, self.cellHeight)
                dotDimensions = Point(6,6)

                xmouseCurrent, ymouseCurrent = Screen.MousePosition() - self
                imouseCurrent, jmouseCurrent = self.i(xmouseCurrent), self.j(ymouseCurrent)
                highlightedByMouse = imouseCurrent == i and jmouseCurrent == j
                highlightedInRange = imouseCurrent == i and j - 1 <= jmouseCurrent <= j + 1 or i - 1 <= imouseCurrent <= i + 1 and jmouseCurrent == j
                selectedByMouse = self.imouse is not None and self.jmouse is not None and self.imouse == i and self.jmouse == j
                selectedAndPressed = selectedByMouse and Screen.LeftMouseDown()
                drawDots = (not highlightedByMouse or selectedByMouse) and not selectedAndPressed

                color = self.colorsNormal[value]
                if highlightedInRange:
                    if not highlightedByMouse:
                        color = self.colorsHighlighted[value]
                #if not drawDots:
                #    color = Color.black
                if selectedAndPressed:
                    color = self.colorsOutline[value]

                dotColor = Color.black
                if selectedByMouse:
                    dotColor = self.colorsNormal[0]

                Screen.DrawRect(position, dimensions, color)

                thickness = 4
                showOutline = highlightedInRange and not highlightedByMouse
                shift = Point(0, -thickness) / 2 if showOutline else Point()
                if drawDots:
                    if value == 1:
                        Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 2, dotDimensions, dotColor)
                    if value == 2:
                        Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, 0), dotDimensions, dotColor)
                        Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, 0), dotDimensions, dotColor)
                    if value == 3:
                        Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, dotDimensions.y * 0.8), dotDimensions, dotColor)
                        Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, dotDimensions.y * 0.8), dotDimensions, dotColor)
                        Screen.DrawRect(position + shift + dimensions / 2 - dotDimensions / 3 + Point(0, -dotDimensions.y * 0.8), dotDimensions, dotColor)
                #Screen.DrawText(position + dimensions / 2 + Point(0, 2), str(value), self.colorText, self.fontSize, "center", "center")
                if showOutline:
                    Screen.DrawRect(position + shift + Point(0, dimensions.y - thickness), Point(dimensions.x, thickness - shift.y), self.colorsNormal[value], filled=True)
                    Screen.DrawLine(position, position + Point(0, dimensions.y+1) + shift, self.colorsOutline[value], thickness=thickness)
                    Screen.DrawLine(position + Point(dimensions.x - thickness+1), position + Point(dimensions.x - thickness+1, dimensions.y+1) + shift, self.colorsOutline[value], thickness=thickness)
                    Screen.DrawLine(position + Point(0, dimensions.y-1), position + Point(dimensions.x - 1, dimensions.y - 1), self.colorsOutline[value], thickness=1)
                    Screen.DrawRect(position + Point(thickness/2 - 1, 0) + shift, dimensions - Point(thickness - 1, thickness), self.colorsOutline[value], filled=False, thickness=thickness)
        Screen.DrawText(Screen.MousePosition(), str(Screen.DeltaTime()))

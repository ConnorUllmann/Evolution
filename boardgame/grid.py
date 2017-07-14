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
    GlowCountFadeTimerMax = 1
    DisplayValueChangePeriodMax = 0.1

    def __init__(self, value, grid, i, j):
        self.value = value
        self.displayValue = value
        self.displayValueTimer = 0
        self.displayValueChangePeriod = Tile.DisplayValueChangePeriodMax
        self.glowCount = 0
        self.grid = grid
        self.width = self.grid.cellWidth
        self.height = self.grid.cellHeight
        self.i = i
        self.j = j
        self.x = grid.X(i) + grid.x
        self.y = grid.Y(j) + grid.y
        self.lastDotPositions = []

    def CardinalNeighbors(self):
        l = self.grid.Get(i=self.i - 1, j=self.j)
        r = self.grid.Get(i=self.i + 1, j=self.j)
        u = self.grid.Get(i=self.i, j=self.j - 1)
        d = self.grid.Get(i=self.i, j=self.j + 1)
        return l, r, u, d

    @property
    def Value(self):
        return self.value % self.grid.max

    @property
    def GlowCount(self):
        return self.glowCount

    @GlowCount.setter
    def GlowCount(self, glowCount):
        self.glowCount = glowCount
        self.grid.glowCountFadeTimer = Tile.GlowCountFadeTimerMax

    @property
    def DisplayValue(self):
        return self.displayValue % self.grid.max

    def UpdateValue(self):
        l, r, u, d = self.CardinalNeighbors()
        self.value = ((0 if l is None else l.Value) +
                      (0 if r is None else r.Value) +
                      (0 if u is None else u.Value) +
                      (0 if d is None else d.Value))
        self.displayValue = 0
        self.grid.moves += 1
        if self.value == 0:
            self.grid.explodeTimer = PlayGrid.ExplodeTimerMax

    def UpdateGlowCounts(self, glowCount):
        l, r, u, d = self.CardinalNeighbors()
        remainingGlowCount = glowCount
        filled = []
        if u is not None:
            if remainingGlowCount > u.Value:
                filled.append(u)
                remainingGlowCount -= u.Value
            else:
                u.GlowCount = remainingGlowCount
                remainingGlowCount = 0

        if r is not None:
            if remainingGlowCount > r.Value:
                filled.append(r)
                remainingGlowCount -= r.Value
            else:
                r.GlowCount = remainingGlowCount
                remainingGlowCount = 0

        if d is not None:
            if remainingGlowCount > d.Value:
                filled.append(d)
                remainingGlowCount -= d.Value
            else:
                d.GlowCount = remainingGlowCount
                remainingGlowCount = 0

        if l is not None:
            if remainingGlowCount > l.Value:
                filled.append(l)
                remainingGlowCount -= l.Value
            else:
                l.GlowCount = remainingGlowCount
                remainingGlowCount = 0

        for neighbor in filled:
            neighbor.GlowCount = neighbor.Value

    @staticmethod
    def GetDotPositions(count, position, dimensions, dotDimensions):
        dotPositions = []
        if count == 1:
            dotPositions.append(position + dimensions / 2 - dotDimensions / 2)
        elif count == 2:
            dotPositions.append(position + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, 0))
            dotPositions.append(position + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, 0))
        elif count == 3:
            dotPositions.append(
                position + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, dotDimensions.y * 0.9))
            dotPositions.append(
                position + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, dotDimensions.y * 0.9))
            dotPositions.append(
                position + dimensions / 2 - dotDimensions / 3 + Point(0, -dotDimensions.y * 0.9))
        elif count == 4:
            dotPositions.append(
                position + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, -dotDimensions.y))
            dotPositions.append(
                position + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, -dotDimensions.y))
            dotPositions.append(
                position + dimensions / 2 - dotDimensions / 3 + Point(-dotDimensions.x, + dotDimensions.y))
            dotPositions.append(
                position + dimensions / 2 - dotDimensions / 3 + Point(dotDimensions.x, + dotDimensions.y))
        return dotPositions;

    @staticmethod
    def RenderBasic(value, x, y, grid):
        position = Point(x, y)
        dimensions = Point(grid.cellWidth, grid.cellHeight)

        color = grid.colorsNormal[value]
        Screen.DrawRect(position, dimensions, color)

        for dotPosition in Tile.GetDotPositions(value, position, dimensions, grid.dotDimensions):
            Screen.DrawRect(dotPosition, grid.dotDimensions, Color.black, filled=True)

    @staticmethod
    def RenderDot(x, y, color, lightness, grid):
        if lightness > 1:
            lightness = 1
        elif lightness < 0:
            lightness = 0
        color = (color[0] * lightness, color[1] * lightness, color[2] * lightness)
        Screen.DrawRect(Point(x, y), grid.dotDimensions, color, filled=True)

    def Render(self):

        if self.displayValue < self.value:
            self.displayValueTimer += Screen.DeltaTime()
            if self.displayValueTimer > self.displayValueChangePeriod:
                self.displayValue += 1
                if self.displayValue == self.value and self.DisplayValue == 0:
                    self.grid.explodeTimer = PlayGrid.ExplodeTimerMax
                self.UpdateGlowCounts(self.displayValue)
                self.displayValueTimer -= self.displayValueChangePeriod
                self.displayValueChangePeriod *= 1.1
        else:
            self.displayValue = self.value
            self.displayValueChangePeriod = Tile.DisplayValueChangePeriodMax

        if self.DisplayValue == 0:
            return

        position = Point(self.x, self.y)
        dimensions = Point(self.width, self.height)

        imouseCurrent, jmouseCurrent = self.grid.iMouseCurrent, self.grid.jMouseCurrent

        highlightedByMouse = imouseCurrent == self.i and jmouseCurrent == self.j
        highlightedInRange = (imouseCurrent == self.i and self.j - 1 <= jmouseCurrent <= self.j + 1) or (self.i - 1 <= imouseCurrent <= self.i + 1 and jmouseCurrent == self.j)
        selectedByMouse = self.grid.selectedTile == self
        selectedAndPressed = selectedByMouse and Screen.LeftMouseDown()
        drawDots = (not highlightedByMouse or selectedByMouse) and not selectedAndPressed

        color = self.grid.colorsNormal[self.DisplayValue]
        if highlightedInRange:
            if not highlightedByMouse:
                color = self.grid.colorsHighlighted[self.DisplayValue]
        if self.grid.glowCountFadeTimer > 0 and self in self.grid.selectedTileCardinalNeighbors:
            color = Color.lerp(color, Color.dark_grey, min(6 * self.grid.glowCountFadeTimer / Tile.GlowCountFadeTimerMax, 1))
        # if not drawDots:
        #    color = Color.black
        if selectedAndPressed:
            color = self.grid.colorsOutline[self.DisplayValue]



        dotColor = Color.black
        if selectedByMouse:
            dotColor = self.grid.colorsNormal[0]

        Screen.DrawRect(position, dimensions, color)

        thickness = 4
        showOutline = highlightedInRange and not highlightedByMouse
        shift = Point(0, -thickness) / 2 if showOutline else Point()
        if drawDots:
            dotPositions = Tile.GetDotPositions(self.DisplayValue, position + shift, dimensions, self.grid.dotDimensions)
            displayDotPositions = []
            speed = 0.2
            while len(self.lastDotPositions) < len(dotPositions):
                self.lastDotPositions.append(position + dimensions/2)
            for m in range(len(dotPositions)):
                displayDotPositions.append(self.lastDotPositions[m] + (dotPositions[m] - self.lastDotPositions[m]).normalized * speed)
            for n in range(len(displayDotPositions)):
                lightness = self.grid.glowCountFadeTimer / Tile.GlowCountFadeTimerMax + 0.25
                color = dotColor if self.glowCount <= n else Color.yellow
                self.RenderDot(displayDotPositions[n].x, displayDotPositions[n].y, color, lightness, self.grid)
            self.lastDotPositions = dotPositions
        # Screen.DrawText(position + dimensions / 2 + Point(0, 2), str(self.DisplayValue), self.colorText, self.fontSize, "center", "center")
        if showOutline:
            Screen.DrawRect(position + shift + Point(0, dimensions.y - thickness),
                            Point(dimensions.x, thickness - shift.y), self.grid.colorsNormal[self.Value], filled=True)
            Screen.DrawLine(position, position + Point(0, dimensions.y + 1) + shift, self.grid.colorsOutline[self.Value],
                            thickness=thickness)
            Screen.DrawLine(position + Point(dimensions.x - thickness + 1),
                            position + Point(dimensions.x - thickness + 1, dimensions.y + 1) + shift,
                            self.grid.colorsOutline[self.Value], thickness=thickness)
            Screen.DrawLine(position + Point(0, dimensions.y - 1), position + Point(dimensions.x - 1, dimensions.y - 1),
                            self.grid.colorsOutline[self.Value], thickness=1)
            Screen.DrawRect(position + Point(thickness / 2 - 1, 0) + shift,
                            dimensions - Point(thickness - 1, thickness), self.grid.colorsOutline[self.Value], filled=False,
                            thickness=thickness)

class PlayGrid(Entity, Grid):
    ExplodeTimerMax = 2

    def __init__(self, x, y, width, height, cellWidth, cellHeight):
        Grid.__init__(self, width, height, cellWidth, cellHeight)
        Entity.__init__(self, x, y)
        self.fontSize = 32
        self.colorText = Color.white
        self.colorOutline = Color.black
        self.colorsNormal = [Color.black, (220, 128, 80), (128, 220, 80), (80, 160, 220), (220, 80, 180), (80, 220, 220)]
        self.colorsHighlighted = [Color.black, (255, 220, 180), (220, 255, 180), (180, 230, 255), (255, 180, 230), (180, 255, 255)]
        self.colorsOutline = [Color.black, (180, 96, 64), (96, 180, 64), (64, 105, 180),(180, 64, 140),  (64, 180, 180)]
        self.max = 5#len(self.colorsNormal)
        self.dotDimensions = Point(4, 4)
        self.glowCountFadeTimer = 0
        self.explodeTimer = 0

        self.moves = 0
        self.selectedTile = None

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
            i, j = self.i(x), self.j(y)
            self.selectedTile = self.Get(i=i, j=j)

            self.glowCountFadeTimer = 0
            for tiles in self.values:
                for tile in tiles:
                    tile.glowCount = 0
                    tile.displayValue = tile.value

        if self.glowCountFadeTimer > 0:
            self.glowCountFadeTimer -= Screen.DeltaTime()
            if self.glowCountFadeTimer <= 0:
                self.glowCountFadeTimer = 0
                for tilesX in self.values:
                    for tiles in tilesX:
                        tiles.glowCount = 0
        if self.explodeTimer > 0:
            self.explodeTimer -= Screen.DeltaTime()
            if self.explodeTimer <= 0:
                self.explodeTimer = 0

        if Screen.LeftMouseReleased():
            if self.selectedTile is not None:
                self.selectedTile.UpdateValue()

    def Render(self):
        spaceBetween = 40
        arrowHeadLength = 6
        arrowThickness = 5
        marginArrow = 8
        margin = 6
        marginBox = 3
        marginGrid = 4

        Screen.DrawRect(self - Point(1, 1), Point(self.width, self.height) + 2 * Point(1, 1),
                        Color.white, filled=False)
        Screen.DrawRect(self - marginGrid * Point(1.5, 1.5), Point(self.width, self.height) + 2 * marginGrid * Point(1.5, 1.5),
                        Color.medium_grey, filled=False)
        Screen.DrawRect(self - marginGrid * Point(2.5, 2.5), Point(self.width, self.height) + 2 * marginGrid * Point(2.5, 2.5),
                        Color.dark_grey, filled=False)

        if self.selectedTile is not None:
            self.selectedTileCardinalNeighbors = self.selectedTile.CardinalNeighbors()
        for j in range(self.rows):
            for i in range(self.columns):
                self.Get(i=i, j=j).Render()

        totalWidth = self.max * (self.cellWidth + margin * 2) + (self.max - 1) * spaceBetween
        for valueTrue in range(self.max):
            value = (valueTrue+1+self.max) % self.max
            x = Screen.Width()/2 - totalWidth / 2 + (self.cellWidth + margin * 2) * valueTrue + valueTrue * spaceBetween
            y = 80

            if value == 0:
                explodeTimerPercent = self.explodeTimer / PlayGrid.ExplodeTimerMax
                explodeDistance = 40 * (1 - explodeTimerPercent ** 6)
                if 0 < explodeTimerPercent < 1:
                    Screen.DrawRect(Point(x, y) - Point(1, 1) * explodeDistance,
                                    Point(self.cellWidth, self.cellHeight) + Point(1, 1) * 2 * explodeDistance,
                                    Color.lerp(Color.black, Color.yellow, explodeTimerPercent ** 6))

            distanceTileMarginBottomToDots = 20
            dotRowSeparationDistance = 4
            neighborCount = 4

            dotSectionHeight = distanceTileMarginBottomToDots + (self.dotDimensions.y + dotRowSeparationDistance) * neighborCount

            if not Screen.LeftMouseDown() and self.selectedTile is not None and value == self.selectedTile.DisplayValue:
                v = min(1, 4 * self.glowCountFadeTimer / Tile.GlowCountFadeTimerMax)
                v = 1 - min(max(1-10*v**2, 1-10*(v-0.5)**2, 0), 1)
                color = (255 * v, 255 * v, 0)
                Screen.DrawRect(Point(x - marginBox, y - marginBox), Point(self.cellWidth - 1 + marginBox * 2, self.cellHeight + marginBox * 2 + dotSectionHeight), color, filled=False, thickness=4)


            Screen.DrawRect(Point(x - margin, y - margin),
                            Point(self.cellWidth + margin * 2, self.cellHeight + margin * 2 + dotSectionHeight), Color.dark_grey,
                            filled=False)

            if valueTrue >= 1:
                b = Point(x - margin - marginArrow, y + self.cellHeight/2)
                a = b + Point(-spaceBetween + marginArrow * 2, 0)
                Screen.DrawLine(a, b, Color.yellow, thickness=arrowThickness)
                Screen.DrawLine(b, b + Point(-arrowHeadLength, -arrowHeadLength), Color.yellow, thickness=arrowThickness)
                Screen.DrawLine(b, b + Point(-arrowHeadLength, arrowHeadLength), Color.yellow, thickness=arrowThickness)

            Tile.RenderBasic(value, x, y, self)
            if self.selectedTile is not None:
                rows = math.floor(self.selectedTile.displayValue / self.max)
                cols = self.selectedTile.displayValue % self.max
                for row in range(rows + (1 if valueTrue < cols else 0)):
                    dotPosition = Point(x + self.cellWidth / 2, y + self.cellHeight + distanceTileMarginBottomToDots + (self.dotDimensions.y + dotRowSeparationDistance) * row)
                    dotColor = Color.multiply(Color.yellow, min(8 * self.glowCountFadeTimer / Tile.GlowCountFadeTimerMax, 1))
                    dotLightness = 1
                    Tile.RenderDot(dotPosition.x - self.dotDimensions.x/2, dotPosition.y - self.dotDimensions.y/2, dotColor, dotLightness, self)
        Screen.DrawText(Point(16, 16), "Moves: {}".format(self.moves), fontSize=28, color=Color.yellow)

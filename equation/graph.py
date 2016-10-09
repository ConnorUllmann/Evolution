from screen import Screen
from equation import Equation

class Graph:

    ID = 0

    @staticmethod
    def GenerateID():
        _id = Graph.ID
        Graph.ID += 1
        return _id

    def __str__(self):
        return "graph-{}".format(self.id)

    def DrawPos(self, x, y):
        xR = self.xRange
        yR = self.yRange
        xB = self.xBounds
        yB = self.yBounds
        return ((x - xR[0]) / (xR[1] - xR[0]) * (xB[1] - xB[0]) + xB[0],
                (y - yR[0]) / (yR[1] - yR[0]) * (yB[1] - yB[0]) + yB[0])

    def Render(self):
        for i in range(0, len(self.equations)):
            equation = self.equations[i]
            points = []
            for target in self.targets:
                x = target[0]
                y = equation.y(x)
                points.append(self.DrawPos(x, y))
            Screen.DrawLines(points, self.equationColors[i])

        for equation in Equation.BestEquationsAllTimePair:
            points = []
            for target in self.targets:
                x = target[0]
                y = equation[1].y(x)
                points.append(self.DrawPos(x, y))
            Screen.DrawLines(points, (0, 255, 0), 3)            

        for target in self.targets:
            x = target[0]
            y = target[1]
            Screen.DrawCircle(self.DrawPos(x, y), 2)

    def SetEquations(self, equations):
        self.equationColors = []
        self.equations = equations
        sumMutationMagnitude = 0
        for equation in self.equations:
            sumMutationMagnitude += equation.genes["mutation_magnitude"].DNA[0]
            color = Screen.RandomColor()
            color = (color[0]/2, color[1]/2, color[2]/2)
            self.equationColors.append(color)
        #print(sumMutationMagnitude / len(self.equations))

    def SetTargets(self, targets):
        self.targets = targets
        self.xRange = [0, 1]
##        for target in self.targets:
##            if target[0] < self.xRange[0]:
##                self.xRange[0] = target[0]
##            if target[0] > self.xRange[1]:
##                self.xRange[1] = target[0]
        self.yRange = [0, 10000]
##        for target in self.targets:
##            if target[1] < self.yRange[0]:
##                self.yRange[0] = target[1]
##            if target[1] > self.yRange[1]:
##                self.yRange[1] = target[1]

    def Evolve(self):
        self.SetEquations(Equation.Generate(self.equations, self.targets))

    def ScreenPositionToXYValue(self, sp):
        x = (self.xRange[1] - self.xRange[0]) * (sp[0] - self.xBounds[0]) / (self.xBounds[1] - self.xBounds[0]) + self.xRange[0]
        y = (self.yRange[1] - self.yRange[0]) * (sp[1] - self.yBounds[0]) / (self.yBounds[1] - self.yBounds[0]) + self.yRange[0]
        return (x, y)

    def __init__(self, equations, targets):
        self.id = Graph.GenerateID()
        
        self.xBounds = (0, Screen.Width() - 0)
        self.yBounds = (0, Screen.Height() - 0)
        
        self.SetEquations(equations)
        self.SetTargets(targets)

        Screen.Instance.AddRenderFunction(self, self.Render)
        

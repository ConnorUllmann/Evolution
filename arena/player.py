from screen import Screen
from wall import Wall
import pygame
from utils import *
import math
from neural_network import NeuralNetwork

def inRange(x, _min, _max):
    return x >= _min and x <= _max

class Player:
    players = []

    def __init__(self, x, y):
        self.color = (255, 255, 255)
        self.radius = 12
        self.x = x
        self.y = y
        self.v = [0, 0]
        
        self.destroyed = False
        Screen.Instance.AddUpdateFunction(self, self.Update)
        Screen.Instance.AddRenderFunction(self, self.Render)
        Screen.PutOnTop(self)
        Player.players.append(self)


        self.writingNeuralNetwork = False
        self.loadNeuralNetworkFromFile = True
        self.nn = None

    def Destroy(self):
        if not self.destroyed:
            self.destroyed = True
            Screen.Instance.RemoveUpdateFunctions(self)
            Screen.Instance.RemoveRenderFunctions(self)
            Player.players.remove(self)

    def Update(self):
        vy = 0.5
        neuralOutputs = [0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            vy = -0.5
            neuralOutputs[0] = 1

        neuralInputs = [self.v[0], self.v[1]]
        lines = 10
        for x in range(lines):
            a = (x+1) / (lines+1) * math.pi - math.pi / 2
            length = 1000
            m = (self.x, self.y)
            n = (self.x + math.cos(a) * length, self.y + math.sin(a) * length)
            p = Player.LineCollidesWall(m, n)
            if p != None:
                n = p
            d = Distance(m, n) / length
            neuralInputs.append(d)

        if self.writingNeuralNetwork:
            with open("log.txt", "a") as output:
                output.write(",".join(str(x) for x in neuralInputs) + ",out=" + ",".join(str(x) for x in neuralOutputs)  + "\n")
        else:
            if self.nn is None:
                if self.loadNeuralNetworkFromFile:
                    self.nn = NeuralNetwork.Load("LastNeuralNetwork")
                else:
                    self.nn = NeuralNetwork([len(neuralInputs), 8, len(neuralOutputs)])
                    batchSize = 30
                    batches = []
                    with open("log.txt", "r") as _input:
                        tests = []
                        for line in _input:
                            lineSplit = line.split(",out=")
                            inputs = list(float(x) for x in lineSplit[0].split(","))
                            outputs = list(float(str(x).replace("\n", "")) for x in lineSplit[1].split(","))
                            tests.append([inputs, outputs])
                            while len(tests) >= batchSize:
                                batches.append(tests[:batchSize])
                                tests = tests[batchSize:]
                    print("Beginning training!")
                    for x in range(1000):
                        self.nn.trainWithBatches(batches, 0.0025)
                    print("Done training!")
                    self.nn.save("LastNeuralNetwork")
            outputs = self.nn.output(neuralInputs)
            if outputs[0] == 1:
                vy = -0.5
        
        self.v[1] += vy
        
        self.x += self.v[0]
        self.y += self.v[1]

        self.y = min(max(self.y, 0), Screen.Instance.height)

        hitWall = False
        for wall in Wall.walls:
            if self.CollidesWall(wall):
                hitWall = True
                break

        if hitWall:
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)
        pass

    def Render(self):
        Screen.DrawCircle((self.x, self.y), self.radius, self.color)
        pass

    @staticmethod
    def LineCollidesWall(m, n):
        intersectionPoints = []
        for wall in Wall.walls:
            a = (LinesIntersectionPoint(m, n, (wall.x, wall.y), (wall.x + wall.w, wall.y)))
            b = (LinesIntersectionPoint(m, n, (wall.x, wall.y), (wall.x, wall.y + wall.h)))
            c = (LinesIntersectionPoint(m, n, (wall.x + wall.w, wall.y), (wall.x + wall.w, wall.y + wall.h)))
            d = (LinesIntersectionPoint(m, n, (wall.x, wall.y + wall.h), (wall.x + wall.w, wall.y + wall.h)))
            if a is not None:
                intersectionPoints.append(a)
            if b is not None:
                intersectionPoints.append(b)
            if c is not None:
                intersectionPoints.append(c)
            if d is not None:
                intersectionPoints.append(d)
        pMin = None
        d2Min = None
        for p in intersectionPoints:
            d2 = DistanceSq(m, p)
            if d2Min is None or d2 < d2Min:
                d2Min = d2
                pMin = p
        return pMin

    def CollidesWall(self, wall):
        xO = inRange(self.x, wall.x, wall.x + wall.w) or inRange(wall.x, self.x, self.x + self.radius)
        yO = inRange(self.y, wall.y, wall.y + wall.h) or inRange(wall.y, self.y, self.y + self.radius)
        return xO and yO

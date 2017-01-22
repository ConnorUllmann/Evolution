from screen import Screen
import pygame
from utils import *
import math
from entity import Entity
from neural_network import NeuralNetwork

class Gladiator(Entity):

    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.color = self.defaultColor = (255, 255, 255)
        self.radius = 16
        
        self.AddState("normal", self.UpdateNormal)
        self.AddState("hit", self.UpdateHit, self.BeginHit, self.EndHit)
        self.AddState("dash", self.UpdateDash)
        self.SetState("normal")

    def UpdateNormal(self):
        pass

    def UpdateHit(self):
        self.hitTimer -= 1
        if self.hitTimer <= 0:
            self.hitTimer = 0
            self.SetState("normal")

    def BeginHit(self):
        self.color = (255, 0, 0)
        self.hitTimer = 60

    def EndHit(self):
        self.color = self.defaultColor

    def UpdateDash(self):
        pass

    def Render(self):
        Screen.DrawCircle(self, self.radius, self.color)

    def collides(self, other):
        return CirclesCollide(self, self.radius, other, other.radius)

    @property
    def stateInt(self):
        if self.state == "normal":
            return 0
        if self.state == "hit":
            return 1
        if self.state == "dash":
            return 2
        return -1

    def stateIntToName(self, stateInt):
        if stateInt == 0:
            return "normal"
        if stateInt == 1:
            return "hit"
        if stateInt == 2:
            return "dash"
        return None

    def ExecuteOutputs(self, outputs):
        if outputs[0] > 0.5:
            self.v.x -= 5
        if outputs[1] > 0.5:
            self.v.x += 5
        if outputs[2] > 0.5:
            self.v.y -= 5
        if outputs[3] > 0.5:
            self.v.y += 5
        self.SetState(self.stateIntToName(outputs[4]))

    def GetNeuralInputs(self, classNames):
        neuralInputs = [self.v.x, self.v.y, self.stateInt]
        entities = []
        for className in classNames:
            entities.extend(Entity.GetAllEntitiesOfType(className))
        length = 1000
        lines = 18
        for i in range(lines):
            m = Point(self.x, self.y)
            n = Point(length, 0)
            n.radians = i / lines * math.pi * 2
            n += m
            for entity in entities:
                collisionPoints = CircleLineCollide(entity, entity.radius, m, n)
                collisionPointsCount = len(collisionPoints)
                if collisionPointsCount == 2:
                    if (collisionPoints[0] - self).lengthSq < (collisionPoints[1] - self).lengthSq:
                        n = collisionPoints[0]
                    else:
                        n = collisionPoints[1]
                elif collisionPointsCount == 1:
                    n = collisionPoints[0]
            neuralInputs.append(m.distanceTo(n) / length)
        return neuralInputs

    @staticmethod
    def NeuralInputsAndOutputsString(neuralInputs, neuralOutputs):
        return ",".join(str(int(x*1000)/1000) for x in neuralInputs) + "|" + ",".join(str(int(x*1000)/1000) for x in neuralOutputs)

class Player(Gladiator):

    def __init__(self, x, y):
        Gladiator.__init__(self, x, y)
        self.color = self.defaultColor = (0, 255, 0)

    def UpdateNormal(self):
        self.v.x = self.v.y = 0
        keys = pygame.key.get_pressed()
        neuralInputs = self.GetNeuralInputs(["AI"])
        neuralOutputs = [0,0,0,0,0]
        neuralOutputs[0] = int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        neuralOutputs[1] = int(keys[pygame.K_RIGHT] or keys[pygame.K_d])
        neuralOutputs[2] = int(keys[pygame.K_UP] or keys[pygame.K_w])
        neuralOutputs[3] = int(keys[pygame.K_DOWN] or keys[pygame.K_s])
        neuralOutputs[4] = self.stateInt
        self.ExecuteOutputs(neuralOutputs)

        allZeroes = True
        for neuralOutput in neuralOutputs:
            if neuralOutput > 0.5:
                allZeroes = False
                break
        if not allZeroes:
            with open("dataset.txt", "a") as output:
                output.write(Gladiator.NeuralInputsAndOutputsString(neuralInputs, neuralOutputs) + "\n")
                    
        self.x += self.v.x
        self.y += self.v.y

        self.x = min(max(self.x, 0), Screen.Instance.width)
        self.y = min(max(self.y, 0), Screen.Instance.height)

class AI(Gladiator):

    def __init__(self, x, y):
        Gladiator.__init__(self, x, y)
        self.color = self.defaultColor = (0, 128, 255)
        self.InitializeNeuralNetwork()

    def UpdateNormal(self):
        neuralInputs = self.GetNeuralInputs(["Player"])
        neuralOutputs = self.GetNeuralOutputs(neuralInputs)
        self.ExecuteOutputs(neuralOutputs)
        
        self.x += self.v.x
        self.y += self.v.y

        self.x = min(max(self.x, 0), Screen.Instance.width)
        self.y = min(max(self.y, 0), Screen.Instance.height)

        players = Entity.GetAllEntitiesOfType("Player")
        for player in players:
            if self.collides(player):
                self.SetState("hit")

    def Render(self):
        Gladiator.Render(self)

    def GetNeuralOutputs(self, neuralInputs):
        return self.nn.output(neuralInputs)

    def UpdateNeuralNetwork(self):
        neuralInputs = self.GetNeuralInputs()
        neuralOutputs = self.GetNeuralOutputs(neuralInputs)

    def TestsToBatches(self, tests, batchSize=30):
        batches = []
        while len(tests) >= batchSize:
            batches.append(tests[:batchSize])
            tests = tests[batchSize:]
        return batches

    def LogFileToBatches(self, filename):
        batches = []
        with open(filename, "r") as _input:
            tests = []
            for line in _input:
                lineSplit = line.split("|")
                inputs = list(float(x) for x in lineSplit[0].split(","))
                outputs = list(float(str(x).replace("\n", "")) for x in lineSplit[1].split(","))
                tests.append([inputs, outputs])
            batches = self.TestsToBatches(tests)
        return batches
        
    def InitializeNeuralNetwork(self, loadFromFile=False):
        if loadFromFile:
            try:
                with open("LastNeuralNetwork.txt", "r") as i:
                    pass
                self.nn = NeuralNetwork.Load("LastNeuralNetwork")
            except:
                pass
                #neuralInputs = self.GetNeuralInputs(["Player"])
                #neuralOutputs = self.GetNeuralOutputs(neuralInputs)
                #self.nn = NeuralNetwork([len(neuralInputs), 8, len(neuralOutputs)])
        else:
            batches = self.LogFileToBatches("dataset.txt")
            print("Beginning training!")
            inputCount = len(batches[0][0][0])
            outputCount = len(batches[0][0][1])
            self.nn = NeuralNetwork([inputCount, 12, outputCount])
            for x in range(100):
                self.nn.trainWithBatches(batches, 0.025)
            print("Done training!")
            self.nn.save("LastNeuralNetwork")
    

from lifeform import Lifeform
from gene import Gene
from part import Part
from screen import *
from random import randint, random
from math import *
from utils import *
from time import time

class Body(Lifeform):
    ANGULAR_FRICTION = 0.9
    FRICTION = 0.99

    ID = 0

    def SetAngle(self, value):
        self.angle = value % (2 * pi)
    def GetAngle(self):
        return self.angle

    def PartCountFromDNA(self):
        return int(len(self.genes["structure"].DNA)/2)

    def PartIndexFromDNA(self, index):
        DNA = self.genes["structure"].DNA
        return DNA[(index*2)%len(DNA)]

    def PartPropertyFromDNA(self, index):
        DNA = self.genes["structure"].DNA
        return DNA[(index*2+1)%len(DNA)]

    def GenerateParts(self):
        parts = []
        partCount = self.PartCountFromDNA()
        for i in range(0, partCount):
            spiralPosition = Spiral(i)
            partIndex = self.PartIndexFromDNA(i)
            _position = (self.x + 2 * self.radius * spiralPosition[0], self.y + 2 * self.radius * spiralPosition[1])
            _body = self
            _radius = self.radius
            _property = self.PartPropertyFromDNA(i)
            part = Part.NewPartFromIndex(partIndex, _position, _body, _radius, _property)
            parts.append(part)
        for part in parts:
            part.Setup()
        return parts

    def StartingLifeFromDNA(self):
        life = 0
        for base in self.genes["life"].DNA:
            life += base
        return life

    def MaturationPeriodFromDNA(self):
        maturationPeriod = 0
        for base in self.genes["maturation_period"].DNA:
            maturationPeriod += base
        return maturationPeriod

    def GenerateID(self):
        self.id = Body.ID
        Body.ID += 1

    def __str__(self):
     return "body-{}".format(self.id)

    def __init__(self, position, parents, genes=None):
        self.GenerateID()
        super().__init__(parents)

        if genes is not None:
            self.genes = genes
        
        self.x = position[0]
        self.y = position[1]
        self.centerOfMass = (self.x, self.y)
        self.torque = 0
        self.angularVelocity = 0
        self.SetAngle(0)
        self.momentum = [0,0]
        self.radius = 10
        self.color = (255, 255, 255)
        self.maturationPeriod = self.MaturationPeriodFromDNA()
        self.timeStart = time()
        self.bannedMates = []
        self.parts = self.GenerateParts()
        self.lifeStart = self.life = self.StartingLifeFromDNA()

        mass = 0
        for part in self.parts:
            mass += part.mass
        self.mass = mass
        
        self.SetAngle(random() * 2 * pi)
        
        Screen.Instance.AddUpdateFunction(self, self.Update)
        Screen.Instance.AddRenderFunction(self, self.Render)

    def speed2(self):
        return LengthSq(Scale(self.momentum, 1/self.mass))
    def speed(self):
        return sqrt(self.speed2())

    def Destroy(self):
        for part in self.parts:
            part.Destroy()
        Screen.Instance.RemoveUpdateFunctions(self)
        Screen.Instance.RemoveRenderFunctions(self)

    def AddImpulse(self, *args):
        torque = Torque(*args)
        torquePushVector = TorquePushVector(*args)
        torquePullVector = TorquePullVector(*args)
        arbitraryMult = 100
        self.momentum = Add(Scale(Add(torquePushVector, torquePullVector), arbitraryMult), self.momentum)
        self.torque += torque

    def ApplyTorque(self):
        self.angularVelocity += self.torque / self.mass
        self.torque = 0

    def Physics(self):
        self.SetAngle(self.GetAngle() + self.angularVelocity)
        self.angularVelocity = self.angularVelocity * Body.ANGULAR_FRICTION
        self.centerOfMass = (self.x, self.y)
        self.ApplyTorque()
        self.x += self.momentum[0] / self.mass
        self.y += self.momentum[1] / self.mass
        self.momentum = Scale(Normalize(self.momentum), Length(self.momentum) * Body.FRICTION)
        
        #print(self.angularVelocity)

    def Mate(self, other):
        if time() - self.timeStart <= self.maturationPeriod:
            return None
        if len(Part.parts) > 200:
            return None
        if other in self.bannedMates:
            return None
        self.bannedMates.append(other)
        return Body(((self.x + other.x) / 2, (self.y + other.y) / 2), [self, other])

    def SubtractLife(self, amount):
        self.life -= amount
        if self.life <= 0:
            self.Destroy()
        return self.life

    def AddLife(self, amount):
        self.life += amount
        return self.life

    def Bounds(self):
        if len(self.parts) > 0:
            lastPart = self.parts[len(self.parts)-1]
            buffer = hypot(lastPart.x() - self.x, lastPart.y() - self.y)
            if self.x < -buffer:
                self.x = Screen.Width() + buffer #-buffer
            if self.y < -buffer:
                self.y = Screen.Height() + buffer #-buffer
            if self.x > Screen.Width() + buffer:
                self.x = -buffer #Screen.Width() + buffer
            if self.y > Screen.Height() + buffer:
                self.y = -buffer #Screen.Height() + buffer
            #if self.x < -buffer or self.x > Screen.Width() + buffer or self.y < -buffer or self.y > Screen.Height() + buffer:
            #    self.Destroy()

    def Update(self):
        self.Physics()
        self.Bounds()

    def Render(self):
        self.color = (0, min(max(255 * self.life / self.lifeStart, 0), 255), 0)
        Screen.DrawCircle((self.x, self.y), int(self.radius*0.8), self.color)
        Screen.Instance.DrawLine((self.x, self.y), (self.x + 15 * cos(self.angle), self.y + 15 * sin(self.angle)), (255, 0, 0))

def CreateStructuredBody(position, genes):
    geneList = []
    for trait in genes:
        geneList.append(Gene(trait, genes[trait][0], genes[trait][1]))
    _genes = {}
    for gene in geneList:
        _genes[gene.trait] = gene
    return Body(position, [], _genes)

def PreGame():
##    body = CreateStructuredBody((400, 200), {
##        "structure":[[0, 0, 4, 2, 2, 2, 3, 3, 4, 6, 5, 5], [0, 5]],
##        "speed":[[1], [0, 1]],
##        "life":[[100000], [1, 100000]],
##        "maturation_period":[[2], [1, 50]]
##        })
##    body = CreateStructuredBody((200, 200), {
##        "structure":[[0, 0, 4, 6, 2, 2, 3, 3, 4, 2, 5, 5], [0, 5]],
##        "speed":[[1], [0, 1]],
##        "life":[[100000], [1, 100000]],
##        "maturation_period":[[2], [1, 50]]
##        })
 #   body.PrintGenes()
    for i in range(0, 20):
        body = Body((randint(0, Screen.Width()), randint(0, Screen.Height())), [])

def UpdateGame():
    pass

def StartGame():
    Screen(600, 400)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Start()

StartGame()

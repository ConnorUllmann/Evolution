from lifeform import Lifeform
from gene import Gene
from part import Part
from screen import *
from random import randint, random
from math import *
from utils import *
from time import time

class Body(Lifeform):
    
    ANGULAR_FRICTION = 0.8
    FRICTION = 0.96

    ID = 0
    bodies = []

    def GenerateID(self):
        self.id = Body.ID
        Body.ID += 1

    def __str__(self):
     return "body-{}".format(self.id)

    def SetAngle(self, value):
        self.angle = value % (2 * pi)
    
    def GetAngle(self):
        return self.angle

    def speed2(self):
        return LengthSq(Scale(self.momentum, 1/self.mass))
    
    def speed(self):
        return sqrt(self.speed2())

# --- \\ Properties From DNA ---

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

    def RefractoryPeriodFromDNA(self):
        refractoryPeriod = 0
        for base in self.genes["refractory_period"].DNA:
            refractoryPeriod += base
        return refractoryPeriod

    def SpeciesThresholdFromDNA(self):
        speciesThreshold = 0
        for base in self.genes["species_threshold"].DNA:
            speciesThreshold += base
        return max(min(speciesThreshold/100, 1), 0)

    def PartCountFromDNA(self):
        return int(len(self.genes["structure"].DNA)/2)

    def PartIndexFromDNA(self, index):
        DNA = self.genes["structure"].DNA
        return DNA[(index*2)%len(DNA)]

    def PartPropertyFromDNA(self, index):
        DNA = self.genes["structure"].DNA
        return DNA[(index*2+1)%len(DNA)]

# --- // Properties From DNA ---

    def GenerateParts(self):
        self.parts = []
        partCount = self.PartCountFromDNA()
        for i in range(0, partCount):
            spiralPosition = Spiral(i)
            partIndex = self.PartIndexFromDNA(i)
            _position = (self.x + Part.SEPARATION_MULT * self.radius * spiralPosition[0], self.y + Part.SEPARATION_MULT * self.radius * spiralPosition[1])
            _body = self
            _radius = self.radius
            _property = self.PartPropertyFromDNA(i)
            part = Part.NewPartFromIndex(partIndex, _position, _body, _radius, _property)
            self.parts.append(part)
        part0 = Part.FirstRealPart(self.parts, False)
        if part0 is not None:
            part0.highlight = True
        for part in self.parts:
            if part is None:
                continue
            part.Setup(self.parts)

    @staticmethod
    def GenerationFromParents(parents):
        if parents is None or len(parents) <= 0:
            return 0
        parentsMaxGeneration = 0
        for parent in parents:
            if parent.generation > parentsMaxGeneration:
                parentsMaxGeneration = parent.generation
        return parentsMaxGeneration+1

    counts = {}
    countsPart = {}
    @staticmethod
    def AddToHalf(half, partsCount):
        if half not in Body.counts:
            Body.counts[half] = 0
            Body.countsPart[half] = 0
        Body.counts[half] += 1
        Body.countsPart[half] += partsCount
        
    @staticmethod
    def RemoveFromHalf(half, partsCount):
        if half in Body.counts:
            Body.counts[half] -= 1
            Body.countsPart[half] -= partsCount

    def __init__(self, position, parents, genes=None):
        self.GenerateID()
        Body.bodies.append(self)
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
        self.visible = True
        self.maturationPeriod = self.MaturationPeriodFromDNA()
        self.timeStart = time()
        self.bannedMates = []
        self.GenerateParts()
        self.partsCount = self.PartsCount() #The number of actual parts (not including empty slots)
        self.destroyed = False
        self.lifeStart = self.life = self.StartingLifeFromDNA()
        self.generation = self.GenerationFromParents(parents)
        self.speciesThreshold = self.SpeciesThresholdFromDNA()

        mass = 0
        for part in self.parts:
            if part is None:
                continue
            mass += part.mass
        self.mass = mass

        maxDistanceSq = -1
        maxDistancePart = None
        for part in self.parts:
            if part is None:
                continue
            distanceSq = DistanceSq((self.x, self.y), (part.x(), part.y()))
            if distanceSq > maxDistanceSq:
                maxDistanceSq = distanceSq
                maxDistancePart = part
        
        self.half = "right" if self.x > Screen.Width()/2 else "left"
        self.partsCountStart = self.PartsCount()
        Body.AddToHalf(self.half, self.partsCountStart)
        
        self.radius = sqrt(maxDistanceSq) + maxDistancePart.radius
        
        self.SetAngle(random() * 2 * pi)
        
        Screen.Instance.AddUpdateFunction(self, self.Update)
        Screen.Instance.AddRenderFunction(self, self.Render)

        Screen.PutOnTop(self)
        if self.partsCount <= 0:
            self.Destroy()

    def PartsCount(self):
        count = 0
        for part in self.parts:
            if part is None:
                continue
            count+=1
        return count

    def HasHeart(self):
        for part in self.parts:
            if part is None:
                continue
            if type(part).__name__ == "Heart":
                return True
        return False

    def Print(self):
        print(" --- Body --- ")
        for trait in self.genes:
            print("[{0}] {1}".format(trait, self.genes[trait].DNAString()))

    def Destroy(self):
        if not self.destroyed:
            self.destroyed = True
            for part in self.parts:
                if part is None:
                    continue
                part.Destroy()
            Screen.Instance.RemoveUpdateFunctions(self)
            Screen.Instance.RemoveRenderFunctions(self)
            Body.bodies.remove(self)
            Body.RemoveFromHalf(self.half, self.partsCountStart)

    #Do not call explicitly--this is used by parts' destroy function when they are removed
    def RemovePart(self, part):
        i = self.parts.index(part)
        self.parts[i] = None

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

    @staticmethod
    def AreSameSpecies(a_body, b_body):
        speciesComparison = Lifeform.CompareGenomes(a_body.genes, b_body.genes)
        return speciesComparison >= a_body.speciesThreshold and speciesComparison >= b_body.speciesThreshold

    def Mate(self, other):
        if time() - self.timeStart <= self.maturationPeriod:
            return None
        if Body.countsPart[self.half] > 200: #len(Part.parts) > 200:
            return None
        if other in self.bannedMates or self in other.bannedMates:
            return None
        if not Body.AreSameSpecies(self, other):
            return None
        _parts = list(self.parts)
        _parts.extend(other.parts)
        for part in _parts:
            if part is None:
                continue
            part.SubtractMass((part.massStart+part.armor)/4)
        #other.bannedMates.append(self)
        #self.bannedMates.append(other)
        child = Body(((self.x + other.x) / 2, (self.y + other.y) / 2), [self, other])
        #other.bannedMates.append(child)
        #self.bannedMates.append(child)
        #child.bannedMates.append(self)
        #child.bannedMates.append(other)
        return child

    def Collides(self, body):
        return CirclesCollide((self.x, self.y), self.radius, (body.x, body.y), body.radius)

    @staticmethod
    def AllCollidingBodies(body):
        collidingBodies = []
        for _body in Body.bodies:
            if _body == body:
                continue
            if body.Collides(_body):
                collidingBodies.append(_body)
        return collidingBodies

    @staticmethod
    def AllCollidingParts(part):
        collidingParts = []
        bodies = Body.AllCollidingBodies(part.body)
        for body in bodies:
            for _part in body.parts:
                if _part is None:
                    continue
                if part.Collides(_part):
                    collidingParts.append(_part)
        return collidingParts

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
            lastPart = None
            n = 1
            while lastPart is None:
                lastPart = self.parts[len(self.parts)-n]
                n += 1
                if n > len(self.parts):
                    return
            buffer = 2*hypot(lastPart.x() - self.x, lastPart.y() - self.y)
            boundsLeft = -buffer #if self.half is None or self.half == "left" else Screen.Width()/2+buffer
            boundsRight = Screen.Width() + buffer #if self.half is None or self.half == "right" else Screen.Width()/2 - buffer
            boundsTop = -buffer
            boundsBottom = Screen.Height() + buffer
            moved = False
            if self.x < boundsLeft:
                self.x = boundsLeft #boundsRight
                moved = True
            if self.y < boundsTop:
                self.y = boundsBottom
                moved = True
            if self.x > boundsRight:
                self.x = boundsRight #boundsLeft
                moved = True
            if self.y > boundsBottom:
                self.y = boundsTop
                moved = True
            if moved:
                self.angle += 0.05 * (random() - 0.5)

    def Update(self):
        for part in self.parts:
            if part is None:
                continue
            part.Collide(Body.AllCollidingParts(part))
            part.Update()

        
        self.Physics()
        self.Bounds()

        if not self.HasHeart():
            self.SubtractLife(10000)

        if time() - self.timeStart > 90:
            self.Destroy()

    def Render(self):
        if not self.visible:
            return
        
        for part in self.parts:
            if part is None:
                continue
            part.Render()
        #self.color = (0, min(max(255 * self.life / self.lifeStart, 0), 255), 0, 128)
        #Screen.DrawCircle((self.x, self.y), int(self.radius), self.color)
        #Screen.Instance.DrawLine((self.x, self.y), (self.x + 15 * cos(self.angle), self.y + 15 * sin(self.angle)), (255, 0, 0))

def CreateStructuredBody(position, genes):
    geneList = []
    for trait in genes:
        geneList.append(Gene(trait, genes[trait][0], genes[trait][1], genes[trait][2]))
    _genes = {}
    for gene in geneList:
        _genes[gene.trait] = gene
    return Body(position, [], _genes)

def Setup():
##    body0 = CreateStructuredBody((400, 200), {
##        "structure":[[0, 0, 4, 2, 2, 2, 3, 3, 4, 6, 5, 5], "int", 2, [0, 8]],
##        "life":[[100000, 100000, 100000, 100000, 100000, 100000, 100000], "int", 1, [1, 100000]],
##        "maturation_period":[[5], "int", 1, [1, 50]],
##        "refractory_period":[[6], "int", 1, [4, 10]],
##        "species_threshold":[[0.08], "float", 0, [0, 0.95]]
##        })
##    body1 = CreateStructuredBody((200, 200), {
##        "structure":[[0, 0, 4, 6, 2, 2, 3, 3, 4, 2, 5, 5], "int", 2, [0, 8]],
##        "life":[[100000, 100000, 100000, 100000, 100000, 100000, 100000], "int", 1, [1, 100000]],
##        "maturation_period":[[5], "int", 1, [1, 50]],
##        "refractory_period":[[6], "int", 1, [4, 10]],
##        "species_threshold":[[0.08], "float", 0, [0, 0.95]]
##        })
    body0 = CreateStructuredBody((400, 200), {
        "structure":[[0, 1, 2, 3, 4, 5, 6, 7], 2, [0, 8]],
        "life":[[0, 0, 0], 1, [1, 10]],
        "maturation_period":[[1, 1], 1, [1, 50]],
        "refractory_period":[[4], 1, [4, 6]],
        "species_threshold":[[6, 7, 5, 5, 0, 9, 8, 9, 1, 2], 2, [0, 10]]
        })
    body1 = CreateStructuredBody((200, 200), {
        "structure":[[7, 6, 5, 4, 3, 2, 1, 0], 2, [0, 8]],
        "life":[[1, 1, 1], 2, [20, 30]],
        "maturation_period":[[2, 2], 1, [1, 50]],
        "refractory_period":[[3], 1, [8, 10]],
        "species_threshold":[[0, 8, 9, 8, 5, 4, 5, 10, 1, 4], 0, [0, 10]]
        })
##    body0.Print()
##    body1.Print()
##    bodyc = Body((300, 200), [body0, body1])
##    bodyc.Print()
##    input("")
    
    body2 = CreateStructuredBody((250, 250), {
        "structure":[[9, 0, 4, 6, 2, 2, 3, 3, 7, 2, 5, 5], 2, [0, 8]],
        "life":[[100000, 100000, 100000, 100000, 100000, 100000], 1, [1, 100000]],
        "maturation_period":[[5, 10], 1, [1, 100]],
        "refractory_period":[[6], 1, [4, 10]],
        "species_threshold":[[1, 5, 3, 9, 8, 8, 10, 7, 4, 2], 0, [0, 10]]
        })
    body2.SetAngle(-pi/2)
    

def PreGame():
    #Setup()
    for i in range(0, 100):
        body = Body((randint(0, Screen.Width()), randint(0, Screen.Height())), [])

maxGeneration = -1
speciesThresholdAverage = 0
def UpdateGame():
    global maxGeneration, speciesThresholdAverage

    if len(Body.bodies) <= 0 and maxGeneration >= 0:
        print("None remain.")
        maxGeneration = -1

    if len(Body.bodies) <= 3:
        bodies = []
        for body in Body.bodies:
            bodies.append(body)
        Body((int(random() * Screen.Width()), int(random() * Screen.Height())), bodies)
        print("Low population - generating children")
        maxGeneration = -1

    speciesThresholdSum = 0
    for body in Body.bodies:
        speciesThresholdSum += body.speciesThreshold
        if body.generation > maxGeneration:
            maxGeneration = body.generation
            print("Generation {}'s first member was just born.".format(maxGeneration))
    speciesThresholdAverage = speciesThresholdSum / len(Body.bodies)
    pygame.display.set_caption("Parts: {}".format(len(Part.parts)))#"SpeciesThresholdAverage: {}".format(int(speciesThresholdAverage*1000)/1000))

def RenderGame():
    pass
    
def StartGame():
    Screen(600, 400)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

StartGame()

from screen import Screen
from math import *
from time import time
from utils import *
from random import shuffle, randint, random

class Part:

    SEPARATION_MULT = 1.2

    ID = 0

    def GenerateID(self):
        self.id = Part.ID
        Part.ID += 1

    @staticmethod
    def NewPartFromIndex(index, *args):
        i = index % 7
        if i == 0:
            return Muscle(*args)
        if i == 1:
            return Bone(*args)
        if i == 2:
            return Heart(*args)
        if i == 3:
            return Gills(*args)
        if i == 4:
            return Propellor(*args)
        if i == 5:
            return Pulser(*args)
        if i == 6:
            return None
        

    def __str__(self):
     return "part-{}".format(self.id)

    parts = []

    def __init__(self, position, body, radius, cost, mass):
        self.GenerateID()
        Part.parts.append(self)
        self.body = body
        self.angleBodyToPart = atan2(position[1]-self.body.y, position[0]-self.body.x)
        self.angleOffset = self.body.GetAngle()
        self.distance = hypot(position[0] - self.body.x, position[1] - self.body.y)
        self.radius = radius
        self.power = 0.05
        self.armor = 0.01
        self.rateRepair = 0.2
        self.color = (80, 80, 80)
        self.cost = cost
        self.massStart = self.mass = mass
        self.timeStart = time()
        self.destroyed = False
        self.highlight = False
        #Screen.Instance.AddUpdateFunction(self, self.Update)
        #Screen.Instance.AddRenderFunction(self, self.Render)

    def Destroy(self):
        if not self.destroyed:
            self.destroyed = True
            Part.parts.remove(self)
            self.body.RemovePart(self)
            #Screen.Instance.RemoveUpdateFunctions(self)
            #Screen.Instance.RemoveRenderFunctions(self)

    def Collides(self, part):
        return CirclesCollide((self.x(), self.y()), self.radius, (part.x(), part.y()), part.radius)

    #Called every frame from the parent body part.
    #"parts" is a list of all parts this body collides with on other bodies
    def Collide(self, parts):
        for part in parts:
            part.SubtractMass(self.power * (self.body.speed2()+1)/30)

    def SubtractMass(self, amount):
        self.mass -= max(amount - self.armor, 0)
        if self.mass <= 0:
            self.mass = 0
            self.Destroy() 
        
    #Gets a random part that is not null from the list of parts
    @staticmethod
    def FirstRealPart(parts, random=False):
        if random:
            shuffle(parts)
        for i in range(0, len(parts)):
            if parts[i] is not None:
                return parts[i]
        return None

    def Neighbors(self):
        collidedParts = []
        for part in self.body.parts:
            if part is self or part is None:
                continue
            if LengthSq((part.x() - self.x(), part.y() - self.y())) <= (part.radius + Part.SEPARATION_MULT * self.body.radius)**2:
                collidedParts.append(part)
        return collidedParts
                
    def Setup(self, body):
        #if len(self.Neighbors() <= 0):
        #   self.body.Destroy()
        pass

    def Update(self):
        self.body.SubtractLife(self.cost)
        if self.mass < self.massStart:
            if self.mass + self.rateRepair >= self.massStart:
                self.mass = self.massStart
            else:
                self.mass = min(self.mass + self.rateRepair, self.massStart)
##        collidedParts = self.CollideAll()
##        for part in collidedParts:
##            self.body.SubtractLife(part.body.speed2() * part.body.mass)
##            part.body.SubtractLife(self.body.speed2() * self.body.mass)

    def angle(self):
        return self.body.GetAngle() - self.angleOffset + self.angleBodyToPart

    def x(self):
        return self.body.x + self.distance * cos(self.angle())

    def y(self):
        return self.body.y + self.distance * sin(self.angle())

    def Render(self):
        if self.highlight:
            Screen.Instance.DrawCircle((self.x(), self.y()), 1.2 * self.radius * 0.25 * (3 + min(max(self.mass/self.massStart, 0), 1)), (255, 255, 255))
        Screen.Instance.DrawCircle((self.x(), self.y()), self.radius * 0.25 * (3 + min(max(self.mass/self.massStart, 0), 1)), self.color)

class Muscle(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 10, 20)
        self.color = (255, 0, 0)
        self.power = 2
        #print("Muscle: [{}]".format(partProperty))

    def Update(self):
        super().Update()

    
class Bone(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 25, 100)
        self.color = (255, 250, 230)
        #print("Bone: [{}]".format(partProperty))


class Heart(Part):
    
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 250, 20)
        self.color = (255, 0, 255)
        self.radiusStart = self.radius
        self.phase = random()
        self.lastMatingTime = time()
        self.refractoryPeriod = self.body.RefractoryPeriodFromDNA()
        #print("Heart: [{}]".format(partProperty))

    def Setup(self, parts):
        hearts = [self]
        phaseSum = self.phase
        for part in parts:
            if part is None or part == self or type(part) is not Heart:
                continue
            hearts.append(part)
            phaseSum += part.phase
        phaseAverage = phaseSum / len(hearts)
        for heart in hearts:
            heart.phase = phaseAverage

    def HeartbeatRadius(self):
        return self.radiusStart * (1 + 0.4*Heartbeat(time()/2 * (1+self.phase)))
            
    def Update(self):
        super().Update()
        self.radius = self.HeartbeatRadius()

    def Collide(self, parts):
        super().Collide(parts)
        
        if len(parts) <= 0:
            return

        if time() - self.lastMatingTime > self.refractoryPeriod:
            for i in range(0, 2):
                part = Part.FirstRealPart(parts, True)
                self.body.Mate(part.body)
            self.lastMatingTime = time()

        
class Gills(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 50, 30)
        self.color = (0, 255, 255)
        #print("Gills: [{}]".format(partProperty))

    def Update(self):
        super().Update()
        #print("Forever: {}".format(100 * self.body.speed2()))
        self.body.AddLife(1000 * self.body.speed2())

    def Render(self):
        super().Render()
        
class Propellor(Part):
    ANGLES = 8
    
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 100, 50)
        self.color = (0, 0, 255)
        self.partProperty = partProperty % Propellor.ANGLES

    def Update(self):
        super().Update()
        force = 0.03
        angle = self.anglePropellor()
        self.body.AddImpulse((self.body.centerOfMass[0], self.body.centerOfMass[1]), (self.x(), self.y()), (-force * cos(angle), -force * sin(angle)))
        #print("Propellor: [{}]".format(partProperty))

    def anglePropellor(self):
        return self.partProperty * 2 * pi / Propellor.ANGLES + self.angle()

    def Render(self):
        super().Render()
        distance = abs(sin(time()*10)) * (2 * self.radius)
        angle = self.anglePropellor()
        offset = (distance * cos(angle), distance * sin(angle))
        color = (128, 255, 255)
        Screen.DrawCircle((self.x() + offset[0], self.y() + offset[1]), self.radius / 2, color)
        Screen.DrawLine((self.x(), self.y()), (self.x() + offset[0], self.y() + offset[1]), color)
        

        
class Pulser(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 500, 100)
        self.color = (255, 255, 0)
        #print("Pulser: [{}]".format(partProperty))

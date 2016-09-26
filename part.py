from screen import Screen
from math import *
from time import time
from utils import *

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

    def __init__(self, position, body, radius, cost):
        self.GenerateID()
        Part.parts.append(self)
        self.body = body
        self.angleBodyToPart = atan2(position[1]-self.body.y, position[0]-self.body.x)
        self.angleOffset = self.body.GetAngle()
        self.distance = hypot(position[0] - self.body.x, position[1] - self.body.y)
        self.radius = radius
        self.color = (80, 80, 80)
        self.cost = cost
        self.mass = 1
        self.destroyed = False
        Screen.Instance.AddUpdateFunction(self, self.Update)
        Screen.Instance.AddRenderFunction(self, self.Render)

    def Destroy(self):
        if not self.destroyed:
            self.destroyed = True
            Part.parts.remove(self)
            Screen.Instance.RemoveUpdateFunctions(self)
            Screen.Instance.RemoveRenderFunctions(self)

    def Collide(self):
        for part in Part.parts:
            if part in self.body.parts:
                continue
            if LengthSq((part.x() - self.x(), part.y() - self.y())) <= (part.radius + self.radius)**2:
                return part
        return None

    def CollideAll(self):
        partsCollided = []
        for part in Part.parts:
            if part in self.body.parts:
                continue
            if LengthSq((part.x() - self.x(), part.y() - self.y())) <= (part.radius + self.radius)**2:
                partsCollided.append(part)
        return partsCollided

    def Neighbors(self):
        collidedParts = []
        for part in self.body.parts:
            if part is self:
                continue

            if LengthSq((part.x() - self.x(), part.y() - self.y())) <= (part.radius + Part.SEPARATION_MULT * self.body.radius)**2:
                collidedParts.append(part)
        return collidedParts
                
    def Setup(self):
        #if len(self.Neighbors() <= 0):
        #   self.body.Destroy()
        pass

    def Update(self):
        self.body.SubtractLife(self.cost)
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
        Screen.Instance.DrawCircle((self.x(), self.y()), self.radius, self.color)

class Muscle(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 10)
        self.color = (255, 0, 0)
        #print("Muscle: [{}]".format(partProperty))

    def Update(self):
        super().Update()

    
class Bone(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 25)
        self.color = (255, 255, 255)
        #print("Bone: [{}]".format(partProperty))


class Heart(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 250)
        self.color = (255, 0, 255)
        #print("Heart: [{}]".format(partProperty))

    def Update(self):
        super().Update()
        
        collidedParts = self.CollideAll()
        for part in collidedParts:
            self.body.Mate(part.body)
            self.body.Mate(part.body)



        
class Gills(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 50)
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
        super().__init__(position, body, radius, 100)
        self.color = (0, 0, 255)
        self.partProperty = partProperty % Propellor.ANGLES

    def Update(self):
        super().Update()
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
        force = 0.002
        angle = self.anglePropellor()
        Screen.DrawLine((self.x(), self.y()), (self.x() + offset[0], self.y() + offset[1]), color)
        self.body.AddImpulse((self.body.centerOfMass[0], self.body.centerOfMass[1]), (self.x(), self.y()), (-force * cos(angle), -force * sin(angle)))
        

        
class Pulser(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 500)
        self.color = (255, 255, 0)
        #print("Pulser: [{}]".format(partProperty))

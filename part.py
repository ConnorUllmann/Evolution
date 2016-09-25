from screen import Screen
from math import *
from time import time
from utils import *

class Part:

    ID = 0

    def GenerateID(self):
        self.id = Part.ID
        Part.ID += 1

    @staticmethod
    def NewPartFromIndex(index, *args):
        if index == 0:
            return Muscle(*args)
        if index == 1:
            return Bone(*args)
        if index == 2:
            return Heart(*args)
        if index == 3:
            return Gills(*args)
        if index == 4:
            return Propellor(*args)
        if index == 5:
            return Pulser(*args)

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
            if LengthSq(part.x() - self.x(), part.y() - self.y()) <= (part.radius + self.radius)**2:
                partsCollided.append(part)
        return partsCollided

    def Setup(self):
        pass #print("Setup " + str(self))

    def Update(self):
        self.body.SubtractLife(self.cost)
        collidedPart = self.Collide()
        if collidedPart is not None:
            self.body.SubtractLife(collidedPart.body.speed2())
            collidedPart.body.SubtractLife(self.body.speed2()) 

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
        super().__init__(position, body, radius, 1000)
        self.color = (255, 0, 255)
        #print("Heart: [{}]".format(partProperty))

    def Update(self):
        super().Update()
        
        collidedPart = self.Collide()
        if collidedPart is not None:
            self.body.Mate(collidedPart.body)

        
class Gills(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 50)
        self.color = (0, 255, 255)
        #print("Gills: [{}]".format(partProperty))

    def Update(self):
        super().Update()
        #print("Forever: {}".format(100 * self.body.speed2()))
        self.body.AddLife(500 * self.body.speed2())

        
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
        force = 0.001
        angle = self.anglePropellor()
        Screen.DrawLine((self.x(), self.y()), (self.x() + offset[0], self.y() + offset[1]), color)
        self.body.AddImpulse((self.body.centerOfMass[0], self.body.centerOfMass[1]), (self.x(), self.y()), (-force * cos(angle), -force * sin(angle)))
        

        
class Pulser(Part):
    def __init__(self, position, body, radius, partProperty):
        super().__init__(position, body, radius, 500)
        self.color = (255, 255, 0)
        #print("Pulser: [{}]".format(partProperty))

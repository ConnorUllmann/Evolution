from .screen import Screen
from .state_machine import StateMachine
from .utils import Point

class Entity(StateMachine, Point):

    ID = 0
    entities = {}

    @staticmethod
    def GetId():
        _id = Entity.ID
        Entity.ID += 1
        return _id

    @staticmethod
    def GetAllEntitiesOfType(name):
        if name in Entity.entities:
            return list(Entity.entities[name])
        else:
            return []

    @staticmethod
    def GetAllEntitiesOfSameType(entity):
        return Entity.GetAllEntitiesOfType(entity.__class__.__name__)

    @staticmethod
    def Add(entity):
        name = entity.__class__.__name__
        if name not in Entity.entities:
            Entity.entities[name] = []
        Entity.entities[name].append(entity)

    @staticmethod
    def Remove(entity):
        name = entity.__class__.__name__
        if name in Entity.entities and entity in Entity.entities[name]:
            Entity.entities[name].remove(entity)
            if len(Entity.entities[name]) <= 0:
                Entity.entities.pop(name, None)
            return True
        return False

    def __init__(self, x=0, y=0):
        Point.__init__(self, x, y)
        StateMachine.__init__(self)
        
        self.id = Entity.GetId()
        Entity.Add(self)
        
        Screen.Instance.AddUpdateFunction(self, self.Update)
        Screen.Instance.AddRenderFunction(self, self.Render)
        Screen.PutOnTop(self)
        
        self.v = Point()
        self.destroyed = False

    def Render(self):
        pass

    def __str__(self):
        return "[{}]{}".format(self.id, self.__class__.__name__)
    
    def Destroy(self):
        if not self.destroyed:
            self.destroyed = True
            Screen.Instance.RemoveUpdateFunctions(self)
            Screen.Instance.RemoveRenderFunctions(self)
            Entity.Remove(self)
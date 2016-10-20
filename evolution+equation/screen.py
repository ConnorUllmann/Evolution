import pygame, time
from random import randint
from thread_manager import ThreadManager

class Screen:

    Instance = None

    @staticmethod
    def Width():
        return Screen.Instance.width
    @staticmethod
    def Height():
        return Screen.Instance.height

    def ClearScreen(self):
        self.screen.fill(self.clearColor)

    def _RemoveUpdateFunctionsByKey(self, key):
        self.updateOrder.remove(key)
        return self.updateFunctions.pop(key, None)

    def _RemoveRenderFunctionsByKey(self, key):
        self.renderOrder.remove(key)
        return self.renderFunctions.pop(key, None)
        
    def RemoveUpdateFunctions(self, key):
        self.updateFunctionsRemoveQueue.append(str(key))
    
    def RemoveRenderFunctions(self, key):
        self.renderFunctionsRemoveQueue.append(str(key))

    def _AddUpdateFunction(self, info):
        key = info[0]
        if key not in self.updateFunctions:
            self.updateFunctions[key] = []
        self.updateOrder.append(key)
        self.updateFunctions[key].append(info[1])
        
    def _AddRenderFunction(self, info):
        key = info[0]
        if key not in self.renderFunctions:
            self.renderFunctions[key] = []
        self.renderOrder.append(key)
        self.renderFunctions[key].append(info[1])

    def AddUpdateFunction(self, key, function):
        self.updateFunctionsAddQueue.append([str(key), function])
    
    def AddRenderFunction(self, key, function):
        self.renderFunctionsAddQueue.append([str(key), function])

    #Cannot be called during a render function! Only use during updates
    @staticmethod
    def PutOnTop(key):
        tempKey = str(key)
        if tempKey not in Screen.Instance.renderOrder:
            return False
        x = Screen.Instance.renderOrder.index(tempKey)
        element = Screen.Instance.renderOrder.pop(x)
        Screen.Instance.renderOrder = Screen.Instance.renderOrder + [element]
        return True

    def __init__(self, width, height, clearColor=(0,0,0)):
        Screen.Instance = self
        self.threadManager = ThreadManager()
        
        self.updateFunctionsAddQueue = []
        self.renderFunctionsAddQueue = []
        self.updateFunctionsRemoveQueue = []
        self.renderFunctionsRemoveQueue = []
        self.updateFunctions = {}
        self.renderFunctions = {}
        self.updateOrder = []
        self.renderOrder = []
        
        self.objectAddQueue = []
        self.objectRemoveQueue = []
        self.objectQueue = {}
        
        self.clearColor = clearColor
        self.width = width
        self.height = height
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.screen.set_alpha(None)
        self.ClearScreen()
        #pygame.font.init()
    
    def Update(self):
        while len(self.updateFunctionsAddQueue) > 0:
            self._AddUpdateFunction(self.updateFunctionsAddQueue.pop())
        while len(self.updateFunctionsRemoveQueue) > 0:
            self._RemoveUpdateFunctionsByKey(self.updateFunctionsRemoveQueue.pop())
        for key in self.updateOrder:
            #print("key: " + key)
            for updateFunction in self.updateFunctions[key]:
                updateFunction()

    def Render(self):
        while len(self.renderFunctionsAddQueue) > 0:
            self._AddRenderFunction(self.renderFunctionsAddQueue.pop())
        while len(self.renderFunctionsRemoveQueue) > 0:
            self._RemoveRenderFunctionsByKey(self.renderFunctionsRemoveQueue.pop())
        self.ClearScreen()
        for key in self.renderOrder:
            #print("key: " + key)
            for renderFunction in self.renderFunctions[key]:
                renderFunction()

    def StartHelper(self):
        while True:
            self.Update()
            self.Render()
            pygame.display.update()

    @staticmethod
    def Start():
        Screen.Instance.threadManager.Run([Screen.Instance.threadManager.Add(lambda: Screen.Instance.StartHelper())])

    @staticmethod
    def DrawLines(positions, color=(255, 255, 255), thickness=1):
        pygame.draw.lines(Screen.Instance.screen, color, False, positions, thickness)

    @staticmethod
    def DrawLine(positionStart=(0,0), positionEnd=(0,0), color=(255,255,255), thickness=1):
        pygame.draw.line(Screen.Instance.screen, color, positionStart, positionEnd, thickness)
        
    @staticmethod
    def DrawCircle(position=(0,0), radius=1, color=(255,255,255), thickness=0):
        intPosition = (int(position[0]), int(position[1]))
        pygame.draw.circle(Screen.Instance.screen, color, intPosition, int(radius), thickness)

    @staticmethod
    def DrawPoint(position=(0,0), color=(255,255,255)):
        intPosition = (int(position[0]), int(position[1]))
        Screen.Instance.screen.set_at(intPosition, color)

    @staticmethod
    def DrawText(position=(0,0), text="", color=(255,255,255), fontSize=12):
        intPosition = (int(position[0]), int(position[1]))
        font = pygame.font.Font(None, fontSize)
        textRendered = font.render(text, 1, color)
        Screen.Instance.screen.blit(textRendered, intPosition)

    @staticmethod
    def RandomColor():
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def MousePosition(self):
        return pygame.mouse.get_pos()

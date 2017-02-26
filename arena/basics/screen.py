import pygame, time, os, platform
from tkinter import *
from random import randint, random
from .thread_manager import ThreadManager
from .point import Point

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

    #def Frame(self):
    #    return Frame(self.root, width=self.width, height=self.height)

    #def grid(self, *args, **kwargs):
    #    self.embed.grid(*args, **kwargs)

    def __init__(self, width, height, clearColor=(0,0,0)):
        Screen.Instance = self
        #self.root = root
        self.width = width
        self.height = height
        self.clearColor = clearColor

        self.keys = None
        
        self.threadManager = ThreadManager()
        
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        #self.background = pygame.Surface(self.screen.get_size())
        #self.background = self.background.convert()
        self.screen.set_alpha(None)
        
        #pygame.font.init()
        pygame.display.init()
        pygame.display.update()
        self.ClearScreen()

        self.camera = Point()

        #self.embed = self.Frame()
        #os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        #if platform.system == "Windows":
        #    os.environ['SDL_VIDEODRIVER'] = 'windib'
        
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

        self.keysPressed = []
        self.keysReleased = []
        self.keysDown = []

    @staticmethod
    def KeyDown(key):
        return Screen.Instance.keyDown(key)
    def keyDown(self, key):
        return self.keysDown[key]

    @staticmethod
    def KeyPressed(key):
        return Screen.Instance.keyPressed(key)
    def keyPressed(self, key):
        return self.keysPressed[key]

    @staticmethod
    def KeyReleased(key):
        return Screen.Instance.keyReleased(key)
    def keyReleased(self, key):
        return self.keysReleased[key]

    def updateKeys(self):
        self.keysDown = pygame.key.get_pressed()
        self.keysPressed = [0] * len(self.keysDown)
        self.keysReleased = [0] * len(self.keysDown)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keysPressed[event.key] = 1
            elif event.type == pygame.KEYUP:
                self.keysReleased[event.key] = 1

    def updateFunctionQueues(self):
        while len(self.updateFunctionsAddQueue) > 0:
            self._AddUpdateFunction(self.updateFunctionsAddQueue.pop())
        while len(self.updateFunctionsRemoveQueue) > 0:
            self._RemoveUpdateFunctionsByKey(self.updateFunctionsRemoveQueue.pop())
    
    def Update(self):
        self.updateKeys()                   
        self.updateFunctionQueues()
        for key in self.updateOrder:
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
            self.keys = pygame.key.get_pressed()
            #print(self.keys)
            self.Update()
            self.Render()
            pygame.display.update()

    @staticmethod
    def Start():
        Screen.Instance.StartHelper()
 #       Screen.Instance.threadManager.Run([Screen.Instance.threadManager.Add(lambda: Screen.Instance.StartHelper())])

    @staticmethod
    def DrawRect(position, dimensions, color=(255, 255, 255), thickness=1, filled=True):
        if filled:
            x = position[0] - Screen.Instance.camera.x
            y = position[1] - Screen.Instance.camera.y
            sx = dimensions[0]
            sy = dimensions[1]
            if x < 0:
                sx += x
            if y < 0:
                sy += y
            if sx > 0 and sy > 0:
                x = min(max(x, 0), Screen.Instance.width)
                y = min(max(y, 0), Screen.Instance.height)
                Screen.Instance.screen.fill(color, (x, y, sx, sy))
        else:
            pygame.draw.rect(Screen.Instance.screen, color, pygame.Rect(position[0] - Screen.Instance.camera.x, position[1] - Screen.Instance.camera.y, dimensions[0], dimensions[1]), thickness)

    @staticmethod
    def DrawLines(positions, color=(255, 255, 255), thickness=1):
        if Screen.Instance.camera.x != 0 or Screen.Instance.camera.y != 0:
            p = []
            for x in positions:
                p.append((x[0] - Screen.Instance.camera.x, x[1] - Screen.Instance.camera.y))
            pygame.draw.lines(Screen.Instance.screen, color, False, p, thickness)
        else:
            pygame.draw.lines(Screen.Instance.screen, color, False, positions, thickness)

    @staticmethod
    def DrawLine(positionStart=(0,0), positionEnd=(0,0), color=(255,255,255), thickness=1):
        pS = (positionStart[0] - Screen.Instance.camera.x, positionStart[1] - Screen.Instance.camera.y)
        pE = (positionEnd[0] - Screen.Instance.camera.x, positionEnd[1] - Screen.Instance.camera.y)
        pygame.draw.line(Screen.Instance.screen, color, pS, pE, thickness)
        
    @staticmethod
    def DrawCircle(position=(0,0), radius=1, color=(255,255,255), thickness=0):
        intPosition = (int(position[0] - Screen.Instance.camera.x), int(position[1] - Screen.Instance.camera.y))
        pygame.draw.circle(Screen.Instance.screen, color, intPosition, int(radius), thickness)

    @staticmethod
    def DrawPoint(position=(0,0), color=(255,255,255)):
        intPosition = (int(position[0] - Screen.Instance.camera.x), int(position[1] - Screen.Instance.camera.y))
        Screen.Instance.screen.set_at(intPosition, color)

    @staticmethod
    def DrawText(position=(0,0), text="", color=(255,255,255), fontSize=12):
        intPosition = (int(position[0] - Screen.Instance.camera.x), int(position[1] - Screen.Instance.camera.y))
        font = pygame.font.Font(None, fontSize)
        textRendered = font.render(text, 1, color)
        Screen.Instance.screen.blit(textRendered, intPosition)

    def MousePosition(self):
        p = pygame.mouse.get_pos()
        return Point(p[0], p[1])

    def RandomPosition(self):
        return Point(random() * Screen.Instance.width, random() * Screen.Instance.height)
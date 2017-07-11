import pygame, time, os, platform
from random import randint, random
from .thread_manager import ThreadManager
from .point import Point
from .utils import PointOnLineAtX, PointOnLineAtY, LinesIntersectionPoint

class Screen:

    Instance = None

    @staticmethod
    def Width():
        return Screen.Instance.width

    @staticmethod
    def Height():
        return Screen.Instance.height

    @staticmethod
    def RayEndpoint(positionStart, positionToward, margin=0):
        vector = (positionToward - positionStart).normalized * 1000000000
        pts = [
            Point(margin, margin),
            Point(Screen.Width() - margin, margin),
            Point(Screen.Width() - margin, Screen.Height() - margin),
            Point(margin, Screen.Height() - margin)
        ]
        collisionPoints = []
        for i in range(len(pts)):
            pt = LinesIntersectionPoint(positionStart, positionStart + vector, pts[i], pts[(i+1)%len(pts)], True)
            if pt is not None:
                collisionPoints.append(pt)

        if len(collisionPoints) == 1:
            return collisionPoints[0]

        maxDistanceSq = None
        maxDistanceCollisionPoint = None
        for collisionPoint in collisionPoints:
            distanceSq = (collisionPoint - positionStart).lengthSq
            if maxDistanceSq is None or distanceSq > maxDistanceSq:
                maxDistanceSq = distanceSq
                maxDistanceCollisionPoint = collisionPoint
        if maxDistanceCollisionPoint is not None:
            return maxDistanceCollisionPoint

        return positionStart + vector

    @staticmethod
    def RandomPosition():
        return Screen.Instance.randomPosition()
    def randomPosition(self):
        return Point(random() * self.width, random() * self.height)

    @staticmethod
    def ClearScreen():
        Screen.Instance.clearScreen()
    def clearScreen(self):
        self.screen.fill(self.clearColor)

    @staticmethod
    def PutOnTop(key):
        #Cannot be called during a render function! Only use during updates
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

    @staticmethod
    def Start():
        Screen.Instance.StartHelper()
        # Screen.Instance.threadManager.Run([Screen.Instance.threadManager.Add(lambda: Screen.Instance.StartHelper())])

    def StartHelper(self):
        self.Begin()
        while True:
            self.Update()
            self.Render()
            pygame.display.update()

    @staticmethod
    def StartGame(beginFunction=None, updateFunction=None, renderFunction=None, title="Untitled", width=800, height=600):
        Screen(width, height)
        pygame.display.set_caption(title)
        if beginFunction is not None:
            Screen.AddBeginFunction(beginFunction)
        if updateFunction is not None:
            Screen.AddUpdateFunction("main", updateFunction)
        if renderFunction is not None:
            Screen.AddRenderFunction("main", renderFunction)
        Screen.Start()

    def __init__(self, width, height, clearColor=(0, 0, 0)):
        Screen.Instance = self
        # self.root = root
        self.width = width
        self.height = height
        self.clearColor = clearColor

        self.lastTime = pygame.time.get_ticks()
        self.delta = 0

        self.threadManager = ThreadManager()

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        # self.background = pygame.Surface(self.screen.get_size())
        # self.background = self.background.convert()
        self.screen.set_alpha(None)

        pygame.display.init()
        pygame.display.update()
        self.clearScreen()
        #
        # x = pygame.font.Font("comicsansms", 72)
        # x = pygame.font.SysFont("comicsansms", 72)
        # print("Initialized font module {}".format(pygame.font.get_init()))

        self.camera = Point()

        # self.embed = self.Frame()
        # os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        # if platform.system == "Windows":
        #    os.environ['SDL_VIDEODRIVER'] = 'windib'

        self.updateFunctionsAddQueue = []
        self.renderFunctionsAddQueue = []
        self.updateFunctionsRemoveQueue = []
        self.renderFunctionsRemoveQueue = []
        self.beginFunctions = []
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

        self.mouseButtonsDown = []
        self.leftMouseDown = False
        self.leftMousePressed = False
        self.leftMouseReleased = False
        self.rightMouseDown = False
        self.rightMousePressed = False
        self.rightMouseReleased = False
        self.mousePosition = Point()

    def Begin(self):
        for function in self.beginFunctions:
            function()

    def Update(self):
        self.updateDeltaTime()
        self.updateKeys()
        self.updateFunctionQueues()
        for key in self.updateOrder:
            for updateFunction in self.updateFunctions[key]:
                updateFunction()
        self.updateMouseButtonStates()
        self.updateMousePosition()

    def Render(self):
        while len(self.renderFunctionsAddQueue) > 0:
            self._addRenderFunction(self.renderFunctionsAddQueue.pop())
        while len(self.renderFunctionsRemoveQueue) > 0:
            self.removeRenderFunctionsByKey(self.renderFunctionsRemoveQueue.pop())
        self.clearScreen()
        for key in self.renderOrder:
            #print("key: " + key)
            for renderFunction in self.renderFunctions[key]:
                renderFunction()


    # --- Function Queues ---

    @staticmethod
    def RemoveUpdateFunctions(key):
        Screen.Instance.removeUpdateFunctions(key)
    def removeUpdateFunctions(self, key):
        self.updateFunctionsRemoveQueue.append(str(key))

    @staticmethod
    def RemoveRenderFunctions(key):
        Screen.Instance.removeRenderFunctions(key)
    def removeRenderFunctions(self, key):
        self.renderFunctionsRemoveQueue.append(str(key))

    @staticmethod
    def AddUpdateFunction(key, function):
        Screen.Instance.addUpdateFunction(key, function)
    def addUpdateFunction(self, key, function):
        self.updateFunctionsAddQueue.append([str(key), function])

    @staticmethod
    def AddRenderFunction(key, function):
        Screen.Instance.addRenderFunction(key, function)
    def addRenderFunction(self, key, function):
        self.renderFunctionsAddQueue.append([str(key), function])

    @staticmethod
    def AddBeginFunction(function):
        Screen.Instance.addBeginFunction(function)
    def addBeginFunction(self, function):
        self.beginFunctions.append(function)

    def updateFunctionQueues(self):
        while len(self.updateFunctionsAddQueue) > 0:
            self._addUpdateFunction(self.updateFunctionsAddQueue.pop())
        while len(self.updateFunctionsRemoveQueue) > 0:
            self.removeUpdateFunctionsByKey(self.updateFunctionsRemoveQueue.pop())

    def removeUpdateFunctionsByKey(self, key):
        self.updateOrder.remove(key)
        return self.updateFunctions.pop(key, None)

    def removeRenderFunctionsByKey(self, key):
        self.renderOrder.remove(key)
        return self.renderFunctions.pop(key, None)

    def _addUpdateFunction(self, info):
        key = info[0]
        if key not in self.updateFunctions:
            self.updateFunctions[key] = []
        self.updateOrder.append(key)
        self.updateFunctions[key].append(info[1])

    def _addRenderFunction(self, info):
        key = info[0]
        if key not in self.renderFunctions:
            self.renderFunctions[key] = []
        self.renderOrder.append(key)
        self.renderFunctions[key].append(info[1])


    # --- Inputs ---

    @staticmethod
    def MousePosition():
        return Screen.Instance.mousePosition

    @staticmethod
    def LeftMouseDown():
        return Screen.Instance.leftMouseDown

    @staticmethod
    def RightMouseDown():
        return Screen.Instance.rightMouseDown

    @staticmethod
    def LeftMousePressed():
        return Screen.Instance.leftMousePressed

    @staticmethod
    def RightMousePressed():
        return Screen.Instance.rightMousePressed

    @staticmethod
    def LeftMouseReleased():
        return Screen.Instance.leftMouseReleased

    @staticmethod
    def RightMouseReleased():
        return Screen.Instance.rightMouseReleased

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

    def updateMouseButtonStates(self):
        mouseButtonsDownPrevious = self.mouseButtonsDown[:] if len(self.mouseButtonsDown) > 0 else [0]*3
        self.mouseButtonsDown = pygame.mouse.get_pressed()
        self.leftMouseDown = self.mouseButtonsDown[0]
        self.rightMouseDown = self.mouseButtonsDown[2]
        self.leftMousePressed = not mouseButtonsDownPrevious[0] and self.leftMouseDown
        self.leftMouseReleased = mouseButtonsDownPrevious[0] and not self.leftMouseDown
        self.rightMousePressed = not mouseButtonsDownPrevious[2] and self.rightMouseDown
        self.rightMouseReleased = mouseButtonsDownPrevious[2] and not self.rightMouseDown

    def updateMousePosition(self):
        p = pygame.mouse.get_pos()
        self.mousePosition = Point(p[0], p[1])

    # --- Time ---

    @staticmethod
    def DeltaTime():
        return Screen.Instance.delta

    def updateDeltaTime(self):
        _time = pygame.time.get_ticks()
        self.delta = (_time - self.lastTime) / 1000.0
        self.lastTime = _time

    # --- Drawing ---

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
            pygame.draw.rect(Screen.Instance.screen, color,
                             pygame.Rect(position[0] - Screen.Instance.camera.x, position[1] - Screen.Instance.camera.y,
                                         dimensions[0], dimensions[1]), thickness)

    @staticmethod
    def DrawLines(positions, color=(255, 255, 255), thickness=1):
        if True: #Screen.Instance.camera.x != 0 or Screen.Instance.camera.y != 0:
            p = []
            for x in positions:
                p.append((x[0] - Screen.Instance.camera.x, x[1] - Screen.Instance.camera.y))
            pygame.draw.lines(Screen.Instance.screen, color, False, p, thickness)
        else:
            pygame.draw.lines(Screen.Instance.screen, color, False, positions, thickness)

    @staticmethod
    def DrawPolygon(vertices, color=(255, 255, 255), thickness=1):
        pygame.draw.polygon(Screen.Instance.screen, color, vertices, thickness)

    @staticmethod
    def DrawLine(positionStart=(0, 0), positionEnd=(0, 0), color=(255, 255, 255), thickness=1):
        pS = (positionStart[0] - Screen.Instance.camera.x, positionStart[1] - Screen.Instance.camera.y)
        pE = (positionEnd[0] - Screen.Instance.camera.x, positionEnd[1] - Screen.Instance.camera.y)
        pygame.draw.line(Screen.Instance.screen, color, pS, pE, thickness)

    @staticmethod
    def DrawRay(positionStart=(0, 0), positionToward=(0, 0), color=(255, 255, 255), thickness=1):
        Screen.DrawLine(positionStart, Screen.RayEndpoint(positionStart, positionToward), color, thickness)

    @staticmethod
    def DrawCircle(position=(0, 0), radius=1, color=(255, 255, 255), thickness=0):
        intPosition = (int(position[0] - Screen.Instance.camera.x), int(position[1] - Screen.Instance.camera.y))
        pygame.draw.circle(Screen.Instance.screen, color, intPosition, int(radius), thickness)

    @staticmethod
    def DrawPoint(position=(0, 0), color=(255, 255, 255)):
        intPosition = (int(position[0] - Screen.Instance.camera.x), int(position[1] - Screen.Instance.camera.y))
        Screen.Instance.screen.set_at(intPosition, color)

    @staticmethod
    def DrawText(position=(0, 0), text="", color=(255, 255, 255), fontSize=12):
        intPosition = (int(position[0] - Screen.Instance.camera.x), int(position[1] - Screen.Instance.camera.y))
        font = pygame.font.Font(None, fontSize)
        textRendered = font.render(text, 1, color)
        Screen.Instance.screen.blit(textRendered, intPosition)
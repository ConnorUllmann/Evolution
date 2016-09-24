import pygame, time
from random import randint
from thread_manager import ThreadManager

def RandomColor():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

class Screen:

    Instance = None

    def ClearScreen(self):
        self.screen.fill(self.clearColor)

    def AddUpdateFunction(self, function):
        self.updateFunctions.append(function)

    def __init__(self, width, height, clearColor=(0,0,0)):
        Screen.Instance = self
        self.threadManager = ThreadManager()
        self.updateFunctions = []
        self.clearColor = clearColor
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.screen.set_alpha(None)
        self.ClearScreen()
        pygame.init()
        pygame.display.init()
        self.threadManager.Run([self.threadManager.Add(lambda: self.RenderStart())])

    def Render(self):
        self.ClearScreen()
        
        for updateFunction in self.updateFunctions:
            updateFunction()

    def RenderStart(self):
        self.Render()
        pygame.display.update()
        time.sleep(0.016)
        self.RenderStart()

    def DrawLines(self, positions, color=(255, 255, 255), thickness=1):
        pygame.draw.lines(self.screen, color, False, positions, thickness)

    def DrawLine(self, positionStart=(0,0), positionEnd=(0,0), color=(255,255,255), thickness=1):
        pygame.draw.line(self.screen, color, positionStart, positionEnd, thickness)
        
    def DrawCircle(self, position=(0,0), radius=1, color=(255,255,255), thickness=0):
        intPosition = (int(position[0]), int(position[1]))
        pygame.draw.circle(self.screen, color, intPosition, radius, thickness)

    def DrawPoint(self, position=(0,0), color=(255,255,255)):
        intPosition = (int(position[0]), int(position[1]))
        self.screen.set_at(intPosition, color)

    def DrawText(self, text, position=(0,0), color=(255,255,255), fontSize=12):
        intPosition = (int(position[0]), int(position[1]))
        font = pygame.font.SysFont("monospace", fontSize)
        textRendered = font.render(text, 1, color)
        self.screen.blit(textRendered, intPosition)

    def MousePosition(self):
        return pygame.mouse.get_pos()

from screen import Screen
from graph import Graph
from equation import Equation
from random import random
from math import *
import pygame

selection = 0

def UpdateGame():
    global graph

    #targets = GetTargets(selection)
    #graph.SetTargets(targets)

    graph.Evolve()
    #input("Waiting")
    pass

def RenderGame():
    global mousePositions
    positions = dict(mousePositions)
    for key in positions:
        position = positions[key]
        Screen.DrawCircle(graph.DrawPos(position[0], position[1]), 3, (255, 0, 0))
    pass

def GetTargets(selection):
    targets = []
    while selection < 0:
        selection += 3
    selection %= 3
    for i in range(0, 100):
        x = i / 100
        yMax = 10000
        point = None
        if selection == 0:
            point = (x, yMax*(1-sin(2*pi*x))/2)
        elif selection == 1:
            point = (x, yMax*(1 - ((1 - x)/2+0.5)**2*sin(2*pi*x*2-pi/4))/2)
        else:
            point = (x, yMax*x**2)
        #print(point)
        targets.append(point)
    return targets

startTracking = False
mousePositions = {}
def StartGame():
    global graph, selection, startTracking, mousePositions
    Screen(600, 400)

    selection = 0
    targets = GetTargets(selection)
    equations = []
    for i in range(0, 20):
        equations.append(Equation([]))

    graph = Graph(equations, targets)
    
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

    while True:
        startTrackingPrevious = startTracking
        events = pygame.event.get()
        targets = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selection -= 1
                    mousePositions = {}
                    targets = GetTargets(selection)
                if event.key == pygame.K_RIGHT:
                    selection += 1
                    mousePositions = {}
                    targets = GetTargets(selection)
                if event.key == pygame.K_SPACE:
                    startTracking = not startTracking
                    if startTracking and not startTrackingPrevious:
                        mousePositions = {}
                    if not startTracking and startTrackingPrevious:
                        mousePositionsKeys = sorted(mousePositions)
                        for key in mousePositionsKeys:
                            position = mousePositions[key]
                            if position[0] >= 0 and position[0] <= 1:
                                targets.append(position)
        
        #keysHeld = pygame.key.get_pressed()
        #startTracking = keysHeld[pygame.K_2]
        if startTracking:
            position = graph.ScreenPositionToXYValue(Screen.Instance.MousePosition())
            mousePositions[int(position[0]*100)] = position
        
        if len(targets) > 0:
            Equation.ClearBestEquations()
            graph.SetTargets(targets)
        

StartGame()

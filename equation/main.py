from screen import Screen
from graph import Graph
from equation import Equation
from random import random
from math import *

def UpdateGame():
    global graph

    graph.Evolve()
    #input("Waiting")
    pass

def RenderGame():
    pass
    
def StartGame():
    global graph
    Screen(600, 400)

    targets = []
    for i in range(0, 100):
        point = (i/100, 10000*(1 - sin(i*2*pi/100))/2)
        #print(point)
        targets.append(point)

    equations = []
    for i in range(0, 100):
        equations.append(Equation([]))

    graph = Graph(equations, targets)
    
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

StartGame()

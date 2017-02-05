from basics import Screen, NeuralNetwork
from gladiator import AI, Player, Swarmling
import pygame, random, math, os

def PreGame():
    pygame.display.set_caption("Arena")

queen = None
hivemind = None
player = None

def GenerateAIs():
    global hivemind, queen
    swarmlings = []
    disrupter = Swarmling(Screen.Instance.width/2, Screen.Instance.height/2)
    disrupter.SetState("stunned")
    for i in range(5):
        p = Screen.Instance.RandomPosition()
        swarmlings.append(Swarmling(p.x, p.y))
    for i in range(15):
        p = Screen.Instance.RandomPosition()
        Swarmling(p.x, p.y)

    nn = NeuralNetwork.Load("hivemind") if os.path.isfile("hivemind.txt") else None
    queen = AI(550, 300, swarmlings, nn)
    hivemind = queen.nn

    for i in range(10):
        p = Screen.Instance.RandomPosition()
        AI(p.x, p.y, None, hivemind)

def UpdateGame():
    global firstFrameTriggered, hivemind, queen
    
    if firstFrameTriggered is False:
        FirstFrame()
        firstFrameTriggered = True

    if hivemind is not None:
        hivemind.save("hivemind")

def RenderGame():
    pass

firstFrameTriggered = False
def FirstFrame():
    global player
    #player = Player(200, 200)
    GenerateAIs()
    
def StartGame():
    Screen(1200, 750)
    #Screen(600, 400)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()

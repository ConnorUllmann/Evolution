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
    swarmlings.append(Swarmling(500, 300))
    swarmlings.append(Swarmling(500, 150))
    swarmlings.append(Swarmling(500, 200))
    swarmlings.append(Swarmling(550, 150))
    swarmlings.append(Swarmling(200, 300))
    swarmlings.append(Swarmling(150, 350))
    swarmlings.append(Swarmling(150, 400))
    swarmlings.append(Swarmling(200, 350))
    swarmlings.append(Swarmling(600, 300))
    swarmlings.append(Swarmling(550, 350))
    swarmlings.append(Swarmling(650, 400))
    swarmlings.append(Swarmling(600, 350))

    nn = NeuralNetwork.Load("hivemind") if os.path.isfile("hivemind.txt") else None
    queen = AI(550, 300, swarmlings, nn)
    hivemind = queen.nn
    AI(500, 100, None, nn)
    AI(500, 200, None, nn)
    AI(500, 400, None, nn)
    AI(500, 500, None, nn)
    AI(300, 100, None, nn)
    AI(300, 200, None, nn)
    AI(300, 400, None, nn)
    AI(300, 500, None, nn)

def UpdateGame():
    global firstFrameTriggered, hivemind, queen
    
    if firstFrameTriggered is False:
        FirstFrame()
        firstFrameTriggered = True

    if hivemind is not None:
        hivemind.save("hivemind")

    with open("output.txt", "a") as output:
        output.write(str(queen.GetNeuralOutputs()) + "\n")

def RenderGame():
    pass

firstFrameTriggered = False
def FirstFrame():
    global player
    #player = Player(200, 200)
    open("output.txt", "w").close()
    GenerateAIs()
    
def StartGame():
    Screen(800, 400)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()

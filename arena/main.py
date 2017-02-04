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
##    swarmlings.append(Swarmling(500, 320))
##    swarmlings.append(Swarmling(500, 170))
##    swarmlings.append(Swarmling(500, 220))
##    swarmlings.append(Swarmling(550, 170))
##    swarmlings.append(Swarmling(200, 320))
##    swarmlings.append(Swarmling(150, 370))
##    swarmlings.append(Swarmling(150, 420))
##    swarmlings.append(Swarmling(200, 370))
##    swarmlings.append(Swarmling(600, 320))
##    swarmlings.append(Swarmling(550, 370))
##    swarmlings.append(Swarmling(650, 420))
##    swarmlings.append(Swarmling(600, 370))

    nn = NeuralNetwork.Load("hivemind") if os.path.isfile("hivemind.txt") else None
    queen = AI(550, 300, swarmlings, nn)
    hivemind = queen.nn
    AI(500, 100, None, hivemind)
    AI(500, 200, None, hivemind)
    AI(500, 400, None, hivemind)
    AI(500, 500, None, hivemind)
    AI(300, 100, None, hivemind)
    AI(300, 200, None, hivemind)
    AI(300, 400, None, hivemind)
    AI(300, 500, None, hivemind)
    AI(500, 150, None, nn)
    AI(500, 250, None, nn)
    AI(500, 450, None, nn)
    AI(500, 550, None, nn)
    AI(300, 150, None, nn)
    AI(300, 250, None, nn)
    AI(300, 450, None, nn)
    AI(300, 550, None, nn)

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

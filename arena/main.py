from basics import Screen, NeuralNetwork
from gladiator import AI, Player, Swarmling
import pygame, random, math, os

def PreGame():
    pygame.display.set_caption("Arena")

queen = None
hivemind = None
player = None
saveTimer = 0
saveTimerMax = 10

def GenerateAIs():
    global hivemind, queen
    swarmlings = []
    disrupters = []
    for i in range(5):
        disrupters.append(Swarmling(Screen.Instance.width/2 + 200 * int(i == 1) - 200 * int(i == 2), Screen.Instance.height/2 + 200 * int(i == 3) - 200 * int(i == 4)))
        disrupters[-1].SetState("stunned")

    for i in range(15):
        p = Screen.RandomPosition()
        swarmlings.append(Swarmling(p.x, p.y))
    # for i in range(15):
    #     p = Screen.Instance.RandomPosition()
    #     Swarmling(p.x, p.y)

    nn = NeuralNetwork.Load("hivemind") if os.path.isfile("hivemind.txt") else None
    queen = AI(550, 300, swarmlings, nn)
    hivemind = queen.nn
    #
    for i in range(10):
        p = Screen.RandomPosition()
        AI(p.x, p.y, None, hivemind)

def UpdateGame():
    global firstFrameTriggered, hivemind, queen, saveTimer, saveTimerMax
    
    if firstFrameTriggered is False:
        FirstFrame()
        firstFrameTriggered = True

    if saveTimer > 0:
        saveTimer -= 1
    else:
        saveTimer = saveTimerMax
        if hivemind is not None:
            hivemind.save("hivemind")
            try:
                NeuralNetwork.Load("hivemind")
            except:
                hivemind.save("hivemind-onerror")

def RenderGame():
    pass

firstFrameTriggered = False
def FirstFrame():
    global player
    #player = Player(200, 200)
    GenerateAIs()
    
def StartGame():
    #Screen(1200, 750)
    Screen(700, 500)
    PreGame()
    Screen.AddUpdateFunction("main", UpdateGame)
    Screen.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()

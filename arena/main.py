from basics import Screen
from gladiator import AI, Player
import pygame, random, math

def PreGame():
    pygame.display.set_caption("Arena")

queen = None
hivemind = None
player = None

def GenerateAIs():
    global player, hivemind, queen
    queen = AI(550, 300, player)
    hivemind = queen.nn
    AI(300, 200, player, hivemind)
    AI(400, 300, player, hivemind)
    AI(500, 300).dummy=True
    AI(500, 150).dummy=True
    AI(500, 200).dummy=True
    AI(550, 150).dummy=True
    AI(200, 300).dummy=True
    AI(150, 350).dummy=True
    AI(150, 400).dummy=True
    AI(200, 350).dummy=True
    AI(600, 300).dummy=True
    AI(550, 350).dummy=True
    AI(650, 400).dummy=True
    AI(600, 350).dummy=True

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
    player = Player(200, 200)
    open("output.txt", "w").close()
    GenerateAIs()
    
def StartGame():
    Screen(800, 800)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()

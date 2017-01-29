from basics import Screen
from gladiator import AI, Player
import pygame, random, math

def PreGame():
    pygame.display.set_caption("Arena")

firstFrameTriggered = False
def FirstFrame():
    global player
    player = Player(200, 200)
    firstborn = AI(500, 100, player)
    nn = firstborn.nn
    AI(550, 100, player, nn)
    AI(500, 150, player, nn)
    AI(500, 200, player, nn)
    AI(550, 150, player, nn)

def UpdateGame():
    global firstFrameTriggered
    if firstFrameTriggered is False:
        FirstFrame()
        firstFrameTriggered = True
    pass

def RenderGame():
    pass
    
def StartGame():
    Screen(800, 400)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()

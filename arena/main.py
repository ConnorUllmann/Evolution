from screen import Screen
from gladiator import AI, Player
import pygame, random, math

def PreGame():
    global player
    pygame.display.set_caption("Arena")
    player = Player(200, 200)
    AI(500, 100)
    AI(400, 300)

def UpdateGame():
    global player
    pygame.event.poll()
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

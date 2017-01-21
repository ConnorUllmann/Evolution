from screen import Screen
from player import Player
import pygame, random, math

def PreGame():
    pygame.display.set_caption("Arena")
    Player(200, 200)
    Player(400, 300)

def UpdateGame():
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

from basics import Screen
import pygame


def PreGame():
    pygame.display.set_caption("Untitled")

def UpdateGame():
    pass

def RenderGame():
    pass

def StartGame():
    Screen(640, 480)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
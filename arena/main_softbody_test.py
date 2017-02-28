from basics import Screen, Softbody, Point
import pygame


def PreGame():
    pygame.display.set_caption("Softbody Test")

def BeginGame():
    softbody = Softbody(320, 240, [Point(-100, 0), Point(-100, -100), Point(0, -100), Point(100, -100),
                                   Point(100, 0), Point(100, 100), Point(0, 100), Point(-100, 100)])

firstFrameTriggered = False
def UpdateGame():
    global firstFrameTriggered
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

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
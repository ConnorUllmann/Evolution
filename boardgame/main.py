from basics import Screen
from grid import PlayGrid

def Begin():
    width = 40
    height= 40
    grid = PlayGrid(width, height)

def Update():
    pass

def Render():
    pass

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render, width=800, height=600)
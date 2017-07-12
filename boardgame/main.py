from basics import Screen
from grid import PlayGrid

def Begin():
    width = 400
    height = 400
    cellWidth = 40
    cellHeight= 40
    grid = PlayGrid(100, 200, width, height, cellWidth, cellHeight)

def Update():
    pass

def Render():
    pass

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render, width=600, height=700)
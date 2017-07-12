from basics import Screen
from grid import PlayGrid

def Begin():
    width = 400
    height = 400
    cellWidth = 40
    cellHeight= 40
    grid = PlayGrid(width, height, cellWidth, cellHeight)
    grid.x = 100
    grid.y = 100

def Update():
    pass

def Render():
    pass

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render, width=600, height=600)
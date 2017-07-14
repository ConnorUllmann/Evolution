from basics import Screen
from grid import PlayGrid

def Begin():
    width = 400
    height = 400
    cellWidth = 50
    cellHeight= 50
    grid = PlayGrid(50, 250, width, height, cellWidth, cellHeight)

def Update():
    pass

def Render():
    pass

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render, width=500, height=700)
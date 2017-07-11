from basics import Screen

def Begin():
    pass

def Update():
    pass

def Render():
    pass

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render, width=800, height=600)
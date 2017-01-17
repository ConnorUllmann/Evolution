from screen import Screen

class Wall:
    walls = []

    def __init__(self, x, y, w, h):
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = (0, 0)
        
        self.destroyed = False
        Screen.Instance.AddUpdateFunction(self, self.Update)
        Screen.Instance.AddRenderFunction(self, self.Render)
        Screen.PutOnTop(self)
        Wall.walls.append(self)

    def Destroy(self):
        if not self.destroyed:
            self.destroyed = True
            Screen.Instance.RemoveUpdateFunctions(self)
            Screen.Instance.RemoveRenderFunctions(self)
            Wall.walls.remove(self)

    def Update(self):
        self.x += self.v[0]
        self.y += self.v[1]
        pass

    def Render(self):
        Screen.DrawRect((self.x, self.y), (self.w, self.h), self.color, filled=False)
        pass

from basics import Screen, Entity, Point, Color, CircleHorizontalLineCollide, CircleVerticalLineCollide, PointInsideCircle, PointInsideRectangle

y1 = None
y2 = None
p = Point()

class Circle(Entity):
    def __init__(self, x, y, radius):
        Entity.__init__(self, x, y)
        self.radius = radius
        self.color = Color.white

    def Update(self):
        global y1, y2, x, p
        Entity.Update(self)
        self.color = Color.yellow if PointInsideCircle(p, self.position, self.radius) else Color.teal

    def Render(self):
        Entity.Render(self)
        Screen.DrawCircle(self.position, self.radius, self.color)

def Begin():
    global circle, x
    circle = Circle(200, 200, 100)
    x = 200
    pass

def Update():
    global circle, p
    a = Screen.MousePosition()
    p.x = a.x
    p.y = a.y
    #circle.x = p.x
    #circle.y = p.y
    pass

def Render():
    global circle, y1, y2, x
    circle.Render()
    a = circle - Point(circle.radius, circle.radius)
    r = 2 * circle.radius * Point(1, 1)
    Screen.DrawRect(a, r, Color.red if PointInsideRectangle(p.x, p.y, a.x, a.y, r.x, r.y) else Color.blue)
    #Screen.DrawLine(Point(x, y1 if y1 is not None else 0), Point(x, y2 if y2 is not None else Screen.Width()))
    pass

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render)
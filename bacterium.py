from lifeform import Lifeform
from gene import Gene
from screen import *
from random import randint

class Bacterium(Lifeform):

    bacteria = []

    def __init__(self, x, y, parents):
        Bacterium.bacteria.append(self)
        super().__init__(parents)
        self.x = x
        self.y = y
        self.radius = 10
        self.color = RandomColor()
        Screen.Instance.AddUpdateFunction(self.Render)

    def Mate(self, other):
        return Bacterium((self.x + other.x) / 2, (self.y + other.y) / 2, [self, other])

    def Render(self):
        self.x += randint(-3, 3)
        self.y += randint(-3, 3)
        Screen.Instance.DrawCircle((self.x, self.y), self.radius, self.color)

Screen(600, 400)

b0 = Bacterium(120, 140, [])
b1 = Bacterium(160, 90, [])

b2 = b0.Mate(b1)
for trait in b0.genes:
    print(trait)
    print(" " + b0.genes[trait].BasesString())
print("")
for trait in b1.genes:
    print(trait)
    print(" " + b1.genes[trait].BasesString())
print("")
for trait in b2.genes:
    print(trait)
    print(" " + b2.genes[trait].BasesString())

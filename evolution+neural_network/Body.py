from brain import Brain
from neural_network import NeuralNetwork
from screen import Screen

class Body:
    bodies = []

    def __init__(self, brain, x, y, w=300, h=500):
        self.color = (255, 255, 255)
        self.radius = 12
        self.brain = brain
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        
        self.destroyed = False
        Screen.Instance.AddUpdateFunction(self, self.Update)
        Screen.Instance.AddRenderFunction(self, self.Render)
        Screen.PutOnTop(self)
        Body.bodies.append(self)

    def Destroy(self):
        if not self.destroyed:
            self.destroyed = True
            Screen.Instance.RemoveUpdateFunctions(self)
            Screen.Instance.RemoveRenderFunctions(self)
            Body.bodies.remove(self)

    def Update(self):
        pass

    def Render(self):
        hTotal = self.height
        wTotal = self.width
        wMax = None
        for w in self.brain.neuralNetwork.sizes:
            if wMax is None or w > wMax:
                wMax = w

        nodePositions = []
        for i in range(len(self.brain.neuralNetwork.sizes)):
            w = self.brain.neuralNetwork.sizes[i]
            nodePositions.append([])
            for j in range(w):
                nodePositions[i].append((self.x + i * hTotal / (len(self.brain.neuralNetwork.sizes)-1), self.y + (j - (w-1)/2)/(wMax - 1)*wTotal))

        for i in range(len(nodePositions)):
            for j in range(len(nodePositions[i])):
                p = nodePositions[i][j]
                if i + 1 < len(nodePositions):
                    for k in range(len(nodePositions[i+1])):
                        m = nodePositions[i+1][k]
                        #print(self.brain.neuralNetwork.weights)
                        v = self.brain.neuralNetwork.weights[i][k][j]
                        c = max(min(255 * (v + 4) / 8, 255), 0)
                        Screen.DrawLine(p, m, (255 - c, c, 0), max(1, int(abs(v)*2)))

        for i in range(len(nodePositions)):
            for j in range(len(nodePositions[i])):
                p = nodePositions[i][j]
                Screen.DrawCircle(p, self.radius, self.color)
        pass

from basics import *
import pygame, math, os

class Gladiator(Entity):

    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.color = self.defaultColor = (255, 255, 255)
        self.radius = 16
        self.speedDash = 20
        self.speedNormal = 2
        self.detectableClasses = []
        
        self.AddState("normal", self.UpdateNormal)
        self.AddState("hit", self.UpdateHit, self.BeginHit, self.EndHit)
        self.AddState("dash", self.UpdateDash, self.BeginDash)
        self.SetState("normal")

    def UpdateNormal(self):
        pass

    def UpdateHit(self):
        self.hitTimer -= 1
        if self.hitTimer <= 0:
            self.hitTimer = 0
            self.SetState("normal")

    def BeginHit(self):
        self.color = (255, 0, 0)
        self.hitTimer = 60

    def EndHit(self):
        self.color = self.defaultColor

    def UpdateDash(self):
        self.UpdatePosition(0.95)
        
        if self.v.lengthSq <= 8**2:
            self.SetState("normal")

    def BeginDash(self, targetAngle):
        self.v = self.speedDash * Point(math.cos(targetAngle), math.sin(targetAngle))

    def Render(self):
        Screen.DrawCircle(self, self.radius * max(0.5, 1 - self.v.lengthSq / self.speedDash**2), self.color)

    def collides(self, other):
        return CirclesCollide(self, self.radius, other, other.radius)

    def UpdatePosition(self, friction):
        self.v *= friction
        self.x += self.v.x
        self.y += self.v.y

        self.x = min(max(self.x, 0), Screen.Instance.width)
        self.y = min(max(self.y, 0), Screen.Instance.height)

    def ExecuteOutputs(self, outputs):
        acc = 3
        if outputs[0] > 0.5:
            self.v.x -= acc
        if outputs[1] > 0.5:
            self.v.x += acc
        if outputs[2] > 0.5:
            self.v.y -= acc
        if outputs[3] > 0.5:
            self.v.y += acc

        if self.v.lengthSq >= self.speedNormal**2:
            self.v = max(self.speedNormal*self.v.normalized, 0.8 * self.v)

        outputStateName = self.StateIdToStateName(outputs[4])
        if outputStateName == "dash":
            self.SetState(outputStateName, outputs[5])
        else:
            self.SetState(outputStateName)

    def GetNeuralInputs(self):
        length = 1000
        lines = 18
        stateId = self.StateNameToStateId(self.state)
        if stateId is None:
            stateId = 0
        neuralInputs = [self.v.x, self.v.y, stateId]
        if len(self.detectableClasses) <= 0:
            return neuralInputs.extend([1] * lines)
        
        entities = []
        for className in self.detectableClasses:
            entities.extend(Entity.GetAllEntitiesOfType(className))
        if self in entities:
            entities.remove(self)
        
        for i in range(lines):
            m = Point(self.x, self.y)
            n = Point(length, 0)
            n.radians = i / lines * math.pi * 2
            n += m
            for entity in entities:
                collisionPoints = CircleLineCollide(entity, entity.radius, m, n)
                collisionPointsCount = len(collisionPoints)
                if collisionPointsCount == 2:
                    if (collisionPoints[0] - self).lengthSq < (collisionPoints[1] - self).lengthSq:
                        n = collisionPoints[0]
                    else:
                        n = collisionPoints[1]
                elif collisionPointsCount == 1:
                    n = collisionPoints[0]
            neuralInputs.append(m.distanceTo(n) / length)
        return neuralInputs

    @staticmethod
    def NeuralInputsAndOutputsString(neuralInputs, neuralOutputs):
        return ",".join(str(int(x*1000)/1000) for x in neuralInputs) + "|" + ",".join(str(int(x*1000)/1000) for x in neuralOutputs)

class Player(Gladiator):

    def __init__(self, x, y):
        Gladiator.__init__(self, x, y)
        self.color = self.defaultColor = (0, 255, 0)
        self.detectableClasses = ["AI"]

    def UpdateNormal(self):
        neuralOutputs = self.GetNeuralOutputs()
        self.ExecuteOutputs(neuralOutputs)
        
        if Screen.KeyDown(pygame.K_SPACE):
            self.SetState("dash", (Screen.Instance.MousePosition() - self).radians)

        self.UpdatePosition(0.9)
        
    def GetNeuralOutputs(self):
        return [
            int(Screen.KeyDown(pygame.K_LEFT) or Screen.KeyDown(pygame.K_a)),
            int(Screen.KeyDown(pygame.K_RIGHT) or Screen.KeyDown(pygame.K_d)),
            int(Screen.KeyDown(pygame.K_UP) or Screen.KeyDown(pygame.K_w)),
            int(Screen.KeyDown(pygame.K_DOWN) or Screen.KeyDown(pygame.K_s)),
            self.StateNameToStateId(self.nextStateName if self.nextStateName is not None else self.state),
            (Screen.Instance.MousePosition() - self).radians if self.nextStateName == "dash" else 0
        ]

    def OutputNeuralInputsAndOutputs(self, neuralInputs, neuralOutputs):
        allZeroes = True
        for neuralOutput in neuralOutputs:
            if neuralOutput > 0.5:
                allZeroes = False
                break
        if not allZeroes:
            neuralInputs = self.GetNeuralInputs()
            with open("dataset.txt", "a") as output:
                output.write(Gladiator.NeuralInputsAndOutputsString(neuralInputs, neuralOutputs) + "\n")
        

class AI(Gladiator):

    def __init__(self, x, y, teacher=None, nn=None):
        Gladiator.__init__(self, x, y)
        self.color = self.defaultColor = (0, 128, 255)
        self.detectableClasses = ["Player", "AI"]

        self.nn = None
        self.teacher = teacher
        if self.teacher is not None:
            self.LearnFromTeacher()
        elif nn is not None:
            self.nn = nn
        else:
            self.InitializeNeuralNetwork("LastNeuralNetwork")

    def UpdateNormal(self):
        self.ExecuteOutputs(self.GetNeuralOutputs())
        self.LearnFromTeacher()
        self.UpdatePosition(0.9)

        players = Entity.GetAllEntitiesOfType("Player")
        for player in players:
            if self.collides(player):
                self.SetState("hit")

    def Render(self):
        Gladiator.Render(self)

    def GetNeuralOutputs(self):
        return self.GetNeuralOutputsFromInputs(self.GetNeuralInputs())

    def GetNeuralOutputsFromInputs(self, neuralInputs):
        return self.nn.output(neuralInputs)

    def LearnFromTeacher(self):
        if self.teacher is not None:
            teacherNeuralInputs = self.teacher.GetNeuralInputs()
            teacherNeuralOutputs = self.teacher.GetNeuralOutputs()
            if self.nn is None:
                self.nn = NeuralNetwork([len(teacherNeuralInputs), 12, len(teacherNeuralOutputs)])
            self.TrainOnSingleTest(teacherNeuralInputs, teacherNeuralOutputs)        
    
    def TrainOnSingleTest(self, singleInput, singleOutput):
        self.nn.train([[singleInput, singleOutput]], 10, 1, 0.025)

    def TestsToBatches(self, tests, batchSize=30):
        batches = []
        while len(tests) >= batchSize:
            batches.append(tests[:batchSize])
            tests = tests[batchSize:]
        return batches

    def LogFileToBatches(self, filename):
        batches = []
        if os.path.isfile(filename):
            with open(filename, "r") as _input:
                tests = []
                for line in _input:
                    lineSplit = line.split("|")
                    inputs = list(float(x) for x in lineSplit[0].split(","))
                    outputs = list(float(str(x).replace("\n", "")) for x in lineSplit[1].split(","))
                    tests.append([inputs, outputs])
                batches = self.TestsToBatches(tests)
        return batches
        
    def InitializeNeuralNetwork(self, filename=None):
        if filename is not None:
            try:
                with open(filename + ".txt", "r") as i:
                    pass
                self.nn = NeuralNetwork.Load(filename)
            except:
                pass
                #neuralInputs = self.GetNeuralInputs(["Player"])
                #neuralOutputs = self.GetNeuralOutputs(neuralInputs)
                #self.nn = NeuralNetwork([len(neuralInputs), 8, len(neuralOutputs)])
        else:
            batches = self.LogFileToBatches("dataset.txt")
            
            if len(batches) <= 0:
                return
            
            print("Beginning training!")
            inputCount = len(batches[0][0][0])
            outputCount = len(batches[0][0][1])
            self.nn = NeuralNetwork([inputCount, 12, outputCount])
            for x in range(100):
                self.nn.trainWithBatches(batches, 0.025)
            print("Done training!")
            self.nn.save("LastNeuralNetwork")
    

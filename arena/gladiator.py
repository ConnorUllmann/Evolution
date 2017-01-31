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
            self.SetState("normal")

    def BeginHit(self):
        self.color = (255, 0, 0)
        self.hitTimer = 60

    def EndHit(self):
        self.color = self.defaultColor
        self.hitTimer = 0

    def UpdateDash(self):
        self.UpdatePosition(0.95)
        
        if self.v.lengthSq <= 8**2:
            self.SetState("normal")

    def BeginDash(self):
        self.v = max(self.v.length, self.speedDash) * self.v.normalized

    def Render(self):
        Screen.DrawCircle(self, self.radius * max(0.5, 1 - self.v.lengthSq / self.speedDash**2), self.color)

    def collides(self, other):
        return CirclesCollide(self, self.radius, other, other.radius)

    def UpdatePosition(self, friction):
        self.v *= friction
        self.x += self.v.x
        self.y += self.v.y

        self.x = min(max(self.x % Screen.Instance.width, 0), Screen.Instance.width)
        self.y = min(max(self.y % Screen.Instance.height, 0), Screen.Instance.height)

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

        stateCountBinaryDigits = self.StateCountBinaryDigits()
        if stateCountBinaryDigits > 0:
            o = list(outputs[4:4+stateCountBinaryDigits])
            for i in range(len(o)):
                o[i] = int(round(o[i]))
            outputStateId = Debinary(o)
            for _id in self.statesById:
                print("{} {}".format(_id, self.statesById[_id].name))
            input("Why are Ids 3-5 instead of 0-3 so that I can use it to assign state by Id?")            
            if outputStateId < self.stateCount:
                outputStateName = self.StateIdToStateName(outputStateId)
                print("> {} {}".format(outputStateId, outputStateName))
                self.SetState(outputStateName)

    def StateCountBinaryDigits(self):
        return ceil(math.log(self.stateCount, 2))

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
            self.SetState("dash")

        self.UpdatePosition(0.9)
        
    def GetNeuralOutputs(self):
        a = [
            int(Screen.KeyDown(pygame.K_LEFT) or Screen.KeyDown(pygame.K_a)),
            int(Screen.KeyDown(pygame.K_RIGHT) or Screen.KeyDown(pygame.K_d)),
            int(Screen.KeyDown(pygame.K_UP) or Screen.KeyDown(pygame.K_w)),
            int(Screen.KeyDown(pygame.K_DOWN) or Screen.KeyDown(pygame.K_s))
        ]
        stateId = self.StateNameToStateId(self.nextStateName if self.nextStateName is not None else self.state)
        a.extend(Binary(stateId, math.ceil(math.log(self.stateCount, 2)), True))
        return a

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
        self.dummy = False

        self.nn = None
        self.teacher = teacher
        if self.teacher is not None:
            self.LearnFromTeacher()
        elif nn is not None:
            self.nn = nn
        else:
            self.InitializeNeuralNetwork("LastNeuralNetwork")

    def UpdateNormal(self):
        if self.dummy:
            return
        
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
        return self.nn.output(neuralInputs, True)

    def LearnFromTeacher(self):
        if self.teacher is not None:
            teacherNeuralInputs = self.teacher.GetNeuralInputs()
            teacherNeuralOutputs = self.teacher.GetNeuralOutputs()
            if self.nn is None:
                self.nn = NeuralNetwork([len(teacherNeuralInputs), 12, 6, len(teacherNeuralOutputs)])
            if self.teacher.nextStateName == "dash":
                self.TrainOnSingleTest(teacherNeuralInputs, teacherNeuralOutputs)
    
    def TrainOnSingleTest(self, singleInput, singleOutput):
        self.nn.train([[singleInput, singleOutput]], 100, 1, 0.05)

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

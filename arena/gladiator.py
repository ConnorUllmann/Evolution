from basics import *
import pygame, math, os

class Gladiator(Entity):

    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.color = self.defaultColor = (255, 255, 255)
        self.radius = 16
        self.speedDash = 20
        self.speedNormal = 4
        self.detectableClasses = []
        
        self.AddState("normal", self.UpdateNormal)
        self.AddState("hit", self.UpdateHit, self.BeginHit, self.EndHit)
        self.AddState("dash", self.UpdateDash, self.BeginDash)
        self.AddState("stunned", self.UpdateStunned)
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

    def UpdateStunned(self):
        self.v = self.speedNormal * self.v.normalized
        self.v.radians += 1

    def UpdateDash(self):
        self.UpdatePosition(0.95)

        entities = self.GetAllDetectableInstances()
        for entity in entities:
            if self.collides(entity):
                #d = self - entity
                #v = Point(self.radius + entity.radius - d.length, 0)
                #v.radians = d.radians
                #self.v += v
                #entity.v -= v
                entity.SetState("hit")
        
        if self.v.lengthSq <= 8**2:
            self.SetState("normal")

    def BeginDash(self):
        self.v = max(self.v.length, self.speedDash) * self.v.normalized

    def Render(self):
        radius = self.radius * max(0.5, 1 - self.v.lengthSq / self.speedDash**2)
        Screen.DrawCircle(self, radius, self.color)
        Screen.DrawLine(self, self + self.v.normalized * radius * 1.05, (max(self.color[0] - 40, 0), max(self.color[1] - 40, 0), max(self.color[2] - 40, 0)), 3)
        #self.RenderNeuralInputs(36, 1000)

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
            self.v = max(self.speedNormal*self.v.normalized, 0.9 * self.v)

        stateIndexStart = 4
        stateCountBinaryDigits = self.StateCountBinaryDigits()
        if stateCountBinaryDigits > 0:
            o = list(outputs[stateIndexStart:stateIndexStart+stateCountBinaryDigits])
            for i in range(len(o)):
                o[i] = int(round(o[i]))
            outputStateId = Debinary(o)
            if outputStateId < self.stateCount:
                outputStateName = self.StateIdToStateName(outputStateId)
                self.SetState(outputStateName)

    def StateCountBinaryDigits(self):
        return ceil(math.log(self.stateCount, 2))

    def GetAllDetectableInstances(self):
        entities = []
        for className in self.detectableClasses:
            entities.extend(Entity.GetAllEntitiesOfType(className))
        if self in entities:
            entities.remove(self)
        return entities

    def RadialSweep(self, lines, length):
        entities = self.GetAllDetectableInstances()
        retPoints = []
        retEntities = []
        for i in range(lines):
            m = Point.Clone(self)
            n = Point(length, 0)
            n.radians = i / lines * math.pi * 2
            n += m
            e = None
            for entity in entities:
                for collisionPoint in CircleLineCollide(entity, entity.radius, m, n):
                    if (collisionPoint - m).lengthSq < (n - m).lengthSq:
                        n = Point.Clone(collisionPoint)
                        e = entity
            retPoints.append(n)
            retEntities.append(e)
        return [retPoints, retEntities]

    def GetNeuralInputs(self):
        length = 1000
        lines = 16

        stateId = self.StateNameToStateId(self.state)
        if stateId is None:
            stateId = 0
        neuralInputs = [self.v.x < -1, self.v.x > 1, self.v.y < -1, self.v.y > 1]
        neuralInputs.extend(Binary(stateId, self.StateCountBinaryDigits(), True))

        if len(self.detectableClasses) <= 0:
            return neuralInputs.extend([1] * lines)

        sweep = self.RadialSweep(lines, length)
        for point, entity in zip(sweep[0], sweep[1]):
            neuralInputs.append(max(1 - (point - self).length / 160, 0))
            neuralInputs.append((entity.__class__.__name__ == self.__class__.__name__) if entity is not None else False)
            neuralInputs.extend(Gladiator.AngleToDirectionalOutput(entity.v.radians if entity is not None else 0))
        return neuralInputs

    def RenderNeuralInputs(self, lines, length):
        for p in self.RadialSweep(lines, length)[0]:
            Screen.Instance.DrawLine(self, p, (255, 255, 0))

    @staticmethod
    def AngleToDirectionalOutput(radians):
        v = Point(math.cos(radians), math.sin(radians))
        threshold = 0.4
        a = [
            v.x < -threshold,
            v.x > threshold,
            v.y < -threshold,
            v.y > threshold
        ]
        return a

    @staticmethod
    def NeuralInputsAndOutputsString(neuralInputs, neuralOutputs):
        return ",".join(str(int(x*1000)/1000) for x in neuralInputs) + "|" + ",".join(str(int(x*1000)/1000) for x in neuralOutputs)

class Player(Gladiator):

    def __init__(self, x, y):
        Gladiator.__init__(self, x, y)
        self.color = self.defaultColor = (0, 255, 0)
        self.detectableClasses = ["AI", "Swarmling"]

    def UpdateNormal(self):
        neuralOutputs = self.GetNeuralOutputs()
        self.ExecuteOutputs(neuralOutputs)
        
        if Screen.KeyDown(pygame.K_SPACE):
            self.SetState("dash")

        self.UpdatePosition(0.9)

        self.OutputNeuralInputsAndOutputs(self.GetNeuralInputs(), neuralOutputs)
        
    def GetNeuralOutputs(self):
        a = [
            int(Screen.KeyDown(pygame.K_LEFT) or Screen.KeyDown(pygame.K_a)),
            int(Screen.KeyDown(pygame.K_RIGHT) or Screen.KeyDown(pygame.K_d)),
            int(Screen.KeyDown(pygame.K_UP) or Screen.KeyDown(pygame.K_w)),
            int(Screen.KeyDown(pygame.K_DOWN) or Screen.KeyDown(pygame.K_s))
        ]
        stateId = self.StateNameToStateId(self.nextStateName if self.nextStateName is not None else self.state)
        a.extend(Binary(stateId, self.StateCountBinaryDigits(), True))
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

class Swarmling(Gladiator):
    def __init__(self, x, y):
        Gladiator.__init__(self, x, y)
        self.color = self.defaultColor = (80, 80, 80)
        self.outerRadius = 160
        self.innerRadius = 20
        self.angle = self.id
        self.detectableClasses = ["Swarmling", "AI"]

    def GetNeuralOutputs(self):
        a = Gladiator.AngleToDirectionalOutput(self.angle)
        stateId = self.StateNameToStateId(self.nextStateName if self.nextStateName is not None else self.state)
        a.extend(Binary(stateId, self.StateCountBinaryDigits(), True))
        return a        

    def UpdateNormal(self):
        entities = self.GetAllDetectableInstances()
        for entity in entities:
            if entity.__class__.__name__ == self.__class__.__name__:
                d2 = (entity - self).lengthSq
                if d2 <= self.outerRadius**2:
                    self.angle += AngleDiff(self.angle, entity.v.radians)/40
                if d2 <= self.innerRadius**2:
                    self.angle += ((entity - self).radians + math.pi - self.angle) / 4
            else:
                d2 = (entity - self).lengthSq
                if d2 <= self.outerRadius**2:
                    self.angle = (entity - self).radians + math.pi
                
        self.UpdatePosition(0.9)

    def Render(self):
        neuralOutputs = self.GetNeuralOutputs()
        self.ExecuteOutputs(neuralOutputs)
        Gladiator.Render(self)      
        

class AI(Gladiator):

    InternalLayerSizes = [40]

    def __init__(self, x, y, teachers=None, nn=None):
        Gladiator.__init__(self, x, y)
        self.color = self.defaultColor = (0, 128, 255)
        self.detectableClasses = ["Player", "AI", "Swarmling"]

        self.nn = nn
        self.teachers = teachers if teachers is not None else []
        self.lastLessons = []

    def UpdateNormal(self):
        self.LearnFromTeachers()
        self.ExecuteOutputs(self.GetNeuralOutputs())
        self.UpdatePosition(0.9)

    @staticmethod
    def NeuralNetworkFromInputsAndOutputs(inputs, outputs):
        sizes = [len(inputs)]
        sizes.extend(AI.InternalLayerSizes)
        sizes.append(len(outputs))
        return NeuralNetwork(sizes)

    def GetNeuralOutputs(self):
        return self.GetNeuralOutputsFromInputs(self.GetNeuralInputs())

    def GetNeuralOutputsFromInputs(self, neuralInputs):
        return self.nn.output(neuralInputs, True)

    def LearnLesson(self, teacherNeuralInputs, teacherNeuralOutputs):
        if self.nn is None:
            self.nn = AI.NeuralNetworkFromInputsAndOutputs(teacherNeuralInputs, teacherNeuralOutputs)

        self.lastLessons.append([teacherNeuralInputs, teacherNeuralOutputs])
        while len(self.lastLessons) > 5:
            self.lastLessons.pop(0)

        #if not self.LessonIsRedundant(teacherNeuralInputs, teacherNeuralOutputs):
        self.TrainOnSingleTest(teacherNeuralInputs, teacherNeuralOutputs)

    def LessonIsRedundant(self, teacherNeuralInputs, teacherNeuralOutputs):
        for lesson in self.lastLessons:
            for i in range(len(teacherNeuralInputs)):
                if round(lesson[0][i]) != round(teacherNeuralInputs[i]):
                    return False
            for i in range(len(teacherNeuralOutputs)):
                if round(lesson[1][i]) != round(teacherNeuralOutputs[i]):
                    return False
        return True

    def LearnFromTeachers(self):
        for teacher in self.teachers:
            self.LearnLesson(teacher.GetNeuralInputs(), teacher.GetNeuralOutputs())
    
    def TrainOnSingleTest(self, singleInput, singleOutput):
        self.nn.train([[singleInput, singleOutput]], 10, 10, 0.01)

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

    def InitializeNeuralNetwork(self, filename="dataset.txt", roundsOfTraining=100):
        batches = self.LogFileToBatches(filename)
        if len(batches) <= 0:
            return

        print("Beginning training!")
        self.nn = AI.NeuralNetworkFromInputsAndOutputs(batches[0][0][0], batches[0][0][1])
        for x in range(roundsOfTraining):
            self.nn.trainWithBatches(batches, 0.025)
        print("Done training!")

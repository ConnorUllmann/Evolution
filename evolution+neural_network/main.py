from neural_network import NeuralNetwork
from training_set import TrainingSet
from genome import Genome
from thread_handler import ThreadHandler
from utils import *
from random import choice
from datetime import datetime

class Brain():

    def sumDNAForTrait(self, trait):
        return sum(self.genome.genes[trait].DNA)

    def initializeAndTrainNeuralNetwork(self, function, nInput, nOutput):
        layers = [nInput]
        layers.extend(self.genome.genes["hidden_layers"].DNA)
        layers.append(nOutput)
        iterations = int(self.sumDNAForTrait("iterations"))
        batchSize = int(self.sumDNAForTrait("batch_size"))
        learningRate = self.sumDNAForTrait("learning_rate") / 1000

        self.trainingSet = TrainingSet(nInput, nOutput, function, 0.25)
        self.neuralNetwork = NeuralNetwork(layers)
        self.neuralNetwork.train(self.trainingSet.tests, iterations, batchSize, learningRate)
        self.neuralNetwork.test(self.trainingSet.tests, "test")

    def test(self):
        self.score = self.neuralNetwork.test(self.trainingSet.exams, "EXAM")

    def initializeGenome(self, parents):
        self.genome = Genome(parents, {
            "hidden_layers":{"start_length":2, "min_length":0, "start_zero":False, "min":1, "max":12, "mutationMagnitude":2},
            "iterations":{"start_length":4, "min_length":1, "start_zero":False, "min":1, "max":500, "mutationMagnitude":100},
            "batch_size":{"start_length":4, "min_length":1, "start_zero":False, "min":1, "max":10, "mutationMagnitude":2},
            "learning_rate":{"start_length":10, "min_length":1, "start_zero":False, "min":1, "max":100, "mutationMagnitude":50}
            })
        #print(self.genome)
    
    def __init__(self, parents):
        self.score = None
        self.initializeGenome(parents)

    def mate(self, other):
        return Brain([self, other])

    def train(self, function, nInput, nOutput):
        self.initializeAndTrainNeuralNetwork(function, nInput, nOutput)

    def save(self, filename):
        self.neuralNetwork.save(filename + "-NeuralNetwork.txt")
        self.genome.save(filename + "-Genome.txt")

def NextGeneration(parents):
    brain = Brain(parents)
    brain.train(Xor, 5, 1)
    brain.test()
    AddBrainToCheckQueue(brain)
    if len(BestScoringBrains) > 0:
        return [brain, choice(BestScoringBrains)]
    return [brain]

def EvolveBrains():
    parents = []
    while True:
        parents = NextGeneration(parents)
        

BestBrainsCheckQueue = []
nBestScoringBrains = 4
BestScoringBrains = []
def AddBrainToCheckQueue(brain):
    BestBrainsCheckQueue.append(brain)
    
def IsBestBrain(brain):
    if len(BestScoringBrains) <= 0:
        BestScoringBrains.append(brain)
        return True

    isBestBrain = False
    inserted = False
    for i in range(len(BestScoringBrains)-1, -1, -1):
        if brain.score > BestScoringBrains[i].score:
            if i == 0:
                BestScoringBrains.insert(0, brain)
                isBestBrain = True
                inserted = True
                break
            continue
        if i+1 >= len(BestScoringBrains):
            BestScoringBrains.append(brain)
        else:
            BestScoringBrains.insert(i+1, brain)
        inserted = True
        break
    
    if not inserted:
        BestScoringBrains.append(brain)

    while len(BestScoringBrains) > nBestScoringBrains:
        BestScoringBrains.pop()
    return isBestBrain

def UpdateCheckQueue():
    timeStart = datetime.now()
    while True:
        if len(BestBrainsCheckQueue) > 0:
            brain = BestBrainsCheckQueue.pop(0)
            if IsBestBrain(brain):
                print("Best score: {} ({})".format(brain.score, datetime.now() - timeStart))
                brain.save("BestScoringBrain")
            

if __name__ == "__main__":
    threadHandler = ThreadHandler()
    threadHandler.AddThread(UpdateCheckQueue, threadName="CheckQueue")
    for i in range(10):
        threadHandler.AddThread(EvolveBrains, threadName="EvolveBrains")
    print("All threads are starting...")
    threadHandler.RunAllThreads()

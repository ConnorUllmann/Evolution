from neural_network import NeuralNetwork
from training_set import TrainingSet
from genome import Genome
from utils import *

class Brain():

    def sumDNAForTrait(self, trait):
        return sum(self.genome.genes[trait].DNA)

    def initializeAndTrainNeuralNetwork(self, function, nInput, nOutput):
        layers = [nInput]
        layers.extend(self.genome.genes["hidden_layers"].DNA)
        layers.append(nOutput)
        iterations = self.sumDNAForTrait("iterations")
        batchSize = self.sumDNAForTrait("batch_size")
        learningRate = self.sumDNAForTrait("learning_rate") / 1000
        regularization = 0

        self.trainingSet = TrainingSet(nInput, nOutput, function, 0.25)
        self.neuralNetwork = NeuralNetwork(layers)
        self.neuralNetwork.train(self.trainingSet.tests, iterations, batchSize, learningRate, regularization)
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
        print(self.genome)
    
    def __init__(self, parents):
        self.score = None
        self.initializeGenome(parents)

    def train(self, function, nInput, nOutput):
        self.initializeAndTrainNeuralNetwork(function, nInput, nOutput)

def Next(parents):
    brain = Brain(parents)
    brain.train(Xor, 10, 1)
    brain.test()
    return brain

if __name__ == "__main__":
    brains = []
    for i in range(100):
        brains.append(Next([]))

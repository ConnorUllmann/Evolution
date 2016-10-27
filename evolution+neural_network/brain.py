from neural_network import NeuralNetwork
from training_set import TrainingSet
from genome import Genome
from thread_handler import ThreadHandler
from utils import *
from random import choice
from datetime import datetime
import threading

class Brain():

    ID = 0
    IDlock = threading.Lock()

    Scores = []
    ScoresLock = threading.Lock()

    @staticmethod
    def NewID():
        Brain.IDlock.acquire()
        try:
            returnID = Brain.ID
            Brain.ID += 1
            return returnID
        finally:
            Brain.IDlock.release()
        return returnID

    @staticmethod
    def StartRecordingScores():
        with open("BestScoringBrain-Scores.txt", "w") as x:
            pass

    @staticmethod
    def FlushScores():
        Brain.ScoresLock.acquire()
        try:
            if len(Brain.Scores) > 0:
                with open("BestScoringBrain-Scores.txt", "a") as output:
                    for score in Brain.Scores:
                        output.write("{}\n".format(score))
                    Brain.Scores = []
        finally:
            Brain.ScoresLock.release()

    def sumDNAForTrait(self, trait):
        return sum(self.genome.genes[trait])

    def train(self, testProportion, trainingSet=None):
        if trainingSet is not None:
            self.trainingSet = trainingSet
        #print("[{}] layers = {}, iterations = {}, learning rate = {}, species threshold = {}".format(self.id, layers[1:-1], iterations, learningRate, self.speciesThreshold))
        if self.neuralNetwork is None:
            nInput = self.trainingSet.nInput
            nOutput = self.trainingSet.nOutput
            layers = [nInput]
            layers.extend(self.genome.genes["hidden_layers"])
            layers.append(nOutput)
            self.neuralNetwork = NeuralNetwork(layers)

        iterations = int(self.sumDNAForTrait("iterations"))
        batchSize = int(self.sumDNAForTrait("batch_size"))
        learningRate = self.sumDNAForTrait("learning_rate") / 1000

        testSample = self.trainingSet.sample(testProportion)
        self.neuralNetwork.train(testSample, iterations, batchSize, learningRate)

    def test(self):
        self.score = self.neuralNetwork.test(self.trainingSet.tests, "ALL")
        Brain.Scores.append(self.score)
        if len(Brain.Scores) >= 10:
            Brain.FlushScores()
        print("[{}] = {}%".format(self.id, int(self.score*1000)/10))
        #print("Brain:\n{}".format(self))
        return self.score

    def initializeGenome(self, parents):
        self.genome = Genome({
            "hidden_layers":{"start_length":[1, 4], "min_length":1, "start_zero":False, "min":1, "max":20, "mutationMagnitude":3},
            "iterations":{"start_length":[4, 10], "min_length":1, "start_zero":False, "min":1, "max":250, "mutationMagnitude":100},
            "batch_size":{"start_length":[1, 4], "min_length":1, "start_zero":False, "min":1, "max":10, "mutationMagnitude":2},
            "learning_rate":{"start_length":[1, 10], "min_length":1, "start_zero":False, "min":1, "max":100, "mutationMagnitude":50},
            "species_threshold":{"start_length":[1, 4], "min_length":1, "start_zero":True, "min":0, "max":100, "mutationMagnitude":20}
            }, parents=parents)
    
    def __init__(self, parents=None, neuralNetwork=None, genome=None):
        self.id = Brain.NewID()
        self.score = None
        if genome is not None:
            self.genome = genome
        else:
            self.initializeGenome(parents)
        self.speciesThreshold = self.sumDNAForTrait("species_threshold") / 1000
        self.neuralNetwork = neuralNetwork

    def canMate(self, other):
        if self == other:
            return False
        #x = self.genome.compare(other.genome)
        return True #self.speciesThreshold <= x < 1

    def mate(self, other):
        if self.canMate(other):
            return Brain([self, other])
        return None

    def save(self, filename):
        self.neuralNetwork.save(filename + "-NeuralNetwork")
        self.genome.save(filename + "-Genome")

    @staticmethod
    def Load(filename):
        nn = NeuralNetwork.Load(filename+"-NeuralNetwork")
        g = Genome.Load(filename+"-Genome")
        brain = Brain(neuralNetwork=nn, genome=g)
        return brain

    def __str__(self):
        return str("GENOME:\n" + str(self.genome) + "\nNEURAL NETWORK:\n" + str(self.neuralNetwork))

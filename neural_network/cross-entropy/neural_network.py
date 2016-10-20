### http://neuralnetworksanddeeplearning.com/chap3.html#the_cross-entropy_cost_function
import json
import random
import sys
from numpy import *
from utils import *
from training_set import *
from datetime import datetime, timedelta

class Network():

    def __init__(self, sizes):
        self.layersCount = len(sizes)
        self.sizes = sizes
        self.biases =  [random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [random.randn(y, x) / sqrt(x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def feedForward(self, o):
        zs = []
        os = [o]
        for b, w in zip(self.biases, self.weights):
            z = reshape(dot(w, o), (-1, 1)) + b
            o = Sigmoid(z)
            zs.append(z)
            os.append(o)
        return os, zs       

    def backprop(self, x, y):
        os, zs = self.feedForward(x)
        delta = os[-1] - reshape(y, (-1, 1))
        ddb = [zeros(b.shape) for b in self.biases]
        ddw = [zeros(w.shape) for w in self.weights]
        ddb[-1] = delta
        ddw[-1] = dot(delta, os[-2].T)
        for l in range(2, self.layersCount):
            z = zs[-l]
            sp = SigmoidDerivative(z)
            delta = dot(self.weights[-l+1].T, delta) * sp
            ddb[-l] = delta
            ddw[-l] = dot(delta, reshape(array(os[-l-1]), (1, -1)))
        return ddb, ddw

    def output(self, a, decimal=False):
        z = reshape(self.feedForward(a)[0][-1], (1, -1))[0]
        if decimal:
            return z
        b = zeros(z.shape)
        for i in range(len(b)):
            b[i] = 1 if z[i] > 0.5 else 0
        return b

    def trainWithBatch(self, batch, learningRate, regularization, nTests):
        nBatch = len(batch)
        db = [zeros(b.shape) for b in self.biases]
        dw = [zeros(w.shape) for w in self.weights]
        for x, y in batch:
            ddb, ddw = self.backprop(x, y)
            db = [_db + _ddb for _db, _ddb in zip(db, ddb)]
            dw = [_dw + _ddw for _dw, _ddw in zip(dw, ddw)]
        self.weights = [(1 - learningRate * (regularization / nTests)) * w - (learningRate / nBatch) * nw for w, nw in zip(self.weights, dw)]
        self.biases =  [b - (learningRate / nBatch) * nb for b, nb in zip(self.biases, db)]

    def trainWithBatches(self, batches, learningRate, regularization, nTests):
        for batch in batches:
            self.trainWithBatch(batch, learningRate, regularization, nTests) 

    def train(self, tests, iterations, batchSize, learningRate, regularization=0):
        print("Beginning training...")
        startTime = datetime.now()
        nTests = len(tests)
        for j in range(iterations):
            random.shuffle(tests)
            batches = [tests[k:k + batchSize] for k in range(0, nTests, batchSize)]
            self.trainWithBatches(batches, learningRate, regularization, nTests)
            if (j+1) % 1000 == 0:
                print("Epoch {} training complete ({})".format(j+1, RemoveMilliseconds(datetime.now() - startTime)))

    def test(self, tests, label=""):
        numberTotal = len(tests)
        numberCorrect = 0
        for test in tests:
            input = test[0]
            output = self.output(input)
            outputExpected = test[1]
            correct = True
            for i, o in zip(outputExpected, output):
                if int(i) != int(o):
                    correct = False
                    break
            outputDecimal = self.output(input, True)
            print("{} {} = {} {} {} = {}".format(label, input, outputExpected, "-   -" if correct else "- @ -", output, outputDecimal))
            numberCorrect += int(correct)
        
        print("\n{} / {} = {}%".format(numberCorrect, numberTotal, int(numberCorrect / numberTotal * 100)))

    def save(self, filename):
        data = {"sizes": self.sizes,
                "weights": [w.tolist() for w in self.weights],
                "biases": [b.tolist() for b in self.biases] }
        f = open(filename, "w")
        json.dump(data, f)
        f.close()
    
    @staticmethod
    def Load(filename):
        f = open(filename, "r")
        data = json.load(f)
        f.close()
        net = Network(data["sizes"])
        net.weights = [array(w) for w in data["weights"]]
        net.biases = [array(b) for b in data["biases"]]
        return net

def GetTrainedNeuralNetworkForFunction(sizes, function, *args):
    if len(sizes) < 2 or function is None:
        return None

    testProportion = 0.2 if len(args) <= 0 else args[0]
    iterations = 10000 if len(args) <= 1 else args[1]
    batchSize = 30 if len(args) <= 2 else args[2]
    learningRate = 1 if len(args) <= 3 else args[3]
    regularization = 0.0 if len(args) <= 4 else args[4]
    
    trainingSet = TrainingSet(sizes[0], sizes[-1], function, testProportion)
    network = Network(sizes)
    network.train(trainingSet.tests, iterations, batchSize, learningRate, regularization)
    print("\n---------------------- TESTS ----------------------")
    network.test(trainingSet.tests, "Test")
    print("\n---------------------- EXAMS ----------------------")
    network.test(trainingSet.exams, "Exam")
    network.save("last-test-network.txt")
    return network

def Run(x):
    if x == 0:
        network = GetTrainedNeuralNetworkForFunction([6, 12, 16, 6, 1], Xor, 0.2, 10000, 8, 5, 0)
    elif x == 1:
        network = GetTrainedNeuralNetworkForFunction([3, 4, 2, 1], Opp)
    else: #GOOD
        network = GetTrainedNeuralNetworkForFunction([6, 14, 16, 14, 4], Add, 0.2, 5000, 30, 1, 0)

Run(1)

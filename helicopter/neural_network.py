### http://neuralnetworksanddeeplearning.com/chap3.html#the_cross-entropy_cost_function
import json
import random
import sys
from numpy import *
from utils import *
from training_set import *
from datetime import datetime, timedelta

class NeuralNetwork():

    def __init__(self, sizes):
        self.layersCount = len(sizes)
        self.sizes = sizes
        self.biases =  [random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [random.randn(y, x) / sqrt(x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def forwardPropagate(self, o):
        zs = []
        os = [o]
        for b, w in zip(self.biases, self.weights):
            z = reshape(dot(w, o), (-1, 1)) + b
            o = Sigmoid(z)
            zs.append(z)
            os.append(o)
        return os, zs       

    def backPropagate(self, x, y):
        os, zs = self.forwardPropagate(x)
        delta = os[-1] - reshape(y, (-1, 1))
        ddb = [zeros(b.shape) for b in self.biases]
        ddw = [zeros(w.shape) for w in self.weights]
        ddb[-1] = delta
        ddw[-1] = dot(delta, reshape(os[-2].T, (1, -1)))
        for l in range(2, self.layersCount):
            z = zs[-l]
            sp = SigmoidDerivative(z)
            delta = dot(self.weights[-l+1].T, delta) * sp
            ddb[-l] = delta
            ddw[-l] = dot(delta, reshape(array(os[-l-1]), (1, -1)))
        return ddb, ddw

    def output(self, a, decimal=False):
        z = reshape(self.forwardPropagate(a)[0][-1], (1, -1))[0]
        if decimal:
            return z
        b = zeros(z.shape)
        for i in range(len(b)):
            b[i] = 1 if z[i] > 0.5 else 0
        return b

    def trainWithBatch(self, batch, learningRate):
        db = [zeros(b.shape) for b in self.biases]
        dw = [zeros(w.shape) for w in self.weights]
        for x, y in batch:
            ddb, ddw = self.backPropagate(x, y)
            db = [_db + _ddb for _db, _ddb in zip(db, ddb)]
            dw = [_dw + _ddw for _dw, _ddw in zip(dw, ddw)]
        m = learningRate / len(batch)
        self.weights = [w - m * nw for w, nw in zip(self.weights, dw)]
        self.biases =  [b - m * nb for b, nb in zip(self.biases, db)]

    def trainWithBatches(self, batches, learningRate):
        for batch in batches:
            self.trainWithBatch(batch, learningRate) 

    def train(self, tests, iterations, batchSize, learningRate):
        #print("Beginning training...")
        startTime = datetime.now()
        nTests = len(tests)
        for j in range(iterations):
            #random.shuffle(tests)
            batches = [tests[k:k + batchSize] for k in range(0, nTests, batchSize)]
            self.trainWithBatches(batches, learningRate)
            #if (j+1) % 100 == 0:
            #    print("Epoch {} / {} training complete ({})".format(j+1, iterations, RemoveMilliseconds(datetime.now() - startTime)))

    def test(self, tests, label=""):
        numberTotal = len(tests)
        numberCorrect = 0
        for test in tests:
            correct = True
            for i, o in zip(test[1], self.output(test[0])):
                if int(i) != int(o):
                    correct = False
                    break
            outputDecimal = self.output(test[0], True)
            #print("{} {} = {} {} {} = {}".format(label, test[0], test[1], "-   -" if correct else "- @ -", self.output(test[0]), outputDecimal))
            numberCorrect += int(correct)
        
        #print("\n{} / {} = {}%".format(numberCorrect, numberTotal, int(numberCorrect / numberTotal * 1000)/10))
        return numberCorrect / numberTotal

    def data(self):
        return {"sizes": self.sizes,
                "weights": [w.tolist() for w in self.weights],
                "biases": [b.tolist() for b in self.biases]}
    
    def save(self, filename):
        data = self.data()
        f = open(filename+".txt", "w")
        json.dump(data, f)
        f.close()
    
    @staticmethod
    def Load(filename):
        f = open(filename+".txt", "r")
        data = json.load(f)
        f.close()
        net = NeuralNetwork(data["sizes"])
        net.weights = [array(w) for w in data["weights"]]
        net.biases = [array(b) for b in data["biases"]]
        return net

    def __str__(self):
        return str(self.data())

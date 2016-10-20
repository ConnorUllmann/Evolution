### http://neuralnetworksanddeeplearning.com/chap3.html#the_cross-entropy_cost_function
import json
import random
import sys
from numpy import *
from utils import *
from training_set import *
from datetime import datetime, timedelta

class Network(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [random.randn(y, x) / sqrt(x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def feedForward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = Sigmoid(dot(w, reshape(a, (-1, 1)))+b)
        return a

    def output(self, a):
        z = reshape(self.feedForward(a), (1, -1))[0]
        b = zeros(z.shape)
        for i in range(len(b)):
            b[i] = 1 if z[i] > 0.5 else 0
        return b

    def train(self, training_data, epochs, mini_batch_size, eta, lmbda = 0.0):
        print("Beginning training...")
        startTime = datetime.now()
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k+mini_batch_size] for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.updateMiniBatch(mini_batch, eta, lmbda, n)
            if j % 1000 == 0 and j > 0:
                print("Epoch {} training complete ({})".format(j, RemoveMilliseconds(datetime.now() - startTime)))

    """ mini_batch = list of tuples (x, y)
        eta        = learning rate
        lmbda      = regularization parameter
        n          = size of the training data set """
    def updateMiniBatch(self, mini_batch, eta, lmbda, n):
        db = [zeros(b.shape) for b in self.biases]
        dw = [zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            ddb, ddw = self.backprop(x, y)
            db = [_db + _ddb for _db, _ddb in zip(db, ddb)]
            dw = [_dw + _ddw for _dw, _ddw in zip(dw, ddw)]
        self.weights = [(1 - eta * (lmbda / n)) * w - (eta / len(mini_batch)) * nw for w, nw in zip(self.weights, dw)]
        self.biases = [b - (eta / len(mini_batch)) * nb for b, nb in zip(self.biases, db)]

    def backprop(self, x, y):
        # feedforward
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = reshape(dot(w, activation), (-1, 1)) + b
            zs.append(z)
            activation = Sigmoid(z)
            activations.append(activation)
            
        # backward pass
        delta = (activations[-1] - reshape(y, (-1, 1)))
        db = [zeros(b.shape) for b in self.biases]
        dw = [zeros(w.shape) for w in self.weights]
        db[-1] = delta
        dw[-1] = dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = SigmoidDerivative(z)
            delta = dot(self.weights[-l+1].transpose(), delta) * sp
            db[-l] = delta
            dw[-l] = dot(delta, reshape(array(activations[-l-1]), (1, -1)))

        return (db, dw)

    def test(self, tests, label=""):
        numberTotal = len(tests)
        numberCorrect = 0
        for test in tests:
            input = test[0]
            outputExpected = test[1]
            output = self.output(input)
            correct = True
            for i, o in zip(outputExpected, output):
                if int(i) != int(o):
                    correct = False
                    break
            outputDecimal = self.feedForward(input).T[0]
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
    epochs = 10000 if len(args) <= 1 else args[1]
    miniBatchSize = 30 if len(args) <= 2 else args[2]
    learningRate = 1 if len(args) <= 3 else args[3]
    lmbda = 0.0 if len(args) <= 4 else args[4]
    
    trainingSet = TrainingSet(sizes[0], sizes[-1], function, testProportion)
    network = Network(sizes)
    network.train(trainingSet.tests, epochs, miniBatchSize, learningRate, lmbda)
    print("\n---------------------- TESTS ----------------------")
    network.test(trainingSet.tests, "Test")
    print("\n---------------------- EXAMS ----------------------")
    network.test(trainingSet.exams, "Exam")
    network.save("last-test-network.txt")
    return network

network = GetTrainedNeuralNetworkForFunction([12, 14, 16, 14, 7], Add, 0.2, 50000, 30, 1, 0)
#network = GetTrainedNeuralNetworkForFunction([6, 12, 16, 6, 1], Xor, 0.2, 10000, 8, 5, 0)
#network = GetTrainedNeuralNetworkForFunction([3, 4, 2, 1], Opp)

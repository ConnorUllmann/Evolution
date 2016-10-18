from numpy import exp, array, random, dot, zeros, reshape, isnan
from utils import *
from training_set import TrainingSet
import math

class NeuronLayer():
    def __init__(self, neuronCount, inputsPerNeuron):
        self.weights = random.randn(neuronCount, inputsPerNeuron) / sqrt(inputsPerNeuron)
        self.neuronCount = neuronCount
        self.inputsPerNeuron = inputsPerNeuron

    def __str__(self):
        return "({} neurons, each with {} inputs):\n{}".format(self.neuronCount, self.inputsPerNeuron, str(self.weights))

class NeuralNetwork():

    #Arguments are the number of neurons in each layer
    def __init__(self, learningRate=1, inputCount=1, *args):
        self.learningRate = learningRate
        self.layers = []
        self.inputCount = inputCount
        for i in range(len(args)):
            _neuronCount = args[i]
            _inputsPerNeuron = args[i-1] if i-1 >= 0 else self.inputCount
            self.layers.append(NeuronLayer(_neuronCount, _inputsPerNeuron))
        self.layersCount = len(self.layers)+1
        self.sizes = [inputCount, *args]

    def Cost(self, a, y):
        return 0.5*np.linalg.norm(a-y)**2
        #return np.sum(np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)))

    #Cost equation for output a and desired output y
    def Delta(self, a, y):
        #print("\na:\n{}".format(a))
        #print("\ny:\n{}".format(y))
        return (a - y)

    def Backprop(self, x, y):
        nabla_w = [zeros(layer.weights.shape) for layer in self.layers]
        activations, zs = self.Think(x)
        #print("\nzs:\n{}".format(zs))

        delta = self.Delta(activations[-1], y)
        nabla_w[-1] = dot(reshape(delta, (-1, 1)), reshape(activations[-2], (1, -1)))
        print("\nDELTA:\n{}".format(delta.shape))
        print("\nACTIVATIONS[-2].T:\n{}".format(activations[-2].T.shape))
        input("\nNABLA:\n{}".format(nabla_w[-1]))
        
        for l in range(2, self.layersCount):
            i = -l
            z = zs[i]
            sp = SigmoidDerivative(z)
            delta = dot(self.layers[i+1].weights.T, delta) * sp
            nabla_w[i] = dot(reshape(delta, (-1, 1)), reshape(activations[i-1], (1, -1)))
##            if i == -2:
##                print("\nsp:\n{}".format(sp))
##                print("\nWEIGHTS:\n{}".format(self.layers[i+1].weights.T.shape))
            
        return nabla_w

    # We train the neural network through a process of trial and error, adjusting the synaptic weights each time.
    def Train(self, function, ignore=None, iterations=1000):
        trainingSet = TrainingSet(self.inputCount, function, ignore)
        n = len(trainingSet.input)
        for iteration in range(iterations):
            weightsSet = None
            for x, y in zip(trainingSet.input, trainingSet.output):
                backprop = self.Backprop(x, y)
                if weightsSet == None:
                    weightsSet = [zeros(bp.shape) for bp in backprop]
                for i in range(len(backprop)):
                    #print("\nWEIGHTS SET:\n{}".format(weightsSet[i]))
                    #print("\nBACKPROP:\n{}".format(backprop[i]))
                    weightsSet[i] += backprop[i]
                    #input("\nWEIGHTS SET:\n{}".format(weightsSet[i]))
            #print("---------------------")
            #print("====== WEIGHTS SET ==")
            #print("---------------------")
            #input(weightsSet)
            for i in range(len(self.layers)):
                self.layers[i].weights += self.learningRate * weightsSet[i]
            print(weightsSet[-1])
            input(self.layers[-1].weights)
            #for layer, weights in zip(self.layers, weightsSet):
            #    layer.weights += self.learningRate * weights #(1 - self.learningRate / n) * layer.weights - self.learningRate / n * weights

    def Think(self, x):
        i = x
        b = []
        a = [x]
        #print("\nX:\n{}".format(x))
        count = 0
        for layer in self.layers:
            count += 1
            #print(count)
            w = layer.weights
            #print(w)
            #if count == 2:
            #    print("Layer #{}:\n{}".format(count, w))
            z = dot(w, i)
            i = Sigmoid(z)
            b.append(z)
            a.append(i)
        return a, b

    # The neural network prints its weights
    def PrintWeights(self):
        for i in range(0, len(self.layers)):
            print("Layer {} {}".format(i+1, self.layers[i].weights))

    def Output(self, inputs, integer=False):
        output = self.Think(inputs)[0][-1]
        ret = []
        for o in output:
            if integer:
                ret.append(1 if o > 0.5 else 0)
            elif isnan(o):
                ret.append('x')
            else:
                ret.append(int(o*10)/10)
        return ret
            
# ----------- TEST FUNCTIONS --------------
def xor(*args):
    x = args[0]
    for i in range(1, len(args)):
        x = (x != args[i])
    return [int(x)]

def example(*args):
    return [int(args[0] != args[1])]

def add(*args):
    mid = int(len(args)/2)
    a = 0
    b = 0
    c = 0
    for i in range(0, int(mid)):
        a += pow(2, i) * args[len(args)-(i+mid)-1]
        b += pow(2, i) * args[len(args)-i-1]
        c += pow(2, i)
    _y = int(a+b)
    _yString = "{0:b}".format(_y)
    _length = len("{0:b}".format(int(c*2+1)))
    ret = []
    for i in range(len(_yString)):
        __y = _yString[i]
        ret.append(int(__y == '1'))
    while len(ret) < _length:
        ret.insert(0, 0)
    #print("{} + {} = {}".format(a, b, _y))
    #print("{} + {} = {}".format(args[:mid], args[mid:], ret))
    return ret
# -----------------------------------------

def Test(function, learningRate, layerSizes, inputs, seed=None):
    if len(inputs) <= 0:
        return

    if seed is not None:
        random.seed(seed)

    testInputs = array(inputs)

    outputs = []
    for a in testInputs:
        outputs.append(function(*a))
    print("\nTEST INPUTS:\n{}".format(testInputs))
    print("\nTEST OUTPUTS:\n{}".format(outputs))

    #layerSizes.insert(0, len(testInputs[0]))
    layerSizes.append(len(outputs[0]))
    network = NeuralNetwork(learningRate, len(testInputs[0]), *layerSizes)

    print("\nStarting Training...")
    network.Train(function, testInputs)
    
    numCorrect = 0
    numTotal = len(testInputs)
    for i in range(numTotal):
        a = testInputs[i]
        o = outputs[i]
        u = network.Output(a, False)
        correct = True
        for j in range(0, len(o)):
            if o[j] != u[j]:
                correct = False
                break
        if correct:
            numCorrect += 1
        print("{} = {}".format(a, o))
        print("{} = {} {}\n ------".format(a, u, "WRONG" if not correct else ""))
    #print(network.PrintWeights())
    print("{} / {} = {}% correct".format(numCorrect, numTotal, int(numCorrect/numTotal*100)))
    return numCorrect/numTotal

if __name__ == "__main__":
##    Test(example, 0.1, [2],
##         [[1, 0, 1],
##          [1, 1, 0],
##          [0, 1, 0],
##          [1, 0, 0]])
##    Test(example, 1, [4, 8, 4],
##         [[1, 0, 1],
##          [1, 1, 0]])
##    Test(example, 10, [4, 8, 4],
##         [[1, 0, 1],
##          [1, 1, 0]])
##    input("\n<ENTER> for next...")
##    Test(xor, 1, [16, 16, 16],
##         [[1, 1, 0, 0, 0],
##          [1, 1, 1, 1, 1],
##          [0, 0, 1, 0, 0],
##          [0, 1, 0, 1, 0],
##          [0, 0, 1, 1, 0],
##          [0, 0, 1, 1, 1],
##          [0, 1, 1, 1, 0]])
##    input("\n<ENTER> for next...")
    totalTests = 0
    totalScore = 0
    while True:
        totalScore += Test(add, 0.1, [14, 16, 14],
             [[1, 1, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 0],
              [0, 0, 1, 0, 0, 1],
              [0, 1, 0, 1, 0, 1],
              [0, 0, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0, 1],
              [1, 0, 1, 1, 1, 0]])
        totalTests += 1
        #if totalTests % 10 == 0:
        print("Average {}% correct in {} tests".format(int(totalScore/totalTests*100), totalTests))
        if totalTests >= 100:
            break

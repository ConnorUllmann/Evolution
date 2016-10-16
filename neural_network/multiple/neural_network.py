from numpy import exp, array, random, dot
from utils import *

class TrainingSet:
    def __init__(self, bitLength, function, ignore=None):        
        inputBinarySet = []
        outputBinarySet = []
        xMax = int(pow(2, bitLength))
        for x in range(0, xMax):
            inputBinary = "{0:b}".format(x)
            while len(inputBinary) < bitLength:
                inputBinary = '0' + inputBinary
            inputBinaryList = []
            for character in inputBinary:
                inputBinaryList.append(int(character))

            if ignore is not None:
                skip = False
                for m in ignore:
                    same = True
                    for i in range(0, len(inputBinaryList)):
                        if inputBinaryList[i] != m[i]:
                            same = False
                    if same:
                        skip = True
                        break
                if skip:
                    continue
                
            inputBinarySet.append(inputBinaryList)
            
            y = function(*inputBinaryList)
            outputBinarySet.append(y)
        
        self.input = array(inputBinarySet)
        self.output = array(outputBinarySet)
        #print("-- IGNORE --\n{}".format(ignore))
        #print("-- IN --\n{}".format(self.input))
        #print("-- OUT --\n{}".format(self.output))

class NeuronLayer():
    def __init__(self, neuronCount, inputsPerNeuron):
        self.weights = 2 * random.random((inputsPerNeuron, neuronCount)) - 1
        self.neuronCount = neuronCount
        self.inputsPerNeuron = inputsPerNeuron

    def __str__(self):
        return "({} neurons, each with {} inputs):\n{}".format(self.neuronCount, self.inputsPerNeuron, str(self.weights))

class NeuralNetwork():

    #Arguments are the number of neurons in each layer
    def __init__(self, learningRate=1, *args):
        self.learningRate = learningRate
        self.layers = []
        self.inputCount = args[0]
        for i in range(0, len(args)-1):
            _neuronCount = args[i+1]
            _inputsPerNeuron = args[i]
            self.layers.append(NeuronLayer(_neuronCount, _inputsPerNeuron))

    # We train the neural network through a process of trial and error, adjusting the synaptic weights each time.
    def Train(self, function, ignore=None, iterations=10000):
        trainingSet = TrainingSet(self.inputCount, function, ignore)
        for iteration in range(iterations):
            # Forward-propagate the training set through our neural network
            outputSet = []
            for output in self.Think(trainingSet.input):
                outputSet.append(output)

            # Calculate the error for each layer (The difference between the desired output and the predicted output).
            # By looking at the weights in layer 1, we can determine by how much layer 1 contributed to the error in layer 2.            
            #Back propagate
            error = [0] * len(self.layers)
            delta = [0] * len(self.layers)
            alter = [0] * len(self.layers)
            for i in range(len(self.layers)-1, -1, -1):
                error[i] = (trainingSet.output - outputSet[i]) if i+1 >= len(self.layers) else delta[i+1].dot(self.layers[i+1].weights.T)
                delta[i] = error[i] * SigmoidDerivative(outputSet[i])

                #y = trainingSet.output if i+1 >= len(self.layers) else outputSet[i+1]
                #a = outputSet[i]
                #error[i] = np.sum(np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)))
                #delta[i] = a - y if i+1 >= len(self.layers) else
                
                alter[i] = (outputSet[i-1] if i > 0 else trainingSet.input).T.dot(delta[i])

            # Adjust the weights.
            for i in range(0, len(self.layers)):
                self.layers[i].weights += self.learningRate * alter[i]

    # The neural network thinks.
    def Think(self, inputs):
        outputs = []
        for i in range(0, len(self.layers)):
            _inputs = outputs[i-1] if i > 0 else inputs
            outputs.append(Sigmoid(dot(_inputs, self.layers[i].weights)))
        return outputs

    # The neural network prints its weights
    def PrintWeights(self):
        for i in range(0, len(self.layers)):
            print("Layer {} {}".format(i+1, self.layers[i]))

    def Output(self, inputs, integer=False):
        output = self.Think(inputs)[-1]
        ret = []
        for o in output:
            if integer:
                ret.append(1 if o > 0.5 else 0)
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

    layerSizes.insert(0, len(testInputs[0]))
    layerSizes.append(len(outputs[0]))
    network = NeuralNetwork(learningRate, *layerSizes)

    network.Train(function, testInputs)
    #network.PrintWeights()

    numCorrect = 0
    numTotal = len(testInputs)
    for i in range(numTotal):
        a = testInputs[i]
        o = outputs[i]
        u = network.Output(a, True)
        correct = True
        for j in range(0, len(o)):
            if o[j] != u[j]:
                correct = False
                break
        if correct:
            numCorrect += 1
        #print("{} = {}".format(a, o))
        #print("{} = {} {}\n ------".format(a, u, "WRONG" if not correct else ""))
    #print("{} / {} = {}% correct".format(numCorrect, numTotal, int(numCorrect/numTotal*100)))
    return numCorrect/numTotal

if __name__ == "__main__":
##    Test(example, 0.1, [4, 8, 4],
##         [[1, 0, 1],
##          [1, 1, 0]])
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
        totalScore += Test(add, 0.05, [14, 16, 14],
             [[1, 1, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 0],
              [0, 0, 1, 0, 0, 1],
              [0, 1, 0, 1, 0, 1],
              [0, 0, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0, 1],
              [1, 0, 1, 1, 1, 0]])
        totalTests += 1
        if totalTests % 10 == 0:
            print("Average {}% correct in {} tests".format(int(totalScore/totalTests*100), totalTests))
        if totalTests >= 100:
            break

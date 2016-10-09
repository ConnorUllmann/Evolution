from numpy import exp, array, random, dot
from utils import *

class TrainingSet:
    def __init__(self, bitLength, function):        
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
            inputBinarySet.append(inputBinaryList)
            
            y = function(*inputBinaryList)
            outputBinarySet.append(int(y))
        
        self.input = array(inputBinarySet)
        self.output = array([outputBinarySet]).T

class NeuronLayer():
    def __init__(self, neuronCount, inputsPerNeuron):
        self.weights = 2 * random.random((inputsPerNeuron, neuronCount)) - 1
        self.neuronCount = neuronCount
        self.inputsPerNeuron = inputsPerNeuron

    def __str__(self):
        return "({} neurons, each with {} inputs):\n{}".format(self.neuronCount, self.inputsPerNeuron, str(self.weights))

class NeuralNetwork():

    #Arguments are the number of neurons in each layer
    def __init__(self, *args):
        self.layers = []
        self.inputCount = args[0]
        for i in range(0, len(args)):
            _neuronCount = args[i+1] if i+1 < len(args) else 1
            _inputsPerNeuron = args[i]
            self.layers.append(NeuronLayer(_neuronCount, _inputsPerNeuron))

    # We train the neural network through a process of trial and error, adjusting the synaptic weights each time.
    def Train(self, function, iterations=100000):
        trainingSet = TrainingSet(self.inputCount, function)
        for iteration in range(iterations):
            # Pass the training set through our neural network
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
                alter[i] = (outputSet[i-1] if i > 0 else trainingSet.input).T.dot(delta[i])

            # Adjust the weights.
            for i in range(0, len(self.layers)):
                self.layers[i].weights += alter[i]

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

def xor(*args):
    x = args[0]
    for i in range(1, len(args)):
        x = (x != args[i])
    return x

def example(*args):
    return args[0] != args[1]

if __name__ == "__main__":

    #Seed the random number generator
    random.seed(1)

    nn = NeuralNetwork(3, 4)

    print("Stage 1) Random starting synaptic weights: ")
    nn.PrintWeights()
    #nn.Train(xor)
    nn.Train(example)
    print("Stage 2) New synaptic weights after training: ")
    nn.PrintWeights()

    # Test the neural network with a new situation.
    print("Stage 3) Considering a new situation [1, 1, 0] -> ?: ")
    output = nn.Think(array([1, 1, 0]))[-1]
    print(output)

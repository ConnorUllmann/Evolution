from neural_network import NeuralNetwork
from training_set import TrainingSet
from utils import *

def GetTrainedNeuralNetworkForFunction(sizes, function, *args):
    if len(sizes) < 2 or function is None:
        return None

    testProportion = 0.2 if len(args) <= 0 else args[0]
    iterations = 10000 if len(args) <= 1 else args[1]
    batchSize = 30 if len(args) <= 2 else args[2]
    learningRate = 1 if len(args) <= 3 else args[3]
    regularization = 0.0 if len(args) <= 4 else args[4]
    
    trainingSet = TrainingSet(sizes[0], sizes[-1], function, testProportion)
    network = NeuralNetwork(sizes)
    network.train(trainingSet.tests, iterations, batchSize, learningRate, regularization)
    print("\n---------------------- TESTS ----------------------")
    network.test(trainingSet.tests, "Test")
    print("\n---------------------- EXAMS ----------------------")
    network.test(trainingSet.exams, "Exam")
    network.save("last-test-network.txt")
    return network

def Run(x):
    if x == 0:
        network = GetTrainedNeuralNetworkForFunction([6, 12, 16, 6, 1], Xor, 0.2, 10000, 8, 1, 0)
    elif x == 1:
        network = GetTrainedNeuralNetworkForFunction([3, 4, 2, 1], Opp, 0.25, 10000, 3, 3, 0)
    else: #GOOD
        network = GetTrainedNeuralNetworkForFunction([6, 14, 16, 14, 4], Add, 0.2, 5000, 30, 1, 0)

if __name__ == "__main__":
    Run(0)

from numpy import array
from random import shuffle, sample
from utils import *

class TrainingSet:
    def __init__(self, nInput, nOutput, function):
        self.nInput = nInput
        self.nOutput = nOutput
        xBinarySet = []
        yBinarySet = []

        xMax = int(pow(2, self.nInput))
        for x in range(0, xMax):
            xBinaryList = Binary(x, self.nInput, True)
            yBinaryList = Binary(function(*xBinaryList), self.nOutput, True)
            xBinarySet.append(xBinaryList)
            yBinarySet.append(yBinaryList)
        
        self.tests = []
        for x, y in zip(array(xBinarySet), array(yBinarySet)):
            self.tests.append((x, y))

    def sample(self, proportion):
        return sample(self.tests, min(max(ceil(len(self.tests) * proportion), 0), len(self.tests)))

    def print(self, tests=None):
        if tests is None:
            tests = self.tests
        for test in tests:
            print("{} = {}".format(test[0], test[1]))

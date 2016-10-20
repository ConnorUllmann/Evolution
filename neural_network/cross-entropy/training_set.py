from numpy import array
from random import shuffle
from utils import *

class TrainingSet:
    def __init__(self, bitLengthInput, bitLengthOutput, function, testProportion=0.1):        
        inputBinarySet = []
        outputBinarySet = []

        xMax = int(pow(2, bitLengthInput))
        for x in range(0, xMax):
            inputBinaryList = Binary(x, bitLengthInput, True)
            inputBinarySet.append(inputBinaryList)
            y = Binary(function(*inputBinaryList), bitLengthOutput, True)
            outputBinarySet.append(y)
        
        tests = []
        for i, o in zip(array(inputBinarySet), array(outputBinarySet)):
            tests.append((i, o))

        if len(tests) <= 0:
            self.exams = []
            self.tests = []
        else:
            shuffle(tests)
            i = max(1, int(len(tests) * testProportion))
            self.exams = tests[:i]
            self.tests = tests[i:]

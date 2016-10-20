from numpy import array
from random import shuffle
from utils import *

class TrainingSet:
    def __init__(self, bitLengthInput, bitLengthOutput, function, testProportion=0.1):        
        xBinarySet = []
        yBinarySet = []

        xMax = int(pow(2, bitLengthInput))
        for x in range(0, xMax):
            xBinaryList = Binary(x, bitLengthInput, True)
            yBinaryList = Binary(function(*xBinaryList), bitLengthOutput, True)
            xBinarySet.append(xBinaryList)
            yBinarySet.append(yBinaryList)
        
        tests = []
        for x, y in zip(array(xBinarySet), array(yBinarySet)):
            tests.append((x, y))

        if len(tests) <= 0:
            self.exams = []
            self.tests = []
        else:
            shuffle(tests)
            i = max(1, int(len(tests) * testProportion))
            self.exams = tests[:i]
            self.tests = tests[i:]

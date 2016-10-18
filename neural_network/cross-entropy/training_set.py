from numpy import array
from random import shuffle

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
            outputBinarySet.append(y)
        
        self.tests = []
        for i, o in zip(array(inputBinarySet), array(outputBinarySet)):
            self.tests.append((i, o))
        shuffle(self.tests)

    def PluckTestSet(self, n=0.1):
        if len(self.tests) <= 0:
            return []
        i = max(1, int(len(self.tests)*n))
        testSet = self.tests[:i]
        self.tests = self.tests[i:]
        return testSet

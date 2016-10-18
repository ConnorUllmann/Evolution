from numpy import array

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

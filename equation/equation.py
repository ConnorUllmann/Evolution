from lifeform import Lifeform
from random import shuffle
from datetime import datetime
from random import randint

class Equation(Lifeform):

    HistoricMinScore = None

    BestEquationsAllTimePair = []

    @staticmethod
    def Generate(parents, targets):
        #Construct pairs and sort them by score
        pairs = []
        for parent in parents:
            pairs.append([parent.Score(targets), parent])
        pairs = sorted(pairs, key=lambda x:x[0])
        #print("{} => {}".format(pairs[0][0], pairs[0][1]))

        #Add qualifying pairs to the "best all-time" list
        BestEquationsAllTimePairMaxLength = 1
        currentBestEquationsAllTimePairLength = len(Equation.BestEquationsAllTimePair)
        if currentBestEquationsAllTimePairLength <= 0:
            Equation.BestEquationsAllTimePair.append(pairs[0])
        elif currentBestEquationsAllTimePairLength < BestEquationsAllTimePairMaxLength:
            for pair in pairs:
                sufficientlyDifferent = True
                for bestPair in Equation.BestEquationsAllTimePair:
                    if Lifeform.CompareGenomes(pair[1].genes, bestPair[1].genes) > 0:
                        sufficientlyDifferent = False
                        break
                if sufficientlyDifferent:
                    Equation.BestEquationsAllTimePair.append(pair)
                    break
        else:
            for pair in pairs:
                sufficientlyDifferent = True
                qualifies = False
                for bestPair in Equation.BestEquationsAllTimePair:
                    if not qualifies and pair[0] < bestPair[0]:
                        qualifies = True
                    if Lifeform.CompareGenomes(pair[1].genes, bestPair[1].genes) > 0:
                        sufficientlyDifferent = False
                        break
                if qualifies and sufficientlyDifferent:
                    Equation.BestEquationsAllTimePair.append(pair)
                    break
        
        Equation.BestEquationsAllTimePair = sorted(Equation.BestEquationsAllTimePair, key=lambda x:x[0])
        while len(Equation.BestEquationsAllTimePair) > BestEquationsAllTimePairMaxLength:
            Equation.BestEquationsAllTimePair.pop()
        
        #Construct set of breeding equations
        newStockCount = min(10, len(pairs))
        pairsFront = pairs[:newStockCount]
        pairsFinal = list(Equation.BestEquationsAllTimePair)
        #shuffle(pairsFront)
        pairsFinal.extend(pairsFront)

        #Find lowest scoring pair
        minScorePair = None
        for pair in pairsFinal:
            if minScorePair is None or pair[0] < minScorePair[0]:
                minScorePair = (pair[0], pair[1])

        #Set lowest all-time score
        if Equation.HistoricMinScore is None or minScorePair[0] < Equation.HistoricMinScore:
            Equation.HistoricMinScore = minScorePair[0]
            print("({}) Min. Score: {}".format(datetime.now(), Equation.HistoricMinScore))
            print("y = {}".format(str(minScorePair[1])))

        #print("-----------------------------------------------")
        #for pair in Equation.BestEquationsAllTimePair:
        #    print(pair[1])
        #print("-----------------------------------------------")

        #Breed
        breeders = []
        kids = []
        for i in range(0, len(parents)):
            pairsTemp = [pairsFinal[i%len(pairsFinal)],
                         pairsFinal[(i+randint(1, max(int(len(pairsFinal)/3), 1)))%len(pairsFinal)],
                         pairsFinal[(i+randint(1, max(int(len(pairsFinal)/3), 1)))%len(pairsFinal)]]
            for pair in pairsTemp:
                breeders.append(pair[1])
            kids.append(Equation(breeders))
        
        #print(len(kids))
        return kids

    def __str__(self):
        return self.asString

    def Score(self, targets):
        score = 0
        for target in targets:
            score += abs(self.y(target[0]) - target[1])**4
        return score

    def y(self, x):
        y = 0
        i = 0
        for base in self.genes["constants"].DNA:
            y += base * pow(x, max(2*i-1, 0))
            i += 1
        return y

    def __init__(self, parents):
        super().__init__(parents)
        s = ""
        DNA = self.genes["constants"].DNA
        i = len(DNA) - 1
        while i >= 0:
            if True or int(DNA[i]) != 0:
                s += str(int(DNA[i])) + ("x^{}".format(max(2*i-1, 0)) if i != 0 else "")
                if i >= 1:
                    s += " + "
            i -= 1
        self.asString = s
            

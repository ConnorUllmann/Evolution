from random import random, randint, shuffle

class Gene:
    MIN_GENE_LENGTH = 2
    MAX_GENE_LENGTH = 6

    @staticmethod
    def GenerateRandomBases(DNA):
        tempList = []
        for i in range(0, len(DNA)):
            tempList.append(i)
        shuffle(tempList)
        return tempList[0:randint(Gene.MIN_GENE_LENGTH, Gene.MAX_GENE_LENGTH)]

    @staticmethod
    def SequenceFromBases(DNA, bases):
        sequence = ""
        for base in bases:
            sequence = "{0}{1}".format(sequence, DNA[base])
        return sequence

    def BasesString(self):
        s = ""
        bases = sorted(self.bases)
        for base in bases:
            s = "{0} {1}".format(s, base)
        return s[1:len(s)]          

    def __init__(self, DNA, bases=None):
        self.DNA = DNA
        self.bases = bases if bases is not None else Gene.GenerateRandomBases(self.DNA)
        self.sequence = Gene.SequenceFromBases(self.DNA, self.bases)

from random import random, randint, shuffle

class Gene:

    def DNAString(self):
        s = ""
        for base in self.DNA:
            s = "{0} {1}".format(s, base)
        return s[1:]

    def Mutate(self, mutationChancePerBase = 0.2):
        for i in range(0, len(self.DNA)):
            if random() < mutationChancePerBase:
                self.DNA[i] = randint(self.min, self.max)

    def __init__(self, trait, DNA, valueRange):
        self.trait = trait
        self.DNA = DNA
        self.valueRange = valueRange
        self.min = self.valueRange[0]
        self.max = self.valueRange[1]

from random import random, randint, shuffle

class Gene:

    def DNAString(self):
        s = ""
        for base in self.DNA:
            s = "{0} {1}".format(s, base)
        return s[1:]

    def Mutate(self, mutationChancePerBase = 0.05):
        for i in range(0, len(self.DNA)):
            if random() < mutationChancePerBase:
                try:
                    _min = int(self.min)
                    _max = int(self.max)
                    self.DNA[i] = randint(_min, _max)
                except ValueError:
                    self.DNA[i] = random() * (self.max - self.min) + self.min

    def __init__(self, trait, DNA, valueRange):
        self.trait = trait
        self.DNA = DNA
        self.valueRange = valueRange
        self.min = self.valueRange[0]
        self.max = self.valueRange[1]

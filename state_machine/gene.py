from random import random, randint, shuffle

class Gene:

    def DNAString(self):
        s = ""
        for base in self.DNA:
            s = "{0} {1}".format(s, base)
        return s[1:]

    def Mutate(self, mutationMagnitude, mutationChancePerBase = 0.2):
        for i in range(0, len(self.DNA)):
            if random() < mutationChancePerBase:
                r = randint(self.min, self.max)
                self.DNA[i] = min(max(self.DNA[i] + (random() - 0.5) * r / 100 * mutationMagnitude, self.min), self.max)
                
    def __init__(self, trait, DNA, minLength, valueRange):
        self.trait = trait
        self.DNA = DNA
        self.minLength = minLength
        self.valueRange = valueRange
        self.min = self.valueRange[0]
        self.max = self.valueRange[1]

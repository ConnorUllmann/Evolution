from random import random, randint, shuffle

class Gene:

    def __str__(self):
        s = ""
        for base in self.DNA:
            s = "{0} {1}".format(s, base)
        return s[1:]

    def mutate(self, mutationChancePerBase = 0.1):
        for i in range(len(self.DNA)):
            if random() < mutationChancePerBase:
                self.DNA[i] = min(max(int(self.DNA[i] + (random() - 0.5) * 2 * self.mutationMagnitude), self.min), self.max)
                
    def __init__(self, trait, DNA, minLength, minValue, maxValue, mutationMagnitude):
        self.trait = trait
        self.DNA = DNA
        self.minLength = minLength
        self.min = minValue
        self.max = maxValue
        self.mutationMagnitude = mutationMagnitude

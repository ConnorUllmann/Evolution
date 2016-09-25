from random import random, randint, shuffle
from gene import Gene

class Lifeform:

    TRAITS = {
        "structure":{"start_length":9, "min_length":2, "min":0, "max":5},
        "speed":{"start_length":3, "min_length":1, "min":0, "max":1},
        "life":{"start_length":4, "min_length":1, "min":3000, "max":50000},
        "maturation_period":{"start_length":1, "min_length":1, "min":2, "max":4}
    }

    @staticmethod
    def GenerateDNARandom(trait):
        DNA = []
        info = Lifeform.TRAITS[trait]
        for i in range(0, info["start_length"]):
            DNA.append(randint(info["min"], info["max"]))
        return DNA

    @staticmethod
    def GenerateDNAFromParents(trait, parents):
        shuffle(parents)
        DNA = []
        parentIndex = 0
        for i in range(0, len(parents[0].genes[trait].DNA)):
            while i >= len(parents[parentIndex].genes[trait].DNA):
                parentIndex = (parentIndex + 1) % len(parents)
            bit = parents[parentIndex].genes[trait].DNA[i]
            parentIndex = (parentIndex + 1) % len(parents)
            DNA.append(bit)

        v = random()
        if v <= 0.025:
            if len(DNA) > Lifeform.TRAITS["structure"]["min_length"]:
                DNA.pop()
        elif v >= 1 - 0.025:
            DNA.append(randint(Lifeform.TRAITS["structure"]["min"], Lifeform.TRAITS["structure"]["max"]))
        
        return DNA

    @staticmethod
    def GenerateGenesRandom():
        genes = {}
        for trait in Lifeform.TRAITS:
            DNA = Lifeform.GenerateDNARandom(trait)
            valueRange = [Lifeform.TRAITS[trait]["min"],Lifeform.TRAITS[trait]["max"]]
            genes[trait] = Gene(trait, DNA, valueRange)
        return genes

    @staticmethod
    def GenerateGenesFromParents(parents):
        genes = {}
        traitsDict = {}
        for parent in parents:
            for trait in parent.genes:
                traitsDict[trait] = True
        traits = list(traitsDict.keys())
        for trait in traits:
            DNA = Lifeform.GenerateDNAFromParents(trait, parents)
            valueRange = [Lifeform.TRAITS[trait]["min"],Lifeform.TRAITS[trait]["max"]]
            genes[trait] = Gene(trait, DNA, valueRange)
        return genes           

    @staticmethod
    def GenerateGenes(parents):
        if parents is not None and len(parents) > 0:
            return Lifeform.GenerateGenesFromParents(parents)
        else:
            return Lifeform.GenerateGenesRandom()

    @staticmethod
    def MutateGenes(genes):
        for trait in genes:
            genes[trait].Mutate()
        return genes

    def PrintGenes(self):
        for trait in self.genes:
            print("[{0}] = {1}".format(trait, self.genes[trait].DNAString()))
        

    def __init__(self, parents):
        self.genes = Lifeform.MutateGenes(Lifeform.GenerateGenes(parents))

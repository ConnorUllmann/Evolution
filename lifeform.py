from random import random, randint, shuffle
from gene import Gene

class Lifeform:

    TRAITS = {
        "structure":{"format":"int", "start_length":17, "min_length":2, "min":0, "max":8},
        "life":{"format":"int", "start_length":6, "min_length":1, "min":9000, "max":100000},
        "maturation_period":{"format":"int", "start_length":1, "min_length":1, "min":2, "max":5},
        "refractory_period":{"format":"int", "start_length":1, "min_length":1, "min":1, "max":4},
        "species_threshold":{"format":"float", "start_length":0, "min_length":0, "min":0, "max":0.95}
    }

    @staticmethod
    def GenerateDNARandom(trait):
        DNA = []
        info = Lifeform.TRAITS[trait]
        for i in range(0, info["start_length"]):
            if info["format"] == "int":
                DNA.append(randint(info["min"], info["max"]))
            if info["format"] == "float":
                DNA.append(random() * (info["max"] - info["min"]) + info["min"])
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
        if v <= 0.25:
            if len(DNA) > Lifeform.TRAITS[trait]["min_length"]:
                DNA.pop()
        elif v >= 1 - 0.25:
            if Lifeform.TRAITS[trait]["format"] == "int":
                DNA.append(randint(Lifeform.TRAITS[trait]["min"], Lifeform.TRAITS[trait]["max"]))
            elif Lifeform.TRAITS[trait]["format"] == "float":
                DNA.append(random() * (Lifeform.TRAITS[trait]["max"] - Lifeform.TRAITS[trait]["min"]) + Lifeform.TRAITS[trait]["min"])
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

    @staticmethod
    def CompareGenomes(a_genes, b_genes):
        same = 0
        diff = 0
        for trait in a_genes:
            if trait in b_genes:
                aLenDNA = len(a_genes[trait].DNA)
                bLenDNA = len(b_genes[trait].DNA)
                maxLen = max(aLenDNA, bLenDNA)
                minLen = min(aLenDNA, bLenDNA)
                diff += maxLen - minLen
                for i in range(0, minLen):
                    if a_genes[trait].DNA[i] == b_genes[trait].DNA[i]:
                        same += 1
                    else:
                        diff += 1
            else:
                diff += len(a_genes[trait].DNA)
        for trait in b_genes:
            if trait not in a_genes:
                diff += len(b_genes[trait].DNA)
        return same / (same + diff)

    def PrintGenes(self):
        for trait in self.genes:
            print("[{0}] = {1}".format(trait, self.genes[trait].DNAString()))
        

    def __init__(self, parents):
        self.genes = Lifeform.MutateGenes(Lifeform.GenerateGenes(parents))

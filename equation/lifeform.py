from random import random, randint, shuffle
from gene import Gene

class Lifeform:

    TRAITS = {
        "constants":{"start_length":12, "min_length":12, "min":-1000000, "max":1000000},
        "mutation_magnitude":{"start_length":1, "min_length":1, "min":0, "max":2}
        }

    @staticmethod
    def GenerateDNARandom(trait):
        DNA = []
        info = Lifeform.TRAITS[trait]
        for i in range(0, info["start_length"]):
            if "start_zero" in info:
                DNA.append(0)
            else:
                DNA.append(randint(info["min"], info["max"]))
        return DNA

    @staticmethod
    def GenerateDNAFromParents(trait, parents):
        shuffle(parents)
        DNA = []
        for i in range(0, len(parents[0].genes[trait].DNA)):
            sumValue = 0
            counted = 0
            for parent in parents:
                if i >= 0 and i < len(parent.genes[trait].DNA):
                    sumValue += parent.genes[trait].DNA[i]
                    counted += 1
            DNA.append(0 if counted == 0 else (sumValue / counted))

        return DNA

    @staticmethod
    def GenerateGenesRandom():
        genes = {}
        for trait in Lifeform.TRAITS:
            DNA = Lifeform.GenerateDNARandom(trait)
            valueRange = [Lifeform.TRAITS[trait]["min"],Lifeform.TRAITS[trait]["max"]]
            genes[trait] = Gene(trait, DNA, Lifeform.TRAITS[trait]["min_length"], valueRange)
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
            genes[trait] = Gene(trait, DNA, Lifeform.TRAITS[trait]["min_length"], valueRange)
        return genes           

    @staticmethod
    def GenerateGenes(parents):
        if parents is not None and len(parents) > 0:
            return Lifeform.GenerateGenesFromParents(parents)
        else:
            return Lifeform.GenerateGenesRandom()

    @staticmethod
    def MutateGenes(genes, mutationMagnitude):
        for trait in genes:
            genes[trait].Mutate(mutationMagnitude)
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
        

    def __init__(self, parents):
        self.genes = Lifeform.GenerateGenes(parents)
        mutationMagnitude = self.genes["mutation_magnitude"].DNA[0]
        self.genes = Lifeform.MutateGenes(self.genes, mutationMagnitude)

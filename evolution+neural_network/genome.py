from random import random, randint, shuffle
from gene import Gene

class Genome:

    def __str__(self):
        s = ""
        for trait in self.genes:
            s += "{} {}\n".format(trait, self.genes[trait])
        return s[:-2]

    def generateDNARandom(self, trait):
        DNA = []
        info = self.structure[trait]
        for i in range(0, info["start_length"]):
            if "start_zero" in info and info["start_zero"] is True:
                DNA.append(0)
            else:
                DNA.append(randint(info["min"], info["max"]))
        return DNA

    def generateDNAFromParents(self, trait, parents):
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

    def generateGenesRandom(self):
        genes = {}
        for trait in self.structure:
            DNA = self.generateDNARandom(trait)
            info = self.structure[trait]
            genes[trait] = Gene(trait, DNA, info["min_length"], info["min"], info["max"], info["mutationMagnitude"])
        return genes

    def generateGenesFromParents(self, parents):
        genes = {}
        traitsDict = {}
        for parent in parents:
            for trait in parent.genes:
                traitsDict[trait] = True
        traits = list(traitsDict.keys())
        for trait in traits:
            DNA = Genome.GenerateDNAFromParents(trait, parents)
            info = self.structure[trait]
            genes[trait] = Gene(trait, DNA, info["min_length"], info["min"], info["max"], info["mutationMagnitude"])
        return genes           

    def generateGenes(self, parents):
        if parents is not None and len(parents) > 0:
            self.genes = self.generateGenesFromParents(parents)
        else:
            self.genes = self.generateGenesRandom()

    def mutateGenes(self):
        for trait in self.genes:
            self.genes[trait].mutate()

    def compare(other):
        return Chromosome.CompareGenes(self.genes, other.genes)

    @staticmethod
    def CompareGenes(a_genes, b_genes):
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

    def __init__(self, parents, structure):
        self.structure = structure
        self.generateGenes(parents)
        #self.mutateGenes()

    #def __getitem__(self, trait):
    #    return self.genes[trait]

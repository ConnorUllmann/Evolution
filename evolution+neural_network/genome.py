from random import random, randint, shuffle
from json import *

class Genome:

    def __str__(self):
        s = ""
        for trait in self.structure:
            s += "Trait={}; Value={}; Rules={}\n".format(trait, self.genes[trait], self.structure[trait])
        return s

    def generateDNARandom(self, trait):
        DNA = []
        info = self.structure[trait]
        startLength = info["start_length"]
        if isinstance(startLength, list):
            length = randint(startLength[0], startLength[1])
        else:
            length = startLength
        for i in range(length):
            if "start_zero" in info and info["start_zero"] is True:
                DNA.append(0)
            else:
                DNA.append(randint(info["min"], info["max"]))
        return DNA

    def generateDNAFromParents(self, trait, parents):
        shuffle(parents)
        DNA = []
        for i in range(0, len(parents[0].genome.genes[trait])):
            sumValue = 0
            counted = 0
            for parent in parents:
                if 0 <= i < len(parent.genome.genes[trait]):
                    sumValue += parent.genome.genes[trait][i]
                    counted += 1
            DNA.append(0 if counted == 0 else round(sumValue / counted))

        v = random()
        if v > 0.9:
            DNA.insert(int(random() * len(DNA)), randint(self.structure[trait]["min"], self.structure[trait]["max"]))
        if v < 0.1 and len(DNA) > self.structure[trait]["min_length"]:
            DNA.pop(int(random() * len(DNA)))

        return DNA

    def generateGenesRandom(self):
        genes = {}
        for trait in self.structure:
            genes[trait] = self.generateDNARandom(trait)
        return genes

    def generateGenesFromParents(self, parents):
        genes = {}
        traitsDict = {}
        for parent in parents:
            for trait in parent.genome.genes:
                traitsDict[trait] = True
        traits = list(traitsDict.keys())
        for trait in traits:
            genes[trait] = self.generateDNAFromParents(trait, parents)
        return genes           

    def generateGenes(self, parents):
        if parents is not None and len(parents) > 0:
            self.genes = self.generateGenesFromParents(parents)
        else:
            self.genes = self.generateGenesRandom()

    def mutateGenes(self, mutationChancePerBase=0.2):
        for trait in self.genes:
            gene = self.genes[trait]
            for i in range(len(gene)):
                if random() < mutationChancePerBase:
                    gene[i] = min(max(int(gene[i] + (random() - 0.5) * 2 * self.structure[trait]["mutationMagnitude"]), self.structure[trait]["min"]), self.structure[trait]["max"])

    def compare(self, other):
        return Genome.CompareGenes(self.genes, other.genes)

    @staticmethod
    def CompareGenes(a_genes, b_genes):
        same = 0
        diff = 0
        for trait in a_genes:
            if trait in b_genes:
                aLenDNA = len(a_genes[trait])
                bLenDNA = len(b_genes[trait])
                maxLen = max(aLenDNA, bLenDNA)
                minLen = min(aLenDNA, bLenDNA)
                diff += maxLen - minLen
                for i in range(0, minLen):
                    if a_genes[trait][i] == b_genes[trait][i]:
                        same += 1
                    else:
                        diff += 1
            else:
                diff += len(a_genes[trait])
        for trait in b_genes:
            if trait not in a_genes:
                diff += len(b_genes[trait])
        return same / (same + diff)

    def save(self, filename):
        with open(filename+"-Genes.txt", "w") as output:
            output.write(dumps(self.genes))
        with open(filename+"-Structure.txt", "w") as output:
            output.write(dumps(self.structure))


    @staticmethod
    def Load(filename):
        genes = {}
        structure = {}
        with open(filename+"-Genes.txt", "r") as input:
            genes = loads(input.read())
        with open(filename+"-Structure.txt", "r") as input:
            structure = loads(input.read())
        return Genome(structure, genes=genes)

    def __init__(self, structure, parents=None, genes=None):
        self.structure = structure
        if genes is not None:
            self.genes = genes
        else:
            self.generateGenes(parents)
        self.mutateGenes()

    #def __getitem__(self, trait):
    #    return self.genes[trait]

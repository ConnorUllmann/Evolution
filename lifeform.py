from random import random, randint, shuffle
from gene import Gene

class Lifeform:

    DNA_LENGTH = 10

    BASE_TRAITS = [
        "size",
        "speed",
        "turnspeed",
        "acceleration"
    ]

    @staticmethod
    def GenerateDNARandom():
        DNA = ""
        for i in range(0, Lifeform.DNA_LENGTH):
            DNA = "{0}{1}".format(DNA, int(round(random())))
        return DNA

    @staticmethod
    def GenerateDNAFromParents(parents):
        shuffle(parents)
        DNA = ""
        parentIndex = 0
        for i in range(0, len(parents[0].DNA)):
            while i >= len(parents[parentIndex].DNA):
                parentIndex = (parentIndex + 1) % len(parents)
            bit = parents[parentIndex].DNA[i]
            parentIndex = (parentIndex + 1) % len(parents)
            DNA = "{0}{1}".format(DNA, int(bit))
        return DNA

    @staticmethod
    def GenerateDNA(parents):
        if parents is not None and len(parents) > 0:
            return Lifeform.GenerateDNAFromParents(parents)
        else:
            return Lifeform.GenerateDNARandom()

    @staticmethod
    def GenerateGenesRandom(DNA):
        genes = {}
        for trait in Lifeform.BASE_TRAITS:
            genes[trait] = Gene(DNA)
        return genes

    @staticmethod
    def GenerateTraitsFromParents(parents):
        traits = {}
        for parent in parents:
            for trait in parent.genes:
                traits[trait] = True
        return list(traits.keys())

    @staticmethod
    def GenerateBasesForTraitFromParents(trait, parents):
        basesReturn = []
        parentsWithTrait = []
        for parent in parents:
            if trait in parent.genes:
                parentsWithTrait.append(parent)

        baseCountBounds = [None, None]
        for parent in parentsWithTrait:
            parentBaseCount = len(parent.genes[trait].bases)
            if baseCountBounds[0] is None or parentBaseCount < baseCountBounds[0]:
                baseCountBounds[0] = parentBaseCount
            if baseCountBounds[1] is None or parentBaseCount > baseCountBounds[1]:
                baseCountBounds[1] = parentBaseCount
        baseCountBounds[0] = max(baseCountBounds[0] - 1, Gene.MIN_GENE_LENGTH)
        baseCountBounds[1] = min(baseCountBounds[1] + 1, Gene.MAX_GENE_LENGTH)

        baseCount = randint(baseCountBounds[0], baseCountBounds[1])

        bases = {}
        for parent in parentsWithTrait:
            for base in parent.genes[trait].bases:
                bases[base] = True
        basesList = list(bases.keys())
        shuffle(basesList)

        for i in range(0, min(baseCount, len(basesList))):
            basesReturn.append(basesList[i])
        return basesReturn

    @staticmethod
    def GenerateGenesFromParents(DNA, parents):
        genes = {}
        traits = Lifeform.GenerateTraitsFromParents(parents)
        for trait in traits:
            bases = Lifeform.GenerateBasesForTraitFromParents(trait, parents)
            genes[trait] = Gene(DNA, bases)
        return genes
            

    @staticmethod
    def GenerateGenes(DNA, parents):
        if parents is not None and len(parents) > 0:
            return Lifeform.GenerateGenesFromParents(DNA, parents)
        else:
            return Lifeform.GenerateGenesRandom(DNA)

    def __init__(self, parents):
        self.DNA = Lifeform.GenerateDNA(parents)
        self.genes = Lifeform.GenerateGenes(self.DNA, parents)

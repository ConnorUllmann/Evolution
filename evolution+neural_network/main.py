from training_set import TrainingSet
from brain import Brain
from thread_handler import ThreadHandler
from utils import *
from random import choice, random
from datetime import datetime

from body import Body
from screen import Screen
from neural_network import NeuralNetwork

        
def AddBrainToCheckQueue(brain):
    BestBrainsCheckQueue.append(brain)
    
def IsBestBrain(brain):
    if len(BestScoringBrains) <= 0:
        BestScoringBrains.append(brain)
        return True

    isBestBrain = False
    inserted = False
    for i in range(len(BestScoringBrains)-1, -1, -1):
        if brain.score >= BestScoringBrains[i].score:
            if i == 0:
                BestScoringBrains.insert(0, brain)
                isBestBrain = True
                inserted = True
                break
            continue
        if i+1 >= len(BestScoringBrains):
            BestScoringBrains.append(brain)
        else:
            BestScoringBrains.insert(i+1, brain)
        inserted = True
        break
    
    if not inserted:
        BestScoringBrains.append(brain)

    while len(BestScoringBrains) > nBestScoringBrains:
        BestScoringBrains.pop()
    return isBestBrain

def UpdateBestBrainCheckQueue():
    timeStart = datetime.now()
    while True:
        if len(BestBrainsCheckQueue) > 0:
            brain = BestBrainsCheckQueue.pop(0)
            if IsBestBrain(brain):
                print("[{}] Best score: {}% ({})\n{}\n".format(brain.id, int(brain.score*1000)/10, datetime.now() - timeStart, brain))
                brain.save("BestScoringBrain")

def NextGeneration(parents, trainingSet):
    brain = Brain(parents)
    brain.trainingSet = trainingSet
    brain.train(0.1)
    brain.test()
    AddBrainToCheckQueue(brain)
    if len(BestScoringBrains) > 0:
        index = int(random() * len(BestScoringBrains))
        count = len(BestScoringBrains)
        while count > 0:
            if brain.canMate(BestScoringBrains[index]):
                return [brain, BestScoringBrains[index]]
            else:
                index = (index + 1) % len(BestScoringBrains)
                count -= 1
    if len(BestScoringBrains) > 0:
        brainRandom = choice(BestScoringBrains)
        for brainTemp in BestScoringBrains:
            if brainRandom.canMate(brainTemp):
                return [brainRandom, brainTemp]
    return [brain]

def EvolveBrains(trainingSet):
    parents = []
    while True:
        parents = NextGeneration(parents, trainingSet)

def ShowBestBrain():
    brain = Brain.Load("BestScoringBrain")
    print(brain)
    trainingSet = TrainingSet(10, 1, Opp)
    brain.trainingSet = trainingSet
    print("\nSCORE: {}%".format(int(brain.test()*1000)/10))

def Simulate():
    trainingSet = TrainingSet(6, 4, Add)
    Brain.StartRecordingScores()
    threadHandler = ThreadHandler()
    threadHandler.AddThread(UpdateBestBrainCheckQueue, threadName="BrainQueue")
    for i in range(5):
        threadHandler.AddThread(EvolveBrains, [trainingSet], threadName="EvolveBrains")
    print("All threads are starting...")
    threadHandler.RunAllThreads()

def SimulateOneBrain():
    trainingSet = TrainingSet(12, 7, Add)
    Brain.StartRecordingScores()
    threadHandler = ThreadHandler()
    threadHandler.AddThread(UpdateBestBrainCheckQueue, threadName="BrainQueue")
    threadHandler.RunAllThreads()
    EvolveBrains(trainingSet)

def Run():
    screen = Screen(1600, 1000)
    screen.Start()
    
    Brain.StartRecordingScores()
    trainingSet = TrainingSet(6, 4, Add)
    brain = Brain([], neuralNetwork=NeuralNetwork([6, 8, 4]))
    brain.trainingSet = trainingSet

    m = 50
    body = Body(brain, m, screen.height / 2, screen.height - m * 2, screen.width - m * 2)
    brain.genome.genes["iterations"] = [10]
    brain.genome.genes["batch_size"] = [10000]
    while True:
        brain.test()
        brain.neuralNetwork.save("BestScoringBrain-NeuralNetwork")
        with open("BestScoringBrain-Scores.txt", "a") as output:
            output.write("{}\n".format(brain.score))
        if brain.score >= 1:
            print("Done!")
            break
        brain.train(0.5)

if __name__ == "__main__":
    BestBrainsCheckQueue = []
    nBestScoringBrains = 5
    BestScoringBrains = []

    #Run()

    #Simulate()
    Run()
    
    #SimulateOneBrain()
    #ShowBestBrain()


import numpy as np
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, geneticTable=None, totalReward=0):
        if geneticTable != None:
            self.geneticTable = geneticTable
        else:
            self.probs = np.random.random_sample(5) * 100
            self.geneticTable = {'_':self.probs[0], 'CD':self.probs[1], 'DC':self.probs[2], 'CC':self.probs[3],\
                'DD':self.probs[4]}

        self.totalReward = totalReward

class EvolutionSimulator:
    
    def __init__(self, totalGenerations = 100, maxMutationSize=5, populationSize=50, totalGames=50,\
        numOfSurvivors=5 , mutationSD=10, rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, agents=None):
    
        self.totalGenerations = totalGenerations
        self.maxMutationSize = maxMutationSize
        self.populationSize = populationSize
        self.totalGames = totalGames
        self.numOfSurvivors = numOfSurvivors
        self.mutationSD = mutationSD


        self.rewardsLookup = {'CD':rewardCD, 'DC':rewardDC, 'CC':rewardCC, 'DD':rewardDD}

        self.stateCount = {'DC':0,'CC':0,'DD':0}

        if agents == None:
            self.agents = []
            for i in range(populationSize):
                self.agents.append(Agent())
        else:
            self.agents = agents
        
        # stateIndexLookup = {'CD':0, 'DC':1, 'CC':2, 'DD':3, '_':4}

        # CCCounts = np.zeros(totalGenerations)
        # averageCCCoopProbs = np.zeros(totalGenerations)

    def repopulate(self):
        # Sort by score
        self.agents.sort(reverse=True, key=lambda x:x.totalReward)

        for agent in self.agents:
            agent.totalReward = 0

        for i in range(self.populationSize-self.numOfSurvivors):
            parents = np.random.choice(self.numOfSurvivors,2,False)

            childProbs = self.crossover(self.agents[parents[0]], self.agents[parents[1]])
            childGeneticTable = self.mutate(childProbs)

            self.agents[self.numOfSurvivors + i].geneticTable = childGeneticTable
    

    def crossover(self, parent1, parent2):
        childProbs = np.zeros(5) 
        for i in range(5):
        # perform uniform crossover
            sample = np.random.choice(1)
            if sample == 1:
                childProbs[i] = list(parent1.geneticTable.values())[i]
            else:
                childProbs[i] = list(parent2.geneticTable.values())[i]

        return childProbs

    def mutate(self, childProbs):
        probs = childProbs
        for i in range(5):
            prob = np.random.normal(childProbs[i], self.mutationSD)
            if prob > 100:
                prob = 100
            elif prob < 0:
                prob = 0
        
            probs[i] = prob

        childGeneticTable = {'_':probs[0], 'CD':probs[1], 'DC':probs[2], 'CC':probs[3],\
            'DD':probs[4]}
        
        return childGeneticTable

    def select_action(self, agentIndex, priorState):
        probCoop = self.agents[agentIndex].geneticTable[priorState]
        
        if  np.random.uniform()*100 <= probCoop:
            return 'C'
        else:
            return 'D'

    def reset_measurements(self):
        self.stateCount = {'DC':0,'CC':0,'DD':0}

    def run_simulation(self):
        for agent1 in range(self.populationSize):
            for agent2 in range(agent1+1,self.populationSize):
                priorState = '_'
                for g in range(self.totalGames):
                    agent1Action = self.select_action(agent1, priorState)
                    agent2Action = self.select_action(agent2, priorState[::-1])
                
                    newState = agent1Action + agent2Action
                
                    self.agents[agent1].totalReward += self.rewardsLookup[newState]
                    self.agents[agent2].totalReward += self.rewardsLookup[newState[-1::-1]]
                    

                if newState == 'CD':
                    self.stateCount['DC'] += 1
                else:
                    self.stateCount[newState] += 1
        
                priorState = newState
            
            self.agentTable = self.repopulate()


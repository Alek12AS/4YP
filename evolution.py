from q_learning import Agent
from random import choice
import numpy as np
import matplotlib.pyplot as plt


class EvolutionSimulator:
    
    def __init__(self, totalGenerations = 100, totalAgents=100, gameIts=100,\
        survivalRate=0.05 , mutationSD=5, rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, agents=None):
    
        self.totalGenerations = totalGenerations
        
        if agents == None:
            self.totalAgents = totalAgents
        else:
            self.totalAgents = len(agents)

        
        self.gameIts = gameIts

        
        self.numOfSurvivors = int(round(self.totalAgents*survivalRate))
        if self.numOfSurvivors < 2:
            self.numOfSurvivors = 2

        self.mutationSD = mutationSD

        self.rewardsLookup = {'CD':rewardCD, 'DC':rewardDC, 'CC':rewardCC, 'DD':rewardDD}

        self.stateCount = {'DC':0,'CC':0,'DD':0}

        if agents == None:
            self.agents = []
            self.create_agents()
        else:
            self.agents = agents
        
        # stateIndexLookup = {'CD':0, 'DC':1, 'CC':2, 'DD':3, '_':4}

        # CCCounts = np.zeros(totalGenerations)
        # averageCCCoopProbs = np.zeros(totalGenerations)

    def create_agents(self):
        for i in range(self.totalAgents):
            randVals = np.random.random_sample(10) * 100

            lookupTable = {'D': {'CC': randVals[0], 'CD': randVals[1], 'DC': randVals[2], 'DD': randVals[3], '_': randVals[4]},
                    'C': {'CC': randVals[5], 'CD': randVals[6], 'DC': randVals[7], 'DD': randVals[8], '_': randVals[9]}}
            
            self.agents.append(Agent(lookupTable=lookupTable))

    def repopulate(self):
        # Sort by score
        self.agents.sort(reverse=True, key=lambda x:x.totalReward)

        parentTables = []
        for i in range(self.numOfSurvivors):
            parentTables.append(self.agents[i].lookupTable.copy())

        for agent in self.agents:
            agent.totalReward = 0

        for i in range(self.totalAgents):
            randIndices = np.random.choice(self.numOfSurvivors,2,False)

            childlookupTable = self.crossover(parentTables[randIndices[0]], parentTables[randIndices[1]])
            self.mutate(childlookupTable)

            self.agents[i].lookupTable = childlookupTable
    

    def crossover(self, parentTable1, parentTable2):
        childlookupTable = {'D': {'CC': 0, 'CD': 0, 'DC': 0, 'DD': 0, '_': 0},\
                    'C': {'CC': 0, 'CD': 0, 'DC': 0, 'DD': 0, '_': 0}}
        
        for action in childlookupTable:
            for state in childlookupTable[action]:
                sample = np.random.choice(2)
                if sample == 1:
                    childlookupTable[action][state] = parentTable1[action][state]
                else:
                    childlookupTable[action][state] = parentTable2[action][state]

        return childlookupTable

    def mutate(self, childlookupTable):
        for action in childlookupTable:
            for state in childlookupTable[action]:
                param = np.random.normal(childlookupTable[action][state], self.mutationSD)
                if param < 0:
                    param = 0
                childlookupTable[action][state] = param

    def select_action(self, agentIndex, priorState):

        coopVal = self.agents[agentIndex].lookupTable['C'][priorState]
        defVal = self.agents[agentIndex].lookupTable['D'][priorState]
        if coopVal+defVal == 0:
            probCoop = 0.5
        else:
            probCoop = coopVal/(coopVal+defVal)
            
        sample = np.random.random_sample()

        if sample <= probCoop:
            return 'C'
        else:
            return 'D'

    def reset_measurements(self):
        self.stateCount = {'DC':0,'CC':0,'DD':0}

    def run_simulation(self):
        for agent1 in range(self.totalAgents):
            for agent2 in range(agent1+1,self.totalAgents):
                priorState = '_'
                for i in range(self.gameIts):
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
            


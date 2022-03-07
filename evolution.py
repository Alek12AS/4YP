from q_learning import Agent
from random import choice
import numpy as np
import matplotlib.pyplot as plt


class EvolutionSimulator:
    
    def __init__(self, totalGenerations = 100, totalAgents=100, gameIts=100,\
        numOfSurvivors=5 , mutationSD=5, rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, agents=None):
    
        self.totalGenerations = totalGenerations
        
        if agents == None:
            self.totalAgents = totalAgents
        else:
            self.totalAgents = len(agents)

        self.gameIts = gameIts
        self.numOfSurvivors = numOfSurvivors
        self.mutationSD = mutationSD


        self.rewardsLookup = {'CD':rewardCD, 'DC':rewardDC, 'CC':rewardCC, 'DD':rewardDD}

        self.stateCount = {'DC':0,'CC':0,'DD':0}

        if agents == None:
            self.create_agents()
        else:
            self.agents = agents
        
        # stateIndexLookup = {'CD':0, 'DC':1, 'CC':2, 'DD':3, '_':4}

        # CCCounts = np.zeros(totalGenerations)
        # averageCCCoopProbs = np.zeros(totalGenerations)

    def create_agents(self):
        self.agents = []
        for i in range(self.totalAgents):
            randVals = np.random.random_sample(10) * 100

            lookupTable = {'D': {'CC': randVals[0], 'CD': randVals[1], 'DC': randVals[2], 'DD': randVals[3], '_': randVals[4]},
                    'C': {'CC': randVals[5], 'CD': randVals[6], 'DC': randVals[7], 'DD': randVals[8], '_': randVals[9]}}
            
            self.agents.append(Agent(lookupTable=lookupTable, epsilon=self.epsilon0))

    def repopulate(self):
        # Sort by score
        self.agents.sort(reverse=True, key=lambda x:x.totalReward)

        for agent in self.agents:
            agent.totalReward = 0

        for i in range(self.totalAgents-self.numOfSurvivors):
            parents = np.random.choice(self.numOfSurvivors,2,False)

            childlookupTable = self.crossover(self.agents[parents[0]], self.agents[parents[1]])
            childlookupTable = self.mutate(childlookupTable)

            self.agents[self.numOfSurvivors + i].lookupTable = childlookupTable
    

    def crossover(self, parent1, parent2):
        childlookupTable = parent1.lookupTable
        
        for action in childlookupTable:
            for state in childlookupTable[action]:
                sample = np.random.choice(2)
                print(sample)
                if sample == 1:
                    childlookupTable[action][state] = parent2.lookupTable[action][state]

        return childlookupTable

    def mutate(self, childlookupTable):

        for action in childlookupTable:
            for state in childlookupTable[action]:
                param = np.random.normal(childlookupTable[action][state], self.mutationSD)
                childlookupTable[action][state] = param
        
        
        return childlookupTable

    def select_action(self, agentIndex, priorState):

        if self.agents[agentIndex]['C'][priorState] >= self.agents[agentIndex]['D'][priorState]:
            return 'C'
        else:
            return 'D'

    def reset_measurements(self):
        self.stateCount = {'DC':0,'CC':0,'DD':0}

    def run_simulation(self):
        for agent1 in range(self.totalAgents):
            for agent2 in range(agent1+1,self.totalAgents):
                priorState = '_'
                for g in range(self.gameIts):
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


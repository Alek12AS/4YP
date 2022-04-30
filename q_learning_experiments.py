from unicodedata import decomposition
import numpy as np
from evolution_experiments import EvolutionExperiments
from q_learning import QLearningSimulator


class QLearningExperiments(EvolutionExperiments):

    def __init__(self, totalGenerations=100, totalAgents=100, gamma=0.99, alpha=0.1, gameIts=10, epsilon0=0.5,\
    epsilonDecay=0.9999,rewardCD=0, rewardDC=0, rewardCC=0.3, rewardDD=0, agents=None, param='Population Size',\
    paramVals=None, repetitions=1):

        self.totalGenerations = totalGenerations
        self.totalAgents = totalAgents
        self.gamma = gamma
        self.alpha = alpha
        self.gameIts = gameIts
        self.epsilon0 = epsilon0
        self.epsilonDecay = epsilonDecay
        self.rewardCD= rewardCD
        self.rewardDC= rewardDC
        self.rewardCC= rewardCC
        self.rewardDD= rewardDD
        self.agents = agents
        self.param = param
        self.paramVals = paramVals
        self.repetitions = repetitions
        
        self.simulations = []
        
        self.initialise_simulations()

    def initialise_simulations(self):
        if self.param == 'Gamma':
            for g in self.paramVals:
                self.simulations.append(QLearningSimulator(self.totalAgents, g, self.alpha, self.gameIts,\
                    self.epsilon0, self.epsilonDecay,self.rewardCD, self.rewardDC, self.rewardCC,\
                    self.rewardDD, self.agents))
        elif self.param == 'Alpha':
            for a in self.paramVals:
                self.simulations.append(QLearningSimulator(self.totalAgents, self.gamma, a, self.gameIts,\
                    self.epsilon0, self.epsilonDecay,self.rewardCD, self.rewardDC, self.rewardCC,\
                    self.rewardDD, self.agents))
        elif self.param == 'Population Size':
            for popSize in self.paramVals:
                self.simulations.append(QLearningSimulator(popSize, self.gamma, self.alpha, self.gameIts,\
                    self.epsilon0, self.epsilonDecay,self.rewardCD, self.rewardDC, self.rewardCC,\
                    self.rewardDD, self.agents))
        elif self.param == 'Iterations Per Game':
            for its in self.paramVals:
                self.simulations.append(QLearningSimulator(self.totalAgents, self.gamma, self.alpha, its,\
                    self.epsilon0, self.epsilonDecay,self.rewardCD, self.rewardDC, self.rewardCC,\
                    self.rewardDD, self.agents))
        

    
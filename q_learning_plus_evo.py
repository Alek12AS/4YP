import numpy as np
from evolution import EvolutionSimulator
from q_learning import QLearningSimulator


class QLearnPlusEvoSimulator(QLearningSimulator, EvolutionSimulator):

    def __init__(self, totalAgents=100, gamma=0.99, alpha=0.1, gameIts=100, epsilon0=0.25,\
        epsilonDecay=0.9999,rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, survivalRate=0.05,\
             mutationSD=2.5, agents=None):

        QLearningSimulator.__init__(self, totalAgents, gamma, alpha, gameIts, epsilon0,\
        epsilonDecay,rewardCD, rewardDC, rewardCC, rewardDD, agents)
        
        self.numOfSurvivors = int(round(self.totalAgents*survivalRate))
        if self.numOfSurvivors < 2:
            self.numOfSurvivors = 2

        self.mutationSD = mutationSD
    
    def repopulate(self):
        EvolutionSimulator.repopulate(self)
        
    def run_simulation(self):
        QLearningSimulator.run_simulation(self)

  
import numpy as np
from evolution import EvolutionSimulator
from q_learning import QLearningSimulator


class QLearnPlusEvoSimulator():

    def __init__(self, totalAgents=100, gamma=0.99, alpha=0.1, gameIts=100, epsilon0=0.25,\
        epsilonDecay=0.9999,rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, agents=None,\
            numOfSurvivors=5 , mutationSD=5):
        
        self.QlearningSim = QLearningSimulator(totalAgents, gamma, alpha, gameIts, epsilon0, epsilonDecay, rewardCD,\
            rewardDC, rewardCC, rewardDD)
        
        self.evoSim = EvolutionSimulator(numOfSurvivors=numOfSurvivors, mutationSD=mutationSD,\
            agents=agents)

    def run_simulation(self):
        self.QlearningSim.run_simulation()
        self.evoSim.agents = self.QlearningSim.agents
        self.evoSim.repopulate()
        self.QlearningSim.agents = self.evoSim.agents


  
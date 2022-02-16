import numpy as np
from q_learning import QLearningSimulator

class QLearningExperiments:

    def __init__(self, totalAgents=100, gamma=0.99, alpha=0.1, gameIts=100, epsilon0=0.25,\
    epsilonDecay=0.9999,rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, agents=None, param='gamma',\
    paramVals=None, numTrainingTours=1):

        simulations = []

        if param == 'gamma':
            for g in range(paramVals):
                simulations.append(QLearningSimulator(totalAgents=totalAgents, gamma=g, alpha=alpha, gameIts=gameIts,\
                     epsilon0=epsilon0,epsilonDecay=epsilonDecay,rewardCD=rewardCD, rewardDC=rewardDC, rewardCC=rewardCC,\
                     rewardDD=rewardDD, agents=agents))
        elif param == 'alpha':
            for a in range(paramVals):
                simulations.append(QLearningSimulator(totalAgents=totalAgents, gamma=gamma, alpha=a, gameIts=gameIts,\
                     epsilon0=epsilon0,epsilonDecay=epsilonDecay,rewardCD=rewardCD, rewardDC=rewardDC, rewardCC=rewardCC,\
                     rewardDD=rewardDD, agents=agents))
        elif param == 'population size':
            for popSize in range(paramVals):
                simulations.append(QLearningSimulator(totalAgents=popSize, gamma=gamma, alpha=alpha, gameIts=gameIts,\
                     epsilon0=epsilon0,epsilonDecay=epsilonDecay,rewardCD=rewardCD, rewardDC=rewardDC, rewardCC=rewardCC,\
                     rewardDD=rewardDD, agents=agents))
        elif param == 'iterations per game':
            for its in range(paramVals):
                simulations.append(QLearningSimulator(totalAgents=totalAgents, gamma=gamma, alpha=alpha, gameIts=its,\
                     epsilon0=epsilon0,epsilonDecay=epsilonDecay,rewardCD=rewardCD, rewardDC=rewardDC, rewardCC=rewardCC,\
                     rewardDD=rewardDD, agents=agents))
        

        self.numTrainingTours = numTrainingTours

        

    def train_populations():
        pass
        

    
        
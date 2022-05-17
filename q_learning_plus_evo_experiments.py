from evolution_experiments import EvolutionExperiments
from q_learning_plus_evo import QLearnPlusEvoSimulator

class QLearningPlusEvolutionExperiments(EvolutionExperiments):
    
    def __init__(self, totalGenerations=100, param='Population_Size', paramVals=None, repetitions=1,\
         populationSize=100, gamma=0.99, alpha=0.1, gameIts=10, epsilon0=0.5, epsilonDecay=0.9999,\
             rewardCD=0, rewardDC=0, rewardCC=0.3, rewardDD=0, survivalRate=0.05, mutationSD=2.5,\
                 agents=None):

        self.gamma = gamma
        self.alpha = alpha
        self.epsilon0 = epsilon0
        self.epsilonDecay = epsilonDecay

        EvolutionExperiments.__init__(self, totalGenerations, populationSize, gameIts,\
        survivalRate, mutationSD, rewardCD, rewardDC, rewardCC, rewardDD,\
             param, paramVals, repetitions, agents)

    
    def initialise_simulations(self):
        if self.param == 'Population_Size':
            for popSize in self.paramVals:
                self.simulations.append(QLearnPlusEvoSimulator(popSize, self.gamma, self.alpha,\
                     self.gameIterations, self.epsilon0, self.epsilonDecay, self.rewardCD, self.rewardDC, self.rewardCC,\
                          self.rewardDD, self.survivalRate, self.mutationSD, self.agents))
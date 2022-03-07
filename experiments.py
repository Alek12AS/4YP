from re import A
import numpy as np
from q_learning import QLearningSimulator
import matplotlib.pyplot as plt

class QLearningExperiments:

    def __init__(self, totalAgents=100, gamma=0.99, alpha=0.1, gameIts=100, epsilon0=0.25,\
    epsilonDecay=0.9998,rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, agents=None, param='Gamma',\
    paramVals=None, repetitions=1):

        self.paramVals = paramVals
        self.param = param
        self.repetitions = repetitions

    
        self.simulations = [[]]*repetitions

        if param == 'Gamma':
            for i in range(repetitions):
                for g in paramVals:
                    self.simulations[i].append(QLearningSimulator(totalAgents=totalAgents, gamma=g, alpha=alpha, gameIts=gameIts,\
                        epsilon0=epsilon0,epsilonDecay=epsilonDecay,rewardCD=rewardCD, rewardDC=rewardDC, rewardCC=rewardCC,\
                        rewardDD=rewardDD, agents=agents))
        elif param == 'Alpha':
            for i in range(repetitions):
                for a in paramVals:
                    self.simulations[i].append(QLearningSimulator(totalAgents=totalAgents, gamma=gamma, alpha=a, gameIts=gameIts,\
                        epsilon0=epsilon0,epsilonDecay=epsilonDecay,rewardCD=rewardCD, rewardDC=rewardDC, rewardCC=rewardCC,\
                        rewardDD=rewardDD, agents=agents))
        elif param == 'Population Size':
            for i in range(repetitions):
                for popSize in paramVals:
                    self.simulations[i].append(QLearningSimulator(totalAgents=popSize, gamma=gamma, alpha=alpha, gameIts=gameIts,\
                        epsilon0=epsilon0,epsilonDecay=epsilonDecay,rewardCD=rewardCD, rewardDC=rewardDC, rewardCC=rewardCC,\
                        rewardDD=rewardDD, agents=agents))
        elif param == 'Iterations Per Game':
            for i in range(repetitions):
                for its in paramVals:
                    self.simulations[i].append(QLearningSimulator(totalAgents=totalAgents, gamma=gamma, alpha=alpha, gameIts=its,\
                        epsilon0=epsilon0,epsilonDecay=epsilonDecay,rewardCD=rewardCD, rewardDC=rewardDC, rewardCC=rewardCC,\
                        rewardDD=rewardDD, agents=agents))
        

        self.stateCounts = {'DC':[[]]*repetitions,'CC':[[]]*repetitions,'DD':[[]]*repetitions}
        self.numTit4Tat = [[]]*self.repetitions
        self.numCooperators = [[]]*self.repetitions
        self.numDefectors = [[]]*self.repetitions
        

    def train_populations(self, maxTourns=10, threshMeanTDE=0.01):
        for i in range(self.repetitions):
            for sim in self.simulations[i]:
                tourn = 0
                meanTDE = threshMeanTDE*2 
                while tourn < maxTourns and meanTDE > threshMeanTDE:
                    sim.run_simulation()
                    meanTDEs = sim.get_mean_TDEs()
                    meanTDE = np.mean(meanTDEs[-500])
                    tourn += 1

    def strat_classifier(self, LT):
        if LT['C']['CC'] > LT['D']['CC'] and LT['C']['CD'] > LT['D']['CD']\
             and LT['C']['DC'] > LT['D']['DC'] and LT['C']['DD'] > LT['D']['DD']\
                  and LT['C']['_'] > LT['D']['_']:
            return 'cooperator'

        elif LT['C']['CC'] < LT['D']['CC'] and LT['C']['CD'] < LT['D']['CD']\
             and LT['C']['DC'] < LT['D']['DC'] and LT['C']['DD'] < LT['D']['DD']\
                 and LT['C']['_'] < LT['D']['_']:
            return 'defector'
        
        elif LT['C']['CC'] > LT['D']['CC'] and LT['C']['CD'] < LT['D']['CD']\
            and LT['C']['DC'] > LT['D']['DC'] and LT['C']['DD'] < LT['D']['DD']\
                and LT['C']['_'] > LT['D']['_']:
            return 'tit4tat'

        
        
    def obtain_results(self):
        for i in range(self.repetitions):
            for sim in self.simulations[i]:
                sim.reset_measurements()
                sim.run_simulation()
                self.stateCounts['DC'][i].append(sim.stateCount['DC'])
                self.stateCounts['CC'][i].append(sim.stateCount['CC'])
                self.stateCounts['DD'][i].append(sim.stateCount['DD'])

                for agent in sim.agents:
                    classif = self.strat_classifier(agent.lookupTable)
                    if classif == 'cooperator':
                        self.numCooperators[i] += 1
                    elif classif == 'defector':
                        self.numDefectors[i] += 1
                    elif classif == 'tit4tat':
                        self.numTit4Tat[i] += 1
                    
    def output_results(self):
        meanCountsDC = np.mean(np.array(self.stateCounts['DC']),0)
        meanCountsCC = np.mean(np.array(self.stateCounts['CC']),0)
        meanCountsDD = np.mean(np.array(self.stateCounts['DD']),0)
        meanNumCooperators = np.mean(np.array(self.numCooperators),0)
        meanNumDefectors = np.mean(np.array(self.numDefectors),0)
        meanNumTit4Tat = np.mean(np.array(self.numTit4Tat),0)

        for val in self.paramVals:
            print(val, end=' ')
        print(' ')
        for n in meanCountsDC:
            print(n, end=' ')
        print('')
        for n in meanCountsCC:
            print(n, end=' ')
        print('')
        for n in meanCountsDD:
            print(n, end=' ')


    
    # def disp_TDEs(self):
    #     for i in range(len(self.paramVals)):
    #         sim = self.simulations[i]
    #         meanTDEs = sim.get_mean_TDEs('C', 'CC')
    #         plt.plot([i for i in range(sim.agents[0].its)], meanTDEs)
    #         plt.xlabel('Iteration')
    #         plt.ylabel('Mean TDE')
    #         plt.title('Mean TDE for CC-C of agents over IPD Iterations (param = {0})'\
    #             .format(self.paramVals[i]))

    #         plt.show()


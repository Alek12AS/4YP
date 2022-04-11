from q_learning_plus_evo import QLearnPlusEvoSimulator

class EvolutionExperiments:

    def __init__(self, totalGenerations, param='Population Size', paramVals=None, repetitions=1,\
         populationSize=100, gamma=0.99, alpha=0.1, gameIts=100, epsilon0=0.25, epsilonDecay=0.9999,\
             rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, survivalRate=0.05, mutationSD=2.5,\
                 agents=None):

        self.totalGenerations = totalGenerations
        self.populationSize = populationSize

        self.paramVals = paramVals
        self.param = param
        self.repetitions = repetitions

        self.simulations = []
        
        if param == 'Population Size':
            for popSize in paramVals:
                self.simulations.append(EvolutionExperiments(popSize, gamma, alpha, gameIts, epsilon0,\
                epsilonDecay, rewardCD, rewardDC, rewardCC, rewardDD, survivalRate, mutationSD,\
                     agents))
        
        numParams = len(self.paramVals)

        self.stateCounts = {'DC':[[0]*totalGenerations]*numParams,'CC':[[0]*totalGenerations]*numParams,\
            'DD':[[0]*totalGenerations]*numParams}
        self.numTit4Tat = [[0]*totalGenerations]*numParams
        self.numCooperators = [[0]*totalGenerations]*numParams
        self.numDefectors = [[0]*totalGenerations]*numParams
        


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
        for i in range(len(self.paramVals)):
            for genNum in range(self.totalGenerations):
                self.simulations[i].reset_measurements()
                self.simulations[i].run_simulation()
                self.stateCounts['DC'][i][genNum] = self.simulations[i].stateCount['DC']
                self.stateCounts['CC'][i][genNum] = self.simulations[i].stateCount['CC']
                self.stateCounts['DD'][i][genNum] = self.simulations[i].stateCount['DD']

                for agent in self.simulations[i].agents:
                    classif = self.strat_classifier(agent.lookupTable)
                    if classif == 'cooperator':
                        self.numCooperators[i][genNum] += 1
                    elif classif == 'defector':
                        self.numDefectors[i][genNum] += 1
                    elif classif == 'tit4tat':
                        self.numTit4Tat[i][genNum] += 1
                    
    def output_results(self):
        f = open("QLearning_plus_Evo_results.txt", "a")
        for i in range(len(self.paramVals)):
            f.write('\n')
            f.write('\n')
            f.write(self.param+': '+str(self.paramVals[i]))
            f.write('\n')
            f.write('DC')
            f.write('\n')
            f.write(' '.join(map(str,self.stateCounts['DC'][i])))
            f.write('\n')
            f.write('CC')
            f.write('\n')
            f.write(' '.join(map(str,self.stateCounts['CC'][i])))
            f.write('\n')
            f.write('DD')
            f.write('\n')
            f.write(' '.join(map(str,self.stateCounts['DD'][i])))
            f.write('\n')
            
            f.write('Number of Cooperators')
            f.write('\n')
            f.write(' '.join(map(str,self.numCooperators[i])))
            f.write('\n')
            f.write('Number of Defectors')
            f.write('\n')
            f.write(' '.join(map(str,self.numDefectors[i])))
            f.write('\n')
            f.write('Number of Tit4Tat Players')
            f.write('\n')
            f.write(' '.join(map(str,self.numTit4Tat[i])))
        f.close()
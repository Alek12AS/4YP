from evolution import EvolutionSimulator

class EvolutionExperiments:

    def __init__(self, totalGenerations = 100, totalAgents=100, gameIts=100,\
        numOfSurvivors=5 , mutationSD=5, rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1,\
             param='Population Size', paramVals=None, repetitions=1, agents=None):

        self.totalGenerations = totalGenerations
        self.totalAgents = totalAgents

        self.paramVals = paramVals
        self.param = param
        self.repetitions = repetitions

        self.simulations = []
        
        if param == 'Population Size':
            for popSize in paramVals:
                self.simulations.append(EvolutionSimulator(totalGenerations, popSize, gameIts,\
                    numOfSurvivors, mutationSD, rewardCD, rewardDC, rewardCC, rewardDD, agents))
        
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
        for i in range(len(self.paramVals)):
            print(self.paramVals[i])
            print('DC')
            for n in self.stateCounts['DC'][i]:
                print(n, end=' ')
            print('CC')
            for n in self.stateCounts['CC'][i]:
                print(n, end=' ')
            print('DD')
            for n in self.stateCounts['DD'][i]:
                print(n, end=' ')
            
            print('Num of Cooperators')
            for n in self.numCooperators[i]:
                print(n, end=' ')
            print('Num of Defectors')
            for n in self.numDefectors[i]:
                print(n, end=' ')
            print('Num of Tit4Tat')
            for n in self.numTit4Tat[i]:
                print(n, end=' ')
            print('')
        
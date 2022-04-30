from evolution import EvolutionSimulator
import numpy as np
import pandas as pd
import csv

class EvolutionExperiments:

    def __init__(self, totalGenerations = 100, totalAgents=100, gameIts=10,\
        survivalRate=0.05 , mutationSD=5, rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1,\
             param='Population_Size', paramVals=None, repetitions=1, agents=None):

        self.totalGenerations = totalGenerations
        self.totalAgents = totalAgents
        self.mutationSD = mutationSD
        self.gameIterations = gameIts
        self.survivalRate = survivalRate
        self.rewardCD= rewardCD
        self.rewardDC= rewardDC
        self.rewardCC= rewardCC
        self.rewardDD= rewardDD
        self.agents = agents
        self.paramVals = paramVals
        self.param = param
        self.repetitions = repetitions

        self.simulations = []

        self.initialise_simulations()
        
    
    def initialise_simulations(self):
        if self.param == 'Population_Size':
            for popSize in self.paramVals:
                self.simulations.append(EvolutionSimulator(self.totalGenerations, popSize, self.gameIterations,\
                    self.survivalRate, self.mutationSD, self.rewardCD, self.rewardDC, self.rewardCC,\
                         self.rewardDD, self.agents))


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
        else:
            return 'other'    

        
    def obtain_results(self):
        for i in range(len(self.paramVals)):
            
            lookupTables = []
            stateCounts = {'DC':[0]*self.totalGenerations,'CC':[0]*self.totalGenerations,\
            'DD':[0]*self.totalGenerations}
            rewardMeans = []
            rewardSDs = []
            self.stratCount = {}
            strategyCount = {'cooperator':[0]*self.totalGenerations, 'defector':[0]*self.totalGenerations,\
                 'tit4tat':[0]*self.totalGenerations, 'other':[0]*self.totalGenerations}

            for genNum in range(self.totalGenerations):
                self.simulations[i].run_simulation()
                
                lt = []
                rwrds = []
                for agent in self.simulations[i].agents:
                    lt.append(pd.DataFrame(agent.lookupTable).round(1)) 
                    rwrds.append(agent.totalReward)

                    classif = self.strat_classifier(agent.lookupTable)
                    
                    strategyCount[classif][genNum] += 1
                    
                
                stateCounts['DC'][genNum] = self.simulations[i].stateCount['DC']
                stateCounts['CC'][genNum] = self.simulations[i].stateCount['CC']
                stateCounts['DD'][genNum] = self.simulations[i].stateCount['DD']
                
                self.count_strategies(self.simulations[i].agents, genNum)
                
                lookupTables.append(lt)
                rewardMeans.append(np.mean(rwrds))
                rewardSDs.append(np.std(rwrds))
                

                self.simulations[i].repopulate()
                self.simulations[i].reset_measurements()
            
            self.output_results(stateCounts, strategyCount, rewardMeans, rewardSDs, i)
            
            

    def print_lookupTables(self, lookupTables, paramNum):
        f = open(self.__class__.__name__+'_lookupTables'+'.txt', 'a')
        f.write('\n--------------------------\n\n')
        f.write(self.param+':'+str(self.paramVals[paramNum])+'\n')
        f.write('Population Size:'+str(self.totalAgents))
        f.write(' Total Generations:'+str(self.totalGenerations))
        f.write(' Mutation SD:'+str(self.mutationSD))
        f.write(' Survival Rate:'+str(self.survivalRate*100)+'%')
        f.write(' Game Iterations:'+str(self.gameIterations))
        f.write('\n\n--------------------------\n\n')
        
        pd.set_option('expand_frame_repr', False)
        pd.set_option('display.max_rows', 10000)
        pd.set_option('display.max_columns', 10000)
        for g in range(self.totalGenerations):
            f.write('Generation #'+str(g+1))
            f.write('\n')
            f.write(str(pd.DataFrame(pd.concat(lookupTables[g], axis=1))))
            f.write('\n')
        f.close()

    def count_strategies(self, agents, genNum):
        states = ['CC', 'CD', 'DC', 'DD', '_']
        
        for agent in agents:
            stratString = '' 
            for state in states:    
                if agent.lookupTable['C'][state] >= agent.lookupTable['D'][state]:
                    stratString += 'C'
                else:
                    stratString += 'D'
            
            if stratString not in self.stratCount.keys():
                self.stratCount[stratString] = [0]*self.totalGenerations
                self.stratCount[stratString][genNum] += 1
            else:
                self.stratCount[stratString][genNum] += 1
  
    
    def output_results(self, stateCounts, strategyCounts, rewardMeans, rewardSDs, paramNum):
        f = open('results_' + self.__class__.__name__ +'/'+self.param+'_results.csv', "a", newline='')
        writer = csv.writer(f)
        # hyperParams = ['Population Size:'+str(self.totalAgents)+' Total Generations:'+str(self.totalGenerations)\
        #      + ' Mutation SD:'+str(self.mutationSD)+ ' Survival Rate:'+str(self.survivalRate*100)+'%'\
        #           + ' Game Iterations:'+str(self.gameIterations)]
        
        # writer.writerow(hyperParams)
        writer.writerow([self.param + ':' + str(self.paramVals[paramNum])])
        writer.writerow(['Generation #'] + [i+1 for i in range(self.totalGenerations)])
        writer.writerow(['CC #'] + stateCounts['CC'])
        writer.writerow(['DC #'] + stateCounts['DC'])
        writer.writerow(['DD #'] + stateCounts['DD'])
        writer.writerow(['Cooperator #'] + strategyCounts['cooperator'])
        writer.writerow(['Defector #'] + strategyCounts['defector'])
        writer.writerow(['Tit4Tat #'] + strategyCounts['tit4tat'])
        writer.writerow(['Other Strats #'] + strategyCounts['other'])
        writer.writerow(['Agent Reward Means'] + list(np.around(rewardMeans, decimals=2)))
        writer.writerow(['Agent Reward SDs'] + list(np.around(rewardSDs, decimals=2)))
        writer.writerow(['Strategy Counts'])
        
        for key, value in self.stratCount.items():
            writer.writerow([key] + value)

        f.close()
        
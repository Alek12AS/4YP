from evolution import EvolutionSimulator
import numpy as np
import pandas as pd

class EvolutionExperiments:

    def __init__(self, totalGenerations = 100, totalAgents=100, gameIts=10,\
        survivalRate=0.05 , mutationSD=5, rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1,\
             param='Population_Size', paramVals=None, repetitions=1, agents=None):

        self.totalGenerations = totalGenerations
        self.totalAgents = totalAgents
        self.mutationSD = mutationSD
        self.gameIterations = gameIts
        self.survivalRate = survivalRate

        self.paramVals = paramVals
        self.param = param
        self.repetitions = repetitions

        self.simulations = []

        self.lookupTables = []
        self.rewards = []
        
        if param == 'Population_Size':
            for popSize in paramVals:
                self.simulations.append(EvolutionSimulator(totalGenerations, popSize, gameIts,\
                    survivalRate, mutationSD, rewardCD, rewardDC, rewardCC, rewardDD, agents))
        
        numParams = len(self.paramVals)


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
        else:
            return 'other'    

        
    def obtain_results(self):
        for i in range(len(self.paramVals)):
            
            lookupTables = []
            stateCounts = {'DC':[0]*self.totalGenerations,'CC':[0]*self.totalGenerations,\
            'DD':[0]*self.totalGenerations}
            rewards = []
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
                
                lookupTables.append(lt)
                rewards.append(rwrds)
                

                self.simulations[i].repopulate()
                self.simulations[i].reset_measurements()
            
            self.output_results(stateCounts, strategyCount, rewards, i)
            self.print_lookupTables(lookupTables, i)

    def print_lookupTables(self, lookupTables, paramNum):
        f = open('evolution_lookupTables.txt', 'a')
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
        
    
    def output_results(self, stateCounts, strategyCounts, rewards, paramNum):
        f = open("evolution_results.txt", "a")
        
        f.write('\n')
        f.write('\n--------------------------\n\n')
        f.write(self.param+':'+str(self.paramVals[paramNum])+'\n')
        f.write('Population Size:'+str(self.totalAgents))
        f.write(' Total Generations:'+str(self.totalGenerations))
        f.write(' Mutation SD:'+str(self.mutationSD))
        f.write(' Survival Rate:'+str(self.survivalRate*100)+'%')
        f.write(' Game Iterations:'+str(self.gameIterations))
        f.write('\n\n--------------------------\n\n')

        f.write('DC_Count: ')
        f.write(' '.join(map(str, stateCounts['DC'])))
        f.write('\n')
        f.write('CC_Count: ')
        f.write(' '.join(map(str, stateCounts['CC'])))
        f.write('\n')
        f.write('DD_Count: ')
        f.write(' '.join(map(str, stateCounts['DD'])))
        f.write('\n')
        
        f.write('Number_of_Cooperators: ')
        f.write(' '.join(map(str, strategyCounts['cooperator'])))
        f.write('\n')
        f.write('Number_of_Defectors: ')
        f.write(' '.join(map(str, strategyCounts['defector'])))
        f.write('\n')
        f.write('Number_of_Tit4Tat_Players: ')
        f.write(' '.join(map(str, strategyCounts['tit4tat'])))
        f.write('\n')
        f.write('Other_Strategies: ')
        f.write(' '.join(map(str, strategyCounts['other'])))
        f.write('\n')
        f.write('Agent_Rewards: ')
        f.write('\n')
        for i in range(self.totalGenerations):
            f.write(str(i)+' '+' '.join(map(str, np.sort(np.around(rewards[i], decimals=1)))))
            f.write('\n')
        f.close()
        
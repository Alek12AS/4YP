import numpy as np
from evolution import EvolutionSimulator
from q_learning import QLearningSimulator


class QLearnPlusEvoSimulator(EvolutionSimulator):


    def run_simulation(self):
        for agent1 in range(self.populationSize):
            for agent2 in range(agent1+1,self.populationSize):
                priorState = '_'
                for g in range(self.totalGames):
                    agent1Action = self.select_action(agent1, priorState)
                    agent2Action = self.select_action(agent2, priorState[::-1])
                
                    newState = agent1Action + agent2Action
                
                    self.agents[agent1].totalReward += self.rewardsLookup[newState]
                    self.agents[agent2].totalReward += self.rewardsLookup[newState[-1::-1]]
                    

                if newState == 'CD':
                    self.stateCount['DC'] += 1
                else:
                    self.stateCount[newState] += 1
        
                priorState = newState
            
            self.agentTable = self.repopulate()

  
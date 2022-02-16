import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Agent:
  
  def __init__(self, lookupTable=None, totalReward=0, epsilon=0.1, gamma=0.9):
    if lookupTable == None:
      self.initialise_lookup_tables(gamma)
    else:
      self.lookupTable = lookupTable

    self.epsilon = epsilon

    self.totalReward = totalReward
    
      
  
  def initialise_lookup_tables(self, gamma):   
    randVals = np.random.random_sample(10) * 0.5*gamma/(1-gamma)

    self.lookupTable = {'D': {'CC': randVals[0], 'CD': randVals[1], 'DC': randVals[2], 'DD': randVals[3], '_': randVals[4]},
                  'C': {'CC': randVals[5], 'CD': randVals[6], 'DC': randVals[7], 'DD': randVals[8], '_': randVals[9]}}
   


class QLearningSimulator:

  def __init__(self, totalAgents=100, gamma=0.9, alpha=0.1, totalIterations=100, epsilon0=0.25,\
  epsilonDecay=0.999,rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, agents=None):
    
    # number of agents N_a 
    self.totalAgents  = totalAgents
    # discount factor for future return
    self.gamma = gamma
    # learning rate
    self.alpha = alpha
    # total iterations in IPD
    self.totalIterations = totalIterations

    # For epsilon greedy
    self.epsilon0 = epsilon0
    self.epsilonDecay = epsilonDecay
    
    self.rewards_lookup = {'CD':rewardCD, 'DC':rewardDC, 'CC':rewardCC, 'DD':rewardDD}
    
    self.stateCount = {'DC':0,'CC':0,'DD':0}
    self.agentSampleSize = 10
    self.trackedAgents = np.random.choice(self.totalAgents, self.agentSampleSize, False)
    self.samplePeriod = 10
    self.TDEs = np.zeros((self.agentSampleSize, ((totalAgents-1)*totalIterations)//self.samplePeriod + 1))
    
    if agents == None:
      self.agents = []
      for i in range(totalAgents):
        self.agents.append(Agent(epsilon=self.epsilon0, gamma=self.gamma))
    else:
      self.agents = agents

  def epsilon_greedy_decision(self, priorState, agent):
    if self.agents[agent].lookupTable['D'][priorState] > self.agents[agent].lookupTable['C'][priorState]:
      greedyOption = 'D'
      randomOption = 'C'
    else:
      greedyOption = 'C'
      randomOption = 'D'

    randomNumber = np.random.random_sample()

    if randomNumber <= self.agents[agent].epsilon:
      decision = randomOption
    else:
      decision = greedyOption
    
    # Decay epsilon for the agent
    self.agents[agent].epsilon = self.agents[agent].epsilon * self.epsilonDecay

    return decision

  def reset_measurements(self):
    self.stateCount = {'DC':0,'CC':0,'DD':0}
    self.trackedAgent = np.random.randint(0, self.totalAgents)
    self.TDEs = np.zeros((self.agentSampleSize, ((self.totalAgents-1)*self.totalIterations)//self.samplePeriod + 1))

  def collect_TDEs(self, agent1, agent2, deltaQ1, deltaQ2):
    
    if agent1 in self.trackedAgents:
      index = np.where(self.trackedAgents == agent1)
      if self.TDEs[index,0] % self.samplePeriod == 0:
        self.TDEs[index, int(self.TDEs[index,0]//self.samplePeriod)] = deltaQ1
      self.TDEs[index,0] += 1

    if agent2 in self.trackedAgents:
      index = np.where(self.trackedAgents == agent2)
      if self.TDEs[index,0] % self.samplePeriod == 0:
        self.TDEs[index, int(self.TDEs[index,0]//self.samplePeriod + 1)] = deltaQ2
      self.TDEs[index,0] += 1

  def update_lookup_tables(self, newState, priorState, agent1, agent2,\
                          agent1Decision, agent2Decision, agent1Reward, agent2Reward):

    maxQb1 = max(self.agents[agent1].lookupTable['D'][newState], self.agents[agent1].lookupTable['C'][newState])

    deltaQ1 = self.alpha*(agent1Reward + self.gamma*maxQb1 - self.agents[agent1].lookupTable[agent1Decision][priorState])
    
    maxQb2 = max(self.agents[agent2].lookupTable['D'][newState[-1::-1]], self.agents[agent2].lookupTable['C'][newState])
            
    deltaQ2 = self.alpha*(agent2Reward + self.gamma*maxQb2 - self.agents[agent2].lookupTable[agent2Decision][priorState[-1::-1]])

    self.agents[agent1].lookupTable[agent1Decision][priorState] += deltaQ1
            
    self.agents[agent2].lookupTable[agent2Decision][priorState[-1::-1]] += deltaQ2

    self.collect_TDEs(agent1, agent2, deltaQ1, deltaQ2)

  def run_simulation(self):
    
    for agent1 in range(self.totalAgents):
      for agent2 in range(agent1+1,self.totalAgents):
        priorState = '_'
        for i in range(self.totalIterations):

          agent1Decision = self.epsilon_greedy_decision(priorState, agent1)
          agent2Decision = self.epsilon_greedy_decision(priorState[-1::-1], agent2)
          
          newState = agent1Decision + agent2Decision
          
          agent1Reward = self.rewards_lookup[newState]
          agent2Reward = self.rewards_lookup[newState[-1::-1]]

          self.agents[agent1].totalReward += agent1Reward
          self.agents[agent2].totalReward += agent2Reward
          

          self.update_lookup_tables(newState, priorState, agent1, agent2,\
                              agent1Decision, agent2Decision, agent1Reward, agent2Reward)

          if newState == 'CD':
            self.stateCount['DC'] += 1
            
          else:
            self.stateCount[newState] += 1

          priorState = newState

  def disp_TDEs(self):
    
    totalGames = (self.totalAgents-1)*self.totalIterations//10
    averagedTDE = np.sum(self.TDEs[:,1:],0)/self.agentSampleSize

    plt.plot([i for i in range(totalGames)], averagedTDE)
    plt.xlabel('Iteration # /10')
    plt.ylabel('Mean TDE')
    plt.title('Mean TDE of a sample of agents over IPD Iterations')

    plt.show()

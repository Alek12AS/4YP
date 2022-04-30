import numpy as np


class Agent:
  
  def __init__(self, lookupTable=None, totalReward=0, epsilon=0.1, its=0):
    
    self.lookupTable = lookupTable

    self.epsilon = epsilon

    self.totalReward = totalReward

    # Keeps track of the iteration number for the agent
    self.its = its

  

class QLearningSimulator:

  def __init__(self, totalAgents=100, gamma=0.99, alpha=0.1, gameIts=10, epsilon0=0.5,\
  epsilonDecay=0.9999,rewardCD=0, rewardDC=0.5, rewardCC=0.3, rewardDD=0.1, agents=None):
    
    # number of agents N_a 

    if agents == None:
      self.totalAgents = totalAgents
    else:
      self.totalAgents = len(agents)

    # discount factor for future return
    self.gamma = gamma
    # learning rate
    self.alpha = alpha
    # total iterations in IPD
    self.gameIts = gameIts

    # For epsilon greedy
    self.epsilon0 = epsilon0
    self.epsilonDecay = epsilonDecay
    
    self.rewards_lookup = {'CD':rewardCD, 'DC':rewardDC, 'CC':rewardCC, 'DD':rewardDD}
    
    self.stateCount = {'DC':0,'CC':0,'DD':0}
    
    if agents == None:
      self.create_agents()
    else:
      self.agents = agents

  def create_agents(self):
    
    self.agents = []
    for i in range(self.totalAgents):
        randVals = np.random.random_sample(10) * 0.5*self.gamma/(1-self.gamma)

        lookupTable = {'D': {'CC': randVals[0], 'CD': randVals[1], 'DC': randVals[2], 'DD': randVals[3], '_': randVals[4]},
                  'C': {'CC': randVals[5], 'CD': randVals[6], 'DC': randVals[7], 'DD': randVals[8], '_': randVals[9]}}
        
        self.agents.append(Agent(lookupTable=lookupTable, epsilon=self.epsilon0))

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

    # Increment agent iteration number
    self.agents[agent].its += 1

    return decision

  def reset_measurements(self):
    self.stateCount = {'DC':0,'CC':0,'DD':0}


  def update_lookup_tables(self, newState, priorState, agent1, agent2,\
                          agent1Decision, agent2Decision, agent1Reward, agent2Reward):
    maxQb1 = max(self.agents[agent1].lookupTable['D'][newState], self.agents[agent1].lookupTable['C'][newState])
    deltaQ1 = self.alpha*(agent1Reward + self.gamma*maxQb1 - self.agents[agent1].lookupTable[agent1Decision][priorState])
    
    maxQb2 = max(self.agents[agent2].lookupTable['D'][newState[-1::-1]], self.agents[agent2].lookupTable['C'][newState])        
    deltaQ2 = self.alpha*(agent2Reward + self.gamma*maxQb2 - self.agents[agent2].lookupTable[agent2Decision][priorState[-1::-1]])

    self.agents[agent1].lookupTable[agent1Decision][priorState] += deltaQ1
    self.agents[agent2].lookupTable[agent2Decision][priorState[-1::-1]] += deltaQ2

  def repopulate(self):
    for agent in self.agents:
      agent.totalReward = 0

  def run_simulation(self):
    
    for agent1 in range(self.totalAgents):
      for agent2 in range(agent1+1,self.totalAgents):
        priorState = '_'
        for i in range(self.gameIts):

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
    


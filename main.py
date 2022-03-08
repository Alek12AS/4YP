import numpy as np
import matplotlib.pyplot as plt
from q_learn_plus_evo import QLearnPlusEvoSimulator
from experiments import QLearningExperiments
from evolution_experiments import EvolutionExperiments

def main():
   
    # g1 = np.linspace(0,1,20,False)
    # g2 = np.linspace(0.99,1,5,False)
    # g3 = np.linspace(0.999,1,5,False)
    # g4 = np.linspace(0.9999,1,5,False)

    # gammaVals = np.concatenate((g1, g2, g3, g4))
    
    # Qexp = QLearningExperiments(param='Gamma', paramVals=gammaVals)

    # Qexp.train_populations()
    # Qexp.obtain_results()
    # Qexp.output_results()

    popSizes = [10,50,100,200]

    evoExp = EvolutionExperiments(totalGenerations=10, paramVals=popSizes)
    evoExp.obtain_results()
    evoExp.output_results()

if __name__ == "__main__":
    main()
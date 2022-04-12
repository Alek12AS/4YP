import numpy as np
import matplotlib.pyplot as plt
from q_learning_experiments import QLearningExperiments
from evolution_experiments import EvolutionExperiments
from q_learning_plus_evo_experiments import QLearningPlusEvolutionExperiments
import time

def main():
    startTime = time.time()
    # g1 = np.linspace(0,1,20,False)
    # g2 = np.linspace(0.99,1,5,False)
    # g3 = np.linspace(0.999,1,5,False)
    # g4 = np.linspace(0.9999,1,5,False)

    # gammaVals = np.concatenate((g1, g2, g3, g4))
    
    # Qexp = QLearningExperiments(param='Gamma', paramVals=[0.99])

    # Qexp.train_populations()
    # Qexp.obtain_results()
    # Qexp.output_results()

    popSizes = [20]

    # evoExp = EvolutionExperiments(totalGenerations=10, paramVals=popSizes)
    # evoExp.obtain_results()
    # print("--- %s seconds ---" % (time.time() - startTime))
    
    evoPlusQ = QLearningPlusEvolutionExperiments(totalGenerations=10, paramVals=popSizes)
    evoPlusQ.obtain_results()
    print("--- %s seconds ---" % (time.time() - startTime))

if __name__ == "__main__":
    main()
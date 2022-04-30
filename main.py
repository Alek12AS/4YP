import numpy as np
import matplotlib.pyplot as plt
from q_learning_experiments import QLearningExperiments
from evolution_experiments import EvolutionExperiments
from q_learning_plus_evo_experiments import QLearningPlusEvolutionExperiments
import time

def main():
    startTime = time.time()
    
    popSizes = [50]

    Qexp = QLearningExperiments(paramVals=popSizes)
    Qexp.obtain_results()

    # evoExp = EvolutionExperiments(totalGenerations=100, paramVals=popSizes)
    # evoExp.obtain_results()
    
    # evoPlusQ = QLearningPlusEvolutionExperiments(totalGenerations=100, paramVals=popSizes)
    # evoPlusQ.obtain_results()
    
    print("--- %s seconds ---" % (time.time() - startTime))

if __name__ == "__main__":
    main()
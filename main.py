import numpy as np
import matplotlib.pyplot as plt
from q_learning import QLearningSimulator
from q_learn_plus_evo import QLearnPlusEvoSimulator
from evolution import EvolutionSimulator
from experiments import QLearningExperiments

def main():
    # sim1 = QLearningSimulator()
    # sim1.run_simulation()
    # sim1.disp_TDEs()

    # evo1 = EvolutionSimulator()
    # evo1.run_simulation()
    # print(evo1.stateCount)
    # gammaVals = np.arange(0.5,1,0.01)
    

    # Qexp = QLearningExperiments(totalAgents=50, gameIts=50, param='Gamma',\
    #      paramVals=gammaVals)

    # Qexp.train_populations()
    # Qexp.obtain_results()
    # Qexp.disp_results()
    
    counts = []

    qLearnPlusEvo = QLearnPlusEvoSimulator(mutationSD=1)
    
    for i in range(15):
        qLearnPlusEvo.run_simulation()
        counts.append(qLearnPlusEvo.stateCount['CC'])
        qLearnPlusEvo.reset_measurements()
        

    plt.plot([i for i in range(15)], counts)
    plt.ylabel('Number of CC states')
    plt.xlabel('Generation Number')
    plt.show()


if __name__ == "__main__":
    main()
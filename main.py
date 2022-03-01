import numpy as np
from q_learning import QLearningSimulator
from evolution import EvolutionSimulator
from experiments import QLearningExperiments

def main():
    # sim1 = QLearningSimulator()
    # sim1.run_simulation()
    # sim1.disp_TDEs()

    # evo1 = EvolutionSimulator()
    # evo1.run_simulation()
    # print(evo1.stateCount)
    gammaVals = np.arange(0.5,1,0.01)
    

    Qexp = QLearningExperiments(totalAgents=50, gameIts=50, param='Gamma',\
         paramVals=gammaVals)

    Qexp.train_populations()
    Qexp.obtain_results()
    Qexp.disp_results()


if __name__ == "__main__":
    main()
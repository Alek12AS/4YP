from q_learning import QLearningSimulator
from evolution import EvolutionSimulator

def main():
    # sim1 = SimulateQLearners()
    # sim1.run_simulation()
    # sim1.disp_TDEs()

    evo1 = EvolutionSimulator()
    evo1.run_simulation()
    print(evo1.stateCount)

if __name__ == "__main__":
    main()
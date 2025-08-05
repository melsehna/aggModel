import argparse
from config import defaultParams
from utils import ensureParams 
from moran import MoranSimulation
from rescueVector import RescueSimulation
from batchRunner import runBatchGrid

def runSingle(modelType='rescue', scenario='E2', penetrance='uniform', beta=1.0, sAB=0.5, tMax=1000, nC=50):
    #  create params ONCE and apply overrides
    params = ensureParams(defaultParams.copy())
    params['beta'] = beta
    params['sAB'] = sAB
    params['penetrance'] = penetrance

    if modelType == 'moran':
        sim = MoranSimulation(D=2, nPerDeme=500, params=params, scenario=scenario)
        history = sim.run(tMax=tMax)
        print(f'Moran simulation complete. Last R frequency: {history[-1]}')
        return history

    sim = RescueSimulation(D=2, nPerDeme=500, params=params, scenario=scenario)
    outcome, history = sim.run(nC=nC, tMax=tMax)
    print(f'Rescue simulation outcome: {outcome}')
    return outcome, history

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Moran or Rescue simulations with parameter overrides.')
    parser.add_argument('--mode', choices=['single', 'batch'], default='single', help='Run single simulation or batch exploration')
    parser.add_argument('--modelType', choices=['moran', 'rescue'], default='rescue')
    parser.add_argument('--scenario', default='E2')
    parser.add_argument('--penetrance', choices=['uniform', 'variable'], default='uniform')
    parser.add_argument('--beta', type=float, default=1.0)
    parser.add_argument('--sAB', type=float, default=0.5)
    parser.add_argument('--tMax', type=int, default=1000)
    parser.add_argument('--runs', type=int, default=10)
    args = parser.parse_args()

    if args.mode == 'single':
        runSingle(modelType=args.modelType, scenario=args.scenario, penetrance=args.penetrance,
                  beta=args.beta, sAB=args.sAB, tMax=args.tMax)
    else:
        df = runBatchGrid(modelType=args.modelType, scenarios=[args.scenario],
                          penetranceModes=[args.penetrance], betas=[args.beta],
                          sABValues=[args.sAB], runs=args.runs, tMax=args.tMax)
        print('Batch exploration complete. Results saved to batchResults.pkl')

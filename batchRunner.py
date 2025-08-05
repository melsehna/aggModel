# batchRunner.py
import numpy as np
import pandas as pd
from config import defaultParams
from moran import MoranSimulation
from rescueVector import RescueSimulation
from utils import ensureParams

def runBatchGrid(modelType='rescue', scenarios=['E2', 'E4'],
                 penetranceModes=['uniform', 'variable'],
                 betas=[0, 1.0], sABValues=[0.5],
                 runs=10, tMax=1000, nC=50):

    results = []

    for scenario in scenarios:
        for penetrance in penetranceModes:
            for beta in betas:
                for sAB in sABValues:
                    # create params fresh for this run
                    params = {
                        'beta': beta,
                        'sAB': sAB,
                        'penetrance': penetrance
                    }
                    params = ensureParams(params)   # now params exists!

                    for rep in range(runs):
                        if modelType == 'moran':
                            sim = MoranSimulation(D=5, nPerDeme=200, params=params, scenario=scenario)
                            history = sim.run(tMax=tMax)
                            rescued = int(history[-1] > 0.9)
                        else:
                            sim = RescueSimulation(D=5, nPerDeme=200, params=params, scenario=scenario)
                            outcome, history = sim.run(nC=nC, tMax=tMax)
                            rescued = 1 if outcome == 'Rescue' else 0

                        results.append({
                            'model': modelType,
                            'scenario': scenario,
                            'penetrance': penetrance,
                            'beta': beta,
                            'sAB': sAB,
                            'replicate': rep,
                            'rescued': rescued,
                            'history': history
                        })
                        if (rep + 1) % 1 == 0:   # print every replicate
                            print(f'  -> Finished replicate {rep+1}/{runs}')

                    print(f'Completed {runs} runs for {scenario}-{penetrance} β={beta} sAB={sAB}')

    import pandas as pd
    df = pd.DataFrame(results)
    df.to_pickle(f'batchResults_{scenario}_{penetrance}.pkl')
    return df

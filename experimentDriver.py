import os
import pandas as pd
from batchRunner import runBatchGrid
from plotUtils import plotPrescueVsBeta
from hypothesis import given, strategies as st

# Experiment parameters
scenarios = ['E1', 'E2', 'E3', 'E4']
penetranceModes = ['variable']
betas = [0, 0.5, 1.0, 2.0, 5.0]
sABValues = [0.5]
runs = 10
tMax = 1000
modelType = 'rescue'

# output directory
outDir = 'batch_sweep_results'
os.makedirs(outDir, exist_ok=True)

allDfs = []

# Run simulations
for scenario in scenarios:
    print(f'\n### Running {scenario} sweep ###')
    df = runBatchGrid(modelType=modelType,
                      scenarios=[scenario],
                      penetranceModes=penetranceModes,
                      betas=betas,
                      sABValues=sABValues,
                      runs=runs,
                      tMax=tMax)

    df.to_pickle(os.path.join(outDir, f'batchResults_{scenario}.pkl'))
    allDfs.append(df)

# Combine results
combinedDf = pd.concat(allDfs, ignore_index=True)
comboPath = os.path.join(outDir, 'batchResults_combined.pkl')
combinedDf.to_pickle(comboPath)
print(f'\nCombined results saved to {comboPath}')
print(combinedDf.groupby(['scenario', 'beta']).rescued.mean())

# Plot
plotPath = os.path.join(outDir, 'prescue_vs_beta_allScenarios.png')
plotPrescueVsBeta(combinedDf, savePath=plotPath)
print(f'Plot saved to {plotPath}')

# === Hypothesis-based Tests ===

def prescue(df, scenario, beta):
    sub = df[(df['scenario']==scenario) & (df['beta']==beta)]
    return sub['rescued'].mean()

@given(beta=st.sampled_from([1.0, 2.0, 5.0]))
def test_bd_suppresses_rescue(beta):
    p_e2 = prescue(combinedDf, 'E2', beta)
    p_e4 = prescue(combinedDf, 'E4', beta)
    assert p_e4 <= p_e2, f'BD suppression failed at beta={beta}'

@given(beta=st.sampled_from([1.0, 2.0, 5.0]))
def test_aggregation_increases_rescue(beta):
    p_low = prescue(combinedDf, 'E2', 0)
    p_high = prescue(combinedDf, 'E2', beta)
    assert p_high >= p_low, f'Aggregation did not increase rescue at beta={beta}'

@given(beta=st.sampled_from([1.0, 2.0, 5.0]))
def test_controls_zero(beta):
    p_e1 = prescue(combinedDf, 'E1', beta)
    p_e3 = prescue(combinedDf, 'E3', beta)
    assert p_e1 < 0.05 and p_e3 < 0.05, f'Controls not near zero at beta={beta}'

# Run Hypothesis Tests
print('\n=== Running Hypothesis Tests on Results ===')
test_bd_suppresses_rescue()
test_aggregation_increases_rescue()
test_controls_zero()
print('All narrative hypotheses validated!')

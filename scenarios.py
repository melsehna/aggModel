import numpy as np
from config import scenarios
from utils import ensureParams

def getAggregation(d, state):
    nc = state[d][('WT','NC')] + state[d][('R','NC')]
    total = sum(state[d].values())
    return nc / total if total > 0 else 0.0

def getDeathRate(d, g, p, state, scenario, params):
    params = ensureParams(params)
    s = scenarios[scenario]
    antibioticOn = s.get('antibiotic', False)
    bdOn = s.get('behaviorDrug', False)
    penetranceMode = params.get('penetrance', 'uniform')

    if not antibioticOn:
        return 1.0
    if g == 'WT':
        if penetranceMode == 'variable' and not bdOn:
            a = getAggregation(d, state)
            return np.exp(-params['beta'] * a)
        return 1.0 + params['sAB']
    return 1.0

def getFitness(d, g, p, state, scenario, params):
    params = ensureParams(params)
    s = scenarios[scenario]
    bdOn = s.get('behaviorDrug', False)
    penetranceMode = params.get('penetrance', 'uniform')

    if g == 'WT':
        base = 1.0 - params['sAB']
        if penetranceMode == 'variable' and not bdOn:
            a = getAggregation(d, state)
            return base + params['gamma'] * a
        return base
    return 1.0 - params['cR']

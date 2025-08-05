# utils.py
import random

def ensureParams(params):
    defaults = {
        'beta': 1.0,
        'sAB': 0.5,
        'cR': 0.05,
        'gamma': 0.1,
        'm': 0.01,
        'bWT': 1.0,
        'bR': 1.0,
        'penetrance': 'uniform',
        'muWtR': 1e-4,
        'muCNc': 1e-5,
        'muNcC': 1e-5,
        'behaviorDrug': False
    }
    for k, v in defaults.items():
        if k not in params:
            params[k] = v
    return params

def mutate(g, p, params):
    params = ensureParams(params)
    muWtR = params['muWtR']
    muCNc = params['muCNc']
    muNcC = params['muNcC']

    newG = 'R' if (g == 'WT' and random.random() < muWtR) else g

    newP = p
    if p == 'C' and random.random() < muCNc:
        newP = 'NC'
    elif p == 'NC' and random.random() < muNcC:
        newP = 'C'

    return newG, newP


def weightedChoice(items, weights):
    if not items or sum(weights) == 0:
        raise ValueError('weightedChoice called with empty or zero weights')
    total = sum(weights)
    r = random.uniform(0, total)
    cum = 0
    for item, w in zip(items, weights):
        cum += w
        if r <= cum:
            return item

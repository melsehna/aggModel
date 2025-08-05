# config.py
defaultParams = {
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

scenarios = {
    'E1': {'antibiotic': False, 'behaviorDrug': False},
    'E2': {'antibiotic': True,  'behaviorDrug': False},
    'E3': {'antibiotic': False, 'behaviorDrug': True},
    'E4': {'antibiotic': True,  'behaviorDrug': True}
}

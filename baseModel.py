# baseModel.py
from scenarios import getAggregation

class PopulationModel:
    def __init__(self, D, nPerDeme, params, scenario):
        self.D = D
        self.scenario = scenario
        self.params = params
        self.state = [
            {('WT','NC'): nPerDeme, ('R','NC'): 0, ('WT','C'): 0, ('R','C'): 0}
            for _ in range(D)
        ]
        self.history = []
        self.time = 0.0

    def aggregation(self, d):
        return getAggregation(d, self.state)
    
    def recordState(self, step=None):
        totalR = sum(deme[('R','NC')] + deme[('R','C')] for deme in self.state)
        total = sum(sum(deme.values()) for deme in self.state)
        freqR = totalR / total if total > 0 else 0.0
        timeValue = self.time if step is None else step
        self.history.append({
            'time': timeValue,
            'freqR': freqR,
            'popSize': total,
            'Rcount': totalR
        })



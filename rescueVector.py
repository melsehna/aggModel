# rescueVector.py

import numpy as np
from utils import mutate
from scenarios import getDeathRate, getAggregation
from baseModel import PopulationModel
from utils import ensureParams

class RescueSimulation(PopulationModel):
    def __init__(self, D, nPerDeme, params, scenario):
        self.params = ensureParams(params)
        super().__init__(D, nPerDeme, self.params, scenario)

    def initializeArrays(self):
        """Initialize compact arrays for counts and rates."""
        self.types = [('WT','NC'), ('WT','C'), ('R','NC'), ('R','C')]
        self.counts = np.zeros((self.D, len(self.types)), dtype=int)
        # populate counts
        for d in range(self.D):
            for i, tp in enumerate(self.types):
                self.counts[d, i] = self.state[d][tp]
        self.updateRates()


    def updateRates(self):
        self.birthRates = np.zeros_like(self.counts, dtype=float)
        self.deathRates = np.zeros_like(self.counts, dtype=float)
        
        bdOn = self.params.get('behaviorDrug', False)
        penetranceMode = self.params.get('penetrance', 'uniform')

        for d in range(self.D):
            a = 0.0 if bdOn else getAggregation(d, self.state)  # no aggregation if BD on
            for i, (g, p) in enumerate(self.types):
                n = self.counts[d, i]
                if n == 0:
                    continue

                # Birth rates
                if g == 'WT':
                    baseBirth = self.params['bWT']
                    if penetranceMode == 'variable' and not bdOn:
                        b = baseBirth + self.params['gamma'] * a
                    else:
                        b = baseBirth
                else:
                    b = self.params['bR']

                # Death rates
                dRate = getDeathRate(d, g, p, self.state, self.scenario, self.params)

                self.birthRates[d, i] = b * n
                self.deathRates[d, i] = dRate * n
                
        self.totalRate = np.sum(self.birthRates) + np.sum(self.deathRates)



    def chooseEvent(self):
        """Choose deme & type index based on total rates."""
        flatRates = np.hstack((self.birthRates.flatten(), self.deathRates.flatten()))
        idx = np.random.choice(len(flatRates), p=flatRates / flatRates.sum())
        eventType = 'birth' if idx < self.birthRates.size else 'death'
        if eventType == 'death':
            idx -= self.birthRates.size
        d, i = divmod(idx, len(self.types))
        return eventType, d, i

    def executeEvent(self, eventType, d, i):
        g, p = self.types[i]
        if eventType == 'birth':
            newG, newP = mutate(g, p, self.params)
            j = self.types.index((newG, newP))
            self.counts[d, j] += 1
            self.state[d][(newG, newP)] += 1
        else:
            if self.counts[d, i] > 0:
                self.counts[d, i] -= 1
                self.state[d][(g, p)] -= 1

    def run(self, nC=50, tMax=10000):
        
        self.initializeArrays()
        self.rescueTime = None  # track when rescue happens

        while self.time < tMax and self.totalRate > 0:
            # Gillespie step
            dt = np.random.exponential(1 / self.totalRate)
            self.time += dt

            # Event selection and execution
            eventType, d, i = self.chooseEvent()
            self.executeEvent(eventType, d, i)
            self.updateRates()
            self.recordState()

            # Calculate total counts
            totalPop = self.counts.sum()
            totalR = self.counts[:, 2].sum() + self.counts[:, 3].sum()

            # Stopping conditions
            if totalPop == 0:
                return 'Extinction', self.history
            if totalR >= nC:
                if self.rescueTime is None:
                    self.rescueTime = self.time
                return 'Rescue', self.history

        return 'Undecided', self.history

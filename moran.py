# moran.py (optimized with numpy)
import numpy as np
from utils import mutate
from scenarios import getDeathRate, getFitness
from baseModel import PopulationModel
from utils import ensureParams

class MoranSimulation(PopulationModel):
    def __init__(self, D, nPerDeme, params, scenario):
        self.params = ensureParams(params)
        super().__init__(D, nPerDeme, self.params, scenario)

    def pickVictim(self):
        # Select a deme proportional to its size
        demeSizes = np.array([sum(deme.values()) for deme in self.state], dtype=float)
        demeProb = demeSizes / demeSizes.sum()
        d = np.random.choice(self.D, p=demeProb)

        # Select individual to die weighted by death rates 
        keys, weights = [], []
        for (g, p), count in self.state[d].items():
            if count > 0:
                keys.append((g, p))
                weights.append(
                    getDeathRate(d, g, p, self.state, self.scenario, self.params) * count
                )


        weights = np.array(weights, dtype=float)
        weights /= weights.sum()
        victimType = keys[np.random.choice(len(keys), p=weights)]
        return d, victimType

    def pickParent(self, localDeme):
        # Determine parent deme range
        if np.random.rand() < (1 - self.params['m']):
            demeRange = [localDeme]
        else:
            demeRange = range(self.D)

        # Select parent weighted by local fitness
        keys, weights = [], []
        for d in demeRange:
            for (g, p), count in self.state[d].items():
                if count > 0:
                    keys.append((d, g, p))
                    weights.append(getFitness(d, g, p, self.state, self.scenario, self.params) * count)

        weights = np.array(weights, dtype=float)
        weights /= weights.sum()
        parentDeme, g, p = keys[np.random.choice(len(keys), p=weights)]
        return parentDeme, g, p

    def step(self):
        # Perform one Moran update
        dVictim, victim = self.pickVictim()
        dParent, g, p = self.pickParent(dVictim)

        # Offspring mutation
        newG, newP = mutate(g, p, self.params)

        # Update state
        self.state[dVictim][victim] -= 1
        self.state[dVictim][(newG, newP)] += 1

    def run(self, tMax=10000):
        for step in range(tMax):
            self.step()
            self.recordState(step)
        return self.history




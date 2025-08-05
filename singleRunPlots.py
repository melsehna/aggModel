# model/singleRunPlots.py

from config import defaultParams
from moran import MoranSimulation
from rescueVector import RescueSimulation   # use the fast version
from plotUtils import plotTrajectory

if __name__ == '__main__':
    print('Running single simulations for Moran model')
    moran = MoranSimulation(D=5, nPerDeme=200, params=defaultParams, scenario='E2_uniform')
    moranHistory = moran.run(tMax=1000)
    plotTrajectory(moranHistory, title=f'Moran model: {moran.scenario}')

    print('Running single simulations for Rescue model')
    rescue = RescueSimulation(D=5, nPerDeme=200, params=defaultParams, scenario='E2_uniform')
    outcome, rescueHistory = rescue.run(nC=50)
    print(f'Rescue simulation outcome: {outcome}')
    plotTrajectory(rescueHistory, title=f'Rescue model: {rescue.scenario} ({outcome})',
                   nC=50, rescueTime=rescue.rescueTime)

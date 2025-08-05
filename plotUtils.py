# plotUtils.py
from turtle import color
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plotTrajectory(history, title='Trajectory', savePath=None, nC=None, rescueTime=None):
    times = [h['time'] for h in history]
    freqs = [h['freqR'] for h in history]
    pops = [h['popSize'] for h in history]
    Rs = [h['Rcount'] for h in history]

    fig, ax1 = plt.subplots(figsize=(9,5))

    # --- Plot resistant frequency ---
    ax1.plot(times, freqs, lw=2, color='blue', label='Resistance frequency')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Resistance frequency', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(times, pops, lw=1.5, color='gray', alpha=0.6, label='Population size')
    ax2.set_ylabel('Population Size', color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')

    if nC is not None:
        initialPop = pops[0]
        thresholdFreq = nC / initialPop
        ax1.axhline(y=thresholdFreq, color='red', linestyle='--', lw=1.5, label='Rescue threshold')

    if rescueTime is not None:
        ax1.axvline(x=rescueTime, color='green', linestyle=':', lw=2, label='Rescue triggered')

    ax1.set_title(title)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    if savePath:
        plt.savefig(savePath, dpi=300)
    

def plotMultipleTrajectories(histories, title='Multiple simulation trajectories', savePath=None):
    plt.figure(figsize=(8, 4))
    for h in histories:
        plt.plot(np.arange(len(h)), h, alpha=0.5)
    plt.xlabel('Time step')
    plt.ylabel('Frequency of resistant (R)')
    plt.title(title)
    if savePath:
        plt.savefig(savePath, dpi=300)
        


def plotPrescueVsBeta(df, penetranceMode='variable', savePath=None):
    """
    Plots P_rescue vs β for all scenarios, with E1/E3 as dashed controls.
    Supports plotting for a single penetrance mode.
    """
    subset = df[df['penetrance'] == penetranceMode]
    scenarios = ['E1', 'E2', 'E3', 'E4']
    
    fig, ax = plt.subplots(figsize=(7,5))

    for scenario in scenarios:
        data = subset[subset['scenario'] == scenario]
        grouped = data.groupby('beta')['rescued'].mean()

        if grouped.empty:
            continue

        # Control scenarios (E1, E3) → dashed & lighter
        if scenario in ['E1', 'E3']:
            ax.plot(grouped.index, grouped.values, '--', lw=2, alpha=0.6, label=scenario)
        else:
            ax.plot(grouped.index, grouped.values, '-o', lw=2, label=scenario)

    ax.set_xlabel('Shielding strength β')
    ax.set_ylabel('Probability of rescue')
    ax.set_title(f'P_rescue vs β ({penetranceMode} penetrance)')
    ax.set_ylim(-0.05, 1.05)
    ax.legend()

    if savePath:
        plt.savefig(savePath, dpi=300, bbox_inches='tight')
    plt.close()

def plotPrescueHeatmap(df, scenario='E2', savePath=None):
    subset = df[(df['scenario'] == scenario) & (df['penetrance'] == 'variable')]
    betaVals = sorted(subset['beta'].unique())
    sABVals = sorted(subset['sAB'].unique())
    matrix = np.zeros((len(sABVals), len(betaVals)))

    for i, s in enumerate(sABVals):
        for j, b in enumerate(betaVals):
            val = subset[(subset['sAB'] == s) & (subset['beta'] == b)]['rescued'].mean()
            matrix[i, j] = val

    fig, ax = plt.subplots(figsize=(6,5))
    cax = ax.imshow(matrix, origin='lower', aspect='auto',
                    extent=[min(betaVals), max(betaVals), min(sABVals), max(sABVals)],
                    cmap='viridis')
    fig.colorbar(cax, label='P_rescue')

    ax.set_xlabel('Shielding Strength β')
    ax.set_ylabel('Antibiotic Strength s_AB')
    ax.set_title(f'Rescue Probability Heatmap ({scenario})')

    if savePath:
        plt.savefig(savePath, dpi=300, bbox_inches='tight')
    plt.close()

def plotAverageDynamics(batchHistories, title='Average Dynamics', savePath=None):
    times = sorted(batchHistories[0].keys())
    wtMeans = np.mean([[h[t]['WT'] for t in times] for h in batchHistories], axis=0)
    rMeans = np.mean([[h[t]['R'] for t in times] for h in batchHistories], axis=0)

    fig, ax = plt.subplots(figsize=(7,5))
    ax.plot(times, wtMeans, lw=2, label='WT', color='blue')
    ax.plot(times, rMeans, lw=2, label='R', color='red')
    # plot standard deviation as shaded area
    wtStd = np.std([[h[t]['WT'] for t in times] for h in batchHistories], axis=0)
    rStd = np.std([[h[t]['R'] for t in times] for h in batchHistories], axis=0)
    ax.fill_between(times, wtMeans - wtStd, wtMeans + wtStd, color='blue', alpha=0.2)
    ax.fill_between(times, rMeans - rStd, rMeans + rStd, color='red', alpha=0.2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Population')
    ax.set_title(title)
    ax.legend()

    if savePath:
        plt.savefig(savePath, dpi=300, bbox_inches='tight')
    plt.close()

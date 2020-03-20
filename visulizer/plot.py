import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import json
import os

# This is in a different directory because my virtual environment was being weird.

if __name__ == "__main__":
    bar_width = 0.35
    opacity = 0.8


    parser = ArgumentParser()
    parser.add_argument('--file', help='File to use that is generated from main.py', required=True)
    parser.add_argument('--out', help='Directory to save the simulation figures to', required=True)
    args = parser.parse_args()


    data = json.load(open(args.file, 'r'))
    sim_count = 0
    for simulation in data:
        fig, ax = plt.subplots()
        # avg_t = []
        # avg_p = []
        num_t = []
        bar_width = .35
        n_groups = len(data[simulation])
        
        index = np.arange(n_groups)  # number of things to graph
        for worker in data[simulation]:
            # avg_t.append(data[simulation][worker]["Average Time"])
            # avg_p.append(data[simulation][worker]["Average Pay"])
            num_t.append(data[simulation][worker]["Num Jobs"])
            
            
        # data1 = plt.bar(index, avg_t, bar_width, alpha=opacity, color='g', label='Average time per job')
        # data2 = plt.bar(index + bar_width, avg_p, bar_width, alpha=opacity, color='b', label='Average pay per job')
        data3 = plt.bar(index + 2*bar_width, num_t, bar_width, alpha=opacity, color='r', label='Number of jobs rewarded')
        
        for i in ax.patches:
            ax.text(i.get_x()+.05, i.get_height()+.31, \
                str(round(i.get_height(), 2)), fontsize=10)

        plt.xlabel('Worker')
        plt.ylabel('Scores')
        plt.title(f'Simulation: {sim_count}')
        plt.legend()

        sim_count += 1
        fname = f'{args.out}/simulation_{sim_count}.png'
        if os.path.exists(fname):
            fname.replace('.png', '_2.png')

        plt.savefig(fname)

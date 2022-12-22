import os
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np


if __name__ == "__main__":
    # results = pd.read_csv(os.path.join("new_results", "pictimo_results_with_distances.csv"))
    # distances = results.distance.dropna().to_list()
    # put the list here
    diatances = []
    distances.sort()
    length = len(distances)
    dis = []
    prob = []
    for distance in distances:
        if len(dis) == 0 or dis[-1] != distance:
            dis.append(distance)
            prob.append(1 / length)
        else:
            prob[-1] += 1 / length
    for i in range(len(prob)):
        if i != 0:
            prob[i] += prob[i - 1]
    plt.plot(dis, prob)
    plt.title("cdf")
    plt.savefig(os.path.join("new_results", "results_by_distance.png"))
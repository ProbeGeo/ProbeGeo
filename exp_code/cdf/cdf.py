import os
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np


def calculate(distances, label):
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
    plt.plot(dis, prob, linewidth=0.8, label=label)
#   plt.scatter(dis, prob, s=1, label=label)


if __name__ == "__main__":
    # put the list here
    
    ip2location = []
    with open('./exp_result/ip2location.txt', 'r') as f:
        for line in f:
            line = line.strip()
            ip2location.append(float(line))
    ip2location.sort()
    calculate(ip2location,'IP2Location Database')
    
    cbgMDGeo = []
    with open('./exp_result/cbgMDGeo.txt', 'r') as f:
        for line in f:
            line = line.strip()
            ip2location.append(float(line))
    calculate(cbgMDGeo,'CBG with MDGeo Landmark')
    cbgMDGeo.sort()
    
    cbgMDGeodynamic = []
    with open('./exp_result/cbgMDGeodynamic.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgMDGeodynamic.append(float(line))
    cbgMDGeodynamic.sort()
    calculate(cbgMDGeodynamic,'CBG with Dynamic MDGeo Landmark')
    
    cbgMDGeostatic = []
    with open('./exp_result/cbgMDGeostatic.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgMDGeostatic.append(float(line))
    cbgMDGeostatic.sort()
    calculate(cbgMDGeostatic,'CBG with Static MDGeo Landmark')
    
    cbgGeoCAM = []
    with open('./exp_result/cbgGeoCAM.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgGeoCAM.append(float(line))
    cbgGeoCAM.sort()
    calculate(cbgGeoCAM,'CBG with GeoCAM Landmark')
    
    cbgLandmarkMiner = []
    with open('./exp_result/cbgLandmarkMiner.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgLandmarkMiner.append(float(line))
    cbgLandmarkMiner.sort()
    calculate(cbgLandmarkMiner,'CBG with LandmarkMiner Landmark')
    
    cbgOpensource = []
    with open('./exp_result/cbgOpensource.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgOpensource.append(float(line))
    cbgOpensource.sort()
    calculate(cbgOpensource,'CBG with OpenSource Landmark')
    
    
    
    
    
    
    octantMDGeo = []
    with open('./exp_result/octantMDGeo.txt', 'r') as f:
        for line in f:
            line = line.strip()
            octantMDGeo.append(float(line))
    octantMDGeo.sort()
    calculate(octantMDGeo,'Octant with MDGeo Landmark')
    
    octantGeoCAM = []
    with open('./exp_result/octantMDGeo.txt', 'r') as f:
        for line in f:
            line = line.strip()
            octantMDGeo.append(float(line))
    octantMDGeo.sort()
    calculate(octantGeoCAM,'Octant with GeoCAM Landmark')
    
    octantLandmarkMiner = []
    with open('./exp_result/octantLandmarkMiner.txt', 'r') as f:
        for line in f:
            line = line.strip()
            octantLandmarkMiner.append(float(line))
    octantLandmarkMiner.sort()
    calculate(octantLandmarkMiner,'Octant with LandmarkMiner Landmark')
    
    octantOpensource = []
    with open('./exp_result/octantOpensource.txt', 'r') as f:
        for line in f:
            line = line.strip()
            octantOpensource.append(float(line))
    octantOpensource.sort()
    calculate(octantOpensource,'Octant with OpenSource Landmark')
    


    plt.legend(loc="lower right",fontsize=6)
    plt.xlabel('The deviation distance (KM)')
    plt.ylabel('CDF (%)')
    plt.xlim(0,300)
    plt.ylim(0,1)
    plt.savefig('results_by_distance.png')
#   plt.savefig('results_by_distance.svg', format='svg')
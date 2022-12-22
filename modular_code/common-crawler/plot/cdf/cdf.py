import os
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np


def calculate(distances, label, line_style):
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
    record = -1
    for i in range(len(prob)):
        if i != 0:
            prob[i] += prob[i - 1]
        if record == -1 and prob[i] >= 0.8:
            record = dis[i]
    plt.axvline(x=record, ymin=0, ymax=0.8, linestyle='--', linewidth=2, color='black')
    plt.axhline(y=0.8, xmin=0, xmax=record / 300, linestyle='--', linewidth=2, color='black')
    plt.plot(dis, prob, linewidth=4, label=label, linestyle=line_style)


if __name__ == "__main__":
    # put the list here
    # plt.set_color_cycle(['red', 'yellow', 'green', 'purlple', 'blue'])cbgMDGeo = []
    cbgMDGeo = []
    with open('./exp_result/cbgMDGeo.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgMDGeo.append(float(line))
    cbgMDGeo.sort()
    calculate(cbgMDGeo, 'ProbeGeo', '-')
    
    
    cbgGeoCAM = []
    with open('./exp_result/cbgGeoCAM.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgGeoCAM.append(float(line))
    cbgGeoCAM.sort()
    calculate(cbgGeoCAM,'GeoCAM', '-.')
    
    cbgLandmarkMiner = []
    with open('./exp_result/cbgLandmarkMiner.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgLandmarkMiner.append(float(line))
    cbgLandmarkMiner.sort()
    calculate(cbgLandmarkMiner,'LandmarkMiner', '--')
    
    cbgOpensource = []
    with open('./exp_result/cbgOpensource.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgOpensource.append(float(line))
    cbgOpensource.sort()
    calculate(cbgOpensource,'OpenSource', ':')

    ip2location = []
    with open('./exp_result/ip2location.txt', 'r') as f:
        for line in f:
            line = line.strip()
            ip2location.append(float(line))
    ip2location.sort()
    calculate(ip2location,'IP2Location', (5, (10, 3)))

    plt.legend(loc="lower right", fontsize=20)
    plt.xlabel('The deviation distance (KM)', fontsize=20)
    plt.ylabel('CDF', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlim(0, 300)
    plt.ylim(0, 1)
    plt.title('(a) The geolocation comparison of CBG.', y=-0.32, fontsize=25, fontweight='semibold', font='Times New Roman')
    # plt.title('(b) The geolocation comparison of Octant.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    # plt.title('(c) The geolocation comparison of Spotter.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    # plt.title('(d) Validation of the validity of new types of landmarks.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    plt.savefig('result_1.png', bbox_inches='tight', dpi=600)
    plt.close()

    
    
    octantMDGeo = []
    with open('./exp_result/octantMDGeo.txt', 'r') as f:
        for line in f:
            line = line.strip()
            octantMDGeo.append(float(line))
    octantMDGeo.sort()
    calculate(octantMDGeo,'ProbeGeo', '-')
    
    
    
    
    
    octantGeoCAM = []
    with open('./exp_result/octantGeoCAM.txt', 'r') as f:
        for line in f:
            line = line.strip()
            octantGeoCAM.append(float(line))
    octantGeoCAM.sort()
    calculate(octantGeoCAM,'GeoCAM', '-.')
    
    octantLandmarkMiner = []
    with open('./exp_result/octantLandmarkMiner.txt', 'r') as f:
        for line in f:
            line = line.strip()
            octantLandmarkMiner.append(float(line))
    octantLandmarkMiner.sort()
    calculate(octantLandmarkMiner,'LandmarkMiner', '--')
    
    octantOpensource = []
    with open('./exp_result/octantOpensource.txt', 'r') as f:
        for line in f:
            line = line.strip()
            octantOpensource.append(float(line))
    octantOpensource.sort()
    calculate(octantOpensource,'OpenSource', ':')
    
    
    ip2location = []
    with open('./exp_result/ip2location.txt', 'r') as f:
        for line in f:
            line = line.strip()
            ip2location.append(float(line))
    ip2location.sort()
    calculate(ip2location,'IP2Location', (5, (10, 3)))

    plt.legend(loc="lower right", fontsize=20)
    plt.xlabel('The deviation distance (KM)', fontsize=20)
    plt.ylabel('CDF', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlim(0, 300)
    plt.ylim(0, 1)
    # plt.title('(a) The geolocation comparison of CBG.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    plt.title('(b) The geolocation comparison of Octant.', y=-0.32, fontsize=25, fontweight='semibold', font='Times New Roman')
    # plt.title('(c) The geolocation comparison of Spotter.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    # plt.title('(d) Validation of the validity of new types of landmarks.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    plt.savefig('result_2.png', bbox_inches='tight', dpi=600)
    plt.close()
    


    spotterMDGeo = []
    with open('./exp_result/spotterMDGeo.txt', 'r') as f:
        for line in f:
            line = line.strip()
            spotterMDGeo.append(float(line))
    spotterMDGeo.sort()
    calculate(spotterMDGeo,'ProbeGeo', '-')

    spotterGeoCAM = []
    with open('./exp_result/spotterGeoCAM.txt', 'r') as f:
        for line in f:
            line = line.strip()
            spotterGeoCAM.append(float(line))
    spotterGeoCAM.sort()
    calculate(spotterGeoCAM,'GeoCAM', '-.')

    spotterLandmarkMiner = []
    with open('./exp_result/spotterLandmarkMiner.txt', 'r') as f:
        for line in f:
            line = line.strip()
            spotterLandmarkMiner.append(float(line))
    spotterLandmarkMiner.sort()
    calculate(spotterLandmarkMiner,'LandmarkMiner', '--')

    spotterOpensource = []
    with open('./exp_result/spotterOpensource.txt', 'r') as f:
        for line in f:
            line = line.strip()
            spotterOpensource.append(float(line))
    spotterOpensource.sort()
    calculate(spotterOpensource,'OpenSource', ':')

    ip2location = []
    with open('./exp_result/ip2location.txt', 'r') as f:
        for line in f:
            line = line.strip()
            ip2location.append(float(line))
    ip2location.sort()
    calculate(ip2location,'IP2Location', (5, (10, 3)))

    plt.legend(loc="lower right", fontsize=20)
    plt.xlabel('The deviation distance (KM)', fontsize=20)
    plt.ylabel('CDF', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlim(0, 300)
    plt.ylim(0, 1)
    # plt.title('(a) The geolocation comparison of CBG.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    # plt.title('(b) The geolocation comparison of Octant.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    plt.title('(c) The geolocation comparison of Spotter.', y=-0.32, fontsize=25, fontweight='semibold', font='Times New Roman')
    # plt.title('(d) Validation of the validity of new types of landmarks.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    plt.savefig('result_3.png', bbox_inches='tight', dpi=600)
    plt.close()



    cbgMDGeo = []
    with open('./exp_result/cbgMDGeo.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgMDGeo.append(float(line))
    cbgMDGeo.sort()
    calculate(cbgMDGeo,'ProbeGeo', '-')

    cbgGeoCAM = []
    with open('./exp_result/cbgGeoCAM.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgGeoCAM.append(float(line))
    cbgGeoCAM.sort()
    calculate(cbgGeoCAM,'GeoCAM', '-.')
    
    cbgMDGeodynamic = []
    with open('./exp_result/cbgMDGeodynamic.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgMDGeodynamic.append(float(line))
    cbgMDGeodynamic.sort()
    calculate(cbgMDGeodynamic,'Probe ProbeGeo', '--')
    
    cbgMDGeostatic = []
    with open('./exp_result/cbgMDGeostatic.txt', 'r') as f:
        for line in f:
            line = line.strip()
            cbgMDGeostatic.append(float(line))
    cbgMDGeostatic.sort()
    calculate(cbgMDGeostatic,'Common ProbeGeo', ':')
    
    ip2location = []
    with open('./exp_result/ip2location.txt', 'r') as f:
        for line in f:
            line = line.strip()
            ip2location.append(float(line))
    ip2location.sort()
    calculate(ip2location,'IP2Location', (5, (10, 3)))

    plt.legend(loc="lower right", fontsize=18)
    plt.xlabel('The deviation distance (KM)', fontsize=20)
    plt.ylabel('CDF', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlim(0, 300)
    plt.ylim(0, 1)
    # plt.title('(a) The geolocation comparison of CBG.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    # plt.title('(b) The geolocation comparison of Octant.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    # plt.title('(c) The geolocation comparison of Spotter.', y=-0.32, fontsize=16, fontweight='semibold', font='Times New Roman')
    plt.title('(d) Validity of landmark types.(CBG)', y=-0.32, fontsize=25, fontweight='semibold', font='Times New Roman')
    plt.savefig('result_4.png', bbox_inches='tight', dpi=600)
    plt.close()
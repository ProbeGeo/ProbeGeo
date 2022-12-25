import os
import pandas as pd


results = pd.read_csv(os.path.join('..', 'data', 'result.csv'))
latitudes = results['latitude'].tolist()
longitudes = results['longitude'].tolist()

with open('lat_lon.txt', 'w') as f:
    for i in range(len(latitudes)):
        f.write(str(latitudes[i]) + ',' + str(longitudes[i]) + '\n')
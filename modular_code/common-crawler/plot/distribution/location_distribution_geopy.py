import geopy
from geopy.geocoders import Nominatim
import pandas as pd
import os
from tqdm import tqdm
from collections import defaultdict
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--start', type = int, default = 0)
args = parser.parse_args()

if __name__ == "__main__":
    geolocator = Nominatim(user_agent="location_distribution_geopy.py")
    results = pd.read_csv(os.path.join('..', 'data', 'geocam_results.csv'))
    types = results['type'].tolist()
    ips = results['ip'].tolist()
    latitudes = results['latitude'].tolist()
    longitudes = results['longitude'].tolist()
    start = args.start
    end = min(start + 10000, len(latitudes))
    all_results = []
    error_count = 0
    for i in tqdm(range(start, end)):
        result = {'ip': ips[i], 'latitude': latitudes[i], 'longitude': longitudes[i]}
        try:
            location = geolocator.reverse(str(latitudes[i]) + ',' + str(longitudes[i]))
            result['address'] = {}
            result['display_name'] = ''
            result['location_raw'] = {}
            if location:
                location_raw = location.raw
                result['location_raw'] = location_raw
                address = location_raw['address'] if 'address' in location_raw else {}
                display_name = location_raw['display_name'] if 'display_name' in location_raw else ''
                result['address'] = address
                result['display_name'] = display_name
        except Exception as e:
            error_count += 1
        all_results.append(result)
    print('Error count: {}'.format(error_count))
    with open(os.path.join('..', 'data', 'geocam_nominatim_detailed_result_' + str(start) + '_' + str(end) + '.json'), 'w') as f:
        json.dump(all_results, f)



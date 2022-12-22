import json
import os
from collections import defaultdict


if __name__ == "__main__":
    count_dict = defaultdict(int)
    with open(os.path.join('..', 'data', 'nominatim_detailed_result.json'), 'r') as f:
        data = json.load(f)
    for d in data:
        if 'address' in d:
            address = d['address']
            for k in address.keys():
                count_dict[k] += 1
        else:
            ip = d['ip']
            latitude = d['latitude']
            longitude = d['longitude']
            print('No address for ip: {}, latitude: {}, longitude: {}'.format(ip, latitude, longitude))
    count_dict = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    print([x[0] for x in count_dict])
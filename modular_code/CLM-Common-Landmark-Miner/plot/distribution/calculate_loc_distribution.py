import os
from matplotlib import pyplot as plt
import pandas as pd


if __name__ == "__main__":
    results = pd.read_csv(os.path.join('..', 'data', 'detailed_result.csv'))
    results.fillna('', inplace = True)
    countries = {}
    provinces = {}
    cities = {}
    precision = {'none': 0, 'country': 0, 'province': 0, 'city': 0, 'district': 0, 'town': 0, 'street': 0}
    for index, result in results.iterrows():
        country = result['country']
        province = result['province']
        city = result['city']
        district = result['district']
        town = result['town']
        street = result['street']
        if country not in countries:
            countries[country] = 0
        countries[country] += 1
        if province not in provinces:
            provinces[province] = 0
        provinces[province] += 1
        if city not in cities:
            cities[city] = 0
        cities[city] += 1
        if street != '' and street != None:
            precision['street'] += 1
        elif town != '' and town != None:
            precision['town'] += 1
        elif district != '' and district != None:
            precision['district'] += 1
        elif city != '' and city != None:
            precision['city'] += 1
        elif province != '' and province != None:
            precision['province'] += 1
        elif country != '' and country != None:
            precision['country'] += 1
        else:
            precision['none'] += 1
    print('Precision:')
    for key in precision:
        print(key, precision[key])
    # print('Countries:')
    # print(countries)
    # print('Provinces:')
    # print(provinces)
    # print('Cities:')
    # print(cities)
    countries = sorted(countries.items(), key = lambda x: x[1], reverse = True)
    provinces = sorted(provinces.items(), key = lambda x: x[1], reverse = True)
    cities.pop('')
    cities = sorted(cities.items(), key = lambda x: x[1], reverse = True)
    
    print("Top 10 countries:")
    for i in range(10):
        print(countries[i])
    print("Top 10 provinces:")
    for i in range(10):
        print(provinces[i])
    print("Top 10 cities:")
    for i in range(10):
        print(cities[i])

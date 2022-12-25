import os
import pandas as pd
import numpy as np
from collections import defaultdict


if __name__ == "__main__":
    results = pd.read_csv(os.path.join('..', 'data', 'geocam_detailed_result.csv'))
    results.fillna('', inplace = True)
    total = len(results)
    countries = defaultdict(int)
    provinces = defaultdict(int)
    cities = defaultdict(int)
    districts = defaultdict(int)
    streets = defaultdict(int)
    precision = defaultdict(int)
    controllable_countries = defaultdict(int)
    controllable_provinces = defaultdict(int)
    controllable_cities = defaultdict(int)
    controllable_districts = defaultdict(int)
    controllable_streets = defaultdict(int)
    controllable_precision = defaultdict(int)
    uncontrollable_countries = defaultdict(int)
    uncontrollable_provinces = defaultdict(int)
    uncontrollable_cities = defaultdict(int)
    uncontrollable_districts = defaultdict(int)
    uncontrollable_streets = defaultdict(int)
    uncontrollable_precision = defaultdict(int)
    for index, result in results.iterrows():
        type_ = result['type']
        country = result['country']
        province = result['province']
        city = result['city']
        district = result['district']
        street = result['street']
        if street != '':
            precision['street'] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_precision['street'] += 1
            else:
                uncontrollable_precision['street'] += 1
        elif district != '':
            precision['district'] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_precision['district'] += 1
            else:
                uncontrollable_precision['district'] += 1
        elif city != '':
            precision['city'] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_precision['city'] += 1
            else:
                uncontrollable_precision['city'] += 1
        elif province != '':
            precision['province'] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_precision['province'] += 1
            else:
                uncontrollable_precision['province'] += 1
        elif country != '':
            precision['country'] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_precision['country'] += 1
            else:
                uncontrollable_precision['country'] += 1
        else:
            precision['unknown'] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_precision['unknown'] += 1
            else:
                uncontrollable_precision['unknown'] += 1
        if country != '':
            countries[country] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_countries[country] += 1
            else:
                uncontrollable_countries[country] += 1
        if province != '':
            provinces[province] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_provinces[province] += 1
            else:
                uncontrollable_provinces[province] += 1
        if city != '':
            cities[city] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_cities[city] += 1
            else:
                uncontrollable_cities[city] += 1
        if district != '':
            districts[district] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_districts[district] += 1
            else:
                uncontrollable_districts[district] += 1
        if street != '':
            streets[street] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_streets[street] += 1
            else:
                uncontrollable_streets[street] += 1
    
    countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
    provinces = sorted(provinces.items(), key=lambda x: x[1], reverse=True)
    cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)
    districts = sorted(districts.items(), key=lambda x: x[1], reverse=True)
    streets = sorted(streets.items(), key=lambda x: x[1], reverse=True)
    controllable_countries = sorted(controllable_countries.items(), key=lambda x: x[1], reverse=True)
    controllable_provinces = sorted(controllable_provinces.items(), key=lambda x: x[1], reverse=True)
    controllable_cities = sorted(controllable_cities.items(), key=lambda x: x[1], reverse=True)
    controllable_districts = sorted(controllable_districts.items(), key=lambda x: x[1], reverse=True)
    controllable_streets = sorted(controllable_streets.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_countries = sorted(uncontrollable_countries.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_provinces = sorted(uncontrollable_provinces.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_cities = sorted(uncontrollable_cities.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_districts = sorted(uncontrollable_districts.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_streets = sorted(uncontrollable_streets.items(), key=lambda x: x[1], reverse=True)

    with open(os.path.join('..', 'data', 'geocam_countries_baidu.csv'), 'w', encoding='utf-8') as f:
        f.write('country,count,controllable_country,count,uncontrollable_country,count\n')
        for (country, total_count), (controllable_country, controllable_count), (uncontrollable_country, uncontrollable_count) in zip(countries, controllable_countries, uncontrollable_countries):
            country = country.replace(',', '.')
            controllable_country = controllable_country.replace(',', '.')
            uncontrollable_country = uncontrollable_country.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(country, total_count, controllable_country, controllable_count, uncontrollable_country, uncontrollable_count))
    
    with open(os.path.join('..', 'data', 'geocam_provinces_baidu.csv'), 'w', encoding='utf-8') as f:
        f.write('province,count,controllable_province,count,uncontrollable_province,count\n')
        for (province, total_count), (controllable_province, controllable_count), (uncontrollable_province, uncontrollable_count) in zip(provinces, controllable_provinces, uncontrollable_provinces):
            province = province.replace(',', '.')
            controllable_province = controllable_province.replace(',', '.')
            uncontrollable_province = uncontrollable_province.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(province, total_count, controllable_province, controllable_count, uncontrollable_province, uncontrollable_count))

    with open(os.path.join('..', 'data', 'geocam_cities_baidu.csv'), 'w', encoding='utf-8') as f:
        f.write('city,count,controllable_city,count,uncontrollable_city,count\n')
        for (city, total_count), (controllable_city, controllable_count), (uncontrollable_city, uncontrollable_count) in zip(cities, controllable_cities, uncontrollable_cities):
            city = city.replace(',', '.')
            controllable_city = controllable_city.replace(',', '.')
            uncontrollable_city = uncontrollable_city.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(city, total_count, controllable_city, controllable_count, uncontrollable_city, uncontrollable_count))

    with open(os.path.join('..', 'data', 'geocam_districts_baidu.csv'), 'w', encoding='utf-8') as f:
        f.write('district,count,controllable_district,count,uncontrollable_district,count\n')
        for (district, total_count), (controllable_district, controllable_count), (uncontrollable_district, uncontrollable_count) in zip(districts, controllable_districts, uncontrollable_districts):
            district = district.replace(',', '.')
            controllable_district = controllable_district.replace(',', '.')
            uncontrollable_district = uncontrollable_district.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(district, total_count, controllable_district, controllable_count, uncontrollable_district, uncontrollable_count))

    with open(os.path.join('..', 'data', 'geocam_streets_baidu.csv'), 'w', encoding='utf-8') as f:
        f.write('street,count,controllable_street,count,uncontrollable_street,count\n')
        for (street, total_count), (controllable_street, controllable_count), (uncontrollable_street, uncontrollable_count) in zip(streets, controllable_streets, uncontrollable_streets):
            street = street.replace(',', '.')
            controllable_street = controllable_street.replace(',', '.')
            uncontrollable_street = uncontrollable_street.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(street, total_count, controllable_street, controllable_count, uncontrollable_street, uncontrollable_count))

    print(precision)
    print(controllable_precision)
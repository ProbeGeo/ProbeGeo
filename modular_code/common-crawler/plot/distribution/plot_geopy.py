import os
import pandas as pd
import numpy as np
from collections import defaultdict
import json


# location hierarchy list without overlap from all_list
building_list = ['building', 'house_number', 'isolated_dwelling', 'amenity', 'shop', 'historic', 'tourism', 'office', 'leisure', 'man_made', 'retail', 'industrial', 'healthcare', 'commercial', 'emergency', 'aeroway', 'club', 'department']
street_list = ['road', 'highway', 'railway', 'aerialway', 'junction', 'neighbourhood', 'residential', 'city_block']
town_list = ['town', 'township', 'borough', 'suburb', 'subdivision', 'subdistrict', 'subward', 'quarter', 'square', 'village', 'hamlet', 'farm', 'farmyard', 'allotments']
district_list = ['city_district', 'district', 'county',]
city_list = ['city', 'municipality', 'municipal_federation', 'state_district',]
province_list = ['state', 'province', 'archipelago',]
country_list = ['country', 'ISO3166-2-lvl', 'ISO3166-2-lvl2', 'ISO3166-2-lvl3', 'ISO3166-2-lvl4', 'ISO3166-2-lvl5', 'ISO3166-2-lvl6', 'ISO3166-2-lvl7', 'ISO3166-2-lvl8', 'ISO3166-2-lvl10', 'ISO3166-2-lvl15', 'landuse']


if __name__ == "__main__":
    results = json.load(open(os.path.join('..', 'data', 'geocam_nominatim_detailed_result_0_8487.json'), 'r', encoding='utf-8'))
    total = len(results)
    countries = defaultdict(int)
    provinces = defaultdict(int)
    cities = defaultdict(int)
    districts = defaultdict(int)
    streets = defaultdict(int)
    buildings = defaultdict(int)
    precision = defaultdict(int)
    controllable_countries = defaultdict(int)
    controllable_provinces = defaultdict(int)
    controllable_cities = defaultdict(int)
    controllable_districts = defaultdict(int)
    controllable_streets = defaultdict(int)
    controllable_buildings = defaultdict(int)
    controllable_precision = defaultdict(int)
    uncontrollable_countries = defaultdict(int)
    uncontrollable_provinces = defaultdict(int)
    uncontrollable_cities = defaultdict(int)
    uncontrollable_districts = defaultdict(int)
    uncontrollable_streets = defaultdict(int)
    uncontrollable_buildings = defaultdict(int)
    uncontrollable_precision = defaultdict(int)
    for i, result in enumerate(results):
        
        type_ = "uncontrollable"
        address = result['address'] if 'address' in result else {}
        country = ''
        province = ''
        city = ''
        district = ''
        street = ''
        building = ''
        if 'country' in address:
            country = address['country']
        else:
            for key in address.keys():
                if key in country_list:
                    country = address[key]
                    break
        if 'province' in address:
            province = address['province']
        else:
            for key in address.keys():
                if key in province_list:
                    province = address[key]
                    break
        if 'city' in address:
            city = address['city']
        else:
            for key in address.keys():
                if key in city_list:
                    city = address[key]
                    break
        if 'district' in address:
            district = address['district']
        else:
            for key in address.keys():
                if key in district_list:
                    district = address[key]
                    break
        if 'street' in address:
            street = address['street']
        else:
            for key in address.keys():
                if key in street_list:
                    street = address[key]
                    break
        if 'building' in address:
            building = address['building']
        else:
            for key in address.keys():
                if key in building_list:
                    building = address[key]
                    break
        if building != '':
            precision['building'] += 1
            if type_  == 'lg':
                controllable_precision['building'] += 1
            else:
                uncontrollable_precision['building'] += 1
        elif street != '':
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
        if building != '':
            buildings[building] += 1
            if type_ == 'lg' or type_ == 'pf':
                controllable_buildings[building] += 1
            else:
                uncontrollable_buildings[building] += 1
    
    countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
    provinces = sorted(provinces.items(), key=lambda x: x[1], reverse=True)
    cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)
    districts = sorted(districts.items(), key=lambda x: x[1], reverse=True)
    streets = sorted(streets.items(), key=lambda x: x[1], reverse=True)
    buildings = sorted(buildings.items(), key=lambda x: x[1], reverse=True)
    controllable_countries = sorted(controllable_countries.items(), key=lambda x: x[1], reverse=True)
    controllable_provinces = sorted(controllable_provinces.items(), key=lambda x: x[1], reverse=True)
    controllable_cities = sorted(controllable_cities.items(), key=lambda x: x[1], reverse=True)
    controllable_districts = sorted(controllable_districts.items(), key=lambda x: x[1], reverse=True)
    controllable_streets = sorted(controllable_streets.items(), key=lambda x: x[1], reverse=True)
    controllable_buildings = sorted(controllable_buildings.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_countries = sorted(uncontrollable_countries.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_provinces = sorted(uncontrollable_provinces.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_cities = sorted(uncontrollable_cities.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_districts = sorted(uncontrollable_districts.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_streets = sorted(uncontrollable_streets.items(), key=lambda x: x[1], reverse=True)
    uncontrollable_buildings = sorted(uncontrollable_buildings.items(), key=lambda x: x[1], reverse=True)

    with open(os.path.join('..', 'data', 'geocam_countries_nominatim.csv'), 'w', encoding='utf-8') as f:
        f.write('country,count,controllable_country,count,uncontrollable_country,count\n')
        for (country, total_count), (controllable_country, controllable_count), (uncontrollable_country, uncontrollable_count) in zip(countries, controllable_countries, uncontrollable_countries):
            country = country.replace(',', '.')
            controllable_country = controllable_country.replace(',', '.')
            uncontrollable_country = uncontrollable_country.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(country, total_count, controllable_country, controllable_count, uncontrollable_country, uncontrollable_count))
    
    with open(os.path.join('..', 'data', 'geocam_provinces_nominatim.csv'), 'w', encoding='utf-8') as f:
        f.write('province,count,controllable_province,count,uncontrollable_province,count\n')
        for (province, total_count), (controllable_province, controllable_count), (uncontrollable_province, uncontrollable_count) in zip(provinces, controllable_provinces, uncontrollable_provinces):
            province = province.replace(',', '.')
            controllable_province = controllable_province.replace(',', '.')
            uncontrollable_province = uncontrollable_province.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(province, total_count, controllable_province, controllable_count, uncontrollable_province, uncontrollable_count))

    with open(os.path.join('..', 'data', 'geocam_cities_nominatim.csv'), 'w', encoding='utf-8') as f:
        f.write('city,count,controllable_city,count,uncontrollable_city,count\n')
        for (city, total_count), (controllable_city, controllable_count), (uncontrollable_city, uncontrollable_count) in zip(cities, controllable_cities, uncontrollable_cities):
            city = city.replace(',', '.')
            controllable_city = controllable_city.replace(',', '.')
            uncontrollable_city = uncontrollable_city.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(city, total_count, controllable_city, controllable_count, uncontrollable_city, uncontrollable_count))

    with open(os.path.join('..', 'data', 'geocam_districts_nominatim.csv'), 'w', encoding='utf-8') as f:
        f.write('district,count,controllable_district,count,uncontrollable_district,count\n')
        for (district, total_count), (controllable_district, controllable_count), (uncontrollable_district, uncontrollable_count) in zip(districts, controllable_districts, uncontrollable_districts):
            district = district.replace(',', '.')
            controllable_district = controllable_district.replace(',', '.')
            uncontrollable_district = uncontrollable_district.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(district, total_count, controllable_district, controllable_count, uncontrollable_district, uncontrollable_count))

    with open(os.path.join('..', 'data', 'geocam_streets_nominatim.csv'), 'w', encoding='utf-8') as f:
        f.write('street,count,controllable_street,count,uncontrollable_street,count\n')
        for (street, total_count), (controllable_street, controllable_count), (uncontrollable_street, uncontrollable_count) in zip(streets, controllable_streets, uncontrollable_streets):
            street = street.replace(',', '.')
            controllable_street = controllable_street.replace(',', '.')
            uncontrollable_street = uncontrollable_street.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(street, total_count, controllable_street, controllable_count, uncontrollable_street, uncontrollable_count))

    with open(os.path.join('..', 'data', 'geocam_buildings_nominatim.csv'), 'w', encoding='utf-8') as f:
        f.write('building,count,controllable_building,count,uncontrollable_building,count\n')
        for (building, total_count), (controllable_building, controllable_count), (uncontrollable_building, uncontrollable_count) in zip(buildings, controllable_buildings, uncontrollable_buildings):
            building = building.replace(',', '.')
            controllable_building = controllable_building.replace(',', '.')
            uncontrollable_building = uncontrollable_building.replace(',', '.')
            f.write('{},{},{},{},{},{}\n'.format(building, total_count, controllable_building, controllable_count, uncontrollable_building, uncontrollable_count))

    print(precision)
    print(controllable_precision)
    print(uncontrollable_precision)
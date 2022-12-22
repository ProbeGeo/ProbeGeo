from geo_translator import location_translator
import pandas as pd
import os
from tqdm import tqdm


if __name__ == "__main__":
    results = pd.read_csv(os.path.join('..', 'data', 'geocam_results.csv'))
    types = results['type'].tolist()
    ips = results['ip'].tolist()
    latitudes = results['latitude'].tolist()
    longitudes = results['longitude'].tolist()
    formatted_addresses = []
    sematic_descriptions = []
    countries = []
    provinces = []
    cities = []
    districts = []
    towns = []
    streets = []
    distances = []
    poi_names = []
    poi_distances = []

    location_inquirier = location_translator()
    for latitude, longitude in tqdm(zip(latitudes, longitudes), total = len(latitudes)):
        success, formatted_address, sematic_description, country, province, city, district, town, street, distance, poi_name, poi_distance = location_inquirier.translate_latitude_longitude(latitude, longitude)
        formatted_addresses.append(formatted_address)
        sematic_descriptions.append(sematic_description)
        countries.append(country)
        provinces.append(province)
        cities.append(city)
        districts.append(district)
        towns.append(town)
        streets.append(street)
        distances.append(distance)
        poi_names.append(poi_name)
        poi_distances.append(poi_distance)

    data_frame = pd.DataFrame({'type': types, 'ip': ips, 'latitude': latitudes, 'longitude': longitudes, 'formatted_address': formatted_addresses, 'sematic_description': sematic_descriptions, 'country': countries, 'province': provinces, 'city': cities, 'district': districts, 'town': towns, 'street': streets, 'distance': distances, 'poi_name': poi_names, 'poi_distance': poi_distances})
    data_frame.to_csv(os.path.join('..', 'data', 'geocam_detailed_result.csv'), index = False)

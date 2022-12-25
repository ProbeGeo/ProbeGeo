import os
from ip_translator import Ip_translator
import pandas as pd
from haversine import haversine


if __name__ == "__main__":
    ip_translator = Ip_translator()
    pictimo_results = pd.read_csv("pictimo_results.csv")

    ip_list = pictimo_results["ip"].tolist()
    print("get ip list: ", len(ip_list))
    ip_set = set(ip_list)
    print("get ip set: ", len(ip_set))
    
    # caculate distance
    for i in pictimo_results.index:
        ip, latitude, longitude = pictimo_results["ip"][i], pictimo_results["latitude"][i], pictimo_results["longitude"][i]
        valid, continent_name, continent_code, country_name, country_code, region_name, region_code, city, real_latitude, real_longitude = ip_translator.get_geo_of_ip(ip)
        if not valid:
            print("get geo info fail: ", ip)
            continue
        pictimo_results.loc[i, "city_keycdn"] = city
        pictimo_results.loc[i, "region_code_keycdn"] = region_code
        pictimo_results.loc[i, "region_name_keycdn"] = region_name
        pictimo_results.loc[i, "country_code_keycdn"] = country_code
        pictimo_results.loc[i, "country_name_keycdn"] = country_name
        pictimo_results.loc[i, "continent_code_keycdn"] = continent_code
        pictimo_results.loc[i, "continent_name_keycdn"] = continent_name
        pictimo_results.loc[i, "latitude_keycdn"] = real_latitude
        pictimo_results.loc[i, "longitude_keycdn"] = real_longitude
        if real_latitude == None or real_longitude == None:
            pictimo_results.loc[i, "distance"] = -1
            continue
        try:
            distance = haversine((float(latitude), float(longitude)), (float(real_latitude), float(real_longitude)), unit='km')
            pictimo_results.loc[i, "distance"] = distance
            print(i, distance, latitude, longitude, real_latitude, real_longitude)
        except Exception as e:
            print(e)
            print("error: ", ip, latitude, longitude, real_latitude, real_longitude)
    pictimo_results.to_csv("pictimo_results_with_distances.csv", index=False)
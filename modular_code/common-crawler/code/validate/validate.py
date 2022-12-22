import requests
import os
import pandas as pd


if __name__ == "__main__":
    ip_geo_list = pd.read_csv("../landmark_generation/ip_geo.csv")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    for idx, item in ip_geo_list.iterrows():
        latitude = item["latitude"]
        longitude = item["longitude"]
        response = requests.get("http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(latitude) + "," + str(longitude) + "&sensor=false", headers=headers)
        print(response.text)
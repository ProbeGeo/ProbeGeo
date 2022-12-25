import requests
import os
from bs4 import BeautifulSoup
import re


class Ip_translator:
    def __init__(self):
        self.base_url = "https://tools.keycdn.com/geo.json"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'keycdn-tools:https://www.baidu.com'
        })

    def get_geo_of_ip(self, ip):
        try:
            response = self.session.get(self.base_url, params={"host": ip}, timeout=5)
        except:
            return False, None, None, None, None, None, None, None, None, None
        if response.status_code == 200:
            try:
                geo_info = response.json()["data"]["geo"]
                continent_name, continent_code = geo_info["continent_name"], geo_info["continent_code"]
                country_name, country_code = geo_info["country_name"], geo_info["country_code"]
                region_name, region_code = geo_info["region_name"], geo_info["region_code"]
                city = geo_info["city"]
                latitude, longitude = geo_info["latitude"], geo_info["longitude"]
                return True, continent_name, continent_code, country_name, country_code, region_name, region_code, city, latitude, longitude
            except:
                return False, None, None, None, None, None, None, None, None, None
        else:
            return False, None, None, None, None, None, None, None, None, None

    def get_geo_of_hostname(self, hostname):
        try:
            response = self.session.get(self.base_url, params={"host": hostname}, timeout=5)
        except:
            return False, "request get fail", None, None, None, None, None, None, None, None, None
        if response.status_code == 200:
            try:
                geo_info = response.json()["data"]["geo"]
                ip = geo_info["ip"]
                continent_name, continent_code = geo_info["continent_name"], geo_info["continent_code"]
                country_name, country_code = geo_info["country_name"], geo_info["country_code"]
                region_name, region_code = geo_info["region_name"], geo_info["region_code"]
                city = geo_info["city"]
                latitude, longitude = geo_info["latitude"], geo_info["longitude"]
                return True, ip, continent_name, continent_code, country_name, country_code, region_name, region_code, city, latitude, longitude
            except:
                return False, "get info fail", None, None, None, None, None, None, None, None, None 
        else:
            return False, "response status not 200", None, None, None, None, None, None, None, None, None


if __name__ == "__main__":
    ip_translator = Ip_translator()
    print(ip_translator.get_geo_of_ip("103.135.247.228"))
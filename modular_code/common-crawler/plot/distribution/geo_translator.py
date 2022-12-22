import requests
import time
import json


class location_translator():
    def __init__(self):
        self.base_url = 'https://api.map.baidu.com/reverse_geocoding/v3/'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
        self.session.headers.update({'Referer': 'https://www.piliang.tech/'})
        self.session.headers.update({'Host': 'api.map.baidu.com'})
        self.params = {'ak': 'gQsCAgCrWsuN99ggSIjGn5nO', 'output': 'json', 'extensions_poi': '1', 'coordtype': 'wgs84ll', 'extensions_poi': '1', 'callback': 'showBaiduResult1', 'location': '39.1,116.7'}

    def translate_latitude_longitude(self, latitude, longitude):
        self.params['location'] = str(latitude) + ',' + str(longitude)
        response = self.session.get(self.base_url, params = self.params)
        start_word = 'showBaiduResult1&&showBaiduResult1('
        end_word = ')'
        result = json.loads(response.text[len(start_word):-len(end_word)])
        if result['status'] == 0:
            result = result['result']
            formatted_address = result['formatted_address']
            sematic_description = result['sematic_description']
            country = result['addressComponent']['country']
            province = result['addressComponent']['province']
            city = result['addressComponent']['city']
            district = result['addressComponent']['district']
            town = result['addressComponent']['town']
            street = result['addressComponent']['street']
            distance = result['addressComponent']['distance']
            if len(result['pois']) > 0:
                poi_name = result['pois'][0]['addr'] + result['pois'][0]['name']
                poi_distance = result['pois'][0]['distance']
            else:
                poi_name = ''
                poi_distance = ''
            return True, formatted_address, sematic_description, country, province, city, district, town, street, distance, poi_name, poi_distance
        else:
            return False, None, None, None, None, None, None, None, None, None, None, None

if __name__ == '__main__':
    location_inquirier = location_translator()
    print(location_inquirier.translate_latitude_longitude(39.90403, 116.407526))
    print(location_inquirier.translate_latitude_longitude(30.90, 117.07526))

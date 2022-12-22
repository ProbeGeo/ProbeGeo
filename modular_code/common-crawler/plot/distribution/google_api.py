import requests
import json
import os

# sample result
# {
#     "results": [
#         {
#             "address_components": [
#                 {
#                     "long_name": "1600",
#                     "short_name": "1600",
#                     "types": [
#                         "street_number"
#                     ]
#                 },
#                 {
#                     "long_name": "Amphitheatre Parkway",
#                     "short_name": "Amphitheatre Pkwy",
#                     "types": [
#                         "route"
#                     ]
#                 },
#                 {
#                     "long_name": "Mountain View",
#                     "short_name": "Mountain View",
#                     "types": [
#                         "locality",
#                         "political"
#                     ]
#                 },
#                 {
#                     "long_name": "Santa Clara County",
#                     "short_name": "Santa Clara County",
#                     "types": [
#                         "administrative_area_level_2",
#                         "political"
#                     ]
#                 },
#                 {
#                     "long_name": "California",
#                     "short_name": "CA",
#                     "types": [
#                         "administrative_area_level_1",
#                         "political"
#                     ]
#                 },
#                 {
#                     "long_name": "United States",
#                     "short_name": "US",
#                     "types": [
#                         "country",
#                         "political"
#                     ]
#                 },
#                 {
#                     "long_name": "94043",
#                     "short_name": "94043",
#                     "types": [
#                         "postal_code"
#                     ]
#                 }
#             ],
#             "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
#             "geometry": {
#                 "location": {
#                     "lat": 37.4224428,
#                     "lng": -122.0842467
#                 },
#                 "location_type": "ROOFTOP",
#                 "viewport": {
#                     "northeast": {
#                         "lat": 37.4239627802915,
#                         "lng": -122.0829089197085
#                     },
#                     "southwest": {
#                         "lat": 37.4212648197085,
#                         "lng": -122.0856068802915
#                     }
#                 }
#             },
#             "place_id": "ChIJeRpOeF67j4AR9ydy_PIzPuM",
#             "plus_code": {
#                 "compound_code": "CWC8+X8 Mountain View, CA",
#                 "global_code": "849VCWC8+X8"
#             },
#             "types": [
#                 "street_address"
#             ]
#         }
#     ],
#     "status": "OK"
# }
class GoogleAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_coordinates(self, address):
        params = {"address": address, "key": self.api_key}
        response = requests.get(self.base_url, params=params)
        json_response = json.loads(response.text)
        if json_response["status"] == "OK":
            location = json_response["results"][0]["geometry"]["location"]
            return json_response["status"], location["lat"], location["lng"]
        else:
            return json_response["status"], None, None
    
    def get_location(self, lat, lon):
        params = {"latlng": f"{lat},{lon}", "key": self.api_key}
        response = requests.get(self.base_url, params=params)
        json_response = json.loads(response.text)
        if json_response["status"] == "OK":
            return json_response["status"], json_response["results"][0]["formatted_address"]
        else:
            return json_response["status"], None


if __name__ == "__main__":
    api = GoogleAPI(None)
    print(api.get_coordinates("1600 Amphitheatre Parkway, Mountain View, CA"))
    print(api.get_location(37.4224428, -122.0842467))
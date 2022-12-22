import requests
import os
import json
import time


if __name__ == "__main__":
    continent_info = json.load(open(os.path.join("results", "continent_info.json"), "r"))["result"]["continents"]
    for continent in continent_info:
        continent_id = continent["id"]
        # if continent_id in ["NA", "EU", "AS"]:
        #     continue
        continent_count = continent["count"]
        num = 0
        # if continent_id == "OC":
        #     num = 800
        while num < continent_count:
            url = "https://api.windy.com/api/webcams/v2/list/continent={}/limit={},{}?show=webcams:url,location,player".format(continent_id, 50, num)
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
            host = "api.windy.com"
            key = "UYT1czjUkRgUU26BUKkGXW6PKq8kV8Se"
            headers = {"User-Agent": user_agent, "Host": host, "x-windy-key": key}
            proxies = {"http": "http://127.0.0.1:65499", "https": "http://127.0.0.1:65499"}
            response = requests.get(url, headers=headers, proxies=proxies)
            # response = requests.get(url, headers=headers, proxies=proxies)
            if response.status_code == 200:
                response_json = response.json()
                webcams = response_json["result"]["webcams"]
                with open(os.path.join("results", "webcams_{}_{}.json".format(continent_id, num)), "w") as f:
                    json.dump(webcams, f)
            else:
                print("Error: {}".format(response.text))
            print("{}: {}/{}".format(continent_id, num, continent_count))
            num += 50
            time.sleep(1)
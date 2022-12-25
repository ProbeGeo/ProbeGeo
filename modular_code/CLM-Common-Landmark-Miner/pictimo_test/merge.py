import os
import json
import pandas as pd


pictimo_results = pd.read_csv(os.path.join("new_results", "pictimo_results_with_distances.csv"))
windy_results = json.load(open(os.path.join("new_results", "all_webcams_with_ip.json"), "r"))

pictimo_ips = pictimo_results["ip"].to_list()
pictimo_latitudes = pictimo_results["latitude"].to_list()
pictimo_longitudes = pictimo_results["longitude"].to_list()
windy_ips = [webcam["ip"] for webcam in windy_results]
windy_latitudes = [webcam["location"]["latitude"] for webcam in windy_results]
windy_longitudes = [webcam["location"]["longitude"] for webcam in windy_results]

num = len(pictimo_ips)
with open("new_results/merged_results.csv", "w") as f:
    f.write("ip,latitude,longitude\n")
    for i, ip in enumerate(pictimo_ips):
        f.write(f"{ip},{pictimo_latitudes[i]},{pictimo_longitudes[i]}\n")
    for i, ip in enumerate(windy_ips):
        if ip not in pictimo_ips:
            f.write(f"{ip},{windy_latitudes[i]},{windy_longitudes[i]}\n")
            num += 1
print(num)
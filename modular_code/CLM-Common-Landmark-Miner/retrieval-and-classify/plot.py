import os
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np


if __name__ == "__main__":
    results = pd.read_csv(os.path.join("new_results", "pictimo_results_with_distances.csv"))
    # countries = {}
    # continents = {}
    # for country in results["country"].to_list():
    #     if country not in countries:
    #         countries[country] = 1
    #     else:
    #         countries[country] += 1
    # windy_results = json.load(open(os.path.join("new_results", "all_webcams_with_ip.json"), "r"))
    # for webcam in windy_results:
    #     if webcam["location"]["continent"] not in continents:
    #         continents[webcam["location"]["continent"]] = 1
    #     else:
    #         continents[webcam["location"]["continent"]] += 1
    # country_info = {item["name"].lower().replace(" ", "-"): item["continent"] for item in json.load(open(os.path.join(os.path.dirname(__file__), "countries_continents.json")))}
    # country_info["aland-islands"] = "Europe"
    # country_info["aruba"] = "North America"
    # country_info["caribbean-netherlands"] = "North America"
    # country_info["china"] = "Asia"
    # country_info["eswatini"] = "Africa"
    # country_info["faeroe-islands"] = "Europe"
    # country_info["french-polynesia"] = "Australia"
    # country_info["greenland"] = "North America"
    # country_info["guadeloupe"] = "North America"
    # country_info["guam"] = "Australia"
    # country_info["hong-kong"] = "Asia"
    # country_info["ireland"] = "Europe"
    # country_info["isle-of-man"] = "Europe"
    # country_info["jersey"] = "Europe"
    # country_info["macao"] = "Asia"
    # country_info["martinique"] = "South America"
    # country_info["netherlands"] = "Europe"
    # country_info["netherlands-antilles"] = "South America"
    # country_info["new-caledonia"] = "Oceania"
    # country_info["puerto-rico"] = "North America"
    # country_info["reunion"] = "Africa"
    # country_info["russian-federation"] = "Eurasia"
    # country_info["saint-pierre-and-miquelon"] = "North America"
    # country_info["sao-tome-and-principe"] = "Africa"
    # country_info["state-of-palestine"] = "Asia"
    # country_info["taiwan"] = "Asia"
    # country_info["virgin-islands-us"] = "Caribbean"
    # for country in countries:
    #     if country in country_info:
    #         continent = country_info[country]
    #         if continent not in continents:
    #             continents[continent] = 0
    #         continents[continent] += countries[country]
    # print(continents)
    # plt.pie(list(continents.values()), labels=list(continents.keys()), autopct="%1.1f%%")
    # plt.title("results by continent")
    # plt.savefig(os.path.join("new_results", "results_by_continent.png"))
    # plt.close()
    distances = results.distance.dropna().to_list()
    distances.sort()
    # print(distances)
    length = len(distances)
    dis = []
    prob = []
    for distance in distances:
        if len(dis) == 0 or dis[-1] != distance:
            dis.append(distance)
            prob.append(1 / length)
        else:
            prob[-1] += 1 / length
    print(dis)
    for i in range(len(prob)):
        if i != 0:
            prob[i] += prob[i - 1]
    plt.plot(dis, prob)
    plt.title("cdf of distance with keycdn results")
    plt.savefig(os.path.join("new_results", "results_by_distance.png"))

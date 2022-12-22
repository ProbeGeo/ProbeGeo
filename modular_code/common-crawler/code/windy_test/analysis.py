import os
import json
import pandas as pd


if __name__ == "__main__":
    with open(os.path.join("results", "webcams_with_ip.txt"), "r") as f:
        webcams = [json.loads(line) for line in f]
    print("get webcams: {}".format(len(webcams)))
    internet_webcams = []
    for webcam in webcams:
        if not webcam["ip_from_original_url"].startswith("192.168."):
            internet_webcams.append(webcam)
    print("get internet webcams: {}".format(len(internet_webcams)))
    no_duplicate_internet_webcams = []
    no_duplicate_ips = []
    for webcam in internet_webcams:
        if webcam["ip_from_original_url"] not in no_duplicate_ips:
            no_duplicate_internet_webcams.append(webcam)
            no_duplicate_ips.append(webcam["ip_from_original_url"])
    print("get no duplicate internet webcams: {}".format(len(no_duplicate_internet_webcams)))
    pictimo_results = pd.read_csv(os.path.join("..", "pictimo_test", "pictimo_results.csv"))
    pictimo_ips = pictimo_results["ip"].values.tolist()
    no_duplicate_internet_webcams_not_in_pictimo = []
    for webcam in no_duplicate_internet_webcams:
        if webcam["ip_from_original_url"] not in pictimo_ips:
            no_duplicate_internet_webcams_not_in_pictimo.append(webcam)
    print("get no duplicate internet webcams not in pictimo: {}".format(len(no_duplicate_internet_webcams_not_in_pictimo)))
    useful_webcams = []
    for webcam in no_duplicate_internet_webcams_not_in_pictimo:
        ret = os.system('ping -n 2 -w 3 %s > nul' % (webcam["ip_from_original_url"],))
        if ret == 0:
            useful_webcams.append(webcam)
    print("get useful internet webcams: {}".format(len(useful_webcams)))
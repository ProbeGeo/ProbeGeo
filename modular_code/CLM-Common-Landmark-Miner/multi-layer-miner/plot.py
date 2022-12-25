import os
import json
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # with open(os.path.join("results", "continent_info.json"), "r") as f:
    #     continent_info = {item["name"]: item["count"] for item in json.load(f)["result"]["continents"]}
    # plt.pie(continent_info.values(), labels=continent_info.keys(), autopct="%1.1f%%")
    # plt.title("Total Windy Continent Distribution")
    # plt.savefig(os.path.join("continent_distribution.png"))
    # plt.close()
    # with open(os.path.join("results", "all_webcams.json"), "r") as f:
    #     all_webcams = json.load(f)
    # precision = {"city": 0, "region": 0, "country": 0, "continent": 0, "none": 0}
    # for webcam in all_webcams:
    #     location = webcam["location"]
    #     if location["city"]:
    #         precision["city"] += 1
    #     elif location["region"]:
    #         precision["region"] += 1
    #     elif location["country"]:
    #         precision["country"] += 1
    #     elif location["continent"]:
    #         precision["continent"] += 1
    #     else:
    #         precision["none"] += 1
    # print(precision)
    # with open(os.path.join("results", "new_all_webcams_with_ip_30000_35000.json"), "r") as f:
    #     all_webcams = json.load(f)
    # sources = {"original_url": 0, "original_page_text": 0, "secondary_page_text": 0, "original_host_name": 0, "not_found": 0}
    # ips = set()
    # original_url_ips = set()
    # original_page_text_ips = set()
    # secondary_page_text_ips = set()
    # original_host_name_ips = set()
    # for webcam in all_webcams:
    #     if webcam["ip_from_original_url"]:
    #         original_url_ips.add(webcam["ip_from_original_url"])
    #         ips.add(webcam["ip_from_original_url"])
    #         sources["original_url"] += 1
    #     elif webcam["ip_from_original_page_text"]:
    #         original_page_text_ips.add(webcam["ip_from_original_page_text"])
    #         ips.add(webcam["ip_from_original_page_text"])
    #         sources["original_page_text"] += 1
    #     elif webcam["ip_from_secondary_page_text"]:
    #         secondary_page_text_ips.add(webcam["ip_from_secondary_page_text"])
    #         ips.add(webcam["ip_from_secondary_page_text"])
    #         sources["secondary_page_text"] += 1
    #     elif webcam["ip_from_original_host_name"]:
    #         original_host_name_ips.add(webcam["ip_from_original_host_name"])
    #         ips.add(webcam["ip_from_original_host_name"])
    #         sources["original_host_name"] += 1
    #     else:
    #         sources["not_found"] += 1
    # print(sources)
    # unique_sources = {"original_url": len(original_url_ips), "original_page_text": len(original_page_text_ips), "secondary_page_text": len(secondary_page_text_ips), "original_host_name": len(original_host_name_ips), "not_found": sources["not_found"]}
    # print(len(ips))
    # print(unique_sources)
    with open(os.path.join("results", "all_webcams_with_ip.json"), "r") as f:
        all_webcams = json.load(f)
    num = 0
    for webcam in all_webcams:
        if "ip_from_original_url" in webcam:
            if webcam["ip_from_original_url"]:
                print(webcam["original_url"])
                num += 1
                if num == 10:
                    break



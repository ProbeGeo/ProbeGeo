import os
import json
import random


if __name__ == "__main__":
    if not os.path.exists(os.path.join("results", "new_all_webcams_with_ip.json")):
        all_webcams = []
        for i in range(111):
            start = i * 500
            end = min((i + 1) * 500 - 1, 55076)
            with open(os.path.join("results", "new_all_webcams_with_ip_{}_{}.json".format(str(start), str(end))), "r") as f:
                webcams = json.load(f)
            all_webcams.extend(webcams)
        with open(os.path.join("results", "new_all_webcams_with_ip.json"), "w") as f:
            json.dump(all_webcams, f)
    else:
        with open(os.path.join("results", "new_all_webcams_with_ip.json"), "r") as f:
            all_webcams = json.load(f)
    random.shuffle(all_webcams)
    ip_from_original_url_num = 0
    ip_from_secondary_url_num = 0
    no_ip_num = 0
    original_page_none_num = 0
    file_size_too_large_num = 0
    not_text_num = 0
    wrong_status_code_num = 0
    request_get_failed_num = 0
    total_num = len(all_webcams)
    for idx, webcam in enumerate(all_webcams):
        if webcam["ip_from_original_url"] is not None:
            ip_from_original_url_num += 1
        elif webcam["ip_from_secondary_url"] is not None:
            ip_from_secondary_url_num += 1
        else:
            webcam_id = webcam["id"]
            with open(os.path.join("results", "webcams_html", "{}.json".format(webcam_id)), "r") as f:
                html_json = json.load(f)
            if not html_json["get_original_page_success"]:
                original_page_none_num += 1
                if html_json["original_page"] == "file size too large":
                    file_size_too_large_num += 1
                elif html_json["original_page"] == "not text":
                    not_text_num += 1
                elif html_json["original_page"] == "wrong status code":
                    wrong_status_code_num += 1
                elif html_json["original_page"] == "request get failed":
                    request_get_failed_num += 1
            no_ip_num += 1
        if idx % 100 == 0:
            print("{}/{}".format(idx, total_num))
    print("ip_from_original_url_num: {}".format(ip_from_original_url_num))
    print("ip_from_secondary_url_num: {}".format(ip_from_secondary_url_num))
    print("no_ip_num: {}".format(no_ip_num))
    print("original_page_none_num: {}".format(original_page_none_num))
    print("file_size_too_large_num: {}".format(file_size_too_large_num))
    print("not_text_num: {}".format(not_text_num))
    print("wrong_status_code_num: {}".format(wrong_status_code_num))
    print("request_get_failed_num: {}".format(request_get_failed_num))
    print("total_num: {}".format(total_num))
import requests
from urllib.parse import urljoin, urlparse
import os
import json
from bs4 import BeautifulSoup
import re
import time
import socket
from ip_translator import Ip_translator
from multiprocessing import Pool
from tqdm import tqdm
from IPy import IP
import random
import argparse
import pdb


ipv4_re = r"((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)"
ipv4_re_pattern = re.compile(ipv4_re)
self_ip = "147.139.94.206"
ip_translator = Ip_translator()
result_list = []


def check_ip(raw_ip):
    try:
        ip = IP(raw_ip)
        if ip.iptype() == "PUBLIC":
            return True
        else:
            return False
    except:
        return False


def get_ip(url):
    if url is None:
        return None
    searchObj = re.search(ipv4_re, url)
    if searchObj:
        ip = searchObj.group(0)
        if ip != self_ip and check_ip(ip):
            return ip
    return None


def get_all_ips(text):
    candidates = []
    res = ipv4_re_pattern.search(text)
    while res:
        start, end = res.span()
        candidates.append(res.group(0))
        res = ipv4_re_pattern.search(text, start+1)
    candidates = list(set(candidates))
    candidates = [ip for ip in candidates if ip != self_ip and check_ip(ip)]
    return candidates


def get_original_url(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    headers = {'User-Agent': user_agent}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            response_json = r.json()
            if "pageUrl" in response_json:
                return response_json["pageUrl"]
    except:
        pass
    return None


max_file_size = 10 * 1024 * 1024
def get_html(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    headers = {'User-Agent': user_agent}
    try:
        r = requests.get(url, headers=headers, timeout=5, stream=True)
        if r.status_code == 200:
            if "content-type" in r.headers and r.headers["content-type"].startswith("text"):
                file_size = int(r.headers["content-length"])
                if file_size < max_file_size:
                    r.encoding = r.apparent_encoding
                    return True, r.text
                else:
                    return False, "file size too large"
            return False, "not text"
        else:
            return False, "wrong status code"
    except:
        return False, "request get failed"


def worker(idx, webcam):
    new_webcam = {}
    new_webcam["id"] = webcam["id"]
    new_webcam["status"] = webcam["status"]
    new_webcam["title"] = webcam["title"]
    new_webcam["location"] = webcam["location"]

    try:
        real_region_code = webcam["location"]["region_code"].split(".")[1]
    except:
        real_region_code = None
    try:
        real_country_code = webcam["location"]["country_code"]
    except:
        real_country_code = None
    try:
        real_continent_code = webcam["location"]["continent_code"]
    except:
        real_continent_code = None

    new_webcam["url"] = webcam["url"]
    if "original_url" in webcam:
        new_webcam["original_url"] = webcam["original_url"]
    else:
        new_webcam["original_url"] = get_original_url("https://node.windy.com/webcams/v1.0/detail/" + webcam["id"])

    new_webcam["ip_from_original_url"] = webcam["ip_from_original_url"] if "ip_from_original_url" in webcam else None
    if new_webcam["ip_from_original_url"] is not None and not check_ip(new_webcam["ip_from_original_url"]):
        new_webcam["ip_from_original_url"] = get_ip(new_webcam["original_url"])
    new_webcam["ip_from_secondary_url"] = None

    get_original_page_success, original_page_text = get_html(new_webcam["original_url"])
    html_json = {"original_url": new_webcam["original_url"], "get_original_page_success": get_original_page_success, "original_page": original_page_text, "secondary_url": None, "secondary_page": None}
    # if found in original_url, use it
    if new_webcam["ip_from_original_url"] is not None:
        result_list[idx] = new_webcam
        with open(os.path.join("results", "webcams_html", "{}.json".format(new_webcam["id"])), "w") as f:
            json.dump(html_json, f)
        return 1
    # if original_page is not connected, give up
    if html_json["original_page"] is None:
        result_list[idx] = new_webcam
        with open(os.path.join("results", "webcams_html", "{}.json".format(new_webcam["id"])), "w") as f:
            json.dump(html_json, f)
        return 0
    # if found in secondary_url, use it
    try:
        soup = BeautifulSoup(html_json["original_page"], "html.parser")
        url_tags = soup.find_all("a", href=True)
        secondary_urls = [url_tag["href"] for url_tag in url_tags]
        for secondary_url in secondary_urls:
            ip = get_ip(secondary_url)
            if ip is not None and check_ip(ip):
                valid, _, _, _, country_code, _, region_code, _, _, _ = ip_translator.get_geo_of_ip(ip)
                if valid:
                    if country_code == real_country_code and region_code == real_region_code:
                        new_webcam["ip_from_secondary_url"] = ip
                        html_json["secondary_url"] = secondary_url
                        html_json["secondary_page"] = get_html(secondary_url)
                        result_list[idx] = new_webcam
                        with open(os.path.join("results", "webcams_html", "{}.json".format(new_webcam["id"])), "w") as f:
                            json.dump(html_json, f)
                        return 1
    except:
        pass
    result_list[idx] = new_webcam
    with open(os.path.join("results", "webcams_html", "{}.json".format(new_webcam["id"])), "w") as f:
        json.dump(html_json, f)
    return 0

        

if __name__ == "__main__":
    os.mkdirs(os.path.join("results", "webcams_html_4_layer"), exists_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    args = parser.parse_args()

    with open(os.path.join("results", "all_webcams_with_ip.json"), "r") as f:
        all_webcams = json.load(f)

    start = args.start
    end = min(start + 5000, len(all_webcams))
    webcams = all_webcams[start:end]
    del all_webcams

    total_num = len(webcams)
    total_get_num = 0

    result_list = [None] * total_num
    idx_list = list(range(total_num))

    tbar = tqdm(zip(idx_list, webcams), total=total_num)

    recorded = 0
    for idx, webcam in tbar:
        total_get_num += worker(idx, webcam)
        tbar.set_description("get {} from {}".format(total_get_num, idx + 1))
        if (idx + 1) % 500 == 0 or (idx + 1) == total_num:
            with open(os.path.join("results", "new_all_webcams_with_ip_4_layer_{}_{}.json".format(start + recorded, start + idx)), "w") as f:
                json.dump(result_list[recorded:idx + 1], f)
            recorded = idx + 1
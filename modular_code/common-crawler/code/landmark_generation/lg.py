from web_parser import web_parser
from location_translator import location_translator
import easyocr
import json
import os
import csv
import time

# write nested list of dict to csv
def nestedlist2csv(list, out_file):
    with open(out_file, 'w') as f:
        w = csv.writer(f)
        fieldnames=list[0].keys()
        w.writerow(fieldnames)
        for row in list:
            w.writerow(row.values())


if __name__ == '__main__':
    ip_geo_list = list()

    # initialize tools used in parser
    reader = easyocr.Reader(['en'])
    translator = location_translator()

    # process all the html file crawled from Internet
    with open(os.path.join("..", "webcam_content_picker", "sample.json"), "r") as f:
        data = json.load(f)
    length = sum(len(urls) for urls in data.values())
    idx = 0
    for web, urls in data.items():
        files = os.listdir(os.path.join("..", "webcam_content_picker", "websites", web))
        htmls = {}
        for file_ in files:
            if file_ != "results.json":
                htmls.update(json.load(open(os.path.join("..", "webcam_content_picker", "websites", web, file_))))
        for url in urls:
            start = time.time()
            html = htmls[url]
            parser = web_parser(url, html, reader, translator)
            ip_geo_dict = dict()
            ip, longitude, latitude = parser.parse()
            if(len(ip)==0):
                continue
            elif(len(ip)==1 and longitude[0] != "" and latitude[0] != ""):
                ip_geo_dict['website'] = web
                ip_geo_dict['url'] = url
                ip_geo_dict['IPv4'] = ip[0]
                ip_geo_dict['longitude'] = longitude[0]
                ip_geo_dict['latitude'] = latitude[0]

                ip_geo_list.append(ip_geo_dict)
            # else:
            #     # TODO: parse a website containing multiple IP
            #     pass
            end = time.time()
            print(idx, "finished,", length - idx, "remaining", "still need", (length - idx) * (end - start), "s")
            idx += 1
    nestedlist2csv(ip_geo_list,'./ip_geo.csv')

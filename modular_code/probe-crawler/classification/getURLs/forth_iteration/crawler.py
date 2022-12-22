import csv




##首先获取LG和非LG网页的内容
##采用bing爬虫
import urllib.request
import urllib.request
import requests
import re
import math
from bs4 import BeautifulSoup as bs

import time
import json
import threading
import csv


headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
def do_something(urllist,be,ed,thread_index):
    f1 = open('urlcontent' + str(int(thread_index)+1) + '.csv', 'a')
    for num in range(be,ed):

        url = urllist[num]
        try:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            r = requests.get(url=url,
                             headers=headers,
                             allow_redirects=False,
                             verify=False,
                             timeout=60)
            r.raise_for_status()

            r.encoding = r.apparent_encoding
            content = r.text
            # soup = bs(content, 'html.parser')

            if('301 Moved Permanently'.lower() in content.lower() or 'Object moved'.lower() in  content.lower()):
                print(url)
                url1='https://'+url.split('://')[1]
                r = requests.get(url=url1,
                                 headers=headers,
                                 allow_redirects=False,
                                 verify=False,
                                 timeout=60)
                r.raise_for_status()
                # 设置该html文档可能的编码
                r.encoding = r.apparent_encoding
                content = r.text
                f1.writelines(url + ',|ProbeGeo|' +url1 + ',|ProbeGeo|' +content.replace('\n',' ').replace('\t',' ') + '\n')
                f1.flush()
            else:
                f1.writelines(url + ',|ProbeGeo|' + url + ',|ProbeGeo|' +content.replace('\n', ' ').replace('\t',' ') + '\n')
                f1.flush()

        except Exception as e:
            print(url)
            print(e)
            continue


def getresponedURLs():
    dictpre = {}
    file1 = open('prefilteredurl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dictpre[','.join(row)] = 0
    print(len(dictpre))

    for i in range(1, 7):
        print(i)
        file1 = open(
            'urlcontent' + str(i) + '.csv', 'r')
        csv_reader1 = csv.reader(file1)
        csv.field_size_limit(500 * 1024 * 1024)
        for row in csv_reader1:
            url = ','.join(row).split(',|ProbeGeo|')[0]
            try:
                html = ','.join(row).split(',|ProbeGeo|')[2]
            except IndexError as e:
                continue
            if (
                    '301 moved permanently' in html.lower() or '302 found' in html.lower() or 'redirected' in html.lower() or html.replace(
                    ' ', '') == ''
            ):
                continue
            if (url[:4] != 'http' or url not in dictpre):
                continue
            dictpre[url] = 1

    file = open('getcontenturl.csv', 'w')
    for key in dictpre:
        if (dictpre[key] == 1):
            file.writelines(key + '\n')

if __name__ == '__main__':

    dicturl=[]
    file1 = open(
        'prefilteredurl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        dicturl.append(','.join(row))


    print(len(dicturl))
    d = 6
    num = int(len(dicturl) / d)
    for i in range(d):
        if (i != (d - 1)):
            t = threading.Thread(target=do_something, args=(dicturl, num * i, num * (i + 1), i))
            t.start()
        else:
            t = threading.Thread(target=do_something,
                                 args=(dicturl, num * i, len(dicturl) , i))
            t.start()
    getresponedURLs()
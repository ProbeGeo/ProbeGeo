import urllib.request
import urllib.request
import requests
import re
import math
from bs4 import BeautifulSoup as bs
from selenium import webdriver
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
def do_something(dictcontent,urllist,be,ed,thread_index):
    f1 = open('inputseed_results_' + str(int(thread_index)) + '.csv', 'a')
    for num in range(be,ed):
        url = urllist[num]
        print(url)
        if(url not in dictcontent):
            continue
        str1 = ''
        try:
            content=dictcontent[url]
            soup = bs(content, 'html.parser')
            for link in soup.findAll("a", href=re.compile("^(http|www)")):
                if link.attrs['href'] is not None:
                    str1+='<URL>'+link.attrs['href']+'</URL>,'
            for iframe in soup.find_all('iframe'):
                url_ifr = iframe['src']  # get iframe src value
                if('http' in url_ifr):
                    str1 += '<URL>' + url_ifr + '</URL>,'
            f1.writelines(url + ',|ProbeGeo|' + str1 + '\n')
            f1.flush()
        except Exception as e:
            f1.writelines(url + ',|ProbeGeo|' + str1 + '\n')
            f1.flush()
            print(url)
            print(e)
            continue


if __name__ == '__main__':
    csv.field_size_limit(500 * 1024 * 1024)
    dicturl = []
    file1 = open('../../../classification/relevant-URLs/second_iteration/relevanceLG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dicturl.append(','.join(row))
    dictcontent={}
    file1 = open('../../../classification/relevant-URLs/second_iteration/LGallcontent.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        url=','.join(row).split(',|ProbeGeo|')[0]
        if(url not in dicturl):
            continue
        try:
            html=','.join(row).split(',|ProbeGeo|')[2]
        except IndexError as e:
            continue
        if(html.replace(' ','')==''):
            continue
        dictcontent[url]=html
    print(len(dictcontent))
    print(len(dicturl))
    d = 10
    num = int(len(dicturl) / d)
    for i in range(d):
        if (i != (d - 1)):
            t = threading.Thread(target=do_something, args=(dictcontent,dicturl, num * i, num * (i + 1), i))
            t.start()
        else:
            t = threading.Thread(target=do_something,
                                 args=(dictcontent,dicturl, num * i, len(dicturl) , i))
            t.start()
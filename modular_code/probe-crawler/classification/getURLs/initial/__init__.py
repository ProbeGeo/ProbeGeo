import csv
import urllib.request
import urllib.request
import requests
import re
import math
from bs4 import BeautifulSoup as bs

import time
import json
import threading


def prefilteredURL():
    ##According to the above classification results, we obtain pre-filtered URLs
    ###record URLs in the webseds
    dictinputseed = {}
    file1 = open(
        '../../../webseds/All-LGseedpages/inputseed.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        dictinputseed[','.join(row).split('//')[1]] = ''
    dictpredict={}
    file1 = open('../../URL-filter/PUbagging_model/baggingresultnew.csv', 'r')
    csv_reader1 = csv.reader(file1)
    i = 0
    for row in csv_reader1:
        if i in range(2991,922884):
            if(','.join(row).split('\t')[2]=='1' and 'http' in ','.join(row).split('\t')[0][:4] ):
                ###remove duplicate URLs
                if(','.join(row).split('\t')[0].split('//')[1] in dictpredict):
                    if(','.join(row).split('\t')[0] not in dictpredict[','.join(row).split('\t')[0].split('//')[1]]):
                        dictpredict[','.join(row).split('\t')[0].split('//')[1]].append(','.join(row).split('\t')[0])
                else:
                    dictpredict[','.join(row).split('\t')[0].split('//')[1]]=[','.join(row).split('\t')[0]]
        i += 1


    dicturl={}
    for key in dictpredict:
        if('https://'+key in dictpredict[key]):
            dicturl['https://'+key]=''
        else:
            dicturl[dictpredict[key][0]] =''


    print(len(dicturl))
    file=open('prefilteredurl.csv','w')
    for key1 in dicturl:
        url = key1
        url_sche = url.split('//')[1]
        ###remove URLs in the webseds
        tag = 0
        for key in dictinputseed:
            if (url_sche in key or key in url_sche):
                tag = 1
                break
        if (tag == 0):
            file.writelines(url + '\n')

headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
def do_something(urllist,be,ed,thread_index):
    f1 = open('urlcontent_results' + str(int(thread_index)) + '.csv', 'a')
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
            # setting possible html encodings
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


def filedeal():
    ##merge html files from Multi-thread into a file
    csv.field_size_limit(500 * 1024 * 1024)
    dictinfo = []
    for i in range(0, 10):
        file1 = open('urlcontent_results'+str(i)+'.csv', 'r')
        csv_reader1 = csv.reader((line.replace('\0', '') for line in file1))
        # csv_reader1 = csv.reader(file1)
        str1 = ''
        for row in csv_reader1:
            if ('http' in ','.join(row)[:4]):
                if (str1 != ''):
                    str1.replace('\n', ' ').replace('\t',' ')
                    dictinfo.append(str1)
                    str1 = ''
                str1 += ','.join(row)
            else:
                str1 += ','.join(row)
        if (str1 != ''):
            str1.replace('\n', ' ').replace('\t',' ')
            dictinfo.append(str1)
    print(len(dictinfo))
    file1=open('urlcontent.csv','w')
    for key in dictinfo:
        file1.writelines(key+'\n')


def getresponedURLs():
    dictpre={}
    file1 = open('prefilteredurl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dictpre[','.join(row)]=0
    file1 = open('urlcontent.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        url = ','.join(row).split(',|ProbeGeo|')[0]
        html=','.join(row).split(',|ProbeGeo|')[2]
        if ('301 moved permanently' in html.lower() or '302 found' in html.lower() or 'redirected' in html.lower() or html.replace(' ','')==''
        ):
            continue
        if (url[:4] != 'http' or url not in dictpre):
            continue
        dictpre[url] =1
    file = open('getcontenturl.csv', 'w')
    for key in dictpre:
        if(dictpre[key]==1):
            file.writelines(key + '\n')


if __name__ == '__main__':
    #According to the above classification results, we obtain pre-filtered URLs
    prefilteredURL()

    #Multi-thread process for downloading web pages
    # dicturl=[]
    # file1 = open(
    #     'prefilteredurl.csv', 'r')
    # csv_reader1 = csv.reader(file1)
    # csv.field_size_limit(500 * 1024 * 1024)
    # for row in csv_reader1:
    #     dicturl.append(','.join(row))
    #
    #
    # print(len(dicturl))
    # d = 10
    # num = int(len(dicturl) / d)
    # for i in range(d):
    #     if (i != (d - 1)):
    #         t = threading.Thread(target=do_something, args=(dicturl, num * i, num * (i + 1), i))
    #         t.start()
    #     else:
    #         t = threading.Thread(target=do_something,
    #                              args=(dicturl, num * i, len(dicturl) , i))
    #         t.start()
    #There are 77,113 URLs (recorded in getcontenturl.csv) respond successfully and we get their html files.
    getresponedURLs()
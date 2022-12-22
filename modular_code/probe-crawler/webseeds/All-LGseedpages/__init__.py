
import json
import re
import threading
import urllib
import selenium
import csv
import json
import re
import csv
import urllib.request
import urllib.request
import requests
import threading
from bs4 import BeautifulSoup as bs
import re
import time
import json
import math
import csv
from selenium import webdriver
import time
import json
import csv
# from selenium.webdriver.chrome.options import Options
def merge():
    #merge four sets of known LG URLs into one list
    dicturltemplate = {}
    filename=['../peeringdb/LGlist.json',
              '../bgp4/LGlist.json',
              '../bgplookingglass/LGlist.json',
              '../tracerouteorg/LGlist.json']
    for i  in  range(0,4):
        f = open(filename[i], encoding='utf-8')
        res = f.read()
        data = json.loads(res)
        for key in data:
            asn = data[key][0]
            lg = data[key][1]
            if(lg==''):
                continue
            if(asn not in dicturltemplate):
                dicturltemplate[asn]={}
                dicturltemplate[asn][lg]=''
            else:
                if(lg not in dicturltemplate[asn]):
                    dicturltemplate[asn][lg] = ''
    print(len(dicturltemplate))
    with open("LGlist.json", "w") as f:
        json.dump(dicturltemplate, f)





def getLGurl():
    file=open('inputseed.csv','w')
    f = open('LGlist.json', encoding='utf-8')  # 打开‘json文件
    res = f.read()  # 读文件
    data = json.loads(res)
    for key in data:
        for key1 in data[key]:
            file.writelines(key1+'\n')




headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }

def do_something(urllist,be,ed,thread_index):
    f1 = open('urlcontent_resulls' + str(int(thread_index)) + '.csv', 'a')
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
            # 设置该html文档可能的编码
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
                f1.writelines(url + ',|ProbeGeo|' +url1 + ',|ProbeGeo|' +content.replace('\n',' ') + '\n')
                f1.flush()
            else:
                f1.writelines(url + ',|ProbeGeo|' + url + ',|ProbeGeo|' +content.replace('\n', ' ') + '\n')
                f1.flush()

        except Exception as e:
            print(url)
            print(e)
            continue


def multithread():
    dictpre = {}
    for i in range(0, 10):
        file1 = open('urlcontent_resulls' + str(i) + '.csv', 'r')
        csv_reader1 = csv.reader((line.replace('\0', '') for line in file1))
        for row in csv_reader1:
            if (',|ProbeGeo|' in ','.join(row)):
                dictpre[','.join(row).split(',|ProbeGeo|')[0]] = ''


    dicturl = []
    file1 = open('inputseed.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        if (','.join(row) not in dictpre):
            dicturl.append(','.join(row))


    print(len(dicturl))
    d = 10
    num = int(len(dicturl) / d)
    for i in range(d):
        if (i != (d - 1)):
            t = threading.Thread(target=do_something, args=(dicturl, num * i, num * (i + 1), i))
            t.start()
        else:
            t = threading.Thread(target=do_something,
                                 args=(dicturl, num * i, len(dicturl), i))
            t.start()


def allLG():

    csv.field_size_limit(500 * 1024 * 1024)
    dictinfo = []
    for i in range(0, 10):
        file1 = open('urlcontent_resulls'+str(i)+'.csv', 'r')
        csv_reader1 = csv.reader((line.replace('\0', '') for line in file1))
        # csv_reader1 = csv.reader(file1)
        str1 = ''
        for row in csv_reader1:
            if ('http' in ','.join(row)[:4]):
                if (str1 != ''):
                    str1.replace('\n', ' ')
                    dictinfo.append(str1)
                    str1 = ''
                str1 += ','.join(row)
            else:
                str1 += ','.join(row)

        if (str1 != ''):
            str1.replace('\n', ' ').replace('\t',' ')
            dictinfo.append(str1)

    print(len(dictinfo))
    with open("LGlistcontent.json", "w") as f:
        json.dump(dictinfo, f)
    file1=open('urlcontentnew.csv','w')
    for key in dictinfo:
        file1.writelines(key+'\n')

def calresponsenum():
    dictcontent={}
    file1 = open('urlcontentnew.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        url=','.join(row).split(',|ProbeGeo|')[0]
        try:
            html=','.join(row).split(',|ProbeGeo|')[2]
        except IndexError as e:
            continue
        if(html.replace(' ','')==''):
            continue
        dictcontent[url]=html
    print(len(dictcontent))


if __name__ == '__main__':
    #merge four sets of known LG URLs into one list
    merge()
    getLGurl()
    #conduct a multithread process for downloading LG pages
    multithread()
    allLG()
    #1,736 html files are downloaded successfully
    calresponsenum()

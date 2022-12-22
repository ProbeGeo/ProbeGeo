# -*- coding: utf-8 -*-
import re
import requests
import selenium
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import json
import threading
import csv
from selenium.webdriver.chrome.options import Options
import tldextract
##obtain all LG title information from the webseds
def deal1():
    dictas = {}
    file1 = open('../../../../webseds/bgp4/AS-ORG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dictas[int(row[0].split('|')[0])] = [row[0].split('|')[1], row[0].split('|')[2]]

    file1 = open('titileinfo.csv', 'w')
    file = open('../../../../webseds/All-LGseedpages/LGlistcontent.json', 'r')

    res = file.read()
    data = json.loads(res)
    for key in data:
        asn = key
        for key1 in data[key]:
            lg = key1
            content = data[key][key1]
            title = re.findall(r'<title>(.*?)<\/title>', content, re.S | re.M)
            if (title):
                if (int(asn) in dictas):
                    file1.writelines(
                        asn + ',' + lg + ',' + title[0] + ',' + dictas[int(asn)][0] + ',' + dictas[int(asn)][1] + '\n')
                    file1.flush()
                else:
                    file1.writelines(asn + ',' + lg + ',' + title[0] + ',,' '\n')
                    file1.flush()


def hint():
    ##collect the company website URL of each individual AS from PeeringDB and get 13K URLs in total. These URLs are parsed using the Tldextract python library [13] and we obtain a list of second-level domains.
    file1=open('orgnamenew.csv','w')
    f = open('../../../../webseds/peeringdb/peeringdbnet.json',
             encoding='utf-8')
    res = f.read()  # 读文件
    data = json.loads(res)
    for key in data['data']:
        if (key['website'] != ''):
            list1 = key['website']
            file1.writelines(str(key['asn'])+','+tldextract.extract(list1)[1]+'\n')

    file1.close()


 # Then we replace the word or phrase (in titles) that matches one second-level domain with ORG.
 # replace AS number with ASN
def replace():
    dictasorg={}
    file = open('orgnamenew.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        dictasorg[int(row[0])]=row[1].lower()


    file1 = open('item.csv', 'w')
    file = open('titileinfo.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        asn=int(row[0])
        listtitlesplit=[]
        title=row[2].lower()
        if ('403' in title or '404' in title or '502' in title):
            continue
        for item in re.split('[ .,()]', title):
            pattern = re.compile('AS[0-9]+')
            pattern1 = re.compile('as[0-9]+')
            if (item != '' and item != '-' and item != '/' and item != '|' and item != '#' and item!='::' and item!='--'):
                if(asn in dictasorg and item==dictasorg[asn]):
                    listtitlesplit.append('Orgname')
                elif(pattern.findall(item) or pattern1.findall(item)):
                    listtitlesplit.append('ASnumber')
                else:
                    listtitlesplit.append(item)
        print(asn)
        print(title)
        print(listtitlesplit)
        if(listtitlesplit!=[]):
            file1.writelines(','.join(listtitlesplit)+'\n')






# After extracting, if these two virtual words are found in the frequent phrases, we will replace them with the name and the number of every AS on the Internet to construct a series of search terms.
def URLs(dictrule):
    dictasinfo={}
    file1 = open('orgnamenew.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dictasinfo[int(row[0])]=[row[1],'']



    file1 = open('../../../../webseds/peeringdb/AS-Org/AS-ORG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        asname=row[0].split('|')[1]
        if(asname==''):
            continue
        if(int(row[0].split('|')[0]) in dictasinfo):
            dictasinfo[int(row[0].split('|')[0])][1]=asname
        else:
            dictasinfo[int(row[0].split('|')[0])] =['',asname]

    # print(len(dictasinfo))
    keyword=[]
    for key in dictrule:
        # print(key)
        if('Orgname' not in key and 'ASnumber' in key):
            for asn in dictasinfo:
                str1=key.replace('ASnumber','AS'+str(asn))
                keyword.append(str1)

        elif('Orgname' in key and 'ASnumber' not in key):
            for asn in dictasinfo:
                if(dictasinfo[asn][0]!='' ):
                    str1=key.replace('Orgname',dictasinfo[asn][0])
                    keyword.append(str1)
                if(dictasinfo[asn][1]!=''):
                    str1 = key.replace('Orgname', dictasinfo[asn][1])
                    keyword.append(str1)
        elif ('Orgname' in key and 'ASnumber'  in key):
            for asn in dictasinfo:
                str1 = key.replace('ASnumber', 'AS' + str(asn))
                if (dictasinfo[asn][0] != ''):
                    str2 = str1.replace('Orgname', dictasinfo[asn][0])
                    keyword.append(str2)
                if (dictasinfo[asn][1] != ''):
                    str2 = str1.replace('Orgname', dictasinfo[asn][1])
                    keyword.append(str2)
                else:
                    keyword.append(str1)
        else:
            keyword.append(key)

    file1=open('URLrecord.csv','a')
    for key in keyword:
        file1.writelines(key+'\n')


if __name__ == '__main__':
    deal1()
    # hint()
    # replace()
    # dictrule={'looking glass ASnumber|Orgname': '', 'net': ''}
    # URLs(dictrule)




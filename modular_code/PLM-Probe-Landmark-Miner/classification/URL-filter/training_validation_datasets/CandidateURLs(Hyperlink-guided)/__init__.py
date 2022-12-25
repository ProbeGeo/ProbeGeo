import json
from collections import OrderedDict
import csv
from random import shuffle

import math

# split the candidate URLs into 98% and 2%, the 2% URLs are labeled

def lastdeal():
    keylist={}
    file1 = open('../../../../crawling/initial/Hyperlink-guided search/crawler/LGinlinkurlfirst.json', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if (','.join(row) not in keylist):
            keylist[','.join(row)] = ''

    print(len(keylist))
    urllist=[]
    for key in keylist:
        urllist.append(key)
    num=math.ceil(len(keylist)*0.02)
    dicttestlable={}
    shuffle(urllist)
    for i in range(0,num):
        print(urllist[i])
        dicttestlable[urllist[i]]=''
    with open("testlabel.json", "w") as f:
        json.dump(dicttestlable, f)


def validation():
    ##1% for validation , and 1% for test
    f = open('testlabel.json', encoding='utf-8')
    res = f.read()
    data = json.loads(res, object_pairs_hook=OrderedDict)
    list1=[]
    for key in data:
        list1.append(key)
    shuffle(list1)
    print(len(data))
    print(int(len(list1)/2))
    dictvalidation={}
    dicttest={}
    for i in range(0,int(len(data)/2)):
        dictvalidation[list1[i]]=data[list1[i]]
    for i in range(int(len(data)/2),len(data)):
        dicttest[list1[i]]=data[list1[i]]
    with open("testlabel-validation.json", "w") as f:
        json.dump(dictvalidation, f)
    with open("testlabel-test.json", "w") as f:
        json.dump(dicttest, f)


if __name__ == '__main__':
    validation()
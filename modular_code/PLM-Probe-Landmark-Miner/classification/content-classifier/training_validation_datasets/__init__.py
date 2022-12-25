import json
from collections import OrderedDict
import csv
from random import shuffle

import math

###we randomly divide the successfully downloaded pre-filtered URLs into 94% for training and 6% for validating and testing
def testdata():
    keylist={}
    file1 = open('../../getURLs/initial/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if (','.join(row) not in keylist):
            keylist[','.join(row)] = ''

    print(len(keylist))
    urllist=[]
    for key in keylist:
        urllist.append(key)


    file2=open('testset.csv','w')
    num=math.ceil(len(keylist)*0.06)

    shuffle(urllist)
    for i in range(0,num):
        file2.writelines(urllist[i]+'\n')


###we randomly divide the 1,085 valid seed html files  into 94% for training and 6% for validating and testing
def testdataseed():
    keylist={}
    file1 = open('../../../webseds/All-LGseedpages/afterManualCheck/isLG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if (','.join(row) not in keylist):
            keylist[','.join(row)] = ''

    print(len(keylist))
    urllist=[]
    for key in keylist:
        urllist.append(key)

    file2=open('seedtestset.csv','w')
    num=math.ceil(len(keylist)*0.06)

    shuffle(urllist)
    for i in range(0,num):
        print(urllist[i])
        file2.writelines(urllist[i]+',|1'+'\n')


def merge():

    keylist = {}
    file1 = open('seedtestset.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if (','.join(row).split(',|')[0] not in keylist):
            keylist[','.join(row).split(',|')[0]] = ','.join(row).split(',|')[1]
    print(len(keylist))
    file1 = open('testset.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if (','.join(row).split(',|')[0] not in keylist):
            keylist[','.join(row).split(',|')[0]] = ','.join(row).split(',|')[1]
    print(len(keylist))
    with open("testlabel.json", "w") as f:
        json.dump(keylist, f)

def validation():
    #3% for validation , and 3% for test
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
    testdata()
    testdataseed()
    merge()
    validation()

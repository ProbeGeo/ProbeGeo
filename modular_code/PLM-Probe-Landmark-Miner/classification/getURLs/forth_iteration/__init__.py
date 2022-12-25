
# -*- coding: utf-8 -*-
import csv

from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from random import shuffle
import json

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from baggingPU import BaggingClassifierPU
import pandas as pd
from sklearn.externals import joblib
def dataprocess1():
    #using the same word bag

    all1 = []
    dictinfo = {}

    file = open('../../../webseds/All-LGseedpages/inputseed.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        if (','.join(row) not in dictinfo):
            dictinfo[','.join(row)] = 1
            all1.append(','.join(row))

    f = open(
        '../../../crawling/initial/URL-based guided search/crawler/fatherURLs.json',
        encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all1.append(key)

    f = open(
        '../../../crawling/initial/Hyperlink-guided search/crawler/LGinlinkurlfirst.json',
        encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all1.append(key)

    f = open(
        '../../../crawling/initial/Title-based guided search/crawler/titlesearchURLs.json',
        encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all1.append(key)

    f = open(
        '../../../crawling/initial/Body-based guided search/crawler/bodysearchURLs.json',
        encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all1.append(key)
    all2=[]
    f = open('../../../crawling/fourth_iteration/Hyperlink guided search/LGinlinkurlfirstnew.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all2.append(key)
    print(len(all2))
    f = open('../../../crawling/fourth_iteration/Similarity guided search/fatherURLsnew.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all2.append(key)
    print(len(all2))

    ###bag of words model
    cv = CountVectorizer(lowercase=True)
    cv.fit(all1)
    ##predicting
    cv_fit_father = cv.transform(all2)
    return cv_fit_father,all2

def bagging(cv_fit_father,all1):
    ###bagging model
    bc = joblib.load( '../../URL-filter/PUbagging_model/bcT100K1:1.pkl')
    file=open('probalineSVC.csv','w')
    probility=bc.predict_proba(cv_fit_father)
    for i in range(0,len(probility)):
        file.writelines(all1[i])
        for key in probility[i]:
            file.writelines('\t'+str(key))
        file.writelines('\n')
####classify new  candidate    URLs into relevant or not
def predict():
    dictnewLG=[]
    proba=[]
    file=open('probalineSVC.csv','r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        dictnewLG.append(','.join(row).split('\t')[0])
        proba.append(float(','.join(row).split('\t')[len(','.join(row).split('\t'))-1]))

    print(len(dictnewLG))
    file=open('baggingresultnew.csv','w')

    for i in range(0,len(proba)):
        if((proba[i])>= 0.2072):
            file.writelines(dictnewLG[i]+'\t'+str(proba[i])+'\t'+'1'+'\n')
        else:
            file.writelines(dictnewLG[i] + '\t' + str(proba[i]) + '\t' + '0' + '\n')


##According to the above classification results, we obtain pre-filtered URLs
def prefilterURL():
    dictinputseed = {}
    file1 = open(
        '../../../webseds/All-LGseedpages/inputseed.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        dictinputseed[','.join(row).split('//')[1]] = ''
    dictpredict={}
    file1 = open('baggingresultnew.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if(','.join(row).split('\t')[2]=='1' and 'http' in ','.join(row).split('\t')[0][:4] ):
            if(','.join(row).split('\t')[0].split('//')[1] in dictpredict):
                if(','.join(row).split('\t')[0] not in dictpredict[','.join(row).split('\t')[0].split('//')[1]]):
                    dictpredict[','.join(row).split('\t')[0].split('//')[1]].append(','.join(row).split('\t')[0])
            else:
                dictpredict[','.join(row).split('\t')[0].split('//')[1]]=[','.join(row).split('\t')[0]]
    dicturl={}
    for key in dictpredict:
        if('https://'+key in dictpredict[key]):
            dicturl['https://'+key]=''
        else:
            dicturl[dictpredict[key][0]] =''


    file = open('prefilteredurl.csv', 'w')
    dictlg = {}
    print(len(dicturl))
    for key in dicturl:
        url = key
        ###remove duplicate URLs
        if ('/lg/' in url and ('ipv4/route' in url or 'ipv6/route' in url)):
            url1 = url.split('/route')[0]
            if (url1 not in dictlg):
                dictlg[url1] = [url]
            else:
                dictlg[url1].append(url)
        elif ('ipv6/lg/route' in url or 'ipv4/lg/route' in url):
            url1 = url.split('/route')[0]
            if (url1 not in dictlg):
                dictlg[url1] = [url]
            else:
                dictlg[url1].append(url)
        else:
            dictlg[url] = []

    for key in dictlg:
        if (dictlg[key] == []):
            url =key
        else:
            url=dictlg[key][0]

        url_sche = url.split('//')[1]
        # 新的
        tag = 0
        for key in dictinputseed:
            if (url_sche in key or key in url_sche):
                tag = 1
                break
        if (tag == 0):
            file.writelines(url + '\n')


if __name__ == '__main__':
    # cv_fit_father, all1 = dataprocess1()
    # bagging(cv_fit_father, all1)
    # predict()
    prefilterURL()
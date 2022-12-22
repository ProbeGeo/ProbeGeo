
import csv
import json

import joblib
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib
#matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.metrics import roc_curve, auc, roc_auc_score

from sklearn.metrics import classification_report as clsr, accuracy_score,recall_score

def preprocess():
    #    #using the same word bag
    allinfo=[]

    contenturl = {}
    file = open('../../getURLs/initial/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        contenturl[','.join(row)] = 0
    print(len(contenturl))

    keylist = {}
    f = open('../../../webseds/All-LGseedpages/afterManualCheck/isLG.csv','r',
             )  # 打开‘json文件
    csv_reader1 = csv.reader(f)
    for row in csv_reader1:
        keylist[','.join(row)] = 0




    file1 = open(
        '../../content-classifier/Extracting_features/isLGtitleplusinput.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        url = ','.join(row).split(',|ProbeGeo|')[0]
        if(url not in keylist):
            continue
        info = url+','+','.join(row).split(',|ProbeGeo|')[1]
        allinfo.append(info)



    file = open('../../content-classifier/Extracting_features/predictLGtitleplusinput.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        url = ','.join(row).split(',|ProbeGeo|')[0]
        if(url not in contenturl):
            continue
        info = url+','+','.join(row).split(',|ProbeGeo|')[1]
        allinfo.append(info)


    allurl1=[]
    allinfo1=[]
    file = open('predictLGtitleplusinput.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        url = ','.join(row).split(',|ProbeGeo|')[0]
        info = url + ',' + ','.join(row).split(',|ProbeGeo|')[1]
        allinfo1.append(info)
        allurl1.append(url)



    cv = CountVectorizer(lowercase=True)
    cv.fit(allinfo)
    ##bag of words
    cv_fit_all = cv.transform(allinfo1)
    ##predicting
    print(len(allinfo))
    print(len(allinfo1))
    return cv_fit_all, allurl1



def bagging(cv_fit_father,allurl):
    ###bagging model
    bc = joblib.load('../../content-classifier/PUbagging_model/bc0.01new.pkl')

    ##predict
    file=open('probalineSVC.csv','w')
    probility=bc.predict_proba(cv_fit_father)
    for i in range(0,len(probility)):
        file.writelines(allurl[i])
        for key in probility[i]:
            file.writelines('\t'+str(key))
        file.writelines('\n')






def KScurve():
    contenturl = {}
    file = open('../../getURLs/third_iteration/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        contenturl[','.join(row)] = 0
    print(len(contenturl))


    file = open('probalineSVC.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        url = ','.join(row).split('\t')[0]
        if(url in contenturl):
            contenturl[url]=float(','.join(row).split('\t')[2])

    d_order = sorted(contenturl.items(), key=lambda x: x[1], reverse=True)




    num=0
    file=open('relevanceprediction.csv','w')
    file1=open('relevanceLG.csv','w')



    for key,value in d_order:
        if(float(value)>= 0.4292):
            num+=1
            file1.writelines(key+'\n')
            file.writelines(key+'\t'+str(contenturl[key])+'\t'+'1'+'\n')
        else:
            file.writelines(key+'\t'+str(contenturl[key])+'\t'+'0'+'\n')
    print(num)



def getcontent():
    keylist={}
    file1 = open( 'relevanceLG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        keylist[','.join(row)] = ''
    print(len(keylist))

    fileopen=open('LGallcontent.csv','w')
    for i in range(1,7):
        print(i)
        file1 = open(
            '../../getURLs/third_iteration/urlcontent'+str(i)+'.csv', 'r')
        csv_reader1 = csv.reader(file1)
        csv.field_size_limit(500 * 1024 * 1024)
        for row in csv_reader1:
            url = ','.join(row).split(',|ProbeGeo|')[0]
            if (url in keylist):
                fileopen.writelines(','.join(row) + '\n')


if __name__ == '__main__':
    # cv_fit_father, all1 = preprocess()
    # bagging(cv_fit_father, all1)
    KScurve()
    getcontent()

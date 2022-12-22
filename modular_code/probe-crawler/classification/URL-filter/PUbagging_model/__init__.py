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

    ##record all URL in the training set
    all = []
    ##label seed URLs in the traning set as 1, lebel other candidate uRLs in the training set as 0
    alllabel = []
    ##record all URLs
    all1=[]
    dictinfo={}


    f = open('../training_validation_datasets/webseds/testlabel.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    file = open('../../../webseds/All-LGseedpages/inputseed.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        if (','.join(row) not in dictinfo):
            dictinfo[','.join(row)] = 1
            all1.append(','.join(row))
            if(','.join(row) not in dicttest):
                all.append(','.join(row))
                alllabel.append(1)


    f = open('../training_validation_datasets/CandidateURLs(URL-based)/testlabel.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    f = open('../../../crawling/initial/URL-based guided search/crawler/fatherURLs.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all1.append(key)
        if(key not in dicttest):
            all.append(key)
            alllabel.append(0)



    f = open('../training_validation_datasets/CandidateURLs(Hyperlink-guided)/testlabel.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    f = open('../../../crawling/initial/Hyperlink-guided search/crawler/LGinlinkurlfirst.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all1.append(key)
        if (key not in dicttest):
            all.append(key)
            alllabel.append(0)



    f = open('../training_validation_datasets/CandidateURLs(Title-based)/testlabel.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    f = open('../../../crawling/initial/Title-based guided search/crawler/titlesearchURLs.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all1.append(key)
        if (key not in dicttest):
            all.append(key)
            alllabel.append(0)



    f = open('../training_validation_datasets/CandidateURLs(Body-based)/testlabel.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    f = open('../../../crawling/initial/Body-based guided search/crawler/bodysearchURLs.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        all1.append(key)
        if (key not in dicttest):
            all.append(key)
            alllabel.append(0)

    #bag-of-words model
    cv = CountVectorizer(lowercase=True)
    cv.fit(all1)
    print(len(cv.get_feature_names()))
    ##training set
    cv_fit_all = cv.transform(all)
    ##test and validation set
    cv_fit_father = cv.transform(all1)
    # print(len(all))
    # print(len(alllabel))
    # print(sum(alllabel))
    return cv_fit_all,alllabel,cv_fit_father,all1

def bagging(cv_fit_all,alllabel,cv_fit_father,all1,c,t,k):
    ###bagging model
    bc = BaggingClassifierPU(
        SVC(class_weight='balanced',C=c,probability=True,kernel='linear'),
        n_estimators=t,  # 1000 trees as usual
        max_samples = int(sum(alllabel)*k), # Balance the positives and unlabeled in each bag
        n_jobs = -1           # Use all cores
    )
    ##这是训练集合得到的模型
    bc.fit(cv_fit_all, alllabel)
    joblib.dump(bc, 'bcT' + str(t) + 'K' + str(K) + '.pkl')
    file=open('probalineSVC'+str(c)+'-'+str(t)+'-'+str(k)+'.csv','w')
    probility=bc.predict_proba(cv_fit_father)
    for i in range(0,len(probility)):
        file.writelines(all1[i])
        for key in probility[i]:
            file.writelines('\t'+str(key))
        file.writelines('\n')


if __name__ == '__main__':
    cv_fit_all, alllabel, cv_fit_father, all1 = dataprocess1()
    ##number of base classifier
    T=[100]
    # the ratio of negative samples (whose number is a variable K) to positive samples (whose number is a constant P=2931 here)
    K=[0.1,0.2,0.5,0.8,0.9, 1,5,10,15]

    for t1 in T:
        for k1 in K:
            bagging(cv_fit_all,alllabel,cv_fit_father,all1,c=10,t=t1,k=k1)

import csv
import json
from sklearn.svm import SVC
from baggingPU import BaggingClassifierPU
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

    ##record all URL in the training set
    urltrain = []
    ##record the extracted feature of each URL in the training set
    infotrain=[]
    ##label seed URLs in the traning set as 1, lebel other pre-filtered URLs in the training set as 0
    labeltrain = []

    ##record all URLs for predicting
    allurl = []
    allinfo=[]

    ##successfully downloaded 77,113 html files (unlabeled samples)
    contenturl = {}
    file = open('../../getURLs/initial/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        contenturl[','.join(row)] = 0
    print(len(contenturl))

    ###1,085 valid seed html files (Positive samples)
    keylist = {}
    f = open('../../../webseeds/All-LGseedpages/afterManualCheck/isLG.csv','r')
    csv_reader1 = csv.reader(f)
    for row in csv_reader1:
        keylist[','.join(row)] = 0
    print(len(keylist))

    f = open('../training_validation_datasets/testlabel.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    print(len(dicttest))

    file1 = open('../Extracting_features/isLGtitleplusinput.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        url = ','.join(row).split(',|ProbeGeo|')[0]
        if(url not in keylist):
            continue
        info = url+','+','.join(row).split(',|ProbeGeo|')[1]
        allurl.append(url)
        allinfo.append(info)
        if(url not in dicttest):
            urltrain.append(url)
            infotrain.append(info)
            labeltrain.append(1)

    file = open('../Extracting_features/predictLGtitleplusinput.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        url = ','.join(row).split(',|ProbeGeo|')[0]
        if(url not in contenturl):
            continue
        info = url+','+','.join(row).split(',|ProbeGeo|')[1]
        allurl.append(url)
        allinfo.append(info)
        if (url not in dicttest):
            urltrain.append(url)
            infotrain.append(info)
            labeltrain.append(0)

    cv = CountVectorizer(lowercase=True)
    cv.fit(allinfo)
    ##bag-of-words model
    cv_fit_all = cv.transform(infotrain)
    ##predict all prefiltered URLs
    cv_fit_father = cv.transform(allinfo)
    print(len(allinfo))
    print(len(infotrain))
    return cv_fit_all, labeltrain, cv_fit_father, allurl


def bagging(cv_fit_all,labeltrain,cv_fit_father,allurl,c):
    ###bagging model
    bc = BaggingClassifierPU(
        SVC(class_weight='balanced',C=c,probability=True,kernel='linear'),
        n_estimators=100,  # 1000 trees as usual
        max_samples = int(sum(labeltrain)), # Balance the positives and unlabeled in each bag
        n_jobs = -1           # Use all cores
    )
    ##trained model
    bc.fit(cv_fit_all, labeltrain)
    joblib.dump(bc, 'bc' + str(c)  + 'new.pkl')
    file=open('probalineSVC'+str(c)+'-'+'new.csv','w')
    probility=bc.predict_proba(cv_fit_father)
    for i in range(0,len(probility)):
        file.writelines(allurl[i])
        for key in probility[i]:
            file.writelines('\t'+str(key))
        file.writelines('\n')


def testroc(c):
    keylist = {}
    f = open('../training_validation_datasets/testlabel-validation.json',encoding='utf-8')
    res = f.read()
    from collections import OrderedDict
    data = json.loads(res, object_pairs_hook=OrderedDict)
    for key in data:
        keylist[key] = [data[key], 0]
    print(len(keylist))
    #record prediction results
    file = open('probalineSVC' + str(c) + '-' + 'new.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        url = ','.join(row).split('\t')[0]
        if (url in keylist):
            keylist[url][1] = float(','.join(row).split('\t')[2])
    testlabel = []
    predictlabel = []
    for key in keylist:
        testlabel.append(int(keylist[key][0]))
        predictlabel.append(float(keylist[key][1]))
    print(len(testlabel))
    fpr, tpr, threshold = roc_curve(testlabel, predictlabel)
    roc_auc = auc(fpr, tpr)  ###calculate auc的值
    print(roc_auc)


def KScurve():
    ##draws the distribution of TPR and FPR of the trained classifier under different $T$
    #choose a T and get prediction results
    contenturl = {}
    file = open('../../getURLs/initial/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        contenturl[','.join(row)] = 0
    print(len(contenturl))
    isLGurl = {}
    file = open('../../../webseeds/All-LGseedpages/afterManualCheck/isLG.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        isLGurl[','.join(row)] = 0
    keylist = {}
    f = open('../training_validation_datasets/testlabel-validation.json',
             encoding='utf-8')
    res = f.read()
    from collections import OrderedDict
    data = json.loads(res, object_pairs_hook=OrderedDict)
    for key in data:
        if(key in contenturl or key in isLGurl ):
            keylist[key] = [data[key], 0]
    print(len(keylist))
    file = open('probalineSVC0.01-new.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        url = ','.join(row).split('\t')[0]
        if (url in keylist):
            keylist[url][1] = float(','.join(row).split('\t')[2])
        if(url in contenturl):
            contenturl[url]=float(','.join(row).split('\t')[2])
        if(url in isLGurl):
            isLGurl[url]=float(','.join(row).split('\t')[2])
    testlabel = []
    predictproba = []
    for key in keylist:
        testlabel.append(int(keylist[key][0]))
        predictproba.append(float(keylist[key][1]))
    fpr, tpr, threshold = roc_curve(testlabel, predictproba)  ###TPR & PFR
    threshold[0]=1
    rocauc_1 = roc_auc_score(testlabel, predictproba)
    print(rocauc_1)

    plt.figure(figsize=(16, 9))
    ks_value = max(abs(fpr - tpr))
    print(ks_value)
    plt.plot(threshold,fpr, label='FPR',linestyle='--',linewidth = '4')
    plt.plot(threshold,tpr, label='TPR',linestyle='--',linewidth = '4')
    plt.legend(fontsize=20)
    plt.grid(ls='--')
    x = np.argwhere(abs(fpr - tpr) == ks_value)[0, 0]
    print(threshold[x:])
    print(tpr[x:])
    x=x



    plt.plot([threshold[x],threshold[x]], [fpr[x], tpr[x]], linewidth=4, color='r')
    plt.xlabel('Threshold', fontsize=30)
    plt.ylabel('TPR/FPR', fontsize=30)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    print(threshold[x])
    print(fpr[x])
    print(tpr[x])
    plt.text(threshold[x], fpr[x]+0.01, '(%0.4f, %0.4f)'%(threshold[x],fpr[x]), fontsize=28)
    plt.text(threshold[x], tpr[x], '(%0.4f, %0.4f)'%(threshold[x],tpr[x]), fontsize=28)
    plt.savefig("KS-curve.png",bbox_inches = 'tight')
    plt.show()



    file=open('relevanceprediction.csv','w')
    for key in contenturl:
        if(float(contenturl[key])>= 0.4292):
            file.writelines(key+'\t'+str(contenturl[key])+'\t'+'1'+'\n')
        else:
            file.writelines(key+'\t'+str(contenturl[key])+'\t'+'0'+'\n')
    for key in isLGurl:
        if(float(isLGurl[key])>= 0.4292):
            file.writelines(key+'\t'+str(isLGurl[key])+'\t'+'1'+'\n')
        else:
            file.writelines(key+'\t'+str(isLGurl[key])+'\t'+'0'+'\n')




def calrecallontest():
    ##To evaluate the generalization ability of the trained classifier, we calculate the TPR and FPR performance on the test set by running  \_init\_.py.

    keylist = {}
    f = open('../training_validation_datasets/testlabel-test.json',
             encoding='utf-8')  #
    res = f.read()  #
    from collections import OrderedDict
    data = json.loads(res, object_pairs_hook=OrderedDict)
    for key in data:
        keylist[key] = [data[key], 0]

    file1 = open('relevanceprediction.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if( ','.join(row).split('\t')[0] in keylist):
            keylist[','.join(row).split('\t')[0]][1]=int(','.join(row).split('\t')[2])
            if(keylist[','.join(row).split('\t')[0]][0]=='1' and keylist[','.join(row).split('\t')[0]][1]==0):
                print(','.join(row).split('\t')[0])

    testlabel = []
    predictlabel = []
    print(len(keylist))
    for key in keylist:
        testlabel.append(int(keylist[key][0]))
        predictlabel.append(int(keylist[key][1]))

    # print(recall_score(testlabel, predictlabel, average='macro'))
    print(clsr(testlabel, predictlabel,digits=4))


if __name__ == '__main__':
    ##data process
    # cv_fit_all, alllabel, cv_fit_father, all1 = preprocess()
    ## train multiple classifiers under different hyperparameters, taking the parameter c as an example, the specific process is as follows
    # for c in [1e-3,1e-2,1e-1,1,10,100,1000]:
    #     print(c)
        # bagging(cv_fit_all, alllabel, cv_fit_father, all1, c)
        # testroc(c)
    #draws the distribution of TPR and FPR of the trained classifier under different $T$
    KScurve()
    #To evaluate the generalization ability of the trained classifier
    calrecallontest()

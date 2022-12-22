
import json
import csv

import math
from pandas import np
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.metrics import classification_report as clsr, accuracy_score,recall_score
import matplotlib.pyplot as plt
# import cv2
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix

###calculate the AUC performance of multiple trained pre-filters on the validation dataset,
def analysis(c):


    resultURL=[]
    resultpredict=[]
    resultproba=[]
    file1 = open('probalineSVC10-100-'+str(c)+'.csv', 'r')
    csv_reader1 = csv.reader(file1)
    i=0
    for row in csv_reader1:
        resultURL.append(','.join(row).split('\t')[0])
        resultproba.append(float(','.join(row).split('\t')[2]))
        i+=1

    print(len(resultURL))
    print(len(resultproba))




    testlabel = []
    testurl = []
    predictproba=[]
    f = open('../training_validation_datasets/webseds/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(0,2991):
        if(resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictproba.append(resultproba[i])



    f = open('../training_validation_datasets/CandidateURLs(URL-based)/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(2991, 436856):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))

            predictproba.append(resultproba[i])
    # print(len(testlabel))
    # print(len(testurl))

    f = open('../training_validation_datasets/CandidateURLs(Hyperlink-guided)/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    print(len(dicttest))
    for i in range(436856,441292):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))

            predictproba.append(resultproba[i])

    f = open('../training_validation_datasets/CandidateURLs(Title-based)/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range( 441292,903091):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictproba.append(resultproba[i])


    f = open('../training_validation_datasets/CandidateURLs(Body-based)/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(903091,922884):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictproba.append(resultproba[i])

    print(len(testlabel))
    print(len(predictproba))
    rocauc_1 = roc_auc_score(testlabel, predictproba)

    return rocauc_1





def KScurve(filename1,m,filename2):

    resultURL = []
    resultproba = []
    file1 = open(filename1, 'r')
    csv_reader1 = csv.reader(file1)
    i = 0
    for row in csv_reader1:
        resultURL.append(','.join(row).split('\t')[0])
        resultproba.append(float(','.join(row).split('\t')[m]))
        if (float(','.join(row).split('\t')[m]) >1):
            print('error')
            print(resultURL[i])
        i += 1

    print(len(resultURL))
    print(len(resultproba))

    testlabel = []
    testurl = []
    predictproba = []
    f = open('../training_validation_datasets/webseds/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(0, 2991):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictproba.append(float(resultproba[i]))

    f = open('../training_validation_datasets/CandidateURLs(URL-based)/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(2991, 436856):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictproba.append(float(resultproba[i]))

    f = open('../training_validation_datasets/CandidateURLs(Hyperlink-guided)/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    print(len(dicttest))
    for i in range(436856, 441292):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))

            predictproba.append(float(resultproba[i]))


    f = open('../training_validation_datasets/CandidateURLs(Title-based)/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(441292, 903091):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictproba.append(float(resultproba[i]))

    f = open('../training_validation_datasets/CandidateURLs(Body-based)/testlabel-validation.json', encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(903091, 922884):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictproba.append(float(resultproba[i]))

    print('the number of URL in the validation set')
    numpos = 0
    print(len(testlabel))
    for i in range(0, len(testlabel)):
        if (testlabel[i] == 1):
            numpos += 1
    print('the number of positive samples in the validation set')
    print(numpos)

    ##plot figure2 in the paper
    fpr, tpr, threshold = roc_curve(testlabel, predictproba)
    threshold[0]=1
    rocauc_1 = roc_auc_score(testlabel, predictproba)
    print(rocauc_1)

    plt.figure(figsize=(12, 10))
    ks_value = max(abs(fpr - tpr))
    print(ks_value)
    plt.plot(threshold,fpr, label='FPR',linestyle='--',linewidth = '4')
    plt.plot(threshold,tpr, label='TPR',linestyle='--',linewidth = '4')
    plt.legend(fontsize=20)
    plt.grid(ls='--')
    x = np.argwhere(abs(fpr - tpr) == ks_value)[0, 0]
    print(threshold[x:])
    print(tpr[x:])
    x=x+5




    plt.plot([threshold[x],threshold[x]], [fpr[x], tpr[x]], linewidth=4, color='r')
    # plt.scatter((x, x), (0, ks_value), color='r')
    plt.xlabel('$T$\n(a)', fontsize=28)
    plt.ylabel('TPR/FPR', fontsize=28)
    plt.xticks(fontsize=28)
    plt.yticks(fontsize=28)
    print(threshold[x])
    print(fpr[x])
    print(tpr[x])
    plt.text(threshold[x], fpr[x]+0.01, '(0.2072,0.1554)', fontsize=28)
    plt.text(threshold[x], tpr[x], '(0.2072,0.9907)', fontsize=28)
    plt.savefig("KS-curve.png",bbox_inches = 'tight')
    plt.show()



    file=open(filename2,'w')
    for i in range(0,len(resultURL)):
        if(resultproba[i]>= 0.2072):

            file.writelines(resultURL[i]+'\t'+str(resultproba[i])+'\t'+'1'+'\n')

        else:
            file.writelines(resultURL[i]+'\t'+str(resultproba[i])+'\t'+'0'+'\n')





def calrecallontest():
    resultURL = []
    resultpredict = []

    file1 = open('baggingresultnew.csv', 'r')
    csv_reader1 = csv.reader(file1)
    i = 0
    for row in csv_reader1:
        resultURL.append(','.join(row).split('\t')[0])
        resultpredict.append(int(','.join(row).split('\t')[2]))
        i += 1

    print(len(resultURL))
    print(len(resultpredict))

    testlabel = []
    testurl = []
    predictlabel = []
    f = open('../training_validation_datasets/webseds/testlabel-test.json',
             encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(0, 2991):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictlabel.append(resultpredict[i])



    f = open('../training_validation_datasets/CandidateURLs(URL-based)/testlabel-test.json',
             encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(2991, 436856):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictlabel.append(resultpredict[i])

    f = open('../training_validation_datasets/CandidateURLs(Hyperlink-guided)/testlabel-test.json',
             encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(436856, 441292):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictlabel.append(resultpredict[i])


    f = open('../training_validation_datasets/CandidateURLs(Title-based)/testlabel-test.json',
             encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(441292, 903091):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictlabel.append(resultpredict[i])


    f = open('../training_validation_datasets/CandidateURLs(Body-based)/testlabel-test.json',
             encoding='utf-8')  #
    res = f.read()  #
    dicttest = json.loads(res)
    for i in range(903091, 922884):
        if (resultURL[i] in dicttest):
            testurl.append(resultURL[i])
            testlabel.append(int(dicttest[resultURL[i]]))
            predictlabel.append(resultpredict[i])


    for i in range(0,len(predictlabel)):
        if(testlabel[i]==1 and predictlabel[i]==0):
            print(testurl[i])
    print(len(testurl))
    print(clsr(testlabel, predictlabel,digits=4))


if __name__ == "__main__":

    #hyperparameter tunning
    # K = [0.1, 0.2, 0.5,0.8, 0.9, 1, 5, 10, 15]
    # for c in K:
    #     print(c)
    #     print(analysis(c))
    #
    #
    # #Figure 2(a) in our paper which draws the distribution of TPR and FPR of the trained pre-filter under different $T$ is also drawn with deal.py.
    # KScurve('probalineSVC10-100-1.csv',2,'baggingresultnew.csv')
    #

    #run deal.py to calculate the TPR and FPR performance of the pre-filter on the test set.
    calrecallontest()






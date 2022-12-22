import csv
import re
import json


def results():
    dictrelev={}
    file=open('../../../classification/relevant-URLs/third_iteration/relevanceLG.csv','r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        dictrelev[','.join(row)]=''
    dictlg={}
    for i in range(0, 15):
        file1 = open('Middle_results_' + str(i) + '.csv', 'r')
        csv_reader1 = csv.reader(file1)
        for row in csv_reader1:
            if(row[0] not in dictrelev):
                continue
            str1=','.join(row)
            title = re.findall(r'<title>(.*?)<\/title>', str1, re.S | re.M)
            for l in title:
                if(l!=''):
                    name=l.split('<URL>')[0]
                    if(name!=''):
                        el=l.split(name)[1]
                        urls= re.findall(r'<URL>(.*?),<\/URL>',el, re.S | re.M)
                        for url in urls:
                            dictlg[url]=name
    with open("fatherURLs.json", "w") as f:
        json.dump(dictlg, f)
    print(len(dictlg))


def removeduple():
    dictpre = {}
    f = open('../../initial/URL-based guided search/crawler/fatherURLs.json',encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] = ''
    f = open('../../initial/Hyperlink-guided search/crawler/LGinlinkurlfirst.json',encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] = ''
    f = open('../../initial/Title-based guided search/crawler/titlesearchURLs.json',encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] = ''
    f = open('../../initial/Body-based guided search/crawler/bodysearchURLs.json',encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] = ''
    f = open('../../second_iteration/Similarity guided search/fatherURLs.json',encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] = ''
    f = open('../../second_iteration/Hyperlink guided search/LGinlinkurlfirst.json',encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        try:
            if ('http' in key[:4] and key != 'http' and key.split('//')[1] not in dictpre):
                dictpre[key.split('//')[1]] = ''
        except IndexError as e:
            continue
    f = open('../../third_iteration/Similarity guided search/fatherURLs.json',encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] = ''

    f = open('../../third_iteration/Hyperlink guided search/LGinlinkurlfirst.json',encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        try:
            if ('http' in key[:4] and key != 'http' and key.split('//')[1] not in dictpre):
                dictpre[key.split('//')[1]] = ''
        except IndexError as e:
            continue
    dictnew={}
    f = open('fatherURLs.json', encoding='utf-8')
    res = f.read()
    from collections import OrderedDict
    data = json.loads(res, object_pairs_hook=OrderedDict)
    for key in data:
        if('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictnew[key]=''
    with open("fatherURLsnew.json", "w") as f:
        json.dump(dictnew, f)
    print(len(dictnew))


if __name__ == '__main__':
    # results()
    removeduple()
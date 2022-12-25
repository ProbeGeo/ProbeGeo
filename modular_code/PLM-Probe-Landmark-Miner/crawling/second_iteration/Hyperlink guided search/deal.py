import csv
import re
import json


def results():
    dictrelev = {}
    file = open('../../../classification/relevant-URLs/initial/relevanceLG.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        dictrelev[','.join(row)] = ''
    dictlg={}
    for i in range(0, 10):
        print(str(i))
        file1 = open('inputseed_results_' + str(i) + '.csv', 'r')
        csv_reader1 = csv.reader((line.replace('\0','') for line in file1))
        csv.field_size_limit(500 * 1024 * 1024)
        for row in csv_reader1:
            try:
                str1=','.join(row)
                # print(str1)
                url=str1.split(',|ProbeGeo|')[0]
                if(url not in dictrelev):
                    continue
                content=str1.split(',|ProbeGeo|')[1]
                    # print(content)
                title = re.findall(r'<URL>(.*?)<\/URL>', content, re.S | re.M)
                for l in title:
                    dictlg[l]=''
            except IndexError as e:
                continue
    with open("LGinlinkurlfirst.json", "w") as f:
        json.dump(dictlg, f)
    print(len(dictlg))


def removeduple():
    dictpre={}
    ##remove the duplicate of the previous candidate URLs
    f = open('../../initial/URL-based guided search/crawler/fatherURLs.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]]=''
    f = open('../../initial/Hyperlink-guided search/crawler/LGinlinkurlfirst.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ( 'http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] =''
    f = open('../../initial/Title-based guided search/crawler/titlesearchURLs.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] = ''
    f = open('../../initial/Body-based guided search/crawler/bodysearchURLs.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if ('http' in key[:4] and key.split('//')[1] not in dictpre):
            dictpre[key.split('//')[1]] = ''
    dictnew={}
    f = open('LGinlinkurlfirst.json', encoding='utf-8')
    res = f.read()
    from collections import OrderedDict
    data = json.loads(res, object_pairs_hook=OrderedDict)
    for key in data:
        try:
            if('http' in key[:4] and key.split('//')[1] not in dictpre):
                dictnew[key]=''
        except IndexError as e:
            continue
    with open("LGinlinkurlfirstnew.json", "w") as f:
        json.dump(dictnew, f)
    print(len(dictnew))


if __name__ == '__main__':
    # results()
    removeduple()
import csv
import csv
import json

import re

from collections import OrderedDict
import mechanize


## we extract texts, id attribute, name attribute, and value attribute  inside input, select, and button elements

def inputfromprefiltered():
    dictpre1 = {}
    file1 = open(
        '../../getURLs/forth_iteration/getcontenturl.csv',
        'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dictpre1[','.join(row)] = 0

    dicturlpre = {}
    for i in range(1,7):
        file1 = open(
            '../../getURLs/forth_iteration/urlcontent'
        +str(i)+'.csv',
            'r')
        csv_reader1 = csv.reader(file1)
        for row in csv_reader1:
            if (','.join(row).split(',|ProbeGeo|')[0] in dictpre1):
                dicturlpre[','.join(row).split(',|ProbeGeo|')[0]] = [','.join(row), '']

        for key in dicturlpre:
            str1 = ''
            # print(dicturlpre)
            for li in ['input', 'select', 'button']:
                title = re.findall(r'\|ProbeGeo\|' + li + '-text:(.*?),\|ProbeGeo\|', dicturlpre[key][0].lower(), re.S | re.M)
                if (title):
                    str1 += ' ' + title[0]
                title = re.findall(r'\|ProbeGeo\|' + li + '-id:(.*?),\|ProbeGeo\|', dicturlpre[key][0].lower(), re.S | re.M)
                if (title):
                    str1 += ' ' + title[0]
                title = re.findall(r'\|ProbeGeo\|' + li + '-name:(.*?),\|ProbeGeo\|', dicturlpre[key][0].lower(), re.S | re.M)
                if (title):
                    str1 += ' ' + title[0]
                title = re.findall(r'\|ProbeGeo\|' + li + '-value:(.*?),\|ProbeGeo\|', dicturlpre[key][0].lower(), re.S | re.M)
                if (title):
                    str1 += ' ' + title[0]
            dicturlpre[key][1] = str1.replace('\n', ' ').replace('\t', ' ')

        file2 = open('predictLGinput'+str(i)+'.csv', 'w')
        for key in dicturlpre:
            file2.writelines(key + ',|ProbeGeo|' + dicturlpre[key][1] + '\n')




def extract():
    dictpre1 = {}
    file1 = open('../../getURLs/forth_iteration/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dictpre1[','.join(row)] = 0




    dicturlpre = {}
    csv.field_size_limit(500 * 1024 * 1024)
    for i in range(1, 7):
        file1 = open(
            'predictLGinput' + str(i) + '.csv', 'r')
        csv_reader1 = csv.reader(file1)
        for row in csv_reader1:
            if(','.join(row).split(',|ProbeGeo|')[0] in dictpre1):
                dicturlpre[','.join(row).split(',|ProbeGeo|')[0]] = [','.join(row),'']


    for key in dicturlpre:
        str1 = ''
        # print(dicturlpre)
        for li in ['input', 'select', 'button']:
            title = re.findall(r'\|ProbeGeo\|' + li + '-text:(.*?),\|ProbeGeo\|', dicturlpre[key][0].lower(), re.S | re.M)
            if (title):
                str1 += ' ' + title[0]
            title = re.findall(r'\|ProbeGeo\|' + li + '-id:(.*?),\|ProbeGeo\|', dicturlpre[key][0].lower(), re.S | re.M)
            if (title):
                str1 += ' ' + title[0]
            title = re.findall(r'\|ProbeGeo\|' + li + '-name:(.*?),\|ProbeGeo\|', dicturlpre[key][0].lower(), re.S | re.M)
            if (title):
                str1 += ' ' + title[0]
            title = re.findall(r'\|ProbeGeo\|' + li + '-value:(.*?),\|ProbeGeo\|', dicturlpre[key][0].lower(), re.S | re.M)
            if (title):
                str1 += ' ' + title[0]
        dicturlpre[key][1] = str1.replace('\n', ' ').replace('\t', ' ')


    file2 = open('predictLGinput.csv', 'w')
    for key in dicturlpre:
        file2.writelines(key+',|ProbeGeo|'+dicturlpre[key][1]+'\n')


#extract title
def meargetitle():

    dictpre1 = {}
    csv.field_size_limit(500 * 1024 * 1024)
    file1 = open('../../getURLs/forth_iteration/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        # 0表示没有内容
        dictpre1[','.join(row)] = 0

    file=open('predictLGtitle.csv','w')
    for i in range(1, 7):
        file1 = open(
            '../../getURLs/forth_iteration/urlcontent'+str(i)+'.csv','r')
        csv_reader1 = csv.reader(file1)
        for row in csv_reader1:
            try:
                html=','.join(row).split(',|ProbeGeo|')[2]
                url=','.join(row).split(',|ProbeGeo|')[0]
                title = re.findall(r'<title>(.*?)<\/title>', html.lower(), re.S | re.M)
                if (title and  url in dictpre1):
                    dictpre1[url]=title[0]
            except IndexError as e:
                continue

    for key in dictpre1:
        file.writelines(key + ',|ProbeGeo|' + dictpre1[key] + '\n')


def titlepluscontrol(f1name,f2name,f3name,f4name):
    keylist={}
    file1 = open(f1name, 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if (','.join(row) not in keylist):
            keylist[','.join(row)] = 0
    print(len(keylist))
    dictisLG = {}
    csv.field_size_limit(500 * 1024 * 1024)
    file1 = open(f2name, 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if(','.join(row).split(',|ProbeGeo|')[0] in keylist and ','.join(row).split(',|ProbeGeo|')[1].replace(' ','')!=''):
            dictisLG[','.join(row).split(',|ProbeGeo|')[0]]=','.join(row).split(',|ProbeGeo|')[1]
    file1 = open(f3name, 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if (','.join(row).split(',|ProbeGeo|')[0] in keylist and ','.join(row).split(',|ProbeGeo|')[1].replace(' ','')!=''):
            if(','.join(row).split(',|ProbeGeo|')[0] in dictisLG):
                dictisLG[','.join(row).split(',|ProbeGeo|')[0]] += ' '+','.join(row).split(',|ProbeGeo|')[1]
            else:
                dictisLG[','.join(row).split(',|ProbeGeo|')[0]] = ','.join(row).split(',|ProbeGeo|')[1]
    print(len(dictisLG))
    file2=open(f4name,'w')
    for key in dictisLG:
        file2.writelines(key+',|ProbeGeo|'+dictisLG[key]+'\n')

if __name__ == '__main__':
    inputfromprefiltered()
    extract()
    meargetitle()
    titlepluscontrol('../../getURLs/forth_iteration/getcontenturl.csv','predictLGtitle.csv','predictLGinput.csv','predictLGtitleplusinput.csv')

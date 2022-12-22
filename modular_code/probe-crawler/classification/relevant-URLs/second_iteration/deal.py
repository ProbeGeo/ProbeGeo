import csv
import csv
import json

import re

from collections import OrderedDict
import mechanize



## we extract texts, id attribute, name attribute, and value attribute  inside input, select, and button elements
from bs4 import BeautifulSoup


def inputfromprefiltered():
    dictpre={}
    file1 = open(
        '../../getURLs/second_iteration/getcontenturl.csv',
        'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        dictpre[','.join(row)] = ''

    file2=open('predictLGinput.csv','w')

    file1 = open(
        '../../getURLs/second_iteration/urlcontent.csv',
        'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        url = ','.join(row).split(',|ProbeGeo|')[0]
        if(url not in dictpre):
            continue
        try:
            html = ','.join(row).split(',|ProbeGeo|')[2]
        except IndexError as e:
            continue
        if (html.replace(' ', '') == ''):
            continue
        try:
            print(url)
            dictinfo={'input-text':[],'input-id':[],'input-name':[],"input-value":[],
                      'select-text': [], 'select-id': [], 'select-name': [], "select-value": [],
                      'button-text': [], 'button-id': [], 'button-name': [], "button-value": []

                      }

            soup = BeautifulSoup(html.lower(), "html.parser")
            for li in ['input', 'select', 'button']:
                VIEWSTATE = soup.find_all([li])
                for view in VIEWSTATE:
                    try:
                        content = view.get_text().replace('\n', ' ').replace('\t', ' ')
                        dictinfo[li+'-text'].append(content)
                    except KeyError as e:
                        dictinfo[li + '-text'].append('')
                        m = 0
                    try:
                        content = view["id"].replace('\n', ' ').replace('\t', ' ')
                        dictinfo[li+'-id'].append(content)
                    except KeyError as e:
                        dictinfo[li+'-id'].append('')
                        m = 0
                    try:
                        content = view["name"].replace('\n', ' ').replace('\t', ' ')
                        dictinfo[li+'-name'].append(content)

                    except KeyError as e:
                        dictinfo[li+'-name'].append('')

                        m = 0
                    try:
                        content = view["value"].replace('\n', ' ').replace('\t', ' ')
                        dictinfo[li+'-value'].append(content)

                    except KeyError as e:
                        dictinfo[li+'-value'].append('')
                        m = 0
            string1=url+',|ProbeGeo|'
            for key in dictinfo:
                string1+=key+":"+','.join(dictinfo[key])+',|ProbeGeo|'
            string1 += '\n'
            file2.writelines(string1)
            file2.flush()
        except AttributeError as e:
            continue
        except UnicodeDecodeError as e:
            continue
        except UnicodeEncodeError as e:
            continue
        except TypeError as e:
            continue
        except UnboundLocalError as e:
            continue

def extract():
    dictpre1 = {}
    file1 = open('../../getURLs/second_iteration/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dictpre1[','.join(row)] = 0


    dicturlpre={}
    file1 = open('predictLGinput.csv', 'r')
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


    file2 = open('predictLGinput.csv', 'w')
    for key in dicturlpre:
        file2.writelines(key+',|ProbeGeo|'+dicturlpre[key][1]+'\n')

#extract title
def meargetitle():
    ##
    dictpre1 = {}
    csv.field_size_limit(500 * 1024 * 1024)
    file1 = open('../../getURLs/second_iteration/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        # 0表示没有内容
        dictpre1[','.join(row)] = 0

    file=open('predictLGtitle.csv','w')
    file1 = open('../../getURLs/second_iteration/urlcontent.csv', 'r')
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
    extract()
    meargetitle()
    titlepluscontrol('../../getURLs/second_iteration/getcontenturl.csv','predictLGtitle.csv','predictLGinput.csv','predictLGtitleplusinput.csv')

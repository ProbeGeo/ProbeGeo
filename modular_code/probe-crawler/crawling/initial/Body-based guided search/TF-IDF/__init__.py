# !usr/bin/env python
# encoding:utf-8
from bs4 import BeautifulSoup
from lxml import etree
import csv
import json
import re


def deal():

    ##extract informative texts from all valid seed html  les and these texts are merged into a document,
    dicturl={}
    file1 = open('../../../../webseds/All-LGseedpages/urlcontentnew.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        url=','.join(row).split(',|ProbeGeo|')[0]
        try:
            html=','.join(row).split(',|ProbeGeo|')[2]
        except IndexError as e:
            continue
        if(html.replace(' ','')==''):
            continue
        try:
            dicturl[url]=''
            # print(html.getElementsByTagName("input"))
            soup = BeautifulSoup(html.lower(), "html.parser")
            VIEWSTATE = soup.find_all(['input', 'select', 'button'])
            # VIEWSTATE = soup.find('input')["id"]
            # VIEWSTATE = soup.find('input')["name"]
            # VIEWSTATE = soup.find('input').get_text()
            for view in VIEWSTATE:
                try:
                    dicturl[url] +=view.get_text().replace('\n', ' ').replace('\t', ' ') + ','
                except KeyError as e:
                    m = 0
        except AttributeError as e:
            continue
        except UnicodeDecodeError as e:
            continue
        except UnicodeEncodeError as e:
            continue
    with open("LGselectcontent.json", "w") as f:
        json.dump(dicturl, f)


###
if __name__ == '__main__':
    deal()
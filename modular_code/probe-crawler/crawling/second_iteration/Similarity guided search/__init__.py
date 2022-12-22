
import urllib.request
import urllib.request
import requests
import re
import math
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import json
import threading
import csv
from selenium.webdriver.chrome.options import Options
import selenium

def do_something(urllist,be,ed,thread_index):

    f1 = open('Middle_results_' + str(int(thread_index)) + '.csv', 'a')
    chrome_options = Options()
    browser = webdriver.Chrome(chrome_options=chrome_options)
    url = 'https://cn.bing.com/search?q=hello&ensearch=1&first=1&FORM=PERE'
    browser.get(url)
    time.sleep(30)

    for num in range(be,ed):
        str1=''
        key = urllib.parse.quote(urllist[num])
        url = 'https://cn.bing.com/search?q=' + key + '&ensearch=1&first=1&FORM=PERE'
        try:
            browser.get(url)
        except selenium.common.exceptions.TimeoutException as e:
            print(e)
            continue
        time.sleep(1)
        js = 'window.scrollTo(0, document.body.scrollHeight);'
        browser.execute_script(js)
        source_code = browser.page_source
        time.sleep(3)
        soup = bs(source_code, "html.parser")
        count = soup.findAll(class_="sb_count")
        resultnum=0
        for c in count:
            try:
                resultnum=int(c.get_text().split(' ')[0].replace(',',''))
                print(resultnum)
            except ValueError as e:
                print(e)
                continue

        if(resultnum!=0 ):
            ##得到有多少页
            page=int(int(resultnum)/30)+1
            if(page>350):
                page=350
            for i in range(0,page):
                url = 'https://cn.bing.com/search?q=' + key + '&ensearch=1&first='+str(i*30+1)+'&FORM=PERE'
                try:
                    browser.get(url)
                except selenium.common.exceptions.TimeoutException as e:
                    print(e)
                    continue

                time.sleep(1)
                js = 'window.scrollTo(0, document.body.scrollHeight);'
                browser.execute_script(js)
                time.sleep(5)
                browser.execute_script(js)
                time.sleep(1)
                source_code = browser.page_source
                if('There are no results for' in source_code.replace('\n','')):
                    print('当前URL检索完成')
                    break
                soup = bs(source_code, "html.parser")
                td = soup.findAll("h2")
                str1+=urllist[num]+','+str(i*30+1)+','+str(resultnum)+','
                str1pre=str1
                str2=''
                for t in td:
                    str1 += '<title>' + t.get_text() + '<URL>'
                    str2 += '<title>' + t.get_text() + '<URL>'

                    pattern = re.compile(r'href="([^"]*)"')
                    h = re.search(pattern, str(t))
                    if h:
                        for x in h.groups():
                            str1 += x + ','
                            str2 += x + ','

                    str1 += '</URL></title>,'
                    str2 += '</URL></title>,'
                str1 += '\n'
                if (str2 in str1pre):
                    print('当前URL检索完成')
                    break

        else:
            continue


        f1.writelines(str1)
        f1.flush()




if __name__ == '__main__':



    dicturl = []
    file1 = open('../../../classification/relevant-URLs/initial/relevanceLG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
       dicturl.append(','.join(row))
    print(len(dicturl))


    print(len(dicturl))
    d = 10
    num = int(len(dicturl) / d)
    for i in range(d):
        if (i != (d - 1)):
            t = threading.Thread(target=do_something, args=(dicturl, num * i, num * (i + 1), i))
            t.start()
            time.sleep(30)
        else:
            t = threading.Thread(target=do_something,
                                 args=(dicturl, num * i, len(dicturl) , i))
            t.start()
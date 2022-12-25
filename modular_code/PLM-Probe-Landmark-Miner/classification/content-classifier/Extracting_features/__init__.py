import csv
import re
import csv
from bs4 import BeautifulSoup


# we extract title from the 1085 valid seed html files
def titlefromseed():

    dictlg={}
    file1 = open('../../../webseeds/All-LGseedpages/afterManualCheck/isLG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        dictlg[row[0]]=''

    file1 = open('../../../webseeds/All-LGseedpages/urlcontentnew.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        html=','.join(row).split(',|ProbeGeo|')[2]
        url=','.join(row).split(',|ProbeGeo|')[0]
        title = re.findall(r'<title>(.*?)<\/title>', html.lower(), re.S | re.M)
        if (title and  url in dictlg):
            dictlg[url]=title[0]

    file=open('isLGtitle.csv','w')
    for key in dictlg:
        file.writelines(key+',|ProbeGeo|'+dictlg[key]+'\n')

# we extract texts, id attribute, name attribute, and value attribute  inside input, select, and button elements
def inputinfofromseed():
    dictlg = {}
    file1 = open('../../../webseeds/All-LGseedpages/afterManualCheck/isLG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        dictlg[row[0]] = ''

    file1 = open('../../../webseeds/All-LGseedpages/urlcontentnew.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:

        url = ','.join(row).split(',|ProbeGeo|')[0]
        if (url not in dictlg):
            continue
        try:
            html = ','.join(row).split(',|ProbeGeo|')[2]
        except IndexError as e:
            continue
        if (html.replace(' ', '') == ''):
            continue
        try:

            # print(html.getElementsByTagName("input"))
            soup = BeautifulSoup(html.lower(), "html.parser")
            VIEWSTATE = soup.find_all(['input','select','button'])
                # VIEWSTATE = soup.find('input')["id"]
                # VIEWSTATE = soup.find('input')["name"]
                # VIEWSTATE = soup.find('input').get_text()

            for view in VIEWSTATE:
                try:
                    dictlg[url] += view.get_text().replace('\n',' ').replace('\t',' ')+ ','
                except KeyError as e:
                    m=0
                try:
                    dictlg[url] += view["id"].replace('\n', ' ').replace('\t', ' ') + ','
                except KeyError as e:
                    m = 0
                try:
                    dictlg[url] += view["name"].replace('\n', ' ').replace('\t', ' ') + ','
                except KeyError as e:
                    m = 0
                try:
                    dictlg[url] += view["value"].replace('\n', ' ').replace('\t', ' ') + ','
                except KeyError as e:
                    m = 0

        except AttributeError as e:
            continue
        except UnicodeDecodeError as e:
            continue
        except UnicodeEncodeError as e:
            continue

    file = open('isLGinput.csv', 'w')
    for key in dictlg:
        file.writelines(key + ',|ProbeGeo|' + dictlg[key] + '\n')

# we extract title from the successfully downloaded pre-filtered URLs
def titlefromprefilter():
    dictpre = {}
    file1 = open('../../getURLs/initial/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        dictpre[','.join(row)] = ''

    file1 = open('../../getURLs/initial/urlcontent.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        try:
            html = ','.join(row).split(',|ProbeGeo|')[2]
            url = ','.join(row).split(',|ProbeGeo|')[0]
            title = re.findall(r'<title>(.*?)<\/title>', html.lower(), re.S | re.M)
            if (title and url in dictpre):
                dictpre[url] = title[0]
        except IndexError as e:
            continue

    file = open('predictLGtitle.csv', 'w')
    for key in dictpre:
        file.writelines(key + ',|ProbeGeo|' + dictpre[key] + '\n')

# we extract texts, id attribute, name attribute, and value attribute  inside input, select, and button elements
def inputfromprefiltered():
    dictpre={}
    file1 = open(
        '../../getURLs/initial/getcontenturl.csv',
        'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        dictpre[','.join(row)] = ''

    file2=open('predictLGinput.csv','w')

    file1 = open(
        '../../getURLs/initial/urlcontent.csv',
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

##extract all valuable information from the above file
def extract():
    dicturlpre = {}
    csv.field_size_limit(500 * 1024 * 1024)
    file1 = open('predictLGinput.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        dicturlpre[','.join(row).split(',|ProbeGeo|')[0]] = [','.join(row), '']
    # dicturlpre['https://zh.wikiversity.org/wiki/Template:Notelist-lg']='https://zh.wikiversity.org/wiki/Template:Notelist-lg,|ProbeGeo|input-text:,,,,,,,|ProbeGeo|input-id:toctogglecheckbox,,,searchinput,,mw-searchbutton,searchbutton,|ProbeGeo|input-name:,,,search,title,fulltext,go,|ProbeGeo|input-value:,,,,special:搜索,搜索,前往,|ProbeGeo|select-text:,|ProbeGeo|select-id:,|ProbeGeo|select-name:,|ProbeGeo|select-value:,|ProbeGeo|button-text:,|ProbeGeo|button-id:,|ProbeGeo|button-name:,|ProbeGeo|button-value:,|ProbeGeo|'
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
        file2.writelines(key + ',|ProbeGeo|' + dicturlpre[key][1] + '\n')

##combine title, URL,  texts, id attribute, name attribute, and value attribute  inside input, select, and button elements of each html file
def titlepluscontrol(f1name,f2name,f3name,f4name):
    ##record URL
    keylist={}
    file1 = open(f1name, 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if (','.join(row) not in keylist):
            keylist[','.join(row)] = 0
    print(len(keylist))
    dictisLG = {}
    csv.field_size_limit(500 * 1024 * 1024)
    ##obtain title
    file1 = open(f2name, 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        if(','.join(row).split(',|ProbeGeo|')[0] in keylist and ','.join(row).split(',|ProbeGeo|')[1].replace(' ','')!=''):
            dictisLG[','.join(row).split(',|ProbeGeo|')[0]]=','.join(row).split(',|ProbeGeo|')[1]
    ##obtain texts inside input, select, and button elements of each html file
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
    titlefromseed()
    inputinfofromseed()
    titlefromprefilter()
    inputfromprefiltered()
    extract()
    titlepluscontrol('../../../webseeds/All-LGseedpages/afterManualCheck/isLG.csv','isLGtitle.csv','isLGinput.csv','isLGtitleplusinput.csv')
    titlepluscontrol('../../getURLs/initial/getcontenturl.csv','predictLGtitle.csv','predictLGinput.csv','predictLGtitleplusinput.csv')

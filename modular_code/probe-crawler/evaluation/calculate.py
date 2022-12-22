
import csv
import json
###provide an overview of experimental results provided by running the hyperlink-guided search and the similarity-guided search.
def initialhowmanyrelevant(relevant,candidate):
    dictrelev = {}
    file = open(relevant, 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        dictrelev[','.join(row)] = 0
    print(len(dictrelev))
    filelist = candidate
    f = open(filelist, encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    #how many candidate uRLs
    print(len(data))
    for key in data:
        if(key in dictrelev):
            dictrelev[key]=1
    num=0
    for key in dictrelev:
        if(dictrelev[key]==1):
            num+=1
    print(num)


def initalhowmanyrelevantall():
    import csv

    relevant = [
        '../classification/relevant-URLs/initial/relevanceLG.csv']
    dictrelev = {}
    for file in relevant:
        file = open(file, 'r')
        csv_reader1 = csv.reader(file)
        for row in csv_reader1:
            dictrelev[','.join(row)] = 0
    print(len(dictrelev))
    dictcandidate={}
    filelist1 = ['../crawling/initial/Body-based guided search/crawler/bodysearchURLs.json',
                 '../crawling/initial/URL-based guided search/crawler/fatherURLs.json',
                 '../crawling/initial/Title-based guided search/crawler/titlesearchURLs.json',
                 ]
    for file in filelist1:
        f = open(file, encoding='utf-8')  #
        res = f.read()  #
        data = json.loads(res)
        for key in data:
            dictcandidate[key]=0
            if (key in dictrelev):
                dictrelev[key] = 1
    num = 0
    for key in dictrelev:
        if (dictrelev[key] == 1):
            num += 1
    ##In total, there are how many relevant URLs
    print(num)
    ##In total, there are how many candidate URLs
    print(len(dictcandidate))


def initialhowmanyobscureVPs(searchmethod):
    dictLG = {}
    dictVPs = {}
    dictseedLG = {}
    dictseedVP = {}

    ###get URLs and VPs from webseds
    f = open('../Practical_applications/Analysis/coverage/VP2AS/seedLGlistupdaterevise1.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if (key not in dictseedLG):
            dictseedLG[key] = data[key]
        for key1 in data[key]['VP']:
            if (data[key]['VP'][key1][0] not in dictseedVP):
                dictseedVP[data[key]['VP'][key1][0]] = ''
    print(len(dictseedLG))
    print(len(dictseedVP))


    ##get URLs and VPs from initial round of iteration
    f = open('../Practical_applications/Analysis/coverage/VP2AS/RelevantLGlistupdaterevise1.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if (key not in dictLG):
            dictLG[key] = data[key]
        for key1 in data[key]['VP']:
            if (data[key]['VP'][key1][0] not in dictVPs):
                dictVPs[data[key]['VP'][key1][0]] = ''
    print(len(dictLG))
    print(len(dictVPs))
    dictnewVP = {}
    f = open(searchmethod, encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    for key in data:
        if (key in dictLG):
            for key1 in dictLG[key]['VP']:
                if (dictLG[key]['VP'][key1][0] not in dictseedVP):
                    dictnewVP[dictLG[key]['VP'][key1][0]] = ''

    # the number of obscure VPs
    print(len(dictnewVP))


def iterationrelevant():
    relevant = [
    '../classification/relevant-URLs/second_iteration/relevanceLG.csv',
    '../classification/relevant-URLs/third_iteration/relevanceLG.csv',
    '../classification/relevant-URLs/forth_iteration/relevanceLG.csv']
    dictrelev = {}
    for file in relevant:
        file = open(file, 'r')
        csv_reader1 = csv.reader(file)
        for row in csv_reader1:
            dictrelev[','.join(row)] = 0
    print(len(dictrelev))

    dictcandidate={}
    filelist1 = ['../crawling/second_iteration/Hyperlink guided search/LGinlinkurlfirst.json',
                 '../crawling/second_iteration/Similarity guided search/fatherURLs.json',
                 '../crawling/third_iteration/Hyperlink guided search/LGinlinkurlfirst.json',
                 '../crawling/third_iteration/Similarity guided search/fatherURLs.json',
                 '../crawling/fourth_iteration/Hyperlink guided search/LGinlinkurlfirst.json',
                 '../crawling/fourth_iteration/Similarity guided search/fatherURLs.json'
                 ]


    for file in filelist1:
        f = open(file, encoding='utf-8')  #
        res = f.read()  #
        data = json.loads(res)
        for key in data:
            dictcandidate[key]=0
            if (key in dictrelev):
                dictrelev[key] = 1
    num = 0
    for key in dictrelev:
        if (dictrelev[key] == 1):
            num += 1
    ##In total, there are how many relevant URLs
    print(num)

def iterationobscureVPs():
    dictLG = {}
    dictVPs = {}
    dictseedLG = {}
    dictseedVP = {}

    seedlist=[ '../Practical_applications/Analysis/coverage/VP2AS/seedLGlistupdaterevise1.json',
               '../Practical_applications/Analysis/coverage/VP2AS/RelevantLGlistupdaterevise1.json' ]
    ###get URLs and VPs from webseds and initial round
    for sed in seedlist:
        f = open(sed,  encoding='utf-8')  #
        res = f.read()  #
        data = json.loads(res)
        for key in data:
            if (key not in dictseedLG):
                dictseedLG[key] = data[key]
            for key1 in data[key]['VP']:
                if (data[key]['VP'][key1][0] not in dictseedVP):
                    dictseedVP[data[key]['VP'][key1][0]] = ''
    print(len(dictseedLG))
    print(len(dictseedVP))

    list1=['../Practical_applications/Analysis/coverage/VP2AS/Relevant2LGlistupdaterevise1.json',
            '../Practical_applications/Analysis/coverage/VP2AS/Relevant3LGlistupdaterevise1.json',
            '../Practical_applications/Analysis/coverage/VP2AS/Relevant4LGlistupdaterevise1.json']
    ##get URLs and VPs from initial round of iteration
    for fi in list1:
        f = open(fi, encoding='utf-8')  #
        res = f.read()  #
        data = json.loads(res)
        for key in data:
            if (key not in dictLG):
                dictLG[key] = data[key]
            for key1 in data[key]['VP']:
                if (data[key]['VP'][key1][0] not in dictVPs):
                    dictVPs[data[key]['VP'][key1][0]] = ''

    print(len(dictLG))
    print(len(dictVPs))
    filelist1 = [
        '../crawling/second_iteration/Hyperlink guided search/LGinlinkurlfirstnew.json',
        '../crawling/second_iteration/Similarity guided search/fatherURLsnew.json',
        '../crawling/third_iteration/Hyperlink guided search/LGinlinkurlfirstnew.json',
        '../crawling/third_iteration/Similarity guided search/fatherURLsnew.json',
        '../crawling/fourth_iteration/Hyperlink guided search/LGinlinkurlfirstnew.json',
        '../crawling/fourth_iteration/Similarity guided search/fatherURLsnew.json'
        ]

    dictnewVP = {}
    for searchmethod in filelist1:
        f = open(searchmethod, encoding='utf-8')  #
        res = f.read()  #
        data = json.loads(res)
        for key in data:
            if (key in dictLG):
                for key1 in dictLG[key]['VP']:
                    if (dictLG[key]['VP'][key1][0] not in dictseedVP):
                        dictnewVP[dictLG[key]['VP'][key1][0]] = ''

    # the number of obscure VPs
    print(len(dictnewVP))

if __name__ == '__main__':
    #for the first round of iteration，we calaulate the number of candidate URLs and relevant URLS from each search method
    # body-bsed guided search 19793, 1114
    # initialhowmanyrelevant('../classification/relevant-URLs/initial/relevanceLG.csv','../crawling/initial/Body-based guided search/crawler/bodysearchURLs.json')
    # URL-bsed guided search 433865,1901
    # initialhowmanyrelevant('../classification/relevant-URLs/initial/relevanceLG.csv','../crawling/initial/URL-based guided search/crawler/fatherURLs.json')
    #title-bsed guided 461799, 2511
    # initialhowmanyrelevant('../classification/relevant-URLs/initial/relevanceLG.csv','../crawling/initial/Title-based guided search/crawler/titlesearchURLs.json')
    #all 877021，4111
    # initalhowmanyrelevantall()
    #hyperlink-guided
    # initialhowmanyrelevant('../classification/relevant-URLs/initial/relevanceLG.csv','../crawling/initial/Hyperlink-guided search/crawler/LGinlinkurlfirst.json')


    # for the first round of iteration，we calaulate the number of obscure VPs from each search method
    # body-bsed guided search  470 obscure VPs
    # initialhowmanyobscureVPs('../crawling/initial/Body-based guided search/crawler/bodysearchURLs.json')
    ##uRL-bsed guided search 324
    # initialhowmanyobscureVPs('../crawling/initial/URL-based guided search/crawler/fatherURLs.json')
    # title-bsed guided 423
    # initialhowmanyobscureVPs('../crawling/initial/Title-based guided search/crawler/titlesearchURLs.json')
    #hyperlink-guided 48
    # initialhowmanyobscureVPs('../crawling/initial/Hyperlink-guided search/crawler/LGinlinkurlfirst.json')

    #for the later three iterations，we calaulate the number of relevant URLS from each search method
    # iterationrelevant()
    #280
    iterationobscureVPs()

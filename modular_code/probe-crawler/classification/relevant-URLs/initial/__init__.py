import csv
import json
def getrelevance():
    contenturl = {}
    file = open('../../getURLs/initial/getcontenturl.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        contenturl[','.join(row)] = 0
    print(len(contenturl))

    file1 = open('relevanceLG.csv', 'w')
    file = open('../../content-classifier/PUbagging_model/relevanceprediction.csv', 'r')
    csv_reader1 = csv.reader(file)
    for row in csv_reader1:
        url = ','.join(row).split('\t')[0]

        if(url in contenturl and ','.join(row).split('\t')[2] =='1'):
            file1.writelines(url+'\n')



def getcontent():

    keylist = {}
    file1 = open('../../../webseds/All-LGseedpages/afterManualCheck/isLG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        keylist[','.join(row)] = ''
    file1 = open( 'relevanceLG.csv', 'r')
    csv_reader1 = csv.reader(file1)
    for row in csv_reader1:
        keylist[','.join(row)] = ''

    fileopen=open('LGallcontent.csv','w')
    file1 = open('../../getURLs/initial/urlcontent.csv', 'r')
    csv_reader1 = csv.reader(file1)
    csv.field_size_limit(500 * 1024 * 1024)
    for row in csv_reader1:
        url = ','.join(row).split(',|ProbeGeo|')[0]
        if(url in keylist):
            fileopen.writelines(','.join(row)+'\n')

if __name__ == '__main__':
    getrelevance()
    getcontent()
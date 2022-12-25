import csv
import re
import json

def results():

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
if __name__ == '__main__':
    results()
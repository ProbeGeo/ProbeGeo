
from sklearn.datasets import fetch_20newsgroups

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#文本预处理, 可选项
import nltk
import string
import json
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
def textPrecessing(text):
    text = text.lower()
    for c in string.punctuation:
        text = text.replace(c, ' ')
    wordLst = nltk.word_tokenize(text)
    stoplist = stopwords.words('english')
    stoplist.append('us')
    stoplist.append('td')
    print(stoplist)
    #remove stopwords
    filtered = [w for w in wordLst if w not in stoplist]
    refiltered =nltk.pos_tag(filtered)
    filtered = [w for w, pos in refiltered if pos.startswith('NN')]
    ps = PorterStemmer()
    filtered = [ps.stem(w) for w in filtered]

    return " ".join(filtered)

#The above area is only run for the first time, for text preprocessing, and commented out from the second run

def textprocess(text):
    # text = text.lower()
    wordLst = nltk.word_tokenize(text)
    stoplist=stopwords.words('english').copy()
    stoplist.append('us')
    stoplist.append('td')
    stoplist.append('TD')
    stoplist.append('Td')
    stoplist.append('tD')
    stoplist.append('tr')
    stoplist.append('TR')
    stoplist.append('US')


    print(wordLst)
    # remove stopwords
    filtered = [w for w in wordLst if w not in stoplist]

    # refiltered = nltk.pos_tag(filtered)
    # filtered = [w for w, pos in refiltered if pos.startswith('NN')]
    return " ".join(filtered)

def tfidfcount():

    docLst = []
    with open('20newsgroups.csv', 'r') as f:
       for line in f.readlines():
           if line != '':
               docLst.append(str(line.strip()))
    index=len(docLst)
    url=[]
    listcont=[]
    f = open('LGselectcontent.json', encoding='utf-8')  #
    res = f.read()  #
    data = json.loads(res)
    text=''
    for key in data:
        url.append(key)
        listcont.append(data[key])
        text+=data[key]

    file=open('itemfrequent.csv','w')
    docLst.append(textprocess(text))
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    X = vectorizer.fit_transform(docLst)
    tfidf = transformer.fit_transform(X)
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    for i in range(len(weight)):
        if(i>=index):
            print("-------output words with weight >0.05. ------")
            # for j in range(len(word)):
            for key in list(zip(word, weight[i])):
                if(key[1]>0.05):
                    print(key)
                    file.writelines(key[0]+','+str(key[1])+'\n')


if __name__ == '__main__':
    # docLst = []
    # dataset = fetch_20newsgroups(shuffle=True, random_state=1,
    #                              remove=('headers', 'footers', 'quotes'))
    # data_samples = dataset.data[:18846] #截取需要的量，n_samples=18846
    # for desc in data_samples :
    #     docLst.append(textPrecessing(desc).encode('utf-8'))
    # with open('20newsgroups.csv', 'w') as f:
    #     for line in docLst:
    #         f.write(str(line)+'\n')
    tfidfcount()
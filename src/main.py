import sklearn
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import glob

mappedWords={}
poemIDs = []

def loadPoems():
    poems = []
    for i, path in enumerate(glob.glob("./res/poems/*")):
        file = open(path, "r", encoding="utf-8")
        print(path)
        poem = file.read()
        poems.append(poem)
        poemIDs.append(i)
        words =  re.findall(r"[\w']+", poem)
        for w in words:
            if w:
                mappedWords[w.lower()] = i
    return poems


def initVectorisers():
    vectorizers = []
    for i, p in enumerate(poems):
        c = CountVectorizer()
        x = c.fit_transform([p])
        vectorizers.append(c)
    return vectorizers

def getWantedWord():
    tab = op('../wantedWords')
    words = []

    for i in range(tab.numRows):
        s = str(tab[i, 0])
        words.append(s)

    return words

def getPoemId():
    poems = loadPoems()
    vec = CountVectorizer()
    X = vec.fit_transform(poems)
    wantedWords = getWantedWord()
    wantedWordsConcat = []
    wantedWordsConcat.append(' '.join(wantedWords))


    tf_transformer = TfidfTransformer(use_idf=False).fit(X)

    clf = MultinomialNB().fit(X, poemIDs)

    X_new_counts = vec.transform(wantedWordsConcat)
    X_new_tfidf = tf_transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)

    return predicted[0]

def getPoemTxt(id):
    path = glob.glob("./res/poems/musset_"+str(id)+".txt")[0]
    file = open(path, "r", encoding="utf-8")
    poem = file.read()
    return poem


poemId = getPoemId()
poemTxt = getPoemTxt(poemId)


extract = " \n".join(poemTxt.split('\n')[2:7])

op('out').par.text =poemId
op('../selectedPoem').text = extract






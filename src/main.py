import sklearn
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import glob
import numpy as np
import synonymsDico

POEM_CHOICE_PROBA_THRESHOLD = 1.5
MIN_DIFF_SYNONYMS_PASS = 1.1
mappedWords={}
poemIDs = []

def loadPoems():
    poems = []
    for i, path in enumerate(glob.glob("../res/poems/*")):
        file = open(path, "r", encoding="utf-8")
        poem = file.read()
        poems.append(poem)
        poemIDs.append(i)
        words =  re.findall(r"[\w']+", poem)
        for w in words:
            if w:
                mappedWords[w.lower()] = i

        file.close()
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

def isGoodPrediction(moy, maxi):
    print("len "+str(len(moy)))
    if len(moy) < 2:
        val = maxi[0] / moy[0]
        print(val)
        return val > POEM_CHOICE_PROBA_THRESHOLD

    oldVal = maxi[len(maxi)-2] / moy[len(moy)-2] 
    newVal = maxi[len(maxi)-1] / moy[len(moy)-1] 
    # si l'ajout des synonyme n'a plus d'impact on arret
    if newVal / oldVal < MIN_DIFF_SYNONYMS_PASS:
        return True;
    return newVal > POEM_CHOICE_PROBA_THRESHOLD
    
def addSynonyms(vocab):
    # A chaque passe on ajoute un synonyme de chaque mot du vocab 
    # On verifie avant que le synonyme ne soit pas present dans le vocab
    for w in vocab:
        synos = synonymsDico.getSynonyms(w)
        for s in synos: 
            if s not in vocab:
                vocab.append(s)
                return;

def getPoemId():
    poems = loadPoems()
    vec = CountVectorizer()
    X = vec.fit_transform(poems)
    # wantedWords = getWantedWord()
    wantedWords = ["amour", "gloire", "beauté"]
    wantedWordsConcat = []
    wantedWordsConcat.append(' '.join(wantedWords))


    tf_transformer = TfidfTransformer(use_idf=False).fit(X)

    clf = MultinomialNB().fit(X, poemIDs)

    X_new_counts = vec.transform(wantedWordsConcat)
    X_new_tfidf = tf_transformer.transform(X_new_counts)

    predicted = clf.predict_proba(X_new_tfidf)[0]

    moy = []
    maxi = []
    moy.append(np.mean(predicted))
    maxi.append(np.max(predicted))

    print(wantedWords)


    while not isGoodPrediction(moy, maxi):
        addSynonyms(wantedWords)

        print(wantedWords)

        wantedWordsConcat[0] = ' '.join(wantedWords)

        X_new_counts = vec.transform(wantedWordsConcat)
        X_new_tfidf = tf_transformer.transform(X_new_counts)

        predicted = clf.predict_proba(X_new_tfidf)[0]

        moy.append(np.mean(predicted))
        maxi.append(np.max(predicted))


    maxId = np.argmax(predicted)

    return maxId

def getPoemTxt(id):
    path = glob.glob("./res/poems/musset_"+str(id)+".txt")[0]
    file = open(path, "r", encoding="utf-8")
    poem = file.read()
    file.close()
    return poem


poemId = getPoemId()
# poemTxt = getPoemTxt(poemId)

print("selectedPoem : "+str(poemId))

# extract = " \n".join(poemTxt.split('\n')[2:7])

# op('out').par.text =poemId
# op('../selectedPoem').text = extract






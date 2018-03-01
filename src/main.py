import sklearn
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import glob

mappedWords={}
poemIDs = []

def loadPoems():
    poems = []
    for i, path in enumerate(glob.glob("../res/poems/*")):
        file = open(path, "r")
        poem = file.read()
        poems.append(poem)
        poemIDs.append(i)
        words =  re.findall(r"[\w']+", poem)
        for w in words:
            if w:
                mappedWords[w.lower()] = i
    return poems

poems = loadPoems()

def initVectorisers():
    vectorizers = []
    for i, p in enumerate(poems):
        c = CountVectorizer()
        x = c.fit_transform([p])
        vectorizers.append(c)
    return vectorizers

#vectorizers = initVectorisers();

#il faut que notre X_train soit tous nos mots (avec doublons) et la target doit etre un tableau avec les indices des poemes de chaque mots 
mot = u'elle'

vec = CountVectorizer()#strip_accents='unicode'
X = vec.fit_transform(poems)#mappedWords.keys()
#wantedWords = ["large", "infini", "interminable", "allongé", "long", "carré", "rangé", "boite", "cadre", "quadrilatère"];
wantedWords = ["large", "joie", "amour", "allongé", "sexe", "carré", "rangé", "boite", "cadre", "quadrilatère"];
wantedWordsConcat = []
wantedWordsConcat.append(' '.join(wantedWords))

print(wantedWordsConcat)

tf_transformer = TfidfTransformer(use_idf=False).fit(X)
# X_train_tfidf = tf_transformer.fit_transform(X)
# print(X_train_tfidf.shape)

#df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
print( len(mappedWords.values()))
clf = MultinomialNB().fit(X, poemIDs)

X_new_counts = vec.transform(wantedWordsConcat)
X_new_tfidf = tf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for word, poemId in zip(wantedWordsConcat, predicted):
    print('%r => %s' % (word, poemId))


#print(df)

def getWordFreq(w):
    founds = []
    for i, v in enumerate(vectorizers):
        #en fait ça donne l'indice de la premiere occurance du mot mais ça compte pas le nb d'occurance
        occ = v.vocabulary_.get(w)
        if i == 90:
            print(str(i)+ ": "+ str(occ)) 

        if occ:
            founds.append((i, occ))
    founds.sort(key=lambda x: x[1])

#print(getWordFreq(mot))






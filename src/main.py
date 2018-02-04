import sklearn
from sklearn.feature_extraction.text import CountVectorizer
import glob

def loadPoems():
    poems = []
    for path in glob.glob("../res/poems/*"):
        file = open(path, "r")
        poems.append(file.read())
    return poems

poems = loadPoems()

vectorizers = []

for p in poems:
    c = CountVectorizer()
    c.fit_transform([p])
    vectorizers.append(c)

mot = "abandonna"

def getWordFreq(w):
    founds = []
    for i, v in enumerate(vectorizers):
        occ = v.vocabulary_.get(w)
        if occ:
            founds.append((i, occ))
    founds.sort(key=lambda x: x[1])

print(getWordFreq(mot))






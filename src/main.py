import sklearn
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import glob
import numpy as np
import synonymsDico

POEM_CHOICE_PROBA_THRESHOLD = 1.5
MIN_DIFF_SYNONYMS_PASS = 1.1
NB_WORDS_MIN_EXTRACT = 20
NB_WORDS_MAX_EXTRACT = 40
mappedWords={}
poemIDs = []
wantedWords = ["bonsoir", "marge", "amer"]
# wantedWords = getWantedWord()


def loadPoems():
    # global poemIDs
    global mappedWords
    poems = []
    paths = []
    for i, path in enumerate(glob.glob("../res/poems/*")):
        paths.append(path)
        file = open(path, "r", encoding="utf-8")
        poem = file.read()
        poems.append(poem)
        poemIDs.append(i)
        words =  re.findall(r"[\w']+", poem)
        for w in words:
            if w:
                mappedWords[w.lower()] = i

        file.close()
    return poems, paths


# def initVectorisers():
#     vectorizers = []
#     for i, p in enumerate(poems):
#         c = CountVectorizer()
#         x = c.fit_transform([p])
#         vectorizers.append(c)
#     return vectorizers

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


def getBestTextId(texts, wantedWords):
    vec = TfidfVectorizer()
    
    X = vec.fit_transform(texts)
    vocabIds = []
    for w in wantedWords:
        id = vec.vocabulary_.get(w)
        if id:
            vocabIds.append(id)
    # print(vec.get_feature_names())
    textsMatrix = X.toarray()
    wantedWordsMatrix = textsMatrix[:,vocabIds]
    wantedWordsMatrixSum = np.sum(wantedWordsMatrix, axis=1)

    id = np.argmax(wantedWordsMatrixSum)
    return id


def getPoemName():
    global poemIDs

    poems, paths = loadPoems()
    
    id = getBestTextId(poems, wantedWords)

    poem = paths[id].replace("../res/poems\\", '')

    return poem

def getPoemTxt(id):
    path = glob.glob("../res/poems/musset_"+str(id)+".txt")[0]
    file = open(path, "r", encoding="utf-8")
    poem = file.read()
    file.close()
    return poem


# def checkSentencesValidity(sentences):
#     for s in sentences:
#         if len(s) < 20:
#             return False
#     return True


def getSentences(text):
    sentencesPoints = text.split('.')
    sentencesInterroPoint = []
    for v in sentencesPoints:
        tmp = v.split('?')
        for t in tmp:
            sentencesInterroPoint.append(t)

    sentencesInterroPointSemicolon = []
    for v in sentencesPoints:
        tmp = v.split(';\n')
        for t in tmp:
            sentencesInterroPointSemicolon.append(t)

    sentences = []
    for s in sentencesInterroPointSemicolon:
        # on considère les phrases exclamatives si elles font la longueur d'un vers
        sentencesExclam = s.split('!\n')
        for t in sentencesExclam:
            sentences.append(t)

    return sentences

# def concatSentences(sentences):
#     nbSentences = len(sentences)
#     for i in range(nbSentences-1):
#         print(nbSentences)
#         print(i)
#         nbWords =  len(re.findall(r"[\w']+", sentences[i]))
#         if nbWords < NB_WORDS_MIN_EXTRACT:
#             sentences[i] += sentences[i+1]
#             del sentences[i+1]
#             nbSentences-=1
#             i-=1

def makeExtract(sentences):
    extract = sentences[0]
    for i in range(1, len(sentences)):
        nbWords =  len(re.findall(r"[\w']+", extract))
        nbWordsSentence = len(re.findall(r"[\w']+", sentences[i]))

        if nbWordsSentence > NB_WORDS_MAX_EXTRACT or nbWords > NB_WORDS_MIN_EXTRACT:
            break

        extract+= " "+sentences[i]
       
    return extract        

def makeExtracts(sentences):
    extracts = []
    for i in range(len(sentences)):
        extracts.append(makeExtract(sentences[i:]))

    return extracts


def getExtract(poemName, ):
    path = "../res/poems/"+poemName
    with open(path, "r", encoding="utf-8") as file:
        rawContent = file.read()
        sentences = getSentences(rawContent)
        extracts = makeExtracts (sentences)

        id = getBestTextId(extracts, wantedWords)
        print(extracts)
        print(extracts[id])


    return extracts[id]



poemName = getPoemName()
# poemTxt = getPoemTxt(poemId)

print("selectedPoem : "+str(poemName))
getExtract(poemName)
# print("extrait : "+)

# extract = " \n".join(poemTxt.split('\n')[2:7])

# op('out').par.text =poemName
# op('../selectedPoem').text = extract






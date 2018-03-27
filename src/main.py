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

# RES_PATH = "./python/res"
RES_PATH = "../res"
POEM_CHOICE_PROBA_THRESHOLD = 1.5
MIN_DIFF_SYNONYMS_PASS = 1.1
NB_WORDS_MIN_EXTRACT = 20
NB_WORDS_MAX_EXTRACT = 40
# mappedWords={}
poemIDs = []
wantedWords = ["bonsoir", "marge"]

# wantedWords = []
# poemFiles = []


def loadWantedWord():
    tab = op('../wantedWords')

    for i in range(tab.numRows):
        s = str(tab[i, 0])
        wantedWords.append(s)


# def loadPoemFiles():
#     tab =  op('poems_files')

#     for i in range(1, tab.numRows):
#         s = str(tab[i, 1])
#         poemFiles.append(s)


def loadPoems():
    # global poemIDs
    # global mappedWords
    poems = []
    paths = []
    for i, path in enumerate(glob.glob(RES_PATH + '/poems/*')):
        paths.append(path)
        file = open(path, "r", encoding="utf-8")
        poem = file.read()
        poems.append(poem)
        poemIDs.append(i)
        # words =  re.findall(r"[\w']+", poem)
        # for w in words:
        #     if w:
        #         mappedWords[w.lower()] = i

        file.close()
    return poems, paths


# def initVectorisers():
#     vectorizers = []
#     for i, p in enumerate(poems):
#         c = CountVectorizer()
#         x = c.fit_transform([p])
#         vectorizers.append(c)
#     return vectorizers


def isGoodPrediction(moy, maxi):
    print("len " + str(len(moy)))
    if len(moy) < 2:
        val = maxi[0] / moy[0]
        print(val)
        return val > POEM_CHOICE_PROBA_THRESHOLD

    oldVal = maxi[len(maxi) - 2] / moy[len(moy) - 2]
    newVal = maxi[len(maxi) - 1] / moy[len(moy) - 1]
    # si l'ajout des synonyme n'a plus d'impact on arret
    if newVal / oldVal < MIN_DIFF_SYNONYMS_PASS:
        return True
    return newVal > POEM_CHOICE_PROBA_THRESHOLD


def addSynonyms(vocabBase, vocabExtended):
    # A chaque passe on ajoute un synonyme de chaque mot du vocab
    # On verifie avant que le synonyme ne soit pas present dans le vocab
    addedSomething = False
    for w in vocabBase:
        synos = synonymsDico.getSynonyms(w)
        for s in synos:
            if s not in vocabExtended:
                vocabExtended.append(s)
                addedSomething = True
                print("added: " + s)
                break
    return addedSomething


def getBestTextId(texts, wantedWords):
    # vec = TfidfVectorizer()
    vec = CountVectorizer()
    # textsTmp = list(texts)
    X = vec.fit_transform(texts)
    # textsTmp.insert(0, wantedWords)
    # tf_transformer = TfidfTransformer(use_idf=False).fit(X)

    # merde =linear_kernel(X[0:1], X).flatten()

    vocabIds = []
    for w in wantedWords:
        id = vec.vocabulary_.get(w)
        if id is not None:
            print(w)
            vocabIds.append(id)
    if vocabIds == []:
        # aucun mot dans tous les poèmes
        return 0, False

    textsMatrix = X.toarray()
    wantedWordsMatrix = textsMatrix[:, vocabIds]
    wantedWordsMatrixSign = np.sign(wantedWordsMatrix)
    wantedWordsMatrixSum = np.sum(wantedWordsMatrix, axis=1)
    wantedWordsMatrixSignSum = np.sum(wantedWordsMatrixSign, axis=1)

    rank = np.argsort(np.argsort(wantedWordsMatrixSum))
    rankSum = np.argsort(np.argsort(wantedWordsMatrixSignSum))

    id = np.argmax(rankSum + rank)
    print(id)
    return id, True


def getBestTextIdWrapperSyno(texts, vocab):
    global wantedWords
    # if "adieu" in vocab:
    #     print(texts)
    id, existence = getBestTextId(texts, vocab)
    vocabExtended = [str(w) for w in vocab]
    while not existence:
        if not addSynonyms(vocab, vocabExtended):  # plus aucun de synonyme
            print("PLUS AUCUN SYNONYMES")
            break
        id, existence = getBestTextId(texts, vocabExtended)
    wantedWords = vocabExtended
    return id


def getPoemName():
    global poemIDs

    poems, paths = loadPoems()

    id = getBestTextIdWrapperSyno(poems, wantedWords)

    # poem = paths[id].replace(RES_PATH + "/poems\\", '')
    poem = paths[id].replace(RES_PATH + "/poems/", '')

    return poem


def getPoemTxt(id):
    path = glob.glob(RES_PATH + "/poems/musset_" + str(id) + ".txt")[0]
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


def makeExtract(sentences):
    extract = sentences[0]
    for i in range(1, len(sentences)):
        nbWords = len(re.findall(r"[\w']+", extract))
        nbWordsSentence = len(re.findall(r"[\w']+", sentences[i]))

        if nbWordsSentence > NB_WORDS_MAX_EXTRACT or nbWords > NB_WORDS_MIN_EXTRACT:
            break

        extract += " " + sentences[i]

    return extract


def makeExtracts(sentences):
    extracts = []
    for i in range(len(sentences)):
        extracts.append(makeExtract(sentences[i:]))

    return extracts


def getExtract(poemName):
    path = RES_PATH + "/poems/" + poemName
    with open(path, "r", encoding="utf-8") as file:
        rawContent = file.read()
        sentences = getSentences(rawContent)
        extracts = makeExtracts(sentences)

        id, existence = getBestTextId(extracts, wantedWords)
        print(id)
        print(extracts[id])

    return extracts[id]

# loadWantedWord()
# loadPoemFiles()
poemName = getPoemName()

print("selectedPoem : " + str(poemName))
extract = getExtract(poemName)

# op('out').par.text =poemName
# op('../selectedPoem').text = extract

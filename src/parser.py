class Word:
    def __init__(self, word, nature, synonyms):
        self.word = word
        self.nature = nature
        self.synonyms = synonyms

        # if nature(words) != list:
        #     words = [words]

        # for w in words:
        #     self.synonyms.append(w)

    def linkSynonyms(self, dico):

        for s in self.synonyms:
            # si le synonyme n'est pas dans le dico
            # on cree un Word sans synonyme et sans
            # nature dans le dico pour le link
            if not (s in dico):
                w = Word(s, "?", findSynonyms(s, dico))
                print(w.__str__())
                dico[s] = w
            s = dico[s]


    def __str__(self):
        sys = ', '.join(self.synonyms)
        return str(self.word) + " (" + str(self.nature) + ") : " + sys


def findSynonyms(word, dico):
    syno = []
    for (key, val) in dico.items():
        if word in val.synonyms:
            syno.append(key)
    return syno


# def parseDicoSyno(path):
#     with open(path, 'r', encoding='utf8') as file:
#         raw = file.readlines()

#         dico = {}
#         word = ""
#         # ajout de tous les mots du dico
#         for i in range(1, len(raw)):
#             if len(raw[i]) < 1:
#                 return

#             line = str(raw[i].replace('\n', ''))
#             if line[-2] == '1':
#                 word = line.split("|")[0]
#             else:
#                 line = line.split("|")
#                 nature = str(line[0])
#                 nature = nature[1:-1]
#                 nature.lower()
#                 synonyms = line[1:]

#                 w = Word(word, nature, synonyms)
#                 dico[word] = w

#         # ajout de tous les synomymes de chaque mot
#         for words in dico.values():
#             words.toString()
#             words.findSynonyms(dico)

#         return dico

def parseDicoSyno(path):
    with open(path, 'r', encoding='utf8') as file:
        lines = file.readlines()
        dico = {}
        current_word = ""

        # premiere passe pour les mots
        for line in lines:
            tokens = line.split('|')
            # on passe a la ligne suivante si y a rien
            if len(tokens) < 2:
                continue
            # si c'est une key on ecrase l'ancienne
            if tokens[1].replace('\n', "") == "1":
                current_word = tokens[0]
            # si c'est une ligne de synonymes
            # on ajoute un Word dans le dico
            elif line[0] == '(':
                nature = tokens[0].replace('(', '').replace(')', '').lower()
                synonyms = [s.replace('\n', "") for s in tokens[1:]]
                dico[current_word] = Word(current_word, nature, synonyms)

        # deuxieme pour le link des synonymes
        for i in list(dico):
           dico[i].linkSynonyms(dico)
        return dico

dico = parseDicoSyno('../res/dico/synonymes.dat')

i = 0   
for (key, val) in dico.items():
    i += 1
    if i > 10:
        exit()
    # print(str(key) + " =>  " + val.__str__())

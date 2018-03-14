class Word :
	def __init__(self, word, nature, synonyms) : 
		self.word = word
		self.nature = nature
		self.synonyms = synonyms

	def addSynonyms(self, words):
		if nature(words) != list:
			words = [words]
		
		for w in words:
			self.synonyms.append(w)

	def findSynonyms(self, dico):
		for s in self.synonyms:
			s = dico[s]

	def toString(self):
		return self.word+" ("+self.nature+") : "



def parseDicoSyno(path):
	file = open(path)
	raw = file.readlines()
	#raw.r

	dico = {}

	#ajout de tous les mots du dico
	for i in range(1, len(raw), 2):
		if len(raw[i]) < 1:
			return

		#a un moment le sens s'inverse et les mots deviennent les natures
		line = str(raw[i].encode('UTF-8'))
		word = line.split("|")[0]
		line = str(raw[i+1].encode('UTF-8'))
		line = line.split('|')
		nature = str(line[0])
		nature = nature[3:-1]
		nature.lower()
		print(nature)
		synonyms = line[1:]

		# w = Word(word, nature, synonyms)
		# dico[word] = w
		

	#ajout de tous les synomymes de chaque mot
	for words in dico.values():
		words.toString()
		words.findSynonyms(dico)

	return dico


dico = parseDicoSyno('./synonymes.dat')
i =0
for (key, val) in dico.items():
	i+=1
	if i > 10 : exit
	print(key +" =>  "+val.toString())
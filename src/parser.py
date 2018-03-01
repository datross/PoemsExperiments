import io

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
	with io.open(path,'r',encoding='utf8') as file:
		raw = file.readlines()
	#raw.r

		dico = {}
		word = ""
		#ajout de tous les mots du dico
		for i in range(1, len(raw)):
			if len(raw[i]) < 1:
				return

			line = str(raw[i].replace('\n', ''))
			if line[-2] == '1':
				word = line.split("|")[0]
			else :
				line = line.split("|")
				nature = str(line[0])
				nature = nature[1:-1]
				nature.lower()
				synonyms = line[1:]

				w = Word(word, nature, synonyms)
				dico[word] = w
			

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
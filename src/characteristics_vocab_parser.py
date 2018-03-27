import re
import numpy as np


def getCharacteristiqueMapping():
	charas = {}

	path = './python/res/characteristics_mapping.csv'
	# path = '../res/characteristics_mapping.csv'
	

	with open(path, 'r', encoding="utf-8") as f:
		content = f.read()
		lines = content.split('\n')
		for line in lines:
			words = line.split(',')
			words = [w.strip() for w in words if len(w)>0]
			ws = []
			if len(words)>1:
				ids = np.random.randint(1, len(words), int(len(words)*0.25), dtype=int)
				for i in ids:
					ws.append(words[i])
			else:
				ws = words
			charas[words[0]] = ws

	return charas

# cara = getCharacteristiqueMapping()
# for m, c in cara.items():
# 	print("("+m+") => ")
# 	print(c)



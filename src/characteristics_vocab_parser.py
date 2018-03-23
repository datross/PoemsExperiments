import re

def getCharacteristiqueMapping():
	charas = {}

	path = '../res/characteristics_mapping.csv'
	
	with open(path, 'r', encoding="utf-8") as f:
		content = f.read()
		lines = content.split('\n')
		for line in lines:
			words = line.split(',')
			words = [w.strip() for w in words if len(w)>0]
			charas[words[0]] = words[1:]

	return charas

# cara = getCharacteristiqueMapping()
# for m, c in cara.items():
# 	print("("+m+") => ")
# 	print(c)



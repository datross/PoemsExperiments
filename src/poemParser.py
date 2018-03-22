from glob import glob 

def getCurrentPeomId():
    return len([p for p in glob("../res/poems/*")])-1



path = ("../res/livres/huguette-bertrand_dans-le-fondu-des-mots.txt")
with open(path, 'r', encoding='utf8') as f:
	content = f.read()
	lines = content.split('\n')
	blankCpt = 0
	idName=getCurrentPeomId()
	id=0
	newFile = open("../res/poems/huguette-bertrand_dans-le-fondu-des-mots_"+str(idName)+".txt", "w+",  encoding='utf8')
	for j in range(len(lines)):
		if id >= len(lines):
			break
		if not lines[id].strip():
			print("blank")
			blankCpt+=1
			id+=1
			continue
		# nouveau poeme
		if blankCpt >= 2:
			idName+=1
			name = "../res/poems/huguette-bertrand_dans-le-fondu-des-mots_"+str(idName)+".txt"
			print("create "+name)
			newFile = open(name, "w+",  encoding='utf8')
			id+=1
			while not lines[id].strip(): id+=1
			id-=1

		newFile.write(lines[id]+'\n')
		blankCpt = 0
		id+=1
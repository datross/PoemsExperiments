import characteristics_networks as cn
import characteristics_vocab_parser as cvp
import math
from center import Center

CENTER_THRESHOLD = 0.1
STRAIGHT_THRESHOLD = 0.1
DISTANT_THRESHOLD = 0.5
CLOSE_THRESHOLD = 0.2
IMG_PATH = "../res/images/sceneShape.jpg"

# utility functions
def distTwoPoint(p1, p2):
	return math.sqrt(pow(p2.x-p1.x, 2) + pow(p2.y-p1.y, 2))

def dist(positions):
	somDist = 0
	# X = [p.x for p in positions]
	# Y = [p.y for p in positions]

	for i in range(len(positions)):
		nextId = (i+1)%len(positions)
		somDist += distTwoPoint(positions[i], positions[nextId])

	return somDist/len(positions)

def getDistanceChara(distance):
	if distance < CLOSE_THRESHOLD : 
		return 'rapproché'
	elif distance > CLOSE_THRESHOLD and distance < DISTANT_THRESHOLD:
		return 'distance-moyenne'
	else:
		return 'éloigné'

def analyseEasyShape(coords):
	characterists = []
	# s'il y a qu'une seul position
	if len(coords) == 1: 
		characterists.append('point')
		if abs(coords[0].x) < CENTER_THRESHOLD and abs(coords[0].y) < CENTER_THRESHOLD :
			characterists.append('centré')
		else:
			characterists.append('excentré')
	# s'il y a deux positions
	else:
		characterists.append('ligne')
		
		if abs(coords[0].x - coords[1].x)< STRAIGHT_THRESHOLD or abs(coords[0].y - coords[1].y) < STRAIGHT_THRESHOLD :
			characterists.append('droit')
		else:
			characterists.append('oblique')


	return characterists

def analyseComplexeShape(img):
	characterists = []
	characterists.append(cn.getForm(img))
	characterists.append(cn.getOrentation(img))
	return characterists

charaMapping = cvp.getCharacteristiqueMapping();

def getVocabulary(img, coordonnates):
	vocab=[]
	characterists=[]
	coords = [Center(x, y) for x,y,_ in coordonnates]
	groups = [g for _,_,g in coordonnates if g==True]

	if len(coords) < 3:
		characterists = analyseEasyShape(coords)
	else:
		characterists = analyseComplexeShape(coords)

	distance = dist(coords) 
	characterists.append(getDistanceChara(distance))
	print(characterists)
	# si ils y a des groupes 
	if len(groups)>0:
		characterists.append('groupe')
	for c in characterists:
		vocab.append(charaMapping[c])

	return vocab


c1 = (-0, 0, 0)
c2 = (0, -1, 0)
c3 = (0, 1, 0)

cara = getVocabulary("merde.jpg", [c1, c2])

# print(dist(c1, c2, c3))

print(cara)

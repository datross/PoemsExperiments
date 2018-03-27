import math
import numpy as np
from center import Center
from importlib.machinery import SourceFileLoader

cn = SourceFileLoader("characteristics_networks", r"C:\Users\Antoine\Desktop\ProjetPrePro\maquette\python\src/characteristics_networks.py").load_module()
cvp = SourceFileLoader("characteristics_vocab_parser", r"C:\Users\Antoine\Desktop\ProjetPrePro\maquette\python\src/characteristics_vocab_parser.py").load_module()

CENTER_THRESHOLD = 0.1
STRAIGHT_THRESHOLD = 0.1
DISTANT_THRESHOLD = 0.5
CLOSE_THRESHOLD = 0.2
CORNER_THRESHOLD = 0.4

IMG_PATH = "./python/res/images/sceneShape.jpg"
POSITIONS =[]

CHARA_MAPPING = cvp.getCharacteristiqueMapping()
table = op('wantedWords')


# utility functions
def distTwoPoint(p1, p2):
    return math.sqrt(pow(p2.x - p1.x, 2) + pow(p2.y - p1.y, 2))

# def selectCharaMapping():
#     global CHARA_MAPPING
#     ids = np.random.randint(0, len(CHARA_MAPPING), int(len(CHARA_MAPPING)*0.25), dtype=int)
#     charas = []
#     for i in ids:
#         charas.append(CHARA_MAPPING[i])
#     CHARA_MAPPING= charas

def dist(positions):
    somDist = 0
    # X = [p.x for p in positions]
    # Y = [p.y for p in positions]

    for i in range(len(positions)):
        nextId = (i + 1) % len(positions)
        somDist += distTwoPoint(positions[i], positions[nextId])

    return somDist / len(positions)



def loadPositions():
    global POSITIONS
    tab = op('/project1/positions')
    for i in range(tab.numRows):
        POSITIONS.append((tab[i, 0], tab[i, 1], tab[i, 2]))

def getSpaceChara(coords):
    points = [(c.x, c.y) for c in coords]
    center = np.mean(points, axis=0)
    center = Center(center[0], center[1])

    chara = []

    if abs(center.x) < CENTER_THRESHOLD and abs(center.y) < CENTER_THRESHOLD:
        chara.append('centre')
        return chara

    if center.x > CENTER_THRESHOLD:
        chara.append('est')
    elif center.x < CENTER_THRESHOLD:
        chara.append('ouest')

    if center.y > CENTER_THRESHOLD:
        chara.append('nord')
    elif center.y < CENTER_THRESHOLD:
        chara.append('sud')

    if abs(center.x) > CORNER_THRESHOLD and abs(center.y) > CORNER_THRESHOLD:
    	chara.append('coin')
    elif abs(center.x) > CORNER_THRESHOLD or abs(center.y) > CORNER_THRESHOLD:
    	chara.append('mur')

    return chara


def getDistanceChara(coords):
	distance = dist(coords) 
	if distance < CLOSE_THRESHOLD : 
		return 'rapproche'
	if distance > CLOSE_THRESHOLD and distance < DISTANT_THRESHOLD:
		return 'distance-moyenne'

	return 'eloigne'

def getOrientationChara(coords):
	cds = list(coords)

	if cds[1].x < cds[0].x:
		tmp = cds[0]
		cds[0] = cds[1]
		cds[1] = tmp

	if abs(cds[0].x - cds[1].x) < STRAIGHT_THRESHOLD :
		return 'vertical'
	if abs(cds[0].y - cds[1].y) < STRAIGHT_THRESHOLD :
		return 'horizontal'
	if cds[0].x < cds[1].x and cds[0].y > cds[1].y :
		return 'oblique-gauche'
	
	return 'oblique-droit'

def analyseEasyShape(coords):
	characterists = []
	# s'il y a qu'une seul position
	if len(coords) <= 1: 
		characterists.append('point')
	# s'il y a deux positions
	else:
		characterists.append('ligne')
		characterists.append(getOrientationChara(coords))

	return characterists

def analyseComplexeShape( coords):
	characterists = []
	characterists.append(cn.getShape(coords))

	orientationLine = cn.getOrientationLine(coords)
	characterists.append(getOrientationChara(orientationLine))

	return characterists

def getVocabulary(coordinnates):
    vocab = []
    characterists = []
    print(coordinnates)
    coords = [Center(x, y) for x, y, _ in coordinnates]
    groups = [g for _, _, g in coordinnates if g == True]

    print(groups)

    if len(coords) < 3:
        characterists = analyseEasyShape(coords)
    else:
        characterists = analyseComplexeShape(coords)

    characterists += getSpaceChara(coords)

    characterists.append(getDistanceChara(coords))

    print(characterists)
    # si ils y a des groupes
    if len(groups) > 0:
        characterists.append('groupe')

    for c in characterists:
        charas = CHARA_MAPPING[c]
        for ch in charas:
            vocab.append(ch)

    return vocab


def testGetOrientation(n):
    for i in range(n):
        coords, image = cn.generateFromShape(cn.SHAPES[np.random.randint(
            0, len(cn.SHAPES))], False)
        coords = [
            Center(coords[0][i], coords[1][i]) for i in range(len(coords[0]))
        ]
        orientationLine = cn.getOrientationLine(coords)
        l = orientationLine
        # print([c.__str__() for c in orientationLine])
        # on draw le lines de la pca
        print(l[1])
        orientation = getOrientationChara(orientationLine)

        p1 = Center(int(cn.WIDTH / 2), int(cn.HEIGHT / 2))
        p2 = Center(int(cn.WIDTH / 2 + 32. * l[1].x), int(cn.HEIGHT / 2 + 32. * l[1].y))
        print(p2)
        line = cn.draw.line(p1.x, p1.y, p2.x, p2.y)
        image[line[0], line[1]] = 2.

        # cn.plt.imshow(image)
        # cn.plt.title("orientation: " + str(orientation))
        # cn.plt.show()

# c1 = (-0.26, -0.24, 0)
# c2 = (0.16, -0.25, 0)
# c3 = (0.26, 0.33, 0)
# c4 = (-0.35, 0.27, 0)
# cara = getVocabulary([c1, c2, c3, c4])
# print(cara)

# selectCharaMapping()
loadPositions()
if len(POSITIONS)>0 :
    cara = getVocabulary(POSITIONS)
    # print(dist(c1, c2, c3))
    print(cara)
    table.setSize(len(cara), 1)
    for i, c in enumerate(cara):
        table[i, 0] = c


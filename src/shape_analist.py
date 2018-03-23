import characteristics_networks as cn
import characteristics_vocab_parser as cvp
import math
import numpy as np
from center import Center

CENTER_THRESHOLD = 0.1
STRAIGHT_THRESHOLD = 0.1
DISTANT_THRESHOLD = 0.5
CLOSE_THRESHOLD = 0.2
IMG_PATH = "../res/images/sceneShape.jpg"

CHARA_MAPPING = cvp.getCharacteristiqueMapping()

# utility functions
def distTwoPoint(p1, p2):
    return math.sqrt(pow(p2.x - p1.x, 2) + pow(p2.y - p1.y, 2))


def dist(positions):
    somDist = 0
    # X = [p.x for p in positions]
    # Y = [p.y for p in positions]

    for i in range(len(positions)):
        nextId = (i + 1) % len(positions)
        somDist += distTwoPoint(positions[i], positions[nextId])

    return somDist / len(positions)


def getSpaceChara(coords):
    points = [(c.x, c.y) for c in coords]
    center = np.mean(points, axis=0)
    center = Center(center[0], center[1])

    chara = []

    if abs(center.x) < CENTER_THRESHOLD and abs(center.y) < CENTER_THRESHOLD:
        chara.append('centré')
        return chara

    if center.x > CENTER_THRESHOLD:
        chara.append('est')
    elif center.x < CENTER_THRESHOLD:
        chara.append('ouest')

    if center.y > CENTER_THRESHOLD:
        chara.append('nord')
    elif center.y < CENTER_THRESHOLD:
        chara.append('sud')

    return chara


def getDistanceChara(coords):
	distance = dist(coords) 
	if distance < CLOSE_THRESHOLD : 
		return 'rapproché'
	if distance > CLOSE_THRESHOLD and distance < DISTANT_THRESHOLD:
		return 'distance-moyenne'

	return 'éloigné'

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
	if len(coords) == 1: 
		characterists.append('point')
	# s'il y a deux positions
	else:
		characterists.append('ligne')
		characterists.append(getOrientationChara(coords))

	return characterists

def analyseComplexeShape(img, coords):
	characterists = []
	characterists.append(cn.getShape(img))

	orientationLine = cn.getOrentationLine(coords)
	characterists.append(getOrientationChara(orientationLine))

	return characterists


charaMapping = cvp.getCharacteristiqueMapping()


def getVocabulary(img, coordonnates):
    vocab = []
    characterists = []
    coords = [Center(x, y) for x, y, _ in coordonnates]
    groups = [g for _, _, g in coordonnates if g == True]

    if len(coords) < 3:
        characterists = analyseEasyShape(coords)
    else:
        characterists = analyseComplexeShape(img, coords)

    characterists += getSpaceChara(coords)

    characterists.append(getDistanceChara(coords))

    print(characterists)
    # si ils y a des groupes
    if len(groups) > 0:
        characterists.append('groupe')

# for c in characterists:
# 	vocab.append(CHARA_MAPPING[c])

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

        cn.plt.imshow(image)
        cn.plt.title("orientation: " + str(orientation))
        cn.plt.show()

c1 = (0, 1, 0)
c2 = (-1, 0, 0)
c3 = (0, 1, 0)

cara = getVocabulary(IMG_PATH, [c1, c2])
# print(dist(c1, c2, c3))
print(cara)


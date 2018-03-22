
from sklearn.neural_network import MLPClassifier
from skimage import draw
import numpy as np
import matplotlib.pyplot as plt


# fonctions utilitaires généralistes


def random(a, b):
    return (b - a) * np.random.random() + a


# fonctions d'analyse d'une forme


def boundingBox(coords):
    """Retourne (xmin, ymin, xmax, ymax)"""
    xmin = coords[0][0]
    xmax = coords[0][0]
    ymin = coords[1][0]
    ymax = coords[1][0]
    for (x, y) in zip(*coords):
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
    return (xmin, ymin, xmax, ymax)


def airePoly(coord):
    sum = 0
    for i in range(len(coord[0])):
        k = (i + 1) % len(coord[0])
        sum += coord[0][i] * coord[1][k] - coord[0][k] * coord[1][i]
    return abs(sum) * 0.5


def aireTriangleGenerique(coord):
    """Pour la postérité"""
    nb = len(coord[0])
    sum = 0
    for i, x in enumerate(coord[0]):
        sub = 0
        if i % 2 == 0:
            ys = reversed(coord[1])
            excluIndex = nb - 1 - i
        else:
            ys = coord[1]
            excluIndex = i

        cpt = 0
        for j, y in enumerate(ys):
            if j != excluIndex:
                if cpt % 2 == 0:
                    sub += x * y
                else:
                    sub -= x * y
                cpt += 1
        sum += sub
    return 0.5 * abs(sum)


# Formes canoniques


def canoniqueCarre():
    return ([-0.5, 0.5, 0.5, -0.5], [-0.5, -0.5, 0.5, 0.5])


def canoniqueTriangle(fractal=0.):
    # aire triangle équilatéral de côté a :
    # aire(a) = a**2 * sqrt(3)/2 = a**2 * 0.8660254037844386
    # aire(a) = 1 => a = 1.07456993182354
    # TODO débile ou très débile ?
    a = 1.07456993182354
    h = 0.9306048591020996
    x_sommet = random(-fractal * 2 * a, fractal * 2 * a)
    y_sommet = random(-fractal * 0.9 * h, fractal * 0.9 * h)
    return ([-a/2, a/2, x_sommet], [-h/3, -h/3, 2*h/3 + y_sommet])


def canoniqueLosange(fractal=0.):
    y_sommet = random(-fractal * 0.7, fractal * 0.7)
    return ([0, 0.5, 0, -0.5],
            [-0.8 + y_sommet, 0, 0.8 - y_sommet, 0])


def canoniqueRectangle(fractal=0.):
    w = 1.5 + random(-fractal * 0.3, 2 * fractal)
    return ([0.5*w, 0.5*w, -0.5*w, -0.5*w], [-0.5, 0.5, 0.5, -0.5])


def canoniqueFleche(fractal=0.):
    # TODO action de fractal
    return ([0, 0.5, 0, -0.5], [-0.2, -0.5, 0.7, -0.5])


# Fonctions de transformation d'une forme

def rotate(coords, angle, pivot=(0, 0)):
    """Effets de bord, ça change coords et le retourne aussi."""
    c = np.cos(angle)
    s = np.sin(angle)
    for i in range(len(coords[0])):
        _x = coords[0][i] - pivot[0]
        _y = coords[1][i] - pivot[1]
        coords[0][i] = _x*c - s*_y + pivot[0]
        coords[1][i] = _x*s + c*_y + pivot[1]
    return coords


def scale(coords, factor, pivot=(0, 0)):
    """Effets de bord, ça change coords et le retourne aussi."""
    for i in range(len(coords[0])):
        _x = coords[0][i] - pivot[0]
        _y = coords[1][i] - pivot[1]
        coords[0][i] = _x*factor + pivot[0]
        coords[1][i] = _y*factor + pivot[1]
    return coords


def displace(coords, displacement):
    """displacement peut être un tuple (x, y) ou alors une liste de tuples.
    Effets de bord, ça change coords et le retourne aussi."""
    if type(displacement) != list:
        displacement = [displacement] * len(coords[0])
    for i in range(len(coords[0])):
        coords[0][i] += displacement[i][0]
        coords[1][i] += displacement[i][1]
    return coords


def scaleInLimits(coords, xmax, ymax, aire_min):
    """Scale la forme en la gardant dans les limites."""
    bb = boundingBox(coords)
    w = bb[2] - bb[0]
    h = bb[3] - bb[1]
    aire = airePoly(coords)
    scale_min = np.sqrt(aire_min / aire)
    scale_max = min(xmax / w, ymax / h)
    scale_factor = random(scale_min, scale_max)
    scale(coords, scale_factor)
    return coords


def translateInLimits(coords, xmax, ymax):
    """Place la forme en restant dans le cadre donné."""
    bb = boundingBox(coords)
    txmin = 0 - bb[0]
    txmax = xmax - bb[2]
    tymin = 0 - bb[1]
    tymax = ymax - bb[3]
    t = (random(txmin, txmax), random(tymin, tymax))
    displace(coords, t)
    return coords


# génération des formes

def displaceRotateScaleTranslateInFrame(coords, xmax, ymax, aire_min=9):
    """Comme le om l'indique, fait varier n'importe quelle forme."""
    # rotation aléatoire
    rotate(coords, random(0, 2*np.pi))
    # scale aléatoire avec boundingBox plus petite inférieure aux limites
    scaleInLimits(coords, xmax, ymax, aire_min)
    # placement aléatoire dans la frame
    translateInLimits(coords, xmax, ymax)
    # enfin on a notre forme
    return coords


WIDTH = 128
HEIGHT = 128


def generateFromShape(shape):
    coords = ([], [])

    if shape == "triangle":
        coords = displaceRotateScaleTranslateInFrame(
            canoniqueTriangle(fractal=1), WIDTH, HEIGHT)
    elif shape == "carre":
        coords = displaceRotateScaleTranslateInFrame(
            canoniqueCarre(), WIDTH, HEIGHT)
    elif shape == "rectangle":
        coords = displaceRotateScaleTranslateInFrame(
            canoniqueRectangle(fractal=1), WIDTH, HEIGHT)
    elif shape == "losange":
        coords = displaceRotateScaleTranslateInFrame(
            canoniqueLosange(fractal=1), WIDTH, HEIGHT)
    elif shape == "fleche":
        coords = displaceRotateScaleTranslateInFrame(
            canoniqueFleche(fractal=1), WIDTH, HEIGHT)

    image = np.zeros((HEIGHT, WIDTH))
    rasterized = draw.polygon(coords[0], coords[1])
    image[rasterized[0], rasterized[1]] = 1.

    return image


def generateFromShapeByOrientation(orientation):
    # TODO générer des formes aléatoire aillant l'orientation demander
    return


def reformatImage(image):
    # return np.reshape(image, (1, image.shape[0] * image.shape[1]))
    return np.ndarray.flatten(image)


def displayShapes(shapes, n):
    for i in range(n):
        forme = np.random.randint(0, len(shapes))
        image = generateFromShape(shapes[forme])
        plt.imshow(image)
        plt.title(shapes[forme])
        plt.show()


shapes = ["triangle", "carre", "rectangle", "losange", "fleche"]
orientations = ["droit", "oblique"]
clfForm = None
clfOrientation = None
# displayShapes(shapes, 20)

# fonction d'apprentissage
def learnForm(nb_train):
    global clfForm
    global shapes
    forme_names = shapes
    formes = np.random.randint(0, len(forme_names), nb_train, dtype=int)
    X = np.array([reformatImage(generateFromShape(forme_names[formes[i]])) for i in range(nb_train)])
    Y = np.array([float(formes[i]) for i in range(nb_train)])


    clfForm = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(100, 20, 5, 2), random_state=1,
                        verbose=True)
    clfForm.fit(X, Y)


def learnOrientation(nb_train):
    global clfOrientation
    global orientations

    orientations_name = orientations
    orients = np.random.randint(0, len(orientations_name), nb_train, dtype=int)
    # TODO  appel a générate shape by rotation
    X = np.array([reformatImage(generateFromShape(orientations_name[orients[i]])) for i in range(nb_train)])
    Y = np.array([float(orients[i]) for i in range(nb_train)])


    clfOrientation = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(100, 20, 5, 2), random_state=1,
                        verbose=True)
    clfOrientation.fit(X, Y)


# test d'apprentissage
def testForm(nb_test):
    global clfForm
    global shapes
    score = 0
    for i in range(nb_test):
        forme = np.random.randint(0, len(shapes), dtype=int)
        image = generateFromShape(shapes[forme])
        result = clfForm.predict([reformatImage(image)])
        if int(round(result[0])) == forme:
            score += 1.
        plt.imshow(image)
        plt.title(shapes[int(round(result[0]))] + "   result: " + str(result[0]))
        plt.show()

    score /= nb_test
    print("Score sur " + str(nb_test) + " samples : " + str(score))

    return score

def getForm(img):
    global clfForm
    global shape
    result = clfForm.predict([reformatImage(img)])
    return shape[int(round(result[0]))]

def getOrientation(img):
    global clfOrientation
    global orientations
    result = clfOrientation.predict([reformatImage(img)])
    return orientations[int(round(result[0]))]


nb_train = 200
nb_test = 20
learnForm(nb_train)
testForm(nb_test)



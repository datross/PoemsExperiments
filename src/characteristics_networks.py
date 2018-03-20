from sklearn.neural_network import MLPClassifier
from skimage import draw
import numpy as np
import matplotlib.pyplot as plt

WIDTH = 64
HEIGHT = 64

def airePoly(coord):
    sum = 0
    for i in range(len(coord[0])):
        k = (i + 1) % len(coord[0])
        sum += coord[0][i] * coord[1][k] - coord[0][k] * coord[1][i]
    return abs(sum) * 0.5

def circular_order(coord):
    points = []
    newCoord = ([], [])
    for (x, y) in zip(*coord):
        points.append((x, y))

    center = np.mean(points, axis=0)
    points = np.array(sorted(points, key=lambda x: np.angle((x-center)[0]+(x-center)[1]*1j)))
    
    for (x, y) in points:
        newCoord[0].append(x)
        newCoord[1].append(y)

    return newCoord


# pour la postérité
def aireTriangleGenerique(coord):
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


def aireTriangle(coord):
    xa = coord[0][0]
    xb = coord[0][1]
    xc = coord[0][2]
    ya = coord[1][0]
    yb = coord[1][1]
    yc = coord[1][2]

    sum = xa * yc - xa * yb + xb * ya - xb * yc + xc * yb - xc * ya
    return 0.5 * abs(sum)


def random(a, b):
    return (b - a) * np.random.random() + a


def generateFromShape(shape):
    X = Y = []
    if shape == "carre":
        size = np.random.randint(2, min(WIDTH, HEIGHT))
        # angle = np.random()*2*np.pi
        # theta = np.radians(angle)
        # c, s = np.cos(theta), np.sin(theta)
        # rotate = np.array(((c,-s), (s, c)))
        # size = random(0, min(WIDTH, HEIGHT) / ((np.sinus(np.pi*0.25 + theta) - 1.41421356237 / 2)*2))
        x = np.random.randint(0, WIDTH - size)
        y = np.random.randint(0, HEIGHT - size)
        X += [x, x, x+size, x+size]
        Y += [y, y+size, y+size, y]
        #pivot = np.array()
        # print("air : "+str(size*size))
        # aireP = airePoly((X, Y))
        # print(aireP)

    if shape == "triangle":
        aire = 0
        while aire < 0.03 * WIDTH * HEIGHT:
            X = []
            Y = []
            for i in range(3):
                X += [np.random.randint(0, WIDTH)]
                Y += [np.random.randint(0, HEIGHT)]
            aire = airePoly((X, Y))

    if shape == "pantagon":
        aire = 0
        while aire < 0.03 * WIDTH * HEIGHT:
            X = []
            Y = []
            for i in range(5):
                X += [np.random.randint(0, WIDTH)]
                Y += [np.random.randint(0, HEIGHT)]

            aire = airePoly(circular_order((X, Y)))
        # aireP = aireTriangleGenerique((X, Y))
        # print(aire)
        # print(aireP)

    coordinates = circular_order((X, Y))
    image = np.zeros((HEIGHT, WIDTH))
    rasterized = draw.polygon(coordinates[0], coordinates[1])
    image[rasterized[0], rasterized[1]] = 1.

    # plt.imshow(image)
    # plt.show()

    # rotateCoordinates = np.dot(coordinates,rotate)
    # rotateRasterized = draw.polygon(rotateCoordinates[0], rotateCoordinates[1])
    # rotateImage = np.zeros((HEIGHT, WIDTH))
    # rotateImage[rotateRasterized[0], rotateRasterized[1]] = 1.

    # plt.imshow(rotateImage)
    # plt.show()

    return image


def reformatImage(image):
    # return np.reshape(image, (1, image.shape[0] * image.shape[1]))
    return np.ndarray.flatten(image)


def displayShapes(shape, n):
    for i in range(n):
        image = generateFromShape(shape)
        plt.imshow(image)
        plt.show()

# test d'apprentissage
def learn(nb_train, forme_names, nb_test) :
    formes = np.random.randint(0, 3, nb_train, dtype=int)
    X = np.array([reformatImage(generateFromShape(forme_names[formes[i]])) for i in range(nb_train)])
    Y = np.array([float(formes[i]) for i in range(nb_train)])


    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(100, 20, 5, 2), random_state=1,
                        verbose=True)
    clf.fit(X, Y)
    score = 0
    for i in range(nb_test):
        forme = np.random.randint(0, 3, dtype=int)
        image = generateFromShape(forme_names[forme])
        result = clf.predict([reformatImage(image)])
        if int(round(result[0])) == forme:
            score += 1.
        plt.imshow(image)
        plt.title(forme_names[int(round(result[0]))] + "   result: " + str(result[0]))
        plt.show()


    score /= nb_test
    print("Score sur " + str(nb_test) + " samples : " + str(score))



nb_train = 10000
nb_test = 100
forme_names = ["triangle", "carre", "pantagon"]

# learn(nb_train, forme_names, nb_test)
image = generateFromShape("pantagon")
plt.imshow(image)
plt.show()


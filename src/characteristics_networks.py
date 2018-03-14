from sklearn.neural_network import MLPClassifier
from skimage import draw
import numpy as np
import matplotlib.pyplot as plt

WIDTH = 32
HEIGHT = 32


def aireTriangle(coord):
    xa = coord[0][0]
    xb = coord[0][1]
    xc = coord[0][2]
    ya = coord[1][0]
    yb = coord[1][1]
    yc = coord[1][2]
    return 0.5 * abs(xa*yc - xa*yb + xb*ya - xb*yc + xc*yb - xc*ya)

def generateFromShape(shape):
    X = []
    Y = []
    if shape == "carre":
        size = np.random.randint(2, min(WIDTH, HEIGHT))
        x = np.random.randint(0, WIDTH - size)
        y = np.random.randint(0, HEIGHT - size)
        X += [x, x, x+size, x+size]
        Y += [y, y+size, y+size, y]

    if shape == "triangle":
        aire = 0
        while aire < 0.03 * WIDTH * HEIGHT:
            X = []
            Y = []
            for i in range(3):
                X += [np.random.randint(0, WIDTH)]
                Y += [np.random.randint(0, HEIGHT)]
            aire = aireTriangle((X, Y))

    coordinates = (Y, X)
    image = np.zeros((HEIGHT, WIDTH))
    rasterized = draw.polygon(coordinates[0], coordinates[1])
    image[rasterized[0], rasterized[1]] = 1.

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

nb_train = 2000
forme_names = ["carre", "triangle"]
formes = np.random.randint(0, 2, nb_train, dtype=int)
X = np.array([reformatImage(generateFromShape(forme_names[formes[i]])) for i in range(nb_train)])
Y = np.array([float(formes[i]) for i in range(nb_train)])

print(X.shape)
print(Y.shape)

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(100, 20, 5, 2), random_state=1,
                    verbose=True)
clf.fit(X, Y)
score = 0
nb_test = 200
for i in range(nb_test):
    forme = np.random.randint(0, 2, dtype=int)
    image = generateFromShape(forme_names[forme])
    result = clf.predict([reformatImage(image)])
    if int(round(result[0])) == forme:
        score += 1.
    # plt.imshow(image)
    # plt.title(forme_names[int(round(result[0]))] + "   result: " + str(result[0]))
    # plt.show()


score /= nb_test
print("Score sur " + str(nb_test) + " samples : " + str(score))

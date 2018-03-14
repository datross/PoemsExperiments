import numpy as np
import matplotlib.pyplot as plt


def square_distance_pairs(points):
    d = np.zeros(len(points))
    for i in range(len(points)):
        d[i] = np.linalg.norm(points[i] - points[(i+1) % len(points)])
    return d


def circular_order(points):
    center = np.mean(points, axis=0)
    return np.array(sorted(points, key=lambda x: np.angle((x-center)[0]+(x-center)[1]*1j)))


def distance_regularity(points):
    points = circular_order(points)


def describe_shape(points):
    if len(points) == 0:
        return "informe"
    elif len(points) == 1:
        return "point"
    elif len(points) == 2:
        return "ligne"
    elif len(points) == 3:
        return "triangle"
    elif len(points) == 4:
        return "carre"
    elif len(points) >= 5:
        return "informe"


def random_points(n):
    return 2 * np.random.rand(n, 2) - 1.


def display_points(points, block=True):
    plt.figure()
    plt.plot(points[:, 0], points[:, 1])
    plt.show(block=block)


points = random_points(5)
print(points)
print(points[:, 0])
display_points(points, block=False)
display_points(circular_order(points))

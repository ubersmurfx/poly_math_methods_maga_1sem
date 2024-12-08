import numpy as np
from matplotlib import pyplot as plt

# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
# https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

def draw_triangles(*triangles: np.array):
    for tr in triangles:
        tr = np.append(tr, [tr[0]], axis=0)
        x, y = tr.T
        plt.scatter(x, y)
        plt.plot(x, y)

    plt.grid()
    plt.show()


def ccw(a, b, c):
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])


# Return true if line segments AB and CD intersect
def intersect(a, b, c, d):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def same_side(p, a, b, c):
    cp1 = np.cross(c-b, p-b)
    cp2 = np.cross(c-b, a-b)
    # print(cp1, cp2, np.dot(cp1, cp2))
    if np.dot(cp1, cp2) >= 0:
        # print(f'{p}, {a}, {b}, {c} {True}')
        return True
    else:
        # print(f'{p}, {a}, {b}, {c} {False}')
        return False


def point_in_triangle(p, tr):
    a = tr[0]
    b = tr[1]
    c = tr[2]

    if same_side(p, a, b, c) and same_side(p, b, a, c) and same_side(p, c, a, b):
        return True
    else:
        return False


# Оказалось, вариант с точками не работает, когда этих самых внутренних точек нет
def check_collision(*triangles):
    tr_1 = triangles[0]
    tr_2 = triangles[1]

    for point in tr_1:
        if point_in_triangle(point, tr_2):
            return True

    for point in tr_2:
        if point_in_triangle(point, tr_1):
            return True

    for i in reversed(range(3)):
        for j in reversed(range(3)):
            if intersect(tr_1[i], tr_1[i-1], tr_2[j], tr_2[j-1]):
                return True

    return False


tr_1 = np.array([[1, 1],
                [2, 3],
                [4, 1]])

# border collision
tr_2 = np.array([[5, 1],
                [3, 3],
                [4, 3]])

# print(intersect(tr_1[1], tr_1[2], tr_2[0], tr_2[1]))

print(check_collision(tr_1, tr_2))
draw_triangles(tr_1, tr_2)

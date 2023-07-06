from math import *
from random import *


class Vec:
    """ Crée un vecteur de coordonnées (x ; y)
        v1 + v2 pour additionner deux vecteurs (la soustraction fonctionne aussi
        v1 * v2 pour le produit vectoriel de v1 et v2
        v1 ^ v2 pour l'angle entre v1 et v2
    """

    def __init__(self, x, y):
        assert (type(x) == int or type(x) == float) and (type(y) == int or type(y) == float)
        self.value = x, y

    def get(self):
        return self.value

    def __add__(self, other):
        return Vec(self.value[0] + other.get()[0], self.value[1] + other.get()[1])

    def __sub__(self, other):
        return Vec(self.value[0] - other.get()[0], self.value[1] - other.get()[1])

    def __neg__(self):
        return Vec(-self.value[0], -self.value[1])

    def __mul__(self, other):
        if type(other) == Vec:
            return self.value[0] * other.get()[0] + self.value[1] * other.get()[1]
        return Vec(self.value[0] * other, self.value[1] * other)

    def __truediv__(self, other):
        return Vec(self.value[0] / other, self.value[1] / other)

    def __floordiv__(self, other):
        return Vec(self.value[0] // other, self.value[1] // other)

    def __xor__(self, other):
        """ Return the angle between the two vectors.
            The result is positive when the rotation is clockwise and negative when anticlockwise. """
        x1, y1 = self.get()
        x2, y2 = other.get()
        return atan2(x1 * y2 - y1 * x2, x1 * x2 + y1 * y2)

    def __len__(self):
        return int(sqrt(self.value[0] ** 2 + self.value[1] ** 2))

    def __int__(self):
        return int(sqrt(self.value[0] ** 2 + self.value[1] ** 2))

    def __float__(self):
        return sqrt(self.value[0] ** 2 + self.value[1] ** 2)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return abs(self.value[0]-other.get()[0]) < 0.001 and abs(self.value[1]-other.get()[1]) < 0.001

    def __hash__(self):
        return hash(self.value)

    def x(self, val=None):
        if val is None:
            return self.value[0]
        self.value = val, self.value[1]

    def y(self, val=None):
        if val is None:
            return self.value[1]
        self.value = self.value[0], val

    def normalised(self):
        if self.value == (0, 0): return Vec(0, 0)
        d = sqrt(self.value[0] ** 2 + self.value[1] ** 2)
        return Vec(self.value[0] / d, self.value[1] / d)

    def copy(self):
        """ Renvoie une copie du vecteur """
        return Vec(*self.value)

    def angle(self, other):
        """ Return the abs of the angle between the 2 vectors """
        return acos(self * other / float(self) * float(other))

    def change_size(self, size: float):
        """ Met la norme du vecteur à size """
        if size == 0:
            return Vec(0, 0)
        root = sqrt(self.value[0] ** 2 + self.value[1] ** 2) / size
        if root < 0.1: return Vec(0, 0)
        return Vec(self.value[0] / root, self.value[1] / root)

    def ortho(self):
        return Vec(-self.value[1], self.value[0])

    def rotate(self, radian, centre=None):
        if centre is None: centre = Vec(0, 0)
        temp = self - centre
        return Vec(cos(radian) * temp.get()[0] - temp.get()[1] * sin(radian),
                   temp.get()[0] * sin(radian) + temp.get()[1] * cos(radian)) + centre


def det(v1, v2):
    x1, y1, x2, y2 = v1.get() + v2.get()
    return x1 * y2 - y1 * x2


class Line:
    def __init__(self, point: Vec, vec: Vec):
        assert vec.get() != (0, 0)
        self.vec = vec
        self.point = point

    def __contains__(self, item):
        x, y = item.get()
        if self.vec.get()[0] == 0 and self.vec.get()[1] == 0:
            return x == self.point.get()[0] and y == self.point.get()[1]
        elif self.vec.get()[0] == 0:
            return x == self.point.get()[0]
        elif self.vec.get()[1] == 0:
            return y == self.point.get()[1]
        return (x - self.point.get()[0]) / self.vec.get()[0] - (y - self.point.get()[1]) / self.vec.get()[1] < 0.0001

    def pos2nb(self, point):
        if self.vec.get()[0] == 0:
            return (point.get()[1] - self.point.get()[1]) / self.vec.get()[1]
        else:
            return (point.get()[0] - self.point.get()[0]) / self.vec.get()[0]

    def inter(self, other):
        x1, y1 = self.point.get()
        x2, y2 = (self.point + self.vec).get()
        x3, y3 = other.point.get()
        x4, y4 = (other.point + other.vec).get()
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        return Vec(x, y)

    def projection(self, point):
        n = self.vec.ortho()
        return self.inter(Line(point, n))


def dist_seg_p(a, b, p):
    """ Trouve la distance minimale entre [a, b] et p. """
    line = Line(a, b - a)
    p2 = line.projection(p)
    if b.x() - a.x() != 0:
        t = (p2.x() - a.x()) / (b.x() - a.x())
    else:
        t = (p2.y() - a.y()) / (b.y() - a.y())
    if 0 <= t <= 1:
        return p.dist(p2)
    elif t < 0:
        return p.dist(a)
    return p.dist(b)


class Msg:
    def __init__(self, msg):
        self.msg = msg

    def get(self):
        return self.msg

    def set(self, msg):
        self.msg = msg

    def __add__(self, other):
        """ Same as set """
        self.msg = other

    def __neg__(self):
        """ Same as get """
        return self.msg

    def __invert__(self):
        return self.msg

    def __str__(self):
        return str(self.msg)


def dist(v1, v2):
    return float(v2 - v1)


def simplifie_rec(tab, d_max):
    if len(tab) <= 2:
        return tab
    line = Line(tab[0], tab[0] - tab[-1])
    dist_max = d_max
    i_max = 0
    for i in range(1, len(tab) - 1):
        d = dist(line.projection(tab[i]), tab[i])
        if d > dist_max:
            dist_max = d
            i_max = i
    if dist_max == d_max:
        return [tab[0], tab[-1]]
    return simplifie_rec(tab[:i_max], d_max) + simplifie_rec(tab[i_max:], d_max)


def perlin_noise(seed, size, setting=0, resolution=10, smooth=True):
    r = Random(seed)
    res = resolution
    corners = [[Vec(1, 0).rotate(r.random() * pi * 2) for _ in range(size[0] // res + 2)] for _ in
               range(size[1] // res + 2)]
    result = []
    for x in range(size[0]):
        result.append([])
        maps = [[], []]
        for y in range(size[1]):
            left_up = corners[y // res][x // res] * Vec(x // res * res - x + 0.5, y // res * res - y + 0.5) + setting
            right_up = corners[y // res][x // res + 1] * Vec((x // res + 1) * res - 0.5 - x,
                                                             y // res * res - y + 0.5) + setting
            left_down = corners[y // res + 1][x // res] * Vec(x // res * res - x + 0.5,
                                                              (y // res + 1) * res - 0.5 - y) + setting
            right_down = corners[y // res + 1][x // res + 1] * Vec((x // res + 1) * res - 0.5 - x,
                                                                   (y // res + 1) * res - 0.5 - y) + setting
            maps[0].append(lerp((left_up + (y % res) / (res - 1) * (left_down - left_up)) / (3 * res) + 0.5) * 2 - 1)
            maps[1].append(lerp((right_up + (y % res) / res * (right_down - right_up)) / (2 * res) + 0.5) * 2 - 1)
        for y in range(len(maps[0])):
            result[-1].append(lerp((maps[0][y] + (x % res) / res * (maps[1][y] - maps[0][y])) / 2 + 0.5) * 2 - 1)
            result[-1][-1] = max(min(result[-1][-1], 1), -1)
            if not smooth:
                if result[-1][-1] > 0.75:
                    result[-1][-1] = 1
                elif result[-1][-1] > 0.25:
                    result[-1][-1] = 0.5
                elif result[-1][-1] > -0.25:
                    result[-1][-1] = 0
                elif result[-1][-1] > -0.75:
                    result[-1][-1] = -0.5
                else:
                    result[-1][-1] = -1
    return result


def lerp(x):
    return 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3


def col(nb):
    temp = max(min(255, nb), 0)
    return temp, temp, temp


def do_nothing(a):
    return a


def merge_sort(tab, func=do_nothing):
    if len(tab) <= 1:
        return tab
    elif len(tab) == 2:
        if func(tab[0]) > func(tab[1]): return tab[1], tab[0]
        return tab
    tab1 = merge_sort(tab[:len(tab)//2], func)
    tab2 = merge_sort(tab[len(tab) // 2:], func)
    tab = ()
    while len(tab1) > 0 or len(tab2) > 0:
        if len(tab1) == 0 or (len(tab2) > 0 and func(tab2[0]) < func(tab1[0])):
            tab += (tab2[0],)
            tab2 = tab2[1:]
        else:
            tab += (tab1[0],)
            tab1 = tab1[1:]
    return tab

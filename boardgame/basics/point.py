from math import *

class Point:

    deg2rad = pi / 180

    @staticmethod
    def Clone(point):
        return Point(point.x, point.y, point.integer)

    def __init__(self, x=0, y=0, integer=False):
        self.integer = bool(integer)
        self.x = x
        self.y = y
        self.iter_index = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, _x):
        self._x = int(round(_x)) if self.integer else _x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, _y):
        self._y = int(round(_y)) if self.integer else _y

    @property
    def normalized(self):
        l = self.length
        if l == 0:
            return Point()
        return Point(self.x / l, self.y / l)

    @property
    def lengthSq(self):
        return self.x**2 + self.y**2

    @lengthSq.setter
    def lengthSq(self, lengthSq):
        return self.normalized * sqrt(lengthSq)

    @property
    def length(self):
        return sqrt(self.lengthSq)

    @length.setter
    def length(self, length):
        return self.normalized * length

    @property
    def radians(self):
        return atan2(self.y, self.x)

    @radians.setter
    def radians(self, radians):
        l = self.length
        self.x = l * cos(radians)
        self.y = l * sin(radians)

    @property
    def degrees(self):
        return self.radians / Point.deg2rad

    @degrees.setter
    def degrees(self, degrees):
        l = self.length
        a = degrees * Point.deg2rad
        self.x = l * cos(a)
        self.y = l * sin(a)

    def rotateRadians(self, radians, center=None):
        if center is not None:
            self.x -= center.x
            self.y -= center.y
        self.radians += radians
        if center is not None:
            self.x += center.x
            self.y += center.y
        return self

    def rotateDegrees(self, degrees, center=None):
        return self.rotateRadians(degrees * Point.deg2rad, center)

    def dot(self, other):
        return self.x * other[0] + self.y * other[1]

    def cross(self, other):
        return self.x * other[1] - self.y * other[0]

    def proj(self, other):
        return self.dot(other) / max(other.lengthSq, 0.0000001) * other

    def reflect(self, normal):
        n = Point(normal.y, -normal.x)
        return self - 2 * self.dot(n) / max(n.lengthSq, 0.0000001) * n

    def distanceTo(self, other):
        return (self - other).length

    def __len__(self):
        return int(self.length)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Point(self.x * other[0], self.y * other[1])
        else:
            return Point(self.x * other, self.y * other)

    def __pow__(self, exponent):
        return Point(self.x**exponent, self.y**exponent)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if isinstance(other, self.__class__):
            return Point(self.x / other[0], self.y / other[1])
        else:
            return Point(self.x / other, self.y / other)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Point(self.x / other[0], self.y / other[1])
        else:
            return Point(self.x / other, self.y / other)

    def __rtruediv__(self, other):
        if isinstance(other, self.__class__):
            return Point(other[0] / self.x, other[1] / self.y)
        else:
            return Point(other / self.x, other / self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __hash__(self):
        d = self.x + self.y
        return int(d * (d + 1) / 2 + self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.lengthSq < other.lengthSq

    def __le__(self, other):
        return self.lengthSq <= other.lengthSq

    def __gt__(self, other):
        return self.lengthSq > other.lengthSq

    def __ge__(self, other):
        return self.lengthSq >= other.lengthSq

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other[0] and self.y == other[1]

    def __ne__(self, other):
        return not (self == other)

    def __iter__(self):
         return self

    def __next__(self):
        if self.iter_index == 2:
            self.iter_index = 0
            raise StopIteration
        v = self[self.iter_index]
        self.iter_index += 1
        return v

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        return None

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value

    def insideRectangle(self, x, y, width, height):
        return self.x >= x and self.y >= y and self.x <= x + width and self.y <= y + height

##class _Animal():
##
##    def __init__(self, name):
##        self.name = name
##
##    def __str__(self):
##        return "[{}]".format(self.name)
##
##class _Creature(Animal, Point):
##
##    def __init__(self, name, x, y):
##        Animal.__init__(self, name)
##        Point.__init__(self, x, y)
##
##    def __str__(self):
##        return "{} {}".format(Animal.__str__(self), Point.__str__(self))

from math import *

class Point:

    deg2rad = pi / 180

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def normalized(self):
        l = self.length
        if l == 0:
            return Point()
        return Point(self.x / l, self.y / l)

    @property
    def lengthSq(self):
        return self.x**2 + self.y**2

    @property
    def length(self):
        return sqrt(self.lengthSq)

    def __len__(self):
        return int(self.length)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def proj(self, other):
        return self.dot(other) / other.lengthSq * other

    def reflect(self, normal):
        n = Point(normal.y, -normal.x)
        return self - 2 * self.dot(n) / n.lengthSq * n

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

    def distanceTo(self, other):
        return (self - other).length

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Point(self.x * other.x, self.y * other.y)
        else:
            return Point(self.x * other, self.y * other)

    def __pow__(self, exponent):
        return Point(self.x**exponent, self.y**exponent)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Point(self.x / other.x, self.y / other.y)
        else:
            return Point(self.x / other, self.y / other)

    def __rtruediv__(self, other):
        if isinstance(other, self.__class__):
            return Point(other.x / self.x, other.y / self.y)
        else:
            return Point(other / self.x, other / self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __hash__(self):
        d = self.x + self.y
        return int(d * (d + 1) / 2 + self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

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
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

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

import math

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def normalized(self):
        l = self.length
        return Point(self.x / l, self.y / l)

    @property
    def lengthSq(self):
        return self.x**2 + self.y**2

    @property
    def length(self):
        return math.sqrt(self.lengthSq)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def proj(self, other):
        return self.dot(other) / other.lengthSq * other

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

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
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
##
##if __name__ == "__main__":
##    p = Point(-20, 8)
##    m = Point(5, 4)
##    r = Point(5, 5)
##    s = Point(5, 5)
##
##    k = p
##    k /= m
##    print(k)
##
##    print("abs({}) = {} == {}".format(p, abs(p), abs(p) == Point(20, 8)))
##
##    print(p.cross(m))
##
##    o = Creature("Gollum", 12, 50)
##    print(o)
##
##    print(20 / p)
##    print(20.1 / p)
##    print(p / 5)
##    print(p / 5.3)
##
##    print("{} = (1.32, 1.76)".format(Point(1, 2).proj(Point(3, 4))))
##
##    print(5 * p)
##    print(5.3 * p)
##    print(p * 5)
##    print(p * 5.3)
##    print(s.length)
##    print(s.lengthSq)
##    print(p.normalized)
##    print(p.normalized.length)
##    
##    print(p)
##    print(-p)
##    print("{} + {} = {}".format(p, m, p + m))
##    print("{} - {} = {}".format(p, m, p - m))
##    print("{} * {} = {}".format(p, m, p * m))
##    print("{} / {} = {}".format(p, m, p / m))
##    print("[0] = {}, [1] = {}, [2] = {}".format(p[0], p[1], p[2]))
##    p[0] = 5
##    print("[0] = {}, [1] = {}, [2] = {}".format(p[0], p[1], p[2]))
##    print("{} == {} = {}".format(r, s, r == s))
##    print("{} != {} = {}".format(r, s, r != s))
##    print("{} == {} = {}".format(m, s, m == s))

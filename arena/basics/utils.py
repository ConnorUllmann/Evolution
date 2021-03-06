from math import *
from numpy import exp
from datetime import timedelta
from pygame import Rect
from .point import Point

def RemoveMilliseconds(delta):
    return delta - timedelta(microseconds=delta.microseconds)

def Spiral(n):
    if n==0:
        n = 1
    elif n==1:
        n = 0
    elif n >= 8:
        n += 1
    
    k = ceil((sqrt(n) - 1) / 2)
    t = 2 * k+1
    m = t**2 
    t -= 1

    if  n >= m - t:
        return (-m + n + k, -k)
    else:
        m -= t
    
    if n >= m - t:
        return (-k, m - n - k)
    else:
        m -= t
    
    if n >= m - t:
        return (m - k - n, k)
    else:
        return (k, -m + n + k + t)

def Heartbeat(x):
    x %= 1
    return 17.0351656925 * x * (1 / (x + 1) - 0.5 * x)**4 * sin(4 * pi * x)

def Sigmoid(x):
    # The Sigmoid function, which describes an S shaped curve.
    # We pass the weighted sum of the inputs through this function to
    # normalise them between 0 and 1.
    return 1.0 / (1.0 + exp(-x))

def SigmoidDerivative(x):
    # The derivative of the Sigmoid function.
    # This is the gradient of the Sigmoid curve.
    # It indicates how confident we are about the existing weight.
    sx = Sigmoid(x)
    return sx * (1.0 - sx)

def IsInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def AngleDiff(a, b):
    diff = b - a
    while diff > pi:
        diff -= 2 * pi
    while diff <= -pi:
        diff += 2 * pi
    return diff

def Cross3(a, b):
    return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

def CirclesCollide(a_pos, a_radius, b_pos, b_radius):
    return (a_pos - b_pos).lengthSq <= (a_radius + b_radius)**2

def RectanglesCollide(ax, ay, aw, ah, bx, by, bw, bh):
    return ax + aw >= bx and bx + bw >= ax and ay + ah >= by and by + bh >= ay

def PointInsideRectangle(px, py, rx, ry, rw, rh):
    return Point(px, py).insideRectangle(rx, ry, rw, rh)

def PointInsideCircle(point, circle_pos, circle_radius):
    return (point - circle_pos).lengthSq <= circle_radius**2

def CircleLineCollide(center, radius, lineA, lineB, asSegment=True):
    ret = []
    if abs(lineA.x - lineB.x) < 0.00001:
        x0 = x1 = lineA.x
        d = radius**2 - (x0 - center.x)**2
        if d < 0:
            return ret
        d = sqrt(d)
        y0 = center.y + d
        u = Point(x0, y0)
        if not asSegment or ColinearPointInsideLineSegment(u, lineA, lineB):
            ret.append(u)
        if d == 0:
            return ret
        y1 = center.y - d
        v = Point(x1, y1)
        if not asSegment or ColinearPointInsideLineSegment(v, lineA, lineB):
            ret.append(v)
        return ret
    m = (lineB.y - lineA.y) / (lineB.x - lineA.x)
    a = m**2 + 1
    b = -2 * m**2 * lineA.x + 2 * m * lineA.y - 2 * m * center.y - 2 * center.x
    c = m**2 * lineA.x**2 - 2 * m * lineA.x * lineA.y + 2 * m * center.y * lineA.x + lineA.y**2 - 2 * center.y * lineA.y + center.y**2 - radius**2 + center.x**2
    d = b**2 - 4 * a * c
    if d < 0:
        return ret
    x0 = (-b + sqrt(d)) / (2 * a)
    y0 = lineA.y + m * (x0 - lineA.x)
    u = Point(x0, y0)
    if not asSegment or ColinearPointInsideLineSegment(u, lineA, lineB):
        ret.append(u)
    if d == 0:
        return ret
    x1 = (-b - sqrt(d)) / (2 * a)
    y1 = lineA.y + m * (x1 - lineA.x)
    v = Point(x1, y1)
    if not asSegment or ColinearPointInsideLineSegment(v, lineA, lineB):
        ret.append(v)
    return ret

def CircleHorizontalLineCollide(circle_pos, circle_radius, y, x1=None, x2=None, filled=True):
    #x1 and x2 must both either be None or non-None
    c = circle_radius**2 - (y - circle_pos.y)**2

    if c <= 0:
        return False

    if x1 is None or x2 is None:
        return True

    if x1 > x2:
        t = x1
        x1 = x2
        x2 = t

    d = sqrt(c)

    m = circle_pos.x - d
    n = circle_pos.x + d

    intersects = x1 <= m <= x2 or x1 <= n <= x2

    if not filled:
        return intersects

    return intersects or (m <= x1 <= n and m <= x2 <= n)

def CircleVerticalLineCollide(circle_pos, circle_radius, x, y1=None, y2=None, filled=True):
    #y1 and y2 must both either be None or non-None
    return CircleHorizontalLineCollide(Point(circle_pos.y, circle_pos.x), circle_radius, x, y1, y2, filled)

# DOESN'T WORK YET!
def CircleCollidesRectangle(circle_pos, circle_radius, rect_x, rect_y, rect_width, rect_height):
    radiusPoint = Point(circle_radius, circle_radius)
    if not RectanglesCollide(circle_pos - radiusPoint, 2 * radiusPoint, rect_x, rect_y, rect_width, rect_height):
        return False

    if CircleHorizontalLineCollide(circle_pos, circle_radius, rect_y, rect_x, rect_x + rect_width, filled=True) or \
        CircleHorizontalLineCollide(circle_pos, circle_radius, rect_y + rect_height, rect_x, rect_x + rect_width, filled=True) or \
        CircleVerticalLineCollide(circle_pos, circle_radius, rect_x, rect_y, rect_y + rect_height, filled=True) or \
        CircleHorizontalLineCollide(circle_pos, circle_radius, rect_x + rect_width, rect_y, rect_y + rect_height, filled=True):
        return True

def LinesIntersect(m, n, t, u):
    det = (n[0] - m[0]) * (u[1] - t[1]) - (u[0] - t[0]) * (n[1] - m[1])
    if det == 0:
        return False
    return 0 < ((u[1] - t[1]) * (u[0] - m[0]) + (t[0] - u[0]) * (u[1] - m[1])) < det and \
           0 < ((m[1] - n[1]) * (u[0] - m[0]) + (n[0] - m[0]) * (u[1] - m[1])) < det

def LinesIntersectionPoint(A, B, E, F, as_seg = True):
    if as_seg and not RectanglesCollide(min(A[0], B[0]), min(A[1], B[1]), abs(A[0]-B[0]), abs(A[1]-B[1]), min(E[0], F[0]), min(E[1], F[1]), abs(E[0]-F[0]), abs(E[1]-F[1])):
        return None

    a1 = B[1]-A[1]
    a2 = F[1]-E[1]
    b1 = A[0]-B[0]
    b2 = E[0]-F[0]
    c1 = B[0]*A[1] - A[0]*B[1]
    c2 = F[0]*E[1] - E[0]*F[1]

    denom = a1*b2 - a2*b1
    if denom == 0:
        return None
    ip = Point((b1*c2 - b2*c1)/denom, (a2*c1 - a1*c2)/denom)
    
    if as_seg and \
        (ip[0] - B[0])**2 + (ip[1] - B[1])**2 > (A[0] - B[0])**2 + (A[1] - B[1])**2 or \
        (ip[0] - A[0])**2 + (ip[1] - A[1])**2 > (A[0] - B[0])**2 + (A[1] - B[1])**2 or \
        (ip[0] - F[0])**2 + (ip[1] - F[1])**2 > (E[0] - F[0])**2 + (E[1] - F[1])**2 or \
        (ip[0] - E[0])**2 + (ip[1] - E[1])**2 > (E[0] - F[0])**2 + (E[1] - F[1])**2:
        return None
    return ip

def PointOnLineAtX(a, b, x):
    diffX = b[0] - a[0]
    if diffX == 0:
        return (a+b)/2
    return Point(x, (x - a[0]) / diffX * (b[1] - a[1]) + a[1])

def PointOnLineAtY(a, b, y):
    diffY = b[1] - a[1]
    if diffY == 0:
        return (a+b)/2
    return Point((y - a[1]) / diffY * (b[0] - a[0]) + a[0], y)

def PointOnLineClosestToPoint(lineA, lineB, point, as_segment=False):
    AB = lineB - lineA
    ret = (point - lineA).proj(AB) + lineA
    if not as_segment or ColinearPointInsideLineSegment(point, lineA, lineB):
        return ret
    r = (ret - lineA).dot(AB)
    if r < 0:
        return lineA
    if r > 1:
        return lineB
    return ret

def AreaTriangle(a, b, c):
    #Will return negative values depending on what side of (a, b) that c is on
    return 0.5 * (a.x * (b.y - c.y) - b.x * (a.y - c.y) + c.x * (a.y - b.y))

def ColinearPointInsideLineSegment(pos, lineA, lineB):
    v = (pos - lineA).dot(lineB - lineA)
    return v >= 0 and v <= (lineB - lineA).lengthSq

def Torque(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[0] - centerOfMass[0], forcePosition[1] - centerOfMass[1])
    return r.cross(forceVector)

def TorquePushVector(centerOfMass, forcePosition, forceVector):
    r = Point(forcePosition[0] - centerOfMass[0], forcePosition[1] - centerOfMass[1])
    return forceVector.proj(r)

def TorquePullVector(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[1] - centerOfMass[1], -forcePosition[0] + centerOfMass[0])
    return forceVector.proj(r)

def Binary(x, digits=-1, asList=False):
    if type(x) is list:
        s = ""
        for c in x:
            s += str(c)
    else:
        s = "{0:b}".format(int(x))
    
    while len(s) < digits:
        s = "0" + s
    if digits > 0:
        s = s[-digits:]

    if asList:
        r = []
        for c in s:
            r.append(int(c))
        return r
    return s

def Debinary(x):
    if type(x) is tuple or type(x) is list:
        k = ''
        for a in x:
            k += str(a)
        return int(k, 2)
    return int(x, 2)

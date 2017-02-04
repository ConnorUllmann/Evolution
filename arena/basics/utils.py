from math import *
from numpy import exp
from datetime import timedelta
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
    x = x % 1
    return 17.0351656925 * x * (1 / (x + 1) - 0.5 * x)**4 * sin(4 * pi * x)

# The Sigmoid function, which describes an S shaped curve.
# We pass the weighted sum of the inputs through this function to
# normalise them between 0 and 1.
def Sigmoid(x):
    return 1.0 / (1.0 + exp(-x))
        
# The derivative of the Sigmoid function.
# This is the gradient of the Sigmoid curve.
# It indicates how confident we are about the existing weight.
def SigmoidDerivative(x):
    sx = Sigmoid(x)
    return sx * (1.0 - sx)

def IsInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def Cross3(a, b):
    return [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

def CirclesCollide(a_pos, a_radius, b_pos, b_radius):
    return (a_pos - b_pos).lengthSq <= (a_radius + b_radius)**2

def LinesIntersect(m, n, t, u):
    a = m[0]
    b = m[1]
    c = n[0]
    d = n[1]
    p = t[0]
    q = t[1]
    r = u[0]
    s = u[1]
    det = (c - a) * (s - q) - (r - p) * (d - b)
    if det == 0:
        return False
    _lambda = ((s - q) * (r - a) + (p - r) * (s - b)) / det
    _gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det
    return (0 < _lambda and _lambda < 1) and (0 < _gamma and _gamma < 1)

def LinesIntersectionPoint(A, B, E, F, as_seg = True): 
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

def ColinearPointInsideLineSegment(pos, lineA, lineB):
    v = (pos - lineA).dot(lineB - lineA)
    return v >= 0 and v <= (lineB - lineA).lengthSq

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

def Torque(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[0] - centerOfMass[0], forcePosition[1] - centerOfMass[1])
    return r.cross(forceVector)
def TorquePushVector(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[0] - centerOfMass[0], forcePosition[1] - centerOfMass[1])
    return Proj(forceVector, r)
def TorquePullVector(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[1] - centerOfMass[1], -forcePosition[0] + centerOfMass[0])
    return forceVector.proj(r)

def AngleDiff(a, b):
    diff = b - a
    while diff > 180:
        diff -= 360
    while diff <= -180:
        diff += 360
    return diff

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

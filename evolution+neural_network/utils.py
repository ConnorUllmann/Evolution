from math import *
from numpy import exp
from datetime import timedelta

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

def Add(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def Scale(a, b):
    return [b * a[0], b * a[1]]

def Length(a):
    return sqrt(a[0]**2 + a[1]**2)

def LengthSq(a):
    return a[0]**2 + a[1]**2

def Normalize(a):
    length = Length(a)
    if length <= 0:
        return (0, 0)
    return Scale(a, 1/length)

def Proj(a, b):
    divisor = LengthSq(b)
    if divisor <= 0:
        return (0,0)
    mult = Dot(a, b) / divisor
    return (mult * b[0], mult * b[1])

def Cross2(a, b):
    return a[0]*b[1]-a[1]*b[0]

def Cross3(a, b):
    return [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

def DistanceSq(a, b):
    return LengthSq(((a[0] - b[0]), (a[1] - b[1])))
def Distance(a, b):
    return Length(((a[0] - b[0]), (a[1] - b[1])))

def CirclesCollide(a_pos, a_radius, b_pos, b_radius):
    return DistanceSq(a_pos, b_pos) <= (a_radius + b_radius)**2

def Torque(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[0] - centerOfMass[0], forcePosition[1] - centerOfMass[1])
    return Cross2(r, forceVector)
def TorquePushVector(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[0] - centerOfMass[0], forcePosition[1] - centerOfMass[1])
    return Proj(forceVector, r)
def TorquePullVector(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[1] - centerOfMass[1], -forcePosition[0] + centerOfMass[0])
    return Proj(forceVector, r)

def Binary(x, digits=-1, asList=False):
    if type(x) is list:
        s = ""
        for c in x:
            s = "{}{}".format(s, c)
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

def Xor(*args):
    x = args[0]
    for i in range(1, len(args)):
        x = (x != args[i])
    return [int(x)]

def Opp(*args):
    return [int(args[0] != args[1])]

def Add(*args):
    mid = int(len(args)/2)
    a = 0
    b = 0
    c = 0
    for i in range(0, int(mid)):
        power = pow(2, i)
        k = len(args) - 1 - i
        a += power * args[k - mid]
        b += power * args[k]
        c += power
    c = c * 2 + 1
    y = int(a + b)
    yString = Binary(y)
    
    ret = []
    for c in yString:
        ret.append(int(c == '1'))
    while len(ret) < len(Binary(c)):
        ret.insert(0, 0)
    #print("{} + {} = {}".format(a, b, y))
    #print("{} + {} = {}".format(args[:mid], args[mid:], ret))
    return ret

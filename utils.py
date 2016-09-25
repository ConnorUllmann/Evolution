from math import *

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

def Dot(a, b):
    total = 0
    for i in range(0, len(a)):
        total += a[i]*b[i]
    return total

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

def Torque(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[0] - centerOfMass[0], forcePosition[1] - centerOfMass[1])
    return Cross2(r, forceVector)
def TorquePushVector(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[0] - centerOfMass[0], forcePosition[1] - centerOfMass[1])
    return Proj(forceVector, r)
def TorquePullVector(centerOfMass, forcePosition, forceVector):
    r = (forcePosition[1] - centerOfMass[1], -forcePosition[0] + centerOfMass[0])
    return Proj(forceVector, r)

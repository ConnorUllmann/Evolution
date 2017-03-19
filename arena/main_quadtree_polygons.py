from basics import Screen, Point, Color, QuadTree, Polygon, PolygonEntity
from random import random
from math import pi

polygons = []
quadtree = None

def GeneratePolygon(x, y):
    vertices = []
    angle = 0.0
    while angle < 2 * pi:
        length = random() * 15 + 5
        angle = min(angle + random() * 0.6 + 0.3, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return Polygon(x, y, vertices)

def Begin():
    global quadtree, polygons
    for i in range(100):
        polygon = PolygonEntity(GeneratePolygon(random() * Screen.Width(), random() * Screen.Height()), Color.light_blue)
        polygons.append(polygon)

def Update():
    global quadtree, polygons

    quadtree = QuadTree(0, 0, Screen.Width(), Screen.Height())
    for polygon in polygons:
        minX = polygon.minX
        minY = polygon.minY
        quadtree.insertObjectWithBoundingBox(polygon, minX, minY, polygon.maxX - minX, polygon.maxY - minY)

    for polygon in polygons:
        minX = polygon.minX
        minY = polygon.minY
        polygonsCollided = quadtree.collidingObjects(minX, minY, polygon.maxX - minX, polygon.maxY - minY)
        polygonsCollided.remove(polygon)
        polygonsCollided = list(filter(lambda x: polygon.collide(x), polygonsCollided))
        if len(polygonsCollided) > 0:
            polygon.color = Color.red

def Render():
    global quadtree, polygons
    quadtree.render()

    size = Point(100, 100)
    position = Screen.MousePosition() - size / 2
    polygonsColliding = quadtree.collidingObjects(position.x, position.y, size.x, size.y)
    polygonsColliding = list(filter(lambda x: x.collideWithRectangle(position.x, position.y, size.x, size.y), polygonsColliding))
    for polygon in polygonsColliding:
        polygon.renderPolygon(Color.yellow, 1)

    Screen.DrawRect(position, size, Color.white, filled=False)

if __name__ == '__main__':
    Screen.StartGame(Begin, Update, Render)

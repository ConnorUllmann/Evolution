from basics import Screen, Softbody, Point, Polygon, PolygonEntity, Color
import pygame, random
from math import pi


def PreGame():
    pygame.display.set_caption("Softbody Test")

mouseClickPosition = None
softbodies = []
def BeginGame():
    global softbodies
    softbodies.append(Softbody(280, 240, [Point(-100, 0), Point(-100, -100), Point(0, -100), Point(100, -100),
                                   Point(25, 0), Point(100, 100), Point(0, 100), Point(-100, 100)]))
    softbodies[0].AddStandardSupportRods()

def CullDeadEntitiesFromList(entities):
    return [entities[i] for i in range(len(entities)) if not entities[i].destroyed]

def GeneratePolygonVertices():
    vertices = []
    angle = 0
    while angle < 2 * pi:
        length = random.random() * 250 + 20
        angle = min(angle + random.random() * 0.1 + 0.05, 2*pi)
        point = Point(length, 0)
        point.radians = angle
        vertices.append(point)
    return vertices

firstFrameTriggered = False
def UpdateGame():
    global firstFrameTriggered, softbodies, mouseClickPosition
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

    softbodies = CullDeadEntitiesFromList(softbodies)

    if Screen.KeyDown(pygame.K_z):
        for softbody in softbodies:
            softbody.rotateDegrees(5)

    if Screen.KeyReleased(pygame.K_x):
        softbody = Softbody(0, Screen.Height(), GeneratePolygonVertices())
        softbody.v = Point(5, -5)
        softbodies.append(softbody)

    if Screen.KeyReleased(pygame.K_c):
        softbody = Softbody(Screen.Width()/2, Screen.Height()/2, GeneratePolygonVertices())
        softbodies.append(softbody)

    if Screen.KeyReleased(pygame.K_d):
        for softbody in softbodies:
            softbody.Destroy()
        softbodies = []

    if Screen.LeftMousePressed():
        mouseClickPosition = Screen.MousePosition()
    if Screen.LeftMouseReleased():
        mouseReleasePosition = Screen.MousePosition()
        softbodiesTemp = []
        for softbody in softbodies:
            softbodiesTemp.extend(softbody.splitOnce(mouseClickPosition, mouseReleasePosition))
        for softbody in softbodies:
            if softbody not in softbodiesTemp:
                softbody.Destroy()
        softbodies = softbodiesTemp

        # softbodies = []
        # for softbody in softbodiesTemp:
        #     if not softbody.contains(Point(280, 240)):
        #         softbody.Destroy()
        #
        #     if not softbody.destroyed:
        #         print("Rods: {}".format(len(softbody.rods)))
        #         print("RodsSupport: {}".format(len(softbody.rodsSupport)))
        #         softbodies.append(softbody)
        # print("Softbodies: {}".format(len(softbodies)))

        mouseClickPosition = None

def RenderGame():
    global mouseClickPosition
    if mouseClickPosition is not None:
        Screen.DrawLine(mouseClickPosition, Screen.MousePosition())
    # points = [Point(322.26804123711355, 217.7319587628865),
    #     Point(322.26804123711355, 217.7319587628865),
    #     Point(322.5000000000001, 240.0),
    #     Point(322.5000000000001, 240.0),
    #     Point(322.73684210526324, 262.73684210526324),
    #     Point(322.73684210526324, 262.73684210526324)]
    # for point in points:
    #     Screen.DrawCircle(point, 5, Color.light_grey)
    # Screen.DrawCircle(Point(321.4583333333334, 140.0), 6, Color.green)
    # Screen.DrawCircle(Point(323.5416666666667, 340.0), 6, Color.green)


def StartGame():
    Screen(640, 480)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()
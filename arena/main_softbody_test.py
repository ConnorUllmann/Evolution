from basics import Screen, Softbody, Point, Polygon, PolygonEntity, Color
import pygame


def PreGame():
    pygame.display.set_caption("Softbody Test")

softbodies = []
def BeginGame():
    global softbodies
    softbodies.append(Softbody(280, 240, [Point(-100, 0), Point(-100, -100), Point(0, -100), Point(100, -100),
                                   Point(25, 0), Point(100, 100), Point(0, 100), Point(-100, 100)]))
    softbodies[0].AddStandardSupportRods()

firstFrameTriggered = False
def UpdateGame():
    global firstFrameTriggered, softbodies
    if not firstFrameTriggered:
        BeginGame()
        firstFrameTriggered = True

    if Screen.KeyDown(pygame.K_z):
        for softbody in softbodies:
            softbody.rotateDegrees(5)

    if Screen.KeyReleased(pygame.K_SPACE):
        softbodiesTemp = []
        for softbody in softbodies:
            softbodiesTemp.extend(softbody.splitOnce(Point(Screen.Width()/2, 0, True), Point(Screen.Width()/2+5, Screen.Height(), True)))
        for softbody in softbodies:
            softbody.Destroy()

        softbodies = []
        for softbody in softbodiesTemp:
            if not softbody.contains(Point(280, 240)):
                softbody.Destroy()

            if not softbody.destroyed:
                print("Rods: {}".format(len(softbody.rods)))
                print("RodsSupport: {}".format(len(softbody.rodsSupport)))
                softbodies.append(softbody)
        print("Softbodies: {}".format(len(softbodies)))

def RenderGame():
    pass
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
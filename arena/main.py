from screen import Screen
from player import Player
from wall import Wall
import pygame, random, math

wallWidth = 32
gap = 30
gapY = 200
screenSpeed = 6
camera = (0, 0)
wallMaxX = 0

def PreGame():
    global player, wallWidth
    pygame.display.set_caption("Helicopter")
    player = Player(200, gapY)
    player.v[0] = screenSpeed
    pass

def UpdateGame():
    global player, camera, wallMaxX, wallWidth, gap, gapY, screenSpeed
    cameraLeftMargin = 200
    newWallMaxX = math.floor((player.x + Screen.Instance.width + wallWidth - cameraLeftMargin) / wallWidth) * wallWidth
    if newWallMaxX > wallMaxX:
        for x in range(wallMaxX, newWallMaxX, wallWidth):
            gapY += random.randint(-30, 30)
            gap += random.randint(-5, 5)

            gap = max(min(gap, 80), 40)
            gapY = max(min(gapY, Screen.Instance.height-gap-10), gap+10)
            
            Wall(x, 0, wallWidth, gapY - gap)
            Wall(x, gapY + gap, wallWidth, Screen.Instance.height - gapY - gap)
            
        wallMaxX = newWallMaxX

    Screen.Instance.camera[0] = player.x - cameraLeftMargin
    Screen.Instance.camera[1] = 0

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
            player.y = gapY
            player.v[1] = 0
    pygame.event.poll()
    
    walls = []
    for wall in Wall.walls:
        walls.append(wall)
    for wall in walls:
        if wall.x - Screen.Instance.camera[0] < -wallWidth:
            wall.Destroy()
    pass

def RenderGame():
    global player, maxX, wallWidth
    pygame.display.set_caption("Helicopter")
    pass
    
def StartGame():
    Screen(800, 400)
    PreGame()
    Screen.Instance.AddUpdateFunction("main", UpdateGame)
    Screen.Instance.AddRenderFunction("main", RenderGame)
    Screen.Start()

if __name__ == '__main__':
    StartGame()

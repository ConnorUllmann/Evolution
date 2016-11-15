import pygame
import tkinter as tk
from tkinter import *
import os, platform, random

def RandomColor():
    return (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
def RandomLightColor():
    return (random.randrange(100, 256), random.randrange(100, 256), random.randrange(100, 256))

class Datum:
    Colors = [(255, 255, 255),
              (64, 255, 64),
              (64, 64, 255),
              (255, 64, 64),
              (255, 64, 255),
              (64, 255, 255),
              (255, 255, 64)]
    TagToColor = {} #Dictionary of all tags which contains a dictionary of all tag values and the color they correspond to
    TagToValues = {} #Dictionary of all tags and the unique values for each
    
    def __init__(self, x, y, metric, tags):
        self.x = x
        self.y = y
        self.metric = metric
        self.tags = {}
        for tag in tags:
            tagList = tag.split(":")
            key = tagList[0].lower()
            value = tagList[1].lower()
            self.tags[key] = value
            if not key in Datum.TagToColor:
                Datum.TagToValues[key] = []
                Datum.TagToColor[key] = {}
            if not value in Datum.TagToColor[key]:
                Datum.TagToValues[key].append(value)
                if len(Datum.Colors) > 0:
                    Datum.TagToColor[key][value] = Datum.Colors.pop()
                else:
                    Datum.TagToColor[key][value] = RandomLightColor()

class Graph:
    Instance = None

    @staticmethod
    def AddDatumToSingleton(x, y, metric, tags):
        Graph.Instance.AddDatum(x, y, metric, tags)

    def AddDatum(self, x, y, metric, tags):
        datum = Datum(x, y, metric, tags)
        self.data.append(datum)
        #self.DrawData()

    def Frame(self):
        return Frame(self.root, width=self.width, height=self.height)

    def grid(self, *args, **kwargs):
        self.embed.grid(*args, **kwargs)

    def ClearScreen(self):
        self.screen.fill(pygame.Color(80,80,80))

    def __init__(self, root, width, height):
        Graph.Instance = self
        self.UpdateTagOptionsFunction = None
        self.TagToSplitOn = None
        self.root = root
        self.width = width
        self.height = height
        self.widthMargin = 20
        self.heightMargin = 20
        self.widthInner = width - self.widthMargin * 2
        self.heightInner = height - self.heightMargin * 2

        self.minX = None
        self.maxX = None
        self.minY = None
        self.maxY = None
        
        self.data = []
              
        self.embed = self.Frame()
        self.PyGameInit()

    def PyGameInit(self):
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.set_alpha(None)
        self.ClearScreen()
        pygame.init()
        pygame.display.init()
        pygame.display.update()

        #self.root.after(0,pygame.display.update)
        #self.root.after(0, self.DrawData)

    def xDraw(self, xValue):
        if self.minX is None or self.maxX is None or self.minX == self.maxX:
            return None
        return int((xValue - self.minX) / (self.maxX - self.minX) * self.widthInner + self.widthMargin)
    def yDraw(self, yValue):
        if self.minY is None or self.maxY is None or self.minY == self.maxY:
            return None
        return int(self.height - ((yValue - self.minY) / (self.maxY - self.minY) * self.heightInner + self.heightMargin))
    def xValue(self, xDraw):
        if self.minX is None or self.maxX is None or self.minX == self.maxX:
            return None
        return (xDraw - self.widthMargin) / self.widthInner * (self.maxX - self.minX) + self.minX
    def yValue(self, yDraw):
        if self.minY is None or self.maxY is None or self.minY == self.maxY:
            return None
        return ((self.height - yDraw) - self.heightMargin) / self.heightInner * (self.maxY - self.minY) + self.minY

    def SetTagOptions(self, tags):
        if self.UpdateTagOptionsFunction is not None:
            self.UpdateTagOptionsFunction(tags)

    def DrawData(self):
        metric = "statemanager.loadtest_request_success_rate"
        dataInMetric = list(filter(lambda x: x.metric != metric, self.data))

        #print("LEN: {0} {1}".format(len(self.data), len(dataInMetric)))

        tagToSplitOn = self.TagToSplitOn() if self.TagToSplitOn is not None else ""

        countByTagValue = {}
        batchCount = {}
        currentCount = {}
        currentX = {}
        currentY = {}
        averagePoints = {}

        tags = []
        for datum in dataInMetric:
            for tag in datum.tags:
                if tag not in tags:
                    tags.append(tag)

            if tagToSplitOn in datum.tags:            
                tagValue = datum.tags[tagToSplitOn]
                if not tagValue in countByTagValue:
                    countByTagValue[tagValue] = 0
                countByTagValue[tagValue] += 1

        self.SetTagOptions(tags)
        
        for tagValue in countByTagValue:
            batchCount[tagValue] = max(int(countByTagValue[tagValue] / 50)+1,1)
            currentCount[tagValue] = 0
            currentX[tagValue] = 0
            currentY[tagValue] = 0
            averagePoints[tagValue] = []
            
        for datum in dataInMetric:
            if self.minX is None or datum.x < self.minX:
                self.minX = datum.x
            if self.maxX is None or datum.x > self.maxX:
                self.maxX = datum.x
            if self.minY is None or datum.y < self.minY:
                self.minY = min(0, datum.y)
            if self.maxY is None or datum.y > self.maxY:
                self.maxY = datum.y

            if tagToSplitOn in datum.tags:  
                tagValue = datum.tags[tagToSplitOn]
                currentX[tagValue] += datum.x
                currentY[tagValue] += datum.y
                currentCount[tagValue] += 1
                if currentCount[tagValue] >= batchCount[tagValue]:
                    averagePoints[tagValue].append((currentX[tagValue] / currentCount[tagValue], currentY[tagValue] / currentCount[tagValue]))
                    currentCount[tagValue] = 0
                    currentX[tagValue] = 0
                    currentY[tagValue] = 0

        #Make an average for the last point
        for tagValue in currentCount:
            if currentCount[tagValue] >= batchCount[tagValue]:
                averagePoints[tagValue].append((currentX[tagValue] / currentCount[tagValue], currentY[tagValue] / currentCount[tagValue]))

        if self.minX == self.maxX or self.minY == self.maxY:
            return
        #print("x:({0}, {1}) y:({2}, {3})".format(self.minX, self.maxX, self.minY, self.maxY))

        mousePosDraw = self.MousePosition()
        mousePosValue = (self.xValue(mousePosDraw[0]), self.yValue(mousePosDraw[1]))

        closestDatum = None
##        closestDistance2 = None
##        for datum in dataInMetric:
##            distance2 = (mousePosValue[0] - datum.x)**2 + (mousePosValue[1] - datum.y)**2
##            if closestDistance2 is None or distance2 < closestDistance2:                
##                closestDatum = datum
##                closestDistance2 = distance2
##        
##        mousePosConvert = (self.xDraw(mousePosValue[0]), self.yDraw(mousePosValue[1]))
##        print("start:({0}, {1}) end:({2}, {3})".format(mousePosDraw[0], mousePosDraw[1], mousePosConvert[0], mousePosConvert[1]))


        self.ClearScreen()

        gridlinesCount = 4
        gridlinesInterval = (self.maxY - self.minY) / gridlinesCount
        for i in range(0, gridlinesCount):
            self.DrawLine((self.xDraw(self.minX), self.yDraw(self.minY + gridlinesInterval * (i+1))),
                          (self.xDraw(self.maxX), self.yDraw(self.minY + gridlinesInterval * (i+1))),
                          (100, 100, 100))
        
        self.DrawLines([(self.xDraw(self.minX), self.yDraw(self.maxY)),
                       (self.xDraw(self.minX), self.yDraw(0)),
                       (self.xDraw(self.maxX), self.yDraw(0)),
                       (self.xDraw(self.minX), self.yDraw(0)),
                       (self.xDraw(self.minX), self.yDraw(self.minY))], (0, 0, 0))

        for datum in dataInMetric:
            if tagToSplitOn in datum.tags and tagToSplitOn in Datum.TagToColor:
                tagValue = datum.tags[tagToSplitOn]
                position = (self.xDraw(datum.x), self.yDraw(datum.y))
                color = Datum.TagToColor[tagToSplitOn][tagValue]
                if datum == closestDatum:
                    self.DrawCircle(position, 5, color)
                else:
                    self.DrawPoint(position, color)            

        for tagValue in countByTagValue:
            if len(averagePoints[tagValue]) > 1:
                points = []
                for point in averagePoints[tagValue]:
                    points.append((self.xDraw(point[0]), self.yDraw(point[1])))
                if tagToSplitOn in Datum.TagToColor:
                    self.DrawLines(points, Datum.TagToColor[tagToSplitOn][tagValue])
            #TODO draw tag values and their color

        self.DrawText("{0}s".format(int(self.maxY*100)/100), (self.xDraw(self.minX) -15, self.yDraw(self.maxY) - 15))
        self.DrawText("{0}s".format(int((self.maxX - self.minX)*100)/100), (self.xDraw(self.maxX) - 30, self.yDraw(self.minY) - 15))
        
        pygame.display.update()
        
    def DrawLines(self, positions, color=(255, 255, 255), thickness=1):
        pygame.draw.lines(self.screen, color, False, positions, thickness)

    def DrawLine(self, positionStart=(0,0), positionEnd=(0,0), color=(255,255,255), thickness=1):
        pygame.draw.line(self.screen, color, positionStart, positionEnd, thickness)
        
    def DrawCircle(self, position=(0,0), radius=1, color=(255,255,255), thickness=0):
        pygame.draw.circle(self.screen, color, position, radius, thickness)

    def DrawPoint(self, position=(0,0), color=(255,255,255)):
        self.screen.set_at(position, color)

    def DrawText(self, text, position=(0,0), color=(255,255,255), fontSize=12):
        font = pygame.font.SysFont("monospace", fontSize)
        textRendered = font.render(text, 1, color)
        self.screen.blit(textRendered, position)

    def MousePosition(self):
        return pygame.mouse.get_pos()
    
#g = Graph(Tk(), 400, 300)
#g.grid(row=0, column=1)

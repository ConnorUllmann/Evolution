
from thread_manager import ThreadManager
from graph import Graph
import tkinter as tk
from tkinter import *
import time
from time import sleep
import random
import os

def Loop(secondsBetweenRuns, function, totalTime=None):
    startTime = time.time()
    currentTime = -1
    while totalTime is None or currentTime - startTime <= totalTime:
        while time.time() - currentTime < secondsBetweenRuns: 
            continue
        currentTime = time.time()
        function()

def Activate(button):
    button['state'] = "normal"
def Deactivate(button):
    button['state'] = "disabled"

class Application(Frame):

    def ActivateMenuButtons(self):
        for menuButton in self.menuButtons:
            menuButton['bg'] = root.cget("background")
            Activate(menuButton)
    def DeactivateMenuButtons(self):
        for menuButton in self.menuButtons:
            Deactivate(menuButton)

    def Update(self):
        #self.graph.AddDatum(random.randrange(0, 600), random.randrange(0, 80000), ["whoa:no"])
        self.graph.DrawData()
        self.after(100, self.Update)

    def SpinOffThread(self, function):
        thread = self.threadManager.Add(function)
        self.threadManager.Run([thread])
        return thread

    def MenuButtonCallbackWrapper(self, function, button):
        def _temp():
            self.DeactivateMenuButtons()
            button['bg'] = '#cfc'
            function()
            self.ActivateMenuButtons()
        return lambda: self.SpinOffThread(_temp)

    def UpdateTagOptions(self, options):
        mustUpdate = False
        if len(self.options) != len(options):
            mustUpdate = True
        else:
            for option in options:
                if option not in self.options:
                    mustUpdate = True

        if not mustUpdate:
            return

        self.options = options
        if len(self.options) > 0:
            Activate(self.tagOptionMenu)
            Activate(self.tagLabel)
        
        oldSelection = self.tagSelection.get()
        self.tagSelection.set('')
        self.tagOptionMenu['menu'].delete(0, 'end')

        for option in options:
            self.tagOptionMenu['menu'].add_command(label=option, command=tk._setit(self.tagSelection, option))

        if oldSelection in options:
            self.tagSelection.set(oldSelection)
        else:
            self.tagSelection.set(options[0] if len(options) > 0 else "")

    def TagToSplitOn(self):
        return self.tagSelection.get()
        
    def Menu(self):
        self.threadManager = ThreadManager()
        
        self.menuButtons = []
        self.info = TestInfo()
        #self.info.append(["WHOA", lambda: Loop(0.1, lambda:self.graph.AddDatum(
        #    random.randrange(0, 600),
        #    random.randrange(0, 80000),
        #    "metric",
        #    ["type:{0}".format("ui-TEST" if random.random() < 0.5 else "backend-TEST"), "endpoint:/hi/"]), 3)])
        for i in range(0, len(self.info)):
            info = self.info[i]
            title = info[0]
            button = Button(self, text=title)
            callback = self.MenuButtonCallbackWrapper(info[1], button)
            button['command'] = callback
            button.grid(row=i, column=0, ipadx=2, ipady=2, padx=3, pady=(3, 20 if i == len(self.info)-1 else 3), columnspan=3, sticky='WE')
            self.menuButtons.append(button)

        rowIndex = len(self.menuButtons)
        
        self.tagLabel = Label(self, text="Tag:")
        self.tagLabel.grid(row=rowIndex, column=0, sticky='E')
        self.tagSelection = StringVar(self)
        self.tagOptionMenu = OptionMenu(self, self.tagSelection, "")
        self.tagOptionMenu.grid(row=rowIndex, column=1, columnspan=2, sticky='WE')
        Deactivate(self.tagOptionMenu)
        Deactivate(self.tagLabel)
        
        
        self.Update()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.options = []
        self.grid(row=0, column=0)
        self.graph = Graph(master, 600, 400)
        self.graph.UpdateTagOptionsFunction = self.UpdateTagOptions
        self.graph.TagToSplitOn = self.TagToSplitOn
        self.graph.grid(row=0, column=3)
        self.Menu()
        
root = Tk()

app = Application(master=root)
app.mainloop()
root.destroy()

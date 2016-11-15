import tkinter as tk
from tkinter import *
from screen import Screen
from body import Body

class Application(Frame):

    def Start(self):
        body = Body()

    def MenuStart(self):
        startButton = tk.Button(self, text="Start", command=self.Start)
        startButton.grid(row=0, column=0)

    def UpdateGame(self):
        pass

    def RenderGame(self):
        pass

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(row=0, column=0, padx=10, pady=10)
        self.screen = Screen(master, 600, 400)
        #self.screen.grid(row=1, column=0)
        Screen.Instance.AddUpdateFunction("main", self.UpdateGame)
        Screen.Instance.AddRenderFunction("main", self.RenderGame)
        Screen.Start()
        self.MenuStart()

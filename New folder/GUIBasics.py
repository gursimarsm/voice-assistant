import tkinter as tk
import pva
from tkinter import *
from tkinter import messagebox



class Window(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        master.title("Personal Assistant")
        A = Label(master, text="Here to help you! (Say 'goodbye' to stop or close the window)")
        A.pack(side="top")
        Button(master, text="Tap to start!", width=100, relief="groove",command=self.Processo_r).pack(side="bottom")
    def Processo_r(self):
        pva.MainClass()


root = Tk()
#instance of the class
app = Window(root)
root.geometry("500x100")
#Runs the application until we close
root.mainloop()



import matplotlib
import os
import math
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import warnings


def select(option):
    root.destroy()
    exec(open(option).read())


root = tk.Tk()
root.title('Register and resampling')
root.geometry('250x180+50+50')
lbl = ttk.Label(root, text="Choose an option below:")
lbl.place(x=50, y=30)
B1 = ttk.Button(root, text='Register', command=lambda: select('Automatic_Registration.py'))
B1.place(x=75, y=60)
B2 = ttk.Button(root, text='Resampling', command=lambda: select('Automatic_Resampling.py'))
B2.place(x=65, y=100)

root.mainloop()

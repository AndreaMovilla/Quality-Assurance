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
root.title('Image Quality Assurance')
root.geometry('300x200+50+50')
lbl = ttk.Label(root, text="Choose type of analysis:")
lbl.place(x=80, y=40)
B1 = ttk.Button(root, text='Volume', command=lambda: select('QA_Volumes.py'))
B1.place(x=100, y=80)
B2 = ttk.Button(root, text='Activity', command=lambda: select('QA_Activity.py'))
B2.place(x=100, y=110)
B3 = ttk.Button(root, text='Resolution', command=lambda: select('QA_Resolution.py'))
B3.place(x=95, y=140)
root.mainloop()
# window.geometry("300x200+10+20")
# window.mainloop()
# analysis_type = input('Write type of QA: volume, activity or resolution ')

# if analysis_type == 'volume':
#    exec(open("QA_Volumes.py").read())
# elif analysis_type == 'activity':
#    exec(open("QA_Activity.py").read())
# elif analysis_type == 'resolution':
#    exec(open("QA_Resolution.py").read())
# else:
#    print('Incorrect input')
#

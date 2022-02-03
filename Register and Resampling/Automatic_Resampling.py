import os
import tkinter as tk
from tkinter import filedialog
import nrrd

master = tk.Tk()


class Path:
    def __init__(self):
        self.selected_directory = "None"
        self.folder_path = tk.StringVar()

    def browse_button(self):
        self.selected_directory = filedialog.askdirectory()
        self.folder_path.set(self.selected_directory)


analysis = Path()
reference = Path()

def mycode():
    import QA_functions as QA_functions
    import ARR_functions as ARR_functions

    root = tk.Tk()
    root.withdraw()
    #  Import data
    global analysis, reference, master




    root = tk.Tk()
    root.withdraw()

    path_fixed_image = reference.selected_directory  # path to reference registered image
    path_segmentations_folder = analysis.selected_directory  # path to segmentations we want to resample
    paths_segmentations = QA_functions.directories(path_segmentations_folder)
    names_segmentations = QA_functions.names(path_segmentations_folder)
    #  Create output folder and change directories
    d = os.path.dirname('Automatic_Resampling.py')  # directory of script
    p = r'Output_Resampling'.format(d)
    try:
        os.makedirs(p)
    except OSError:
        pass

    for i in range(0, len(paths_segmentations)):
        ARR_functions.resampling(path_fixed_image, paths_segmentations[i], p, names_segmentations[i])

master.title('Automatic Resampling')
tk.Label(master, text="Reference image").grid(row=0)
tk.Label(master, text="Segmentation folder").grid(row=1)

e1 = tk.Button(master, text="Select reference image", command=reference.browse_button)
lbl1 = tk.Label(master, textvariable=reference.folder_path)
lbl1.grid(row=0, column=2)
e2 = tk.Button(master, text="Select segmentation folder", command=analysis.browse_button)
lbl2 = tk.Label(master, textvariable=analysis.folder_path)
lbl2.grid(row=1, column=2)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)


tk.Button(master, text='Quit', command=master.quit).grid(row=6, column=1, sticky=tk.W, pady=4)

tk.mainloop()

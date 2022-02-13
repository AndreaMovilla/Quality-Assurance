import os
import tkinter as tk
from tkinter import filedialog
import nrrd

master = tk.Tk()


class Path:
    def __init__(self):
        self.selected_directory = "None"
        self.folder_path = tk.StringVar()
        self.file_path = tk.StringVar()
        
    def browse_button(self):
        self.selected_directory = filedialog.askdirectory()
        self.folder_path.set(self.selected_directory)
        
    def browse_file(self):
        self.selected_file = filedialog.askopenfilename()
        self.file_path.set(self.selected_file)

analysis = Path()
reference = Path()

def mycode():
    import QA_functions as QA_functions
    import ARR_functions as ARR_functions



    root = tk.Tk()
    root.withdraw()
    #  Import data
    global analysis, reference, master
    master.destroy()
    path_fixed_image = reference.selected_file  # path to fixed image
    path_moving_images_folder = analysis.selected_directory  # images we want to register
    master.destroy()
    paths_moving_images = QA_functions.directories(path_moving_images_folder)
    names_moving_images = QA_functions.names(path_moving_images_folder)
   

    #  Create output folder and change directories
    d = os.path.dirname('Automatic_Registration.py')  # directory of script
    p = r'Output_Registration'.format(d)
    try:
        os.makedirs(p)
    except OSError:
        pass

    for i in range(0, len(paths_moving_images)):
        ARR_functions.register(path_fixed_image, paths_moving_images[i], p, names_moving_images[i])

master.title('Automatic Registration')
tk.Label(master, text="Reference image").grid(row=0)
tk.Label(master, text="Images to register folder").grid(row=1)

e1 = tk.Button(master, text="Select reference image", command=reference.browse_file)
lbl1 = tk.Label(master, textvariable=reference.file_path)
e2 = tk.Button(master, text="Select images to register folder", command=analysis.browse_button)
lbl2 = tk.Label(master, textvariable=analysis.folder_path)

lbl1.grid(row=0, column=2)
lbl2.grid(row=1, column=2)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)


tk.Button(master, text='Rum', command=mycode).grid(row=6, column=1, sticky=tk.W, pady=4)

tk.mainloop()


import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

# Create window
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

    import os
    import QA_functions as QA_functions
    import pandas as pd
    import numpy as np

    #  Import data
    global analysis, reference, e3, e4, e5, e6, master
    main_path = analysis.selected_directory
    main_path_ref = reference.selected_directory
    excelname = e3.get()

    ad_time = [int(e4.get()), int(e5.get())]
    half_life = int(e6.get())
    time = ad_time[0] - ad_time[1]
    master.destroy()
    #  Create output folder and change directories
    d = os.path.dirname('QA_Activity')  # directory of script
    p = r'Output_QA_Activity'.format(d)
    try:
        os.makedirs(p)
    except OSError:
        pass
    os.chdir(p)
    # Importing the images
    segref = QA_functions.importnrrd(os.path.join(main_path_ref, 'Reference_segmentations'))
    segref_names = QA_functions.names(os.path.join(main_path_ref, 'Reference_segmentations'))
    imageref = QA_functions.importnrrd(os.path.join(main_path_ref, 'PET'))[0]

    seg = QA_functions.importnrrd(os.path.join(main_path, 'Reference_segmentations'))
    seg_names = QA_functions.names(os.path.join(main_path, 'Reference_segmentations'))
    images = QA_functions.importnrrd(os.path.join(main_path, 'PET'))
    images_names = QA_functions.names(os.path.join(main_path, 'PET'))

    # Segmentation for both types of images
    segmentations_ref_bool = []
    for i in range(0, len(segref)):
        segmentations_ref_bool.append(segref[i].astype('bool'))

    segmentations_bool = []
    for i in range(0, len(seg)):
        segmentations_bool.append(seg[i].astype('bool'))

    # Intensity for each segmentation in the reference image
    intensities_ref = []
    std_intensities_ref = []
    dic_ref = {'Names': segref_names}
    # dic_ref_std = {'Names': segref_names}

    for i in range(0, len(segref)):
        segmented_image_ref = np.copy(imageref)
        segmented_image_ref[~segmentations_ref_bool[i]] = np.nan
        intensity_ref = round(int(np.nanmean(segmented_image_ref)), 2)
        std_int_ref = round(int(np.nanstd(segmented_image_ref)), 2)
        intensities_ref.append(intensity_ref)
        std_intensities_ref.append(std_int_ref)
    dic_ref['Activity concentration (Bq per ml)'] = intensities_ref
    dic_ref['STD activity concentration (Bq per ml)'] = std_intensities_ref

    # We carry out all segmentations in the images for one study. We obtain the RC
    dic = {'Names': seg_names}
    dicr = {'Names': seg_names}
    dic2 = {'Names': seg_names}
    dic3 = {'Names': seg_names}
    for j in range(0, len(images)):
        RCtotal = []
        # RC_uncertainty_total = []
        intensity_total = []
        std_intensity_total = []
        for i in range(0, len(seg)):
            segmented_image = np.copy(images[j])
            segmented_image[~segmentations_bool[i]] = np.nan
            intensity = round(np.nanmean(segmented_image) * np.exp(-np.log(2) * time / half_life), 2)
            stdintensity = round(np.nanstd(segmented_image) * np.exp(-np.log(2) * time / half_life), 2)

            RC = round(intensity / intensities_ref[i], 2)
            # RC_uncertainty = ((stdintensity/intensities_ref[i])**2 + (intensity*std_intensities_ref[i]/intensities_ref[i]**2)**2)**0.5
            #  RC_uncertainty_total.append(RC_uncertainty)
            RCtotal.append(RC)
            intensity_total.append(intensity)
            std_intensity_total.append(stdintensity)
        dic2[images_names[j]] = intensity_total
        dic3[images_names[j]] = std_intensity_total
        dic[images_names[j]] = RCtotal
        # dicr[pets[j]] = RC_uncertainty_total

    # Saving RC and volumes in .xlsx
    writer = pd.ExcelWriter(excelname)
    dfref = pd.DataFrame(data=dic_ref)
    dfref = dfref.T
    dfref.to_excel(writer, sheet_name="Static activity C")

    df = pd.DataFrame(data=dic)
    df = df.T
    df.to_excel(writer, sheet_name="RC")

    # dfr = pd.DataFrame(data=dicr)
    # dfr = dfr.T
    # dfr.to_excel(writer, sheet_name="STD RC")

    df2 = pd.DataFrame(data=dic2)
    df2 = df2.T
    df2.to_excel(writer, sheet_name="Activity C (Bq per ml)")

    df3 = pd.DataFrame(data=dic3)
    df3 = df3.T
    df3.to_excel(writer, sheet_name="STD activity C (Bq per ml)")
    writer.save()


master.title('QA Activity')
tk.Label(master, text="Reference directory").grid(row=0)
tk.Label(master, text="Analysis directory").grid(row=1)
tk.Label(master, text="Excel name with extension").grid(row=2)
tk.Label(master, text="Static study time (s)").grid(row=3)
tk.Label(master, text="Analysis study time (s)").grid(row=4)
tk.Label(master, text="Half life (s)").grid(row=5)

e1 = tk.Button(master, text="Select reference directory", command=reference.browse_button)
lbl1 = tk.Label(master, textvariable=reference.folder_path)
lbl1.grid(row=0, column=2)

e2 = tk.Button(master, text="Select analysis directory", command=analysis.browse_button)
lbl2 = tk.Label(master, textvariable=analysis.folder_path)
lbl2.grid(row=1, column=2)
e3 = tk.Entry(master)
e4 = tk.Entry(master)
e5 = tk.Entry(master)
e6 = tk.Entry(master)
e3.insert(-1, 'name.xlsx')
e4.insert(-1, '2000')
e5.insert(-1, '2500')
e6.insert(-1, '160')


e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)

tk.Button(master, text='run', command=mycode).grid(row=6, column=1, sticky=tk.W, pady=4)

tk.mainloop()

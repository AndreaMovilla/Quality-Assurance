
import matplotlib
import os
import math
import tkinter as tk
from tkinter import filedialog
import warnings

warnings.filterwarnings('ignore', category=RuntimeWarning)

matplotlib.use('Qt5Agg')
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
    import pandas as pd
    import nrrd

    #  Import data
    global analysis, reference, e3, master
    main_path = analysis.selected_directory
    main_path_ref = reference.selected_directory
    excelname = e3.get()
    master.destroy()
    #  Create output folder and change directories
    d = os.path.dirname('QA_Resolution')  # directory of script
    p = r'Output_QA_Resolution'.format(d)
    try:
        os.makedirs(p)
    except OSError:
        pass
    os.chdir(p)

    # Importing the images
    segref_names = QA_functions.names(os.path.join(main_path_ref, 'Reference_segmentations'))
    segref = QA_functions.importnrrd(os.path.join(main_path_ref, 'Reference_segmentations'))
    headerref = QA_functions.importheader(os.path.join(main_path_ref, 'Reference_segmentations'))
    imageref = QA_functions.importnrrd(os.path.join(main_path_ref, 'PET'))[0]

    seg = QA_functions.importnrrd(os.path.join(main_path, 'Reference_segmentations'))
    header = QA_functions.importheader(os.path.join(main_path, 'Reference_segmentations'))
    images = QA_functions.importnrrd(os.path.join(main_path, 'PET'))
    images_names = QA_functions.names(os.path.join(main_path, 'PET'))

    # Reference segmentations in 3 slices
    segreftotal = []
    for i in range(0, len(segref)):
        segplanesref = QA_functions.repeatseg(segref[i])
        segreftotal.append(segplanesref)

    segrefbool = []
    for i in range(0, len(segreftotal)):
        segrefbool.append(segreftotal[i].astype('bool'))

    # Analysis for reference image
    dicref = {'Names': segref_names}

    contrast_ref_total = []
    std_c_more_40_reftotal = []
    std_c_less_40_reftotal = []
    c_more_40_reftotal = []
    c_less_40_reftotal = []
    ref_rods = []
    seg_holes_ref = []
    segrefvolume = []
    for i in range(0, len(segrefbool)):
        volume = QA_functions.threshold40(segrefbool[i], imageref)
        filename = '40S_' + segref_names[i] + '_ref' + '.nrrd'
        header_sg = headerref[i]
        nrrd.write(filename, volume[0], header_sg, index_order='F')
        segrefvolume.append(volume[0])
        seg_holes_ref.append(volume[0])
        c_more_40 = round(volume[1], 2)
        std_more_40 = round(volume[3], 2)
        c_less_40 = round(volume[2], 2)
        std_less_40 = round(volume[4], 2)
        contrast_ref = round(c_more_40/c_less_40, 2)
        contrast_ref_total.append(contrast_ref)
        c_more_40_reftotal.append(c_more_40)
        std_c_more_40_reftotal.append(std_more_40)
        c_less_40_reftotal.append(c_less_40)
        std_c_less_40_reftotal.append(std_less_40)
        ref_rods.append(volume[5])

    dicref['Static contrast'] = contrast_ref_total
    dicref['Static FDG (Bq per ml)'] = c_more_40_reftotal
    dicref['Static BG (Bq per ml)'] = c_less_40_reftotal
    dicref['Rods per sector'] = ref_rods
    dicref['Static STD FDG (Bq per ml)'] = std_c_more_40_reftotal
    dicref['Static STD BG (Bq per ml)'] = std_c_less_40_reftotal

    # Segmentations in 3 slices
    segtotal = []
    for i in range(0, len(seg)):
        segplanes = QA_functions.repeatseg(seg[i])
        segtotal.append(segplanes)

    segBGbool = []
    for i in range(0, len(segtotal)):
        segBGbool.append(segtotal[i].astype('bool'))

    # contrast, RC and volume  quotient per sector

    dic = {'Names': segref_names}
    dic2 = {'Names': segref_names}
    dicBG = {'Names': segref_names}
    dicstd_BG = {'Names': segref_names}
    dicFDG = {'Names': segref_names}
    dicstd_FDG = {'Names': segref_names}
    dic_volumes_holes = {'Names': segref_names}
    dic_volumes = {'Names': segref_names}

    for j in range(0, len(images)):
        contrast_total = []
        RCtotal = []
        rods_quotient_total = []
        c_more_40_total = []
        c_less_40_total = []
        std_c_more_40_total = []
        std_c_less_40_total = []
        rods = []
        for i in range(0, len(segBGbool)):
            volume = QA_functions.threshold40(segBGbool[i], images[j])
            filename = '40S_' + segref_names[i] + '_' + images_names[j] + '.nrrd'
            header_sg = header[i]
            nrrd.write(filename, volume[0], header_sg, index_order='F')
            c_more_40 = round(volume[1], 2)
            c_less_40 = round(volume[2], 2)
            std_more_40 = round(volume[3], 2)
            std_less_40 = round(volume[4], 2)
                        contrast = round(c_more_40 / c_less_40, 2)
            contrast_total.append(contrast)
            rods.append(round(volume[5], 2))
            rods_quotient = round((volume[5]/ref_rods[i]), 2)
            rods_quotient_total.append(rods_quotient)
            c_more_40_total.append(c_more_40)
            c_less_40_total.append(c_less_40)
            std_c_more_40_total.append(std_more_40)
            std_c_less_40_total.append(std_less_40)
            RC = contrast / contrast_ref_total[i]
            RCtotal.append(RC)
        dic[images_names[j]] = contrast_total
        dic2[images_names[j]] = RCtotal
        dicBG[images_names[j]] = c_less_40_total
        dicstd_BG[images_names[j]] = std_c_less_40_total
        dicFDG[images_names[j]] = c_more_40_total
        dicstd_FDG[images_names[j]] = std_c_more_40_total
        dic_volumes[images_names[j]] = rods_quotient_total
        dic_volumes_holes[images_names[j]] = rods

    # Saving results in xlsx file

    writer = pd.ExcelWriter(excelname, engine='xlsxwriter')

    dfref = pd.DataFrame(data=dicref)
    dfref = dfref.T
    dfref.to_excel(writer, sheet_name="Static")

    df1 = pd.DataFrame(data=dicBG)
    df1 = df1.T
    df1.to_excel(writer, sheet_name="BG concentration (Bq per ml)")

    df2 = pd.DataFrame(data=dicFDG)
    df2 = df2.T
    df2.to_excel(writer, sheet_name="FDG concentration (Bq per ml)")

    df3 = pd.DataFrame(data=dic)
    df3 = df3.T
    df3.to_excel(writer, sheet_name="Contrast")

    df4 = pd.DataFrame(data=dic2)
    df4 = df4.T
    df4.to_excel(writer, sheet_name="Contrast CR")

    df5 = pd.DataFrame(data=dic_volumes)
    df5 = df5.T
    df5.to_excel(writer, sheet_name="Rod RC")

    df8 = pd.DataFrame(data=dic_volumes_holes)
    df8 = df8.T
    df8.to_excel(writer, sheet_name="Rods per sector")

    df6_std = pd.DataFrame(data=dicstd_BG)
    df6_std = df6_std.T
    df6_std.to_excel(writer, sheet_name="BG STD (Bq per ml)")

    df7_std = pd.DataFrame(data=dicstd_FDG)
    df7_std = df7_std.T
    df7_std.to_excel(writer, sheet_name="FDG STD (Bq per ml)")
    writer.save()
    os._exit(os.EX_OK)


#  Create window

master.title('QA Resolution')
tk.Label(master, text="Reference directory").grid(row=0)
tk.Label(master, text="Analysis directory").grid(row=1)
tk.Label(master, text="Excel name with extension").grid(row=2)
e1 = tk.Button(master, text="Select reference directory", command=reference.browse_button)
lbl1 = tk.Label(master, textvariable=reference.folder_path)
lbl1.grid(row=0, column=2)
e2 = tk.Button(master, text="Select analysis directory", command=analysis.browse_button)
lbl2 = tk.Label(master, textvariable=analysis.folder_path)
lbl2.grid(row=1, column=2)
e3 = tk.Entry(master)


e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e3.insert(-1, 'name.xlsx')


tk.Button(master, text='run', command=mycode).grid(row=6, column=1, sticky=tk.W, pady=4)
tk.mainloop()

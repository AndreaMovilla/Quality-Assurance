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
	import pandas as pd

	#  Import data
	global analysis, reference, e3, e4, e5, master
	main_path = analysis.selected_directory
	main_path_ref = reference.selected_directory
	excelname = e3.get()
	voxeldim = e4.get()
	voxeldimref = e5.get()
	master.destroy()
	#  Create output folder and change directories
	d = os.path.dirname('QA_Volume')
	p = r'Output_QA_Activity'.format(d)
	try:
		os.makedirs(p)
	except OSError:
		pass
	os.chdir(p)

	# Importing the images
	segref = QA_functions.importnrrd(os.path.join(main_path_ref, 'Reference_segmentations'))
	headerref = QA_functions.importheader(os.path.join(main_path_ref, 'Reference_segmentations'))
	imageref = QA_functions.importnrrd(os.path.join(main_path_ref, 'PET'))[0]

	seg = QA_functions.importnrrd(os.path.join(main_path, 'Reference_segmentations'))
	seg_names = QA_functions.names(os.path.join(main_path, 'Reference_segmentations'))
	header = QA_functions.importheader(os.path.join(main_path, 'Reference_segmentations'))
	images = QA_functions.importnrrd(os.path.join(main_path, 'PET'))
	images_names = QA_functions.names(os.path.join(main_path, 'PET'))

	#  Volumes from reference image with threshold segmentation
	volumenesref = []

	dicref = {'Names': seg_names}
	for i in range(0, len(segref)):
		volumenref = QA_functions.thresholdseg(segref[i], imageref, voxeldimref)
		filename = 'TS_' + seg_names[i] + '_' + 'static.nrrd'
		detached_header = False
		header_ref = headerref[i]
		nrrd.write(filename, volumenref[1], header_ref, index_order='F')
		volumenesref.append(round(volumenref[0], 2))
	dicref['Static'] = volumenesref

	#  Volume and RC calculation using threshold segmentation. Data stored in dictionaries
	dic = {'Names': seg_names}
	dic2 = {'Names': seg_names}
	for j in range(0, len(images_names)):
		volumenes = []
		RCtotal = []
		for i in range(0, len(seg)):
			volumen = QA_functions.thresholdseg(seg[i], images[j], voxeldim)
			filename = 'TS_' + seg_names[i] + '_' + images_names[j] + '.nrrd'
			detached_header = False
			header_sg = header[i]
			nrrd.write(filename, volumen[1], header_sg, index_order='F')
			RC = round(volumen[0]/volumenesref[i], 2)
			RCtotal.append(RC)
			volumenes.append(round(volumen[0], 2))
		dic[images_names[j]] = volumenes
		dic2[images_names[j]] = RCtotal

	# Saving results in xlsx file
	writer = pd.ExcelWriter(excelname)
	dfref = pd.DataFrame(data=dicref)
	dfref = dfref.T
	dfref.to_excel(writer, sheet_name="Static volume (ml)")

	df1 = pd.DataFrame(data=dic)
	df1 = df1.T
	df1.to_excel(writer, sheet_name="Volumes (ml)")

	df2 = pd.DataFrame(data=dic2)
	df2 = df2.T
	df2.to_excel(writer, sheet_name="CR")
	writer.save()


master.title('QA Volume')
tk.Label(master, text="Reference directory").grid(row=0)
tk.Label(master, text="Analysis directory").grid(row=1)
tk.Label(master, text="Excel name with extension").grid(row=2)
tk.Label(master, text="Static voxel volume (mm^3)").grid(row=3)
tk.Label(master, text="Analysis voxel volume (mm^3)").grid(row=4)

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


e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e3.insert(-1, 'name.xlsx')
e4.insert(-1, '8')
e5.insert(-1, '64')

tk.Button(master, text='Quit', command=master.quit).grid(row=6, column=1, sticky=tk.W, pady=4)

tk.mainloop()

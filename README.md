# Quality-Assurance
Test repository for Quality Assurance

This package was created using Python 3.7 in the integrated development environment PyCharm. It contains 2 folders:

1. ‘Automatic registration and resampling’: Python scripts to perform automatic registration and resampling of several PET images images at once .
	-requirements.txt: file containing all python modules used in the scripts of this folder. 

	-R&R.py: script that runs the type of analysis desired: register or resampling

	-ARR_funtions.py: file containing all the functions used in the scripts of this folder.

	-Automatic_registration.py: Script to perform a basic automatic registration of images contained in a specific 	folder. Given reference fixed image and folder of moving images, it provides registered moving images and the 	transforms used for each one of them.

	-Automatic_resampling.py: Script to perform a basic automatic resampling of segmentations contained in a 	specific folder. Given already registered image and folder of segmentations, it provides resampled 	segmentations.

	To run  ‘Automatic registration and resampling’: Install requirements.txt. Open R&R.py. An emergent window will appear, asking the user to choose between register and resampling. 
	Another emergent window will appear, asking for the directories needed for the type of analysis chosen. An output folder with the registered images or resampled segmentations will 
	appear in the script folder. All images must be in NRRD format.



2. ‘Quantification_Analysis’: Python codes to perform volume, activity concentration and resolution quantification analysis of several PET images at once. 
	-requirements.txt: file containing all python modules used in the scripts of this folder. 
	
	-Quality_Assurance.py: script that runs the type of quantification desired.

	-QA_functions.py: file containing all the functions used in the scripts of this folder.
	
	-QA_Volumes.py: script to perform volume quantification analysis. Given reference segmentations and images of	moving and static studies, it provides volume segmentations obtained with a growing region algorithm. 	Creates and XLSX file with the volumes (in ml) of each segmentation and the recovery coefficient of said 	volumes (RC=Vol_moving/Vol_static).

	-QA_Activity.py: script to perform activity concentration quantification analysis. Given reference segmentations 	and images for moving and static studies, it provides the activity concentration of each segmentation and its 	recovery coefficient (RC=A_moving/A_static)

	-QA_Resolution.py: script to perform resolution quantification analysis. Given one-plane reference segmentations
	 of rod sectors , and images for moving and static studies, it provides the contrast (C) of each sector and the number of rods recovery coefficient  	(RC=Rods_moving/Rods_static)


	Before running, it’s important to organize the directories as follows:

	directory_to_static_image ->  PET (containing static image)
					     	     Reference_segmentations (containing segmentations based on static image)

 
	directory_to_images -> PET (containing images to analyse)
				    	   Reference_segmentations (containing segmentations resampled)


	All images must be in NRRD format.

	To run ‘Quantification_analysis’: Install requirements.txt. Open and run Quantification_Analysis.py. An emergent window will appear. It will ask you to choose the type of analysis desired: volume, activity or 	resolution. Another emergent window will appear, asking for the input needed for the type of quantification chosen. After adding the input click “run”. It will automatically create  in the script directory an output folder with the results obtained.
	

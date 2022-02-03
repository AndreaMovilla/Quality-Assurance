import math
import numpy as np
import nrrd
from os import walk
from os.path import splitext
from os.path import join
from skimage import measure


def importnrrd(path):
	foodir = path
	barlist = list()
	for root, dirs, files in walk(foodir):
		for f in files:
			if splitext(f)[1].lower() == ".nrrd":
				barlist.append(join(root, f))

	imagenes_nrrd = []
	barlist_sorted = sorted(barlist)
	for i in range(0, len(barlist_sorted)):
		imagenes_nrrd.append(nrrd.read(barlist_sorted[i])[0])

	return imagenes_nrrd


def importheader(path):
	foodir = path
	barlist = list()

	for root, dirs, files in walk(foodir):
		for f in files:
			if splitext(f)[1].lower() == ".nrrd":
				barlist.append(join(root, f))

	imagenes_nrrd = []
	barlist_sorted = sorted(barlist)
	for i in range(0, len(barlist_sorted)):
		imagenes_nrrd.append(nrrd.read(barlist_sorted[i], index_order='F')[1])

	return imagenes_nrrd


def directories(path):
	foodir = path
	barlist = list()

	for root, dirs, files in walk(foodir):
		for f in files:
			if splitext(f)[1].lower() == ".nrrd":
				barlist.append(join(root, f))
	barlist_sorted = sorted(barlist)
	return barlist_sorted


def names(path):
	foodir = path
	names = list()
	for root, dirs, files in walk(foodir):
		for f in files:
			if splitext(f)[1].lower() == ".nrrd":
				g = f.replace(".nrrd", "")
				names.append(g)
	names_sorted = sorted(names)
	return names_sorted


def get_nbhd(pt, checked, dims):
	nbhd = []

	if (pt[0] > 0) and not checked[pt[0]-1, pt[1], pt[2]]:
		nbhd.append((pt[0]-1, pt[1], pt[2]))
	if (pt[1] > 0) and not checked[pt[0], pt[1]-1, pt[2]]:
		nbhd.append((pt[0], pt[1]-1, pt[2]))
	if (pt[2] > 0) and not checked[pt[0], pt[1], pt[2]-1]:
		nbhd.append((pt[0], pt[1], pt[2]-1))

	if (pt[0] < dims[0]-1) and not checked[pt[0]+1, pt[1], pt[2]]:
		nbhd.append((pt[0]+1, pt[1], pt[2]))
	if (pt[1] < dims[1]-1) and not checked[pt[0], pt[1]+1, pt[2]]:
		nbhd.append((pt[0], pt[1]+1, pt[2]))
	if (pt[2] < dims[2]-1) and not checked[pt[0], pt[1], pt[2]+1]:
		nbhd.append((pt[0], pt[1], pt[2]+1))

	return nbhd


def grow(img, seed, t, value):
	"""
	img: ndarray, ndim=3
		An image volume.
	seed: tuple, len=3
		Region growing starts from this point.
	t: int
		The image neighborhood radius for the inclusion criteria.
	"""
	seg = np.zeros(img.shape, dtype=np.bool)
	checked = np.zeros_like(seg)

	seg[seed] = True
	checked[seed] = True
	needs_check = get_nbhd(seed, checked, img.shape)

	while len(needs_check) > 0:
		pt = needs_check.pop()

		# Its possible that the point was already checked and was
		# put in the needs_check stack multiple times.
		if checked[pt]: continue

		checked[pt] = True

		# Handle borders.
		imin = max(pt[0] - t, 0)
		imax = min(pt[0] + t, img.shape[0] - 1)
		jmin = max(pt[1] - t, 0)
		jmax = min(pt[1] + t, img.shape[1] - 1)
		kmin = max(pt[2] - t, 0)
		kmax = min(pt[2] + t, img.shape[2] - 1)

		if img[pt] >= value:
			seg[pt] = True
			needs_check += get_nbhd(pt, checked, img.shape)
		else:
			if img[imin:imax + 1, jmin:jmax + 1, kmin:kmax + 1].mean() > value:
				# Include the voxel in the segmentation and
				# add its neighbors to be checked.
				seg[pt] = True
				needs_check += get_nbhd(pt, checked, img.shape)

	imageseg2 = np.copy(img)*0
	imageseg2[seg] = 1
	return imageseg2


def thresholdseg(seg, image, voxeldim):
	segmentbool = seg.astype('bool')
	imageseg = np.copy(image)
	imageseg[~segmentbool] = np.nan
	vmax = np.nanmax(imageseg)

	coord = np.where(imageseg == vmax)
	coordinates = (coord[0][0], coord[1][0], coord[2][0])
	# Mean intensity
	v70 = np.mean(imageseg[imageseg >= 0.7 * vmax])
	v40 = 0.4 * v70
	# Segmentation with seeded region growing
	imageseg3 = grow(image, coordinates, 1, v40)

	# Volume calculation
	numerovoxels = len(imageseg3[imageseg3 == 1])
	volumen = numerovoxels * (voxeldim) / 1000
	return volumen, imageseg3

def nonzero_clusters(a):
	blobs = a == 1
	blobs_labels, num_labels = measure.label(blobs, background=0, return_num=True, connectivity=None)
	return num_labels/3

def threshold40(seg, image):
	segmentbool = seg.astype('bool')
	imageseg = np.copy(image)
	imageseg[~segmentbool] = np.nan
	vmax = np.nanmax(imageseg)
	v40 = vmax*0.4
	# mean intensities
	c_more_40 = np.mean(imageseg[imageseg >= v40])
	if math.isnan(np.mean(imageseg[imageseg <= v40])):
		c_less_40 = 0
	else:
		c_less_40 = np.mean(imageseg[imageseg <= v40])
	std_more_40 = np.nanstd(imageseg[imageseg >= v40])
	std_less_40 = np.nanstd(imageseg[imageseg <= v40])
	# segmentation of voxels with I> 40%I max
	hole_coords = np.where(imageseg <= v40)
	imageseg2 = np.copy(image) * 0
	imageseg2[hole_coords] = 1
	num_clusters = nonzero_clusters(imageseg2)
	return imageseg2, c_more_40, c_less_40, std_more_40, std_less_40, num_clusters


def repeatseg(image):
	image1 = np.roll(image, 6, axis=1)
	image2 = np.roll(image, -6, axis=1)
	finalimage = image+image1+image2
	return finalimage


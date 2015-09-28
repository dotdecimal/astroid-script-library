# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown, Daniel Patenaude
# Date:     09/28/2015
# Desc:     Using an existing DICOM pbs plan, run a dose calculation

import os.path
import sys
from lib import thinknode_worker as thinknode
from lib import dosimetry_worker as dosimetry
from lib import dicom_worker as dicom
from lib import decimal_logging as dl
from lib import rt_types as rt_types
from lib import vtk_worker as vtk
import json

iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

def get_pbs_machine():
	# return '56059bf100c0de90c4a6290f98cf2afe' #MGH
	return '56059baf00c041b883a89631a4a12e2f' #Procure

def dose_to_vtk(dose_id):
	img_data = json.loads(thinknode.get_immutable(iam, 'dicom', dose_id))

	img = rt_types.image_3d()
	img.from_json(img_data)
	img2 = img.expand_data()

	vtk.write_vtk_image3('dose_pbs.vtk', img2)

def run():
	study_id = dicom.make_rt_study_from_dir(iam, 'F:/Datasets/p.d/Proton/ProCure-PBS/prostate')
	# study_id = '560596110100e6ecd3c01d49ac9b0fe4' #Procure Prostate

	study_calc = \
		thinknode.function(iam["account_name"], 'dicom', "merge_ct_image_slices",
			[
				thinknode.reference(study_id)
			])
	study_id = thinknode.do_calculation(iam, study_calc, False)

	beam_index = 0
	pbs_machine = get_pbs_machine()
	beam_id = dicom.get_beam_from_study(iam, study_id, beam_index)
	spots = dicom.get_spots_from_beam(iam, beam_id)

	# Dose calc data
	fluences = dicom.get_fluences_from_beam(iam, beam_id)
	stopping_img = dicom.get_stopping_power_img(iam, study_id)
	dose_grid = dosimetry.get_dose_grid(iam, stopping_img, 16.0)
	beam_geometry = dicom.get_beam_geometry(iam, study_id, beam_index)
	bixel_grid = dosimetry.get_pbs_bixel_grid(iam, spots, 2.0)
	layers = dicom.get_pbs_layers(iam, pbs_machine, spots, beam_id)

	calc = \
		thinknode.function(iam["account_name"], "dosimetry", "compute_pbs_pb_dose_to_grid",
			[
				thinknode.reference(fluences),
				thinknode.reference(stopping_img),
				thinknode.reference(dose_grid),
				thinknode.reference(beam_geometry),
				thinknode.reference(bixel_grid),
				thinknode.reference(layers),
				thinknode.none,
				thinknode.value([])
			])

	# dl.debug('Dose Calc Command: ' + calc)

	# Perform pbs dose calculation request
	res = thinknode.do_calculation(iam, calc, False)
	# Write dose results to vtk image for viewing in Paraview
	dose_to_vtk(res)	
	dl.event("Done!")	

# Work is performed from here:
run()
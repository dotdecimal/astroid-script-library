# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown, Daniel Patenaude
# Date:     09/28/2015
# Desc:     Post folder to thinknode, get dicom_patient and compute dose


import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import dosimetry_worker as dosimetry
import decimal_logging as dl
import dicom_worker as dicom
import rt_types as rt_types
import vtk_worker as vtk
import json

iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

def dose_to_vtk(dose_id):
	img_data = json.loads(thinknode.get_immutable(iam, 'dicom', dose_id))

	img = rt_types.image_3d()
	img.from_json(img_data)
	img2 = img.expand_data()

	vtk.write_vtk_image3('ct_set.vtk', img2)

def run():
	study_id = dicom.make_rt_study_from_dir(iam, 'F:/Datasets/p.d/Proton/XXX')

	study_calc = \
		thinknode.function(iam["account_name"], 'dicom', "merge_ct_image_slices",
			[
				thinknode.reference(study_id)
			])
	study_id = thinknode.do_calculation(iam, study_calc, False)
	dl.debug("study_id: " + study_id)

	beam_index = 0

	# Dose calc data
	stopping_img = dicom.get_stopping_power_img(iam, study_id)
	dose_grid = dosimetry.get_dose_grid(iam, stopping_img, 8.0)
	beam_geometry = dicom.get_beam_geometry(iam, study_id, beam_index)
	bixel_grid = dosimetry.get_grid_on_image_2d(iam, stopping_img, 2)

	beam_id = dicom.get_beam_from_study(iam, study_id, beam_index)
	sad = dicom.get_sad(iam, beam_id)

	calc = thinknode.function(iam["account_name"], "dosimetry", "compute_sobp_pb_dose_to_grid2",
        [
			thinknode.reference(stopping_img),
			thinknode.reference(dose_grid),
			thinknode.reference(beam_geometry),
			thinknode.reference(bixel_grid),         
            dosimetry.make_sobp_layers(iam, sad[0], 120, 100), # got sad from DICOM, range and mod from energy and lookup 
            thinknode.reference(dicom.get_aperture_from_beam(iam, study_id, beam_index)), 
            thinknode.value([]) # degraders
        ])

	# dl.debug('Dose Calc Command: ' + calc)

	# Perform pbs dose calculation request
	res = thinknode.do_calculation(iam, calc, False)
	# Write dose results to vtk image for viewing in Paraview
	dose_to_vtk(res)
	dl.event("Done!")	

# Work is performed from here:
run()
# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown, Daniel Patenaude
# Date:     09/28/2015
# Desc:     Using an existing DICOM pbs plan, run a dose calculation


import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import dosimetry_worker as dosimetry
import dicom_worker as dicom
import decimal_logging as dl
import rt_types as rt_types
import vtk_worker as vtk
import thinknode_id as tn_id


iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))


def dose_to_vtk(dose_id):
    img_data = thinknode.get_immutable(iam, 'dicom', dose_id, False)

    img = rt_types.image_3d()
    img.from_json(img_data)
    img2 = img.expand_data()

    vtk.write_vtk_image3('dose_pbs.vtk', img2)

def run():
    study_id = dicom.make_rt_study_from_dir(iam, 'C:/Users/abrown/data/proton/prostate')

    study_calc = \
        thinknode.function(iam["account_name"], 'dicom', "merge_ct_image_slices",
            [
                thinknode.reference(study_id)
            ])
    study_id = thinknode.post_calculation(iam, study_calc)
    # study_id = tn_id.prostate_patient_study()

    beam_index = 0
    pbs_machine = tn_id.pbs_machine_procure()
    beam_id = dicom.get_beam_from_study(iam, study_id, beam_index)
    spots = dicom.get_spots_from_beam(iam, beam_id)

    # Dose calc data
    fluences = dicom.get_fluences_from_beam(iam, beam_id)
    fluences_res = thinknode.get_immutable(iam, 'dosimetry', fluences)

    fluences_res2 = []
    for f in fluences_res:
        fluences_res2.append(1.0)

    print("fluences: " + fluences)
    stopping_img = dicom.get_stopping_power_img(iam, study_id)
    dose_grid = dosimetry.get_dose_grid(iam, stopping_img, 4.0)
    beam_geometry = dicom.get_beam_geometry(iam, study_id, beam_index)
    bixel_grid = dosimetry.get_pbs_bixel_grid(iam, spots, 2.0)
    layers = dicom.get_pbs_layers(iam, pbs_machine, spots, beam_id)

	# MAKE A LAYER WITH A SINGLE SPOT AT A SINGLE ENGY (IN A LOOP FOR EVERY SPOT)
	# Call create_pbs_layers_from_spots for every spot and do the dose calc with that layer
	#	As you read a spot from pydicom you'll have the spot and the fluence
	# Push the dose calc up as a thinknode array request
	# Loop over the index of each array request (image3) and write this to DICOM

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

    # dl.debug('Dose Calc Command: ' + str(calc))

    # Perform pbs dose calculation request
    res = thinknode.do_calculation(iam, calc, False)
    # Write dose results to vtk image for viewing in Paraview
    dose_to_vtk(res)    
    dl.event("Done!")    

# Work is performed from here:
run()
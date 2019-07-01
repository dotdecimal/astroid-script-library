# Copyright (c) 2019 .decimal, LLC. All rights reserved.
# Author:   Daniel Patenaude
# Date:     6/11/2019
# Desc:     Extract the PBS spots to individual DICOM doses for a proton plan file

import os.path
import sys, json
import pydicom as dicom
sys.path.append("lib")
import thinknode_worker as thinknode
import dicom_worker as dicom_worker
import dosimetry_worker as dosimetry
import rt_types as rt
import vtk_worker as vtk

dicom_dataset_path = 'C:/Users/Dabo/Documentation/Data/Gamma/ProCure/NJ-Aperture'
pbs_machine_file = "C:/Users/Dabo/Documentation/Software/Astroid/demo-data/nj_pbs_machine.json"

# Get Identify Access Management configuration
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

# Get each of the DICOM files from the patient directory
dicom_file_list = {}
ct_count = 0
dose_count = 0
for dirname, dirnames, filenames in os.walk(dicom_dataset_path):
    for filename in filenames:
        if dicom_worker.valid_dicom_filetype(filename):
            file = os.path.join(dirname, filename)
            ds = dicom.dcmread(file)
            modality = ds.Modality
            # Store each DICOM file to a dictionary so we can access it later. Note: This may be wasteful of system
            # memory so it may need to be revisited
            if modality == 'CT':
                dicom_file_list["CT_" + str(ct_count)] = ds
                ct_count = ct_count + 1
            if modality == 'RTSTRUCT':
                dicom_file_list["RTSTRUCT"] = ds
            if modality == 'RTPLAN':
                dicom_file_list["RTPLAN"] = ds
            if modality == 'RTDOSE':
                dicom_file_list["RTDOSE_" + str(ct_count)] = ds
                dose_count = dose_count + 1

if not 'RTPLAN' in dicom_file_list:
    print('Missing RT ION PLAN from dataset')
    sys.exit()
if not 'RTSTRUCT' in dicom_file_list:
    print('Missing RT STRUCTURE SET from dataset')
    sys.exit()

# Get the pbs machine spec
with open(pbs_machine_file) as machine_data_file:
    pbs_machine_data = json.load(machine_data_file)
pbs_machine_id = json.loads(thinknode.post_immutable_named(iam, "dosimetry", pbs_machine_data, "pbs_machine_spec", False).text)['id']

# study_id = dicom_worker.make_rt_study_from_dir(iam, dicom_dataset_path)
study_id = '5d19f9410100ef78626643e4f4bf59d6'

study_calc = \
    thinknode.function(iam["account_name"], 'dicom', "merge_ct_image_slices",
        [
            thinknode.reference(study_id)
        ])
study_id = thinknode.post_calculation(iam, study_calc)

hu_rsp_curve = \
{
    "scanner_name": "Scanner1",
    "scan_energy": 120.0,
    "fov_range": {
        "max": 1000.0,
        "min": 0.0
    },
    "samples": [[-1000.0, 0.001], [-706.0, 0.311], [-96.0, 0.930], [0.0, 1.0],
                [6.0, 1.027], [30.0, 1.028], [44.0, 1.043], [56.0, 1.051],
                [64.0, 1.059], [198.0, 1.098], [872.0, 1.422], [1744.0, 2.844]]
}

stopping_img = dicom_worker.get_stopping_power_img(iam, study_id, hu_rsp_curve)
dose_grid = dosimetry.get_dose_grid(iam, stopping_img, 2.0)

study = thinknode.get_immutable(iam, 'dosimetry', study_id, True)

# # Get the patient structure and compute the dose grid on that bounding box
# structure_set_result = study["structure_set"]
# patient_structure = 0
# for structure in structure_set_result["structures"]["structure_list"]:
#     print(structure["roi_type"])
#     # if (structure["roi_type"] == "EXTERNAL")
# sys.exit()

ion_plan_result = study["plan"]
rt_ion_plan = rt.rt_ion_plan()
rt_ion_plan.from_json(ion_plan_result)
beam_index = 1
for b in rt_ion_plan.beams:
    ion_beam = rt.rt_ion_beam()
    ion_beam.from_json(b)
    dose_calc_ids = []
    for c in ion_beam.control_points:
        control_point = rt.rt_control_point()
        control_point.from_json(c)

        # get the list of spot_placements so we can later compute the bounding box
        spot_placements = []
        for s in control_point.layer.spots:
            weighted_spot = rt.weighted_spot()
            weighted_spot.from_json(s)

            spot_placement = rt.spot_placement()
            spot_placement.energy = weighted_spot.energy
            spot_placement.position = weighted_spot.position
            spot_placements.append(spot_placement.expand_data())
        # spot_bounding_box = dosimetry.get_spot_bounding_box(spot_placements)
        spot_list_bounding_box = \
            thinknode.function(iam["account_name"], 'dosimetry', "spot_list_bounding_box",
            [
                thinknode.value(spot_placements),
            ])

        # Loop through each spot to compute dose
        for s in control_point.layer.spots:
            weighted_spot = rt.weighted_spot()
            weighted_spot.from_json(s)
            if weighted_spot.fluence < 0.0001:
                # Ignore low fluence or 'off' spots
                continue
            fluences = [weighted_spot.fluence]

            spot_placement = rt.spot_placement()
            spot_placement.energy = weighted_spot.energy
            spot_placement.position = weighted_spot.position
            single_spot_layer = \
                thinknode.function(
                    iam["account_name"], "dosimetry", "create_pbs_layers_from_spots",
                    [
                        thinknode.reference(pbs_machine_id),
                        thinknode.array_named_type("dosimetry", "spot_placement", [thinknode.value(spot_placement.expand_data())]),
                        thinknode.value(control_point.gantry_angle)
                    ])
            layer_id = thinknode.post_calculation(iam, single_spot_layer)

            beam_geometry = dicom_worker.get_beam_geometry(iam, study_id, beam_index - 1)
            spot_box_with_margin = \
                thinknode.function(iam["account_name"], 'dosimetry', "add_margin_to_box_2d",
                [
                    spot_list_bounding_box,
                    thinknode.value([30., 30.])
                ])
            bixel_grid = \
                thinknode.function(iam["account_name"], "dosimetry", "make_grid_for_box_2d",
                    [
                        spot_box_with_margin,
                        thinknode.value([0.5, 0.5])
                    ])
            # # dose_grid = \
            # #     thinknode.function(iam["account_name"], 'dosimetry', "add_margin_to_box_3d",
            # #     [
            # #         thinknode.value(spot_list_bounding_box),
            # #         thinknode.value([15., 15.])
            # #     ])

            print(fluences)
            print(spot_box_with_margin)
            print(single_spot_layer)

            dose_calc = \
                thinknode.function(
                    iam["account_name"], "dosimetry", "compute_pbs_pb_dose_to_grid",
                    [
                        thinknode.value(fluences),
                        thinknode.reference(stopping_img),
                        thinknode.reference(dose_grid),
                        thinknode.reference(beam_geometry),
                        bixel_grid,
                        thinknode.reference(layer_id),
                        thinknode.value(thinknode.none),
                        thinknode.value([])
                    ])
            dose_calc_id = thinknode.post_calculation(iam, dose_calc)
            dose_calc_ids.append(dose_calc_id)
            #break # stop after the first spot
        break # stop after the first control point

    print("Beam Dose calc Ids: " + str(dose_calc_ids))

    folder = dicom_dataset_path + "/beam_" + str(beam_index) + "_results"
    if not os.path.exists(folder):
        os.mkdir(folder)

    file_count = 1
    for id in dose_calc_ids:
        dicom_file_calc = \
            thinknode.function(
                iam["account_name"], "dicom", "write_dose_image",
                [
                    thinknode.reference(id),
                    thinknode.value("Spot Test"),
                    thinknode.value("12345")
                ])
        dicom_blob = thinknode.do_calculation(iam, dicom_file_calc, True)
        f = open(folder + "/spot_dose_" + str(file_count) + ".dcm", "wb")
        f.write(dicom_blob)
        image = thinknode.get_immutable(iam, "dosimetry", id, True)
        vtk.write_vtk_image3(folder + "/spot_dose_" + str(file_count) + ".vtk", image)
        file_count += 1

    break #stop after the first beam
    beam_index += 1

print('Complete!')
# Copyright (c) 2018 .decimal, LLC. All rights reserved.
# Author:   Kevin Erhart
# Date:     04/30/2018
# Desc:     Performs a raytrace (line integral) over a stopping power image
#			from isocenter outward at a given angle, where one structure has
#			a density override applied (CT & SS are read from disk and posted
#			to Thinknode, use anonymized data files)

import os.path
import binascii
import sys
from lib import thinknode_worker as thinknode
from lib import dosimetry_worker as dosimetry
from lib import decimal_logging as dl
from lib import dicom_worker as dicom
from lib import rt_types as rt_types
from lib import vtk_worker as vtk
from lib import thinknode_id as tn_id
import json

iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))
study_id = ''

# Set study_id to a known value or
# set the directory location for the input files (CT & SS)
dir_loc = 'C:/XXX'

# Set the name of the structure to override RSP
override_structure = 'External'

# Define the list of rays to use (add more rays to do additional ray traces)
ray_list = []
ray_1 = {}
ray_1['origin'] = [0., -175., -50.]     # Start point of the ray in image space coordinates
ray_1['direction'] = [ 0., 0., 1.] 		 # Unit vector in the direction for this ray
ray_list.append(ray_1)
ray_2 = {}
ray_2['origin'] = [0., -175., -50.]     # Start point of the ray in image space coordinates
ray_2['direction'] = [ 0., 0., -1.] 	 # Unit vector in the direction for this ray
ray_list.append(ray_2)
ray_3 = {}
ray_3['origin'] = [0., -175., -50.]     # Start point of the ray in image space coordinates
ray_3['direction'] = [ 0., 1., 0.] 		 # Unit vector in the direction for this ray
ray_list.append(ray_3)
ray_4 = {}
ray_4['origin'] = [0., -175., -50.]     # Start point of the ray in image space coordinates
ray_4['direction'] = [ 0., -1., 0.] 	 # Unit vector in the direction for this ray
ray_list.append(ray_4)



if len(study_id) == 0:
	study_id = dicom.make_rt_study_from_dir(iam, dir_loc)

	study_calc = \
		thinknode.function(iam["account_name"], 'dicom', "merge_ct_image_slices",
			[
				thinknode.reference(study_id)
			])
	study_id = thinknode.do_calculation(iam, study_calc, False)

dl.debug("study_id: " + study_id)

# Need to get the CT images as a dicom_object
# ct_calc = \
# 	thinknode.function(iam["account_name"], 'dicom', "import_files_to_dicom_object",
# 		[
# 			thinknode.array_named_type('dosimetry', 'filesystem_item', file_ids),
# 			thinknode.value(False)
# 		])
# ct_res = thinknode.post_calculation(iam, calc)

study_data = thinknode.get_immutable(iam, 'dosimetry', study_id)
ct_union = {}
ct_union['ct_image'] = study_data['ct']
ct_res = json.loads(thinknode.post_immutable_named(iam, 'dosimetry', ct_union, 'dicom_object').text)['id']
print("CT Obj: " + str(ct_res))
# ct_res = 'xxx' # Put above CT Obj ID here on subsequent runs for efficiency reasons
ct_calc_1 = thinknode.function(iam["account_name"], "dosimetry", 'get_ct_image_slice_descriptions', [thinknode.reference(ct_res)])
ct_slice_list = thinknode.post_calculation(iam, ct_calc_1)


# Get the target structure and convert to Dosimetry structure_geometry
ss_id = thinknode.do_calc_item_property(iam, 'structure_set', thinknode.schema_named_type('dosimetry', 'rt_structure_set'), study_id)
structure_list = thinknode.do_calc_item_property(iam, 'structures', thinknode.schema_named_type('dosimetry', 'rt_structure_list'), ss_id)
structure_array = thinknode.do_calc_item_property(iam, 'structure_list', thinknode.schema_array_named_type('dosimetry', 'rt_structure'), structure_list)
structures = dicom.get_property_array_item_ids(iam, structure_array, 'rt_structure')
print("Structures Ready")
t_id = ""
for s in structures:
	# Get structure name
	t_id = thinknode.do_calc_item_property(iam, 'name', thinknode.schema_standard_type("string_type"), s, True, False, True)
	print("Structure name: " + str(t_id))
	if t_id == override_structure:
		s_geom = thinknode.do_calc_item_property(iam, 'geometry', thinknode.schema_named_type('dosimetry', 'rt_roi_geometry'), s)
		t_id = thinknode.do_calc_item_property(iam, 'slices', thinknode.schema_array_named_type('dosimetry', 'rt_contour'), s_geom)
		break
print("Target Located: " + str(t_id))
sg_calc = thinknode.function(iam['account_name'], 'dosimetry', "get_geometry_from_structure", 
	[
		thinknode.reference(t_id),
		thinknode.reference(ct_slice_list)
	])
sg = thinknode.post_calculation(iam, sg_calc)

# Get the stopping power image using the default HU to RSP curve
stopping_img = dicom.get_stopping_power_img(iam, study_id)

# Get and print the image data so we can see the bounds of it (helpful for debugging if you don't already know the image bounds)
# stopping_img_data = thinknode.get_immutable(iam, 'planning', stopping_img, True)
# print('Origin: ' + str(stopping_img_data['origin']))
# print('Spacing: ]' + str(stopping_img_data['axes'][0][0]) + ', ' + str(stopping_img_data['axes'][1][1]) + ', ' + str(stopping_img_data['axes'][2][2]) + ']')
# print('Pixel Count: ' + str(stopping_img_data['size']))

# Add a RSP value override to 'override' structure
density_calc = thinknode.function(iam["account_name"], "dosimetry", "override_image_inside_structure",
    [
		thinknode.reference(stopping_img),
		thinknode.reference(sg), # Structure to override
		thinknode.value(1.0), # New RSP to set
		thinknode.value(0.5) # Fraction of pixel that must be inside structure for the RSP to be overridden
    ])
img_with_override = thinknode.do_calculation(iam, density_calc, False)

integral_results = []
for ray in ray_list:
	calc = thinknode.function(iam["account_name"], "dosimetry", "compute_image_integral_over_ray_3d",
    [
		thinknode.reference(img_with_override),
		thinknode.value(ray)
    ])
	# Perform the calculation request
	integral_results.append(thinknode.do_calculation(iam, calc, True))

print('Integral Results: ' + str(integral_results))

dl.event("Done!")	

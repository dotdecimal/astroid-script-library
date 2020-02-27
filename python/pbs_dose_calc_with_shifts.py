# Copyright (c) 2020 .decimal, LLC. All rights reserved.
# Author:   Kevin Erhart
# Date:     02/26/2020
# Desc:     Facilitates robustness analysis calculations


import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import decimal_logging as dl
import rt_types as rt_types
import vtk_worker as vtk
import thinknode_id as tn_id


# User Set this data ----------------------------------------------

optimization_id = "5e5720080100ff09ab217fa73bedf054"
beam_num = 0

# Define the dose grid location and resolution
local_bounds = {}
local_bounds['corner'] = [-160.0, 4.0, 160.0]
local_bounds['size'] = [160.0, 80.0, 80.0]
grid_spacing = 2.0

# Robust simulation data
isocenter_shift = [0.0, 5.0, 0.0] # set to [] to use original beam isocenter
stopping_power_error_ratio = 0.95 # set to 0.0 to use original RSP data 

# ------------------------------------------------------------------


iam = thinknode.authenticate(thinknode.read_config('thinknode-dcs.cfg'))

# Function to write the dose image to vtk file format
def dose_to_vtk(dose_id):
	img_data = thinknode.get_immutable(iam, 'dosimetry', dose_id, False)
	img = rt_types.image_3f()
	img.from_json(img_data)
	img2 = img.expand_data()
	vtk.write_vtk_image3('dose_pbs.vtk', img2)


def run_dose_calc():

	# Attempt to automate the above IDs
	optimization_request = thinknode.get_calc_request(iam, 'dosimetry', optimization_id)
	dij_array_request = thinknode.get_calc_request(iam, 'dosimetry', optimization_request['function']['args'][0]['reference'])
	beam_dij_request = thinknode.get_calc_request(iam, 'dosimetry', dij_array_request['array']['items'][beam_num]['reference'])

	stopping_img = beam_dij_request['function']['args'][0]['reference']
	dose_points = beam_dij_request['function']['args'][1]['reference']
	beam_geometry = beam_dij_request['function']['args'][2]['reference']
	bixel_grid = beam_dij_request['function']['args'][3]['reference']
	layers = beam_dij_request['function']['args'][4]['reference']
	dcs_aps = beam_dij_request['function']['args'][5]['reference']
	degraders = beam_dij_request['function']['args'][6]['reference']

	# Shift the beam center
	if len(isocenter_shift) == 3:
		beam_geom_request = thinknode.get_calc_request(iam, 'dosimetry', beam_geometry)
		beam_obj_request = thinknode.get_calc_request(iam, 'dosimetry', beam_geom_request['object']['properties']['image_to_beam']['reference'])
		new_beam_request = thinknode.get_calc_request(iam, 'dosimetry', beam_obj_request['function']['args'][0]['reference'])
		new_beam_request['function']['args'][3]['value'][0] += isocenter_shift[0]
		new_beam_request['function']['args'][3]['value'][1] += isocenter_shift[1]
		new_beam_request['function']['args'][3]['value'][2] += isocenter_shift[2]
		beam1 = thinknode.do_calculation(iam, new_beam_request, False)
		beam_obj_request['function']['args'][0]['reference'] = beam1
		beam2 = thinknode.do_calculation(iam, beam_obj_request, False)
		beam_geom_request['object']['properties']['image_to_beam']['reference'] = beam2
		beam_geometry = thinknode.do_calculation(iam, beam_geom_request, False)

	# Scale the RSP data
	if stopping_power_error_ratio != 1.0:
		rsp_image_calc = thinknode.function(iam["account_name"], "dosimetry", "scale_image_values_3d",
			[
				thinknode.reference(stopping_img),
				thinknode.value(stopping_power_error_ratio),
				thinknode.value("relative stopping power"),
				thinknode.value("relative stopping power")
			])
		stopping_img = thinknode.do_calculation(iam, rsp_image_calc, False)

	calc_local_dose_grid = \
		thinknode.function(iam["account_name"], "dosimetry", "compute_adaptive_grid",
			[
				thinknode.value(local_bounds),
				thinknode.value(local_bounds),
				thinknode.value(grid_spacing),
				thinknode.value([]),
			])
	local_dose_grid_id = thinknode.do_calculation(iam, calc_local_dose_grid, False)

	calc_local_dose_points = \
		thinknode.function(iam["account_name"], "dosimetry", "get_points_on_adaptive_grid",
			[
				thinknode.reference(local_dose_grid_id)
			])
	local_dose_points_id = thinknode.do_calculation(iam, calc_local_dose_points, False)

	fluences_optional = thinknode.do_calc_item_property(iam, 'some', thinknode.schema_array_array_standard_type("float_type"), optimization_id)
	fluences_calc = thinknode.do_calc_array_item(iam, 0, thinknode.schema_array_standard_type("float_type"), fluences_optional)

	calc_dij = \
		thinknode.function(iam["account_name"], "dosimetry", "compute_pbs_pb_dij",
			[
				thinknode.reference(stopping_img),
				thinknode.reference(local_dose_points_id),
				thinknode.reference(beam_geometry),
				thinknode.reference(bixel_grid),
				thinknode.reference(layers),
				thinknode.reference(dcs_aps),
				# thinknode.reference(degraders)
				thinknode.value([])
			])

	# Perform pbs dij calculation request
	dij_id = thinknode.do_calculation(iam, calc_dij, False)

	calc_dose = \
		thinknode.function(iam["account_name"], "dosimetry", "multiply_dij_by_fluences",
			[
				thinknode.reference(dij_id),
				thinknode.reference(fluences_calc),
				thinknode.reference(local_dose_grid_id)
			])

	# Perform pbs dij calculation request
	res = thinknode.do_calculation(iam, calc_dose, False)

	# Write dose results to vtk image for viewing in Paraview
	dose_to_vtk(res)	
	dl.event("Done!")	

# Work is performed from here:
run_dose_calc()
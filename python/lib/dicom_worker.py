# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown
# Date:     07/10/2015
# Desc:     Worker to perform common dicom calculations and pull common dicom objects

import os.path
import binascii
from lib import thinknode_worker as thinknode
from lib import dosimetry_worker as dosimetry
from lib import decimal_logging as dl
from lib import rt_types as rt_types
import requests
import json

from multiprocessing import Pool
import functools
from joblib import Parallel, delayed

dicom_filetypes = [".img", ".dcm"]

#####################################################################
# functions to make a dicom_patient from a file directory
#####################################################################

# Takes in a file name and returns true if its extension is valid, otherwise returns false
# 	param filename: The name of the file to check
def valid_dicom_filetype(filename):
	# dl.debug("valid_dicom_filetype")
	for ext in dicom_filetypes:
		if filename[len(filename)-len(ext):] == ext:
			return True;
	# dl.error('Invalid filetype found: ' + filename)
	return False

# Posts a filesystem_item to iss in thinknode and returns the id of the item
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param item: The filesystem_item to be posted to thinknode
#	returns filesystem iss id
def post_filesystem_item(iam, item, dicom=True):
	dl.debug("post_filesystem_item")
	if dicom:
		res = thinknode.post_immutable_named(iam, 'dicom', item, 'filesystem_item')
	else:
		scope = thinknode.make_named_type_scope(iam, 'launcher', 'filesystem_item')
		res = thinknode.post_immutable(iam, 'launcher', item, scope, 'filesystem_item')
	obj = json.loads(res.text)
	return obj['id']

# Posts a filesystem_item_contents to iss in thinknode and returns the id of the item
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param item: The filesystem_item_contents to be posted to thinknode
#	returns filesystem item contents iss id
def post_filesystem_item_contents(iam, item):
	dl.debug("post_filesystem_item_contents")
	res = thinknode.post_dependency_immutable(iam, "dosimetry", item, 'filesystem_item_contents')
	obj = json.loads(res.text)
	return obj['id']

# Takes in a filename and reads in file in binary mode
#	param filename: The name of the file to read in to a blob
# 	returns a blob of the file
def read_file(filename):
	dl.debug("read_file")
	fp = open(filename, 'rb')
	output_string = ''
	bytes_read = fp.read()
	fp.close()
	return bytes_read 

	# Used for non-msgpack uploading
	# output_string = binascii.b2a_base64(bytes_read)
	# o_s = output_string[:len(output_string)-1]
	# s = str(o_s)
	# blob_data = s[2:len(s)-1]
	# b = rt_types.blob_type()
	# b.blob = blob_data
	# return b

# Takes in a filename, reads in the file to a blob and uploads to thinknode as filesystem_item
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param filename: The name of the file to be uploaded to thinknode
#	returns the id of the filesystem_item
def upload_file(filename, iam, dicom_only=True):
	dl.debug("upload_file")
	dl.event('Reading file: ' + filename)
	file_basename = os.path.basename(filename)

	if dicom_only and valid_dicom_filetype(file_basename) != True:
		return 'bad filetype'	
	else:
		b = read_file(filename)	

		fsic = rt_types.filesystem_item_contents()
		del fsic.directory
		fsi = rt_types.filesystem_item()
		fsi.name = file_basename
		fsi.contents = fsic

		json_data = thinknode.to_json(fsi)
		json_data["contents"]["file"] = b

		# Used for non-msgpack uploading
		# obj_id = post_filesystem_item(iam, thinknode.to_json(fsi))
		obj_id = post_filesystem_item(iam, json_data, dicom_only)
		dl.debug('Filesystem item: ' + obj_id)
		
		return obj_id

def upload_file_list(iam, dir_name, upload_file_list, dicom_only=True):
	dl.debug("upload_file_list")
	tn_dir = rt_types.filesystem_item_contents()

	tn_dir.directory = Parallel(n_jobs=8,  backend="threading")(
             map(delayed(functools.partial(upload_file, iam=iam, dicom_only=dicom_only)), upload_file_list))    

	# Remove bad files
	new_dir = []
	for f in tn_dir.directory:
		if f != 'bad filetype':
			new_dir.append(f)
	tn_dir.directory = new_dir

	del tn_dir.file
	fsi = rt_types.filesystem_item()
	fsi.name = dir_name
	fsi.contents = tn_dir

	print(thinknode.to_json(fsi))

	obj_id = post_filesystem_item(iam, thinknode.to_json(fsi), dicom_only)
	dl.debug('Directory id: ' + obj_id)	
	return obj_id

# Takes in a directory path and uploads all the files in the path to thinknode as filesystem_items
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param dirname: The name of the directory to be uploaded to thinknode
# 	returns id of the filesystem_item that holds a directory of the files
def upload_dir(iam, dir_name, dicom_only=True):
	dl.debug("upload_dir")
	dl.event('Uploading directory: ' + dir_name)
	
	tn_dir = rt_types.filesystem_item_contents()
	upload_files=[]
	for dirname, dirnames, filenames in os.walk(dir_name):
		# print path to all subdirectories first.
		for subdirname in dirnames:
			print(os.path.join(dirname, subdirname))

		# print path to all filenames.
		for filename in filenames:
			upload_files.append(os.path.join(dirname, filename))

	return upload_file_list(iam, dir_name, upload_files)

# Upload a directory of dicom files into new rt_study
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param dir_name: complete directory path
# 	returns a study iss ID
def make_rt_study_from_dir(iam, dir_name):
	dl.debug("make_rt_study_from_dir")
	dir_id = upload_dir(iam, dir_name)
	dl.debug('dir_id')
	dl.debug(dir_id)
	res = thinknode.get_immutable(iam, 'dicom', dir_id)
	dl.debug('Got immutable: ' + str(res))
	dir_obj = res
	file_ids = []
	for file_id in dir_obj["contents"]["directory"]:
		file_ids.append(thinknode.reference(file_id))
	calc = \
		thinknode.function(iam["account_name"], 'dicom', "import_files_to_new_study",
			[
				thinknode.array_named_type('dosimetry', 'filesystem_item', file_ids)
			])
	dl.debug(str(calc))

	res = thinknode.do_calculation(iam, calc, False, False)
	dl.debug('initial study:')
	dl.debug(res)
	return res

# Upload a directory of dicom files into a list dicom_objects
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param filtered_upload_file_list: complete list of files to upload
# 	returns iss ID for dicom_object list
def make_dicom_object_from_dir(iam, dir_name, filtered_upload_file_list):
	dl.debug("make_dicom_object_from_dir")
	dir_id = upload_file_list(iam, dir_name, filtered_upload_file_list)
	dl.debug('dir_id')
	dl.debug(dir_id)
	res = thinknode.get_immutable(iam, 'dicom', dir_id)
	dl.debug('Got immutable: ' + str(res))
	dir_obj = res
	file_ids = []
	for file_id in dir_obj["contents"]["directory"]:
		file_ids.append(thinknode.reference(file_id))
	calc = \
		thinknode.function(iam["account_name"], 'dicom', "import_files_to_dicom_object",
			[
				thinknode.array_named_type('dosimetry', 'filesystem_item', file_ids),
				thinknode.value(False)
			])
	dl.debug(str(calc))

	res = thinknode.post_calculation(iam, calc)
	dl.debug(res)

	return res

# Run a calcuation to turn a filesytem_item in to a dicom_data object
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param filesytem_item_id: The thinknode id for the filesystem_item
#	returns the id of the dicom_data object
def run_calc_parse_dicom_filesystem(iam, filesytem_item_id):	
	dl.debug("run_calc_parse_dicom_filesystem")
	calc = \
		thinknode.function("dicom", "parse_dicom_filesystem_item",
			[
				thinknode.reference(filesytem_item_id)
			])

	res = thinknode.do_calculation(iam, 'dicom', calc, False)
	return res

#####################################################################
# functions to pull data out of a dicom_patient
#####################################################################

# Takes a list of dicom_objects and gets the individual ID for each object
#	param iam: connection settings (url, user token, and ids for context and realm)
#	param list_id: The thinknode id for the list of dicom_objects
def get_dicom_object_ids(iam, list_id):
	dl.debug("get_dicom_object_ids")

	ids = []
	dd_index = 0
	not_end = True

	while not_end:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dosimetry", "dicom_object"), list_id, True, False, True)
		dl.debug('dd: ' + dd)
		if 'failed' in dd:
			not_end = False
			break
		ids.append(dd)
		dd_index = dd_index + 1

	dl.debug("Number of array items: " + str(dd_index))
	return ids

# Takes a property that is a list of items and gets the individual ID for each item
#	param iam: connection settings (url, user token, and ids for context and realm)
#	param list_id: The thinknode id for the property array
#	param type_name: The named type of the items in the array
def get_property_array_item_ids(iam, list_id, type_name):
	dl.debug("get_property_array_item_ids")
	ids = []
	dd_index = 0
	not_end = True
	while not_end:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dosimetry", type_name), list_id, True, False, True)
		dl.debug('dd: ' + dd)
		if 'failed' in dd:
			not_end = False
			break
		ids.append(dd)
		dd_index = dd_index + 1
	dl.debug("Number of array items: " + str(dd_index))
	return ids

# Takes in a thinknode id for a dicom_patient and returns id for the rt_plan
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param patient_id: The thinknode id for the dicom_patient to pull the plan from
#	returns the id of the rt_plan from the patient
def get_plan(iam, patient_id):
	dl.debug("get_plan")
	dd_array = thinknode.do_calc_item_property(iam, 'patient', thinknode.schema_array_named_type("dosimetry", "dicom_data"), patient_id)
	dl.debug('dd_array: ' + dd_array)

	dd_index = 0
	not_found = True

	while not_found:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dosimetry", "dicom_data"), dd_array)
		dl.debug('dd: ' + dd)

		dd_obj = thinknode.do_calc_item_property(iam, 'dicom_obj', thinknode.schema_named_type("dosimetry", "dicom_object"), dd)
		dl.debug('dd_obj: ' + dd_obj)

		plan = thinknode.do_calc_item_property(iam, 'plan', thinknode.schema_named_type("dosimetry", "rt_plan"), dd_obj)
		if not plan:
			dl.debug('dd object was not a plan object!!')
			dd_index = dd_index + 1
		else:
			dl.debug('plan: ' + plan)
			return plan

# Create a beam_geometry data type based on dicom study and specified beam index
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param study_id: rt_study iss id
#	param beam_index: index of the beam to create geometry for
#	returns: a beam_geometry data type for the specific plan and beam
def get_beam_geometry(iam, study_id, beam_index):
	dl.debug("get_beam_geometry")

	beam_id = get_beam_from_study(iam, study_id, beam_index)
	control_pt_id = get_first_control_point_from_beam(iam, beam_id)
	sad = thinknode.do_calc_item_property(iam, 'virtual_sad', thinknode.schema_array_standard_type("float_type"), beam_id)
	iso_center = thinknode.do_calc_item_property(iam, 'iso_center_position', thinknode.schema_array_standard_type("float_type"), control_pt_id)
	gantry_angle = thinknode.do_calc_item_property(iam, 'gantry_angle', thinknode.schema_standard_type("float_type"), control_pt_id)
	couch_angle = thinknode.do_calc_item_property(iam, 'patient_support_angle', thinknode.schema_standard_type("float_type"), control_pt_id)

	# patient_position = thinknode.do_calc_item_property(iam, 'dicom', 'patient_position', thinknode.schema_standard_type("string"), control_pt_id)
	plan_id = thinknode.do_calc_item_property(iam, 'plan', thinknode.schema_named_type("rt_plan"), study_id)
	setups_array = thinknode.do_calc_item_property(iam, 'patient_setups', thinknode.schema_array_named_type("dosimetry", 'rt_patient_setup'), plan_id)
	setup = thinknode.do_calc_array_item(iam, 0, thinknode.schema_named_type("dosimetry", 'rt_patient_setup'), setups_array)

	patient_position = thinknode.do_calc_item_property(iam, 'position', thinknode.schema_named_type("dosimetry", 'patient_position_type'), setup)

	calc = \
		thinknode.function(iam["account_name"], "dosimetry", "construct_beam_geometry",
			[
				thinknode.reference(sad),
				thinknode.reference(iso_center),
				thinknode.reference(gantry_angle),
				thinknode.reference(couch_angle),
				thinknode.reference(patient_position)
			])

	print("    CALC: " + str(calc))	

	res = thinknode.post_calculation(iam, calc)
	return res

# Takes in a thinknode id for a rt_plan and the index of the beam returns id for the rt_ion_beam
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param study_id: The thinknode id for the rt_plan to pull the rt_ion_beam from
#	param beam_index: The index of the beam to get
#	returns the id of the rt_ion_beam from the rt_plan
def get_beam_by_index(iam, study_id, beam_index):
	dl.debug("get_beam_by_index")

	plan = thinknode.do_calc_item_property(iam, 'plan', thinknode.schema_named_type("dosimetry", "rt_plan"), study_id)
	beam_array = thinknode.do_calc_item_property(iam, 'beams', thinknode.schema_array_named_type("dosimetry", "rt_ion_beam"), plan)
	beam = thinknode.do_calc_array_item(iam, beam_index, thinknode.schema_named_type("dosimetry", "rt_ion_beam"), beam_array)
	return beam

# Takes in a thinknode id for a rt_plan and the index of the beam returns id for the aperture associated  with that beam
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param study_id: The thinknode id for the rt_plan to pull the aperture from
#	param beam_index: The index of the beam to get
#	returns the id of the aperture from the specified rt_ion_beam
def get_aperture_from_beam(iam, study_id, beam_index):
	dl.debug("get_aperture_from_beam")

	beam_id = get_beam_by_index(iam, study_id, beam_index)
	rt_ap = thinknode.do_calc_item_property(iam, 'block', thinknode.schema_named_type("dosimetry", 'rt_ion_block'), beam_id)
	ap_poly = thinknode.do_calc_item_property(iam, 'data', thinknode.schema_named_type("dosimetry", 'polyset'), rt_ap)
	ap_ds_edge = thinknode.do_calc_item_property(iam, 'downstream_edge', thinknode.schema_standard_type('float_type'), rt_ap)

	struct_calc = \
		thinknode.structure(thinknode.schema_named_type('aperture'),
			{
				"downstream_edge": thinknode.reference(ap_ds_edge), 
				"shape": thinknode.reference(ap_poly)
			})
	aperture = thinknode.post_calculation(iam, struct_calc)
	return aperture

# Get the SAD from a defined beam
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param beam_id: beam number to get the sad for
#	returns: the specific beam SAD object iss id
def get_sad(iam, beam_id):
	dl.debug("get_sad")
	sad_array = thinknode.do_calc_item_property(iam, 'virtual_sad', thinknode.schema_array_standard_type("float_type"), beam_id)
	sad_wait = thinknode.wait_for_calculation(iam, 'dosimetry', sad_array, False)
	sad = thinknode.get_immutable(iam, 'dicom', sad_array)
	dl.debug("sad: " + str(sad))
	return sad

# Get the weighted spot list from a pbs beam
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param beam_id: beam issid to get the spot list from
#	returns: weighted_spot_list
def get_weighted_spot_list_from_beam(iam, beam_id):
	dl.debug("get_weighted_spot_list_from_beam")
	calc = \
		thinknode.function(iam["account_name"], "dicom", "get_weighted_spot_list_from_beam",
			[
				thinknode.reference(beam_id)
			])
	res = thinknode.post_calculation(iam, calc)

	thinknode.wait_for_calculation(iam, 'dicom', res, False)
	spot_list = thinknode.get_immutable(iam, 'dicom', res)

	sorted_spots = dosimetry.sort_spots_by_energy(spot_list)

	return sorted_spots

# Get PBS spots from a specific beam
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param beam_id: beam iss id
# 	returns: specific beam's pbs spots
def get_spots_from_beam(iam, beam_id):
	dl.debug("get_spots_from_beam")
	wsp_id = get_weighted_spot_list_from_beam(iam, beam_id)

	calc = \
		thinknode.function(iam["account_name"], "dosimetry", "extract_spot_placements",
			[
				thinknode.value(wsp_id)
			])

	res = thinknode.post_calculation(iam, calc)

	return res	

def get_sorted_weighted_spot_list_from_beam(iam, beam_id):
	dl.debug("get_weighted_spot_list_from_beam")	
	wsl_calc = \
		thinknode.function(iam["account_name"], "dicom", "weighted_spot_list_from_beam",
			[
				thinknode.reference(beam_id)
			])
	wsl_res = thinknode.post_calculation(iam, wsl_calc)
	print("Got wsl response: " + wsl_res)
	dl.debug("get_weighted_spot_list_from_beam")	
	sl_calc = \
		thinknode.function(iam["account_name"], "dosimetry", "extract_spot_placements",
			[
				thinknode.reference(wsl_res)
			])

	sl_res = thinknode.post_calculation(iam, sl_calc)
	return sl_res


# Get PBS fluences from a specific beam
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param beam_id: beam iss id
#	returns: specific beam's fluences
def get_fluences_from_beam(iam, beam_id):
	dl.debug("get_fluences_from_beam")
	wsp_id = get_weighted_spot_list_from_beam(iam, beam_id)

	calc = \
		thinknode.function(iam["account_name"], "dosimetry", "extract_spot_fluence_values",
			[
				thinknode.value(wsp_id)
			])
	res = thinknode.post_calculation(iam, calc)
	return res	

# Create PBS layers from spots in DICOM rt_study
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param pbs_machine: the pbs machine model
#   param spots: The spot list whose layers will be computed
#   param beam_id: beam number to get the layers for
def get_pbs_layers(iam, pbs_machine, spots, beam_id):
    dl.debug("get_pbs_layers")
    control_pt_id = get_first_control_point_from_beam(iam, beam_id)

    gantry_angle = thinknode.do_calc_item_property(iam, 'gantry_angle', thinknode.schema_standard_type("dosimetry", "float_type"), control_pt_id)

    layers_calc = thinknode.function(iam["account_name"], "dosimetry", "create_pbs_layers_from_spots",
            [
                thinknode.reference(pbs_machine),
                thinknode.reference(spots),
                thinknode.reference(gantry_angle)
            ])
    res = thinknode.post_calculation(iam, layers_calc)
    return res  

# Get a specific beam's iss id from the dicom rt_study
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param study_id: rt_study iss id
#	param beam_index: beam number from rt_plan to get iss id of
#	returns: specified beam number's iss id
def get_beam_from_study(iam, study_id, beam_index):
	dl.debug("get_beam_from_study")
	plan_id = thinknode.do_calc_item_property(iam, 'plan', thinknode.schema_named_type("dosimetry", "rt_plan"), study_id)

	beams = thinknode.do_calc_item_property(iam, 'beams', thinknode.schema_array_named_type("dosimetry", "rt_ion_beam"), plan_id)

	beam_id = thinknode.do_calc_array_item(iam, beam_index, thinknode.schema_named_type("dosimetry", "rt_ion_beam"), beams)
	return beam_id

# Get the first control point iss id of the specified beam
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param beam_id: beam iss id
#	returns: first control point's iss id of specified beam
def get_first_control_point_from_beam(iam, beam_id):
	dl.debug("get_first_control_point_from_beam")
	control_pts = thinknode.do_calc_item_property(iam, 'control_points', thinknode.schema_array_named_type("dosimetry", "rt_control_point"), beam_id)	

	control_pt_id = thinknode.do_calc_array_item(iam, 0, thinknode.schema_named_type("dosimetry", "rt_control_point"), control_pts)
	dl.debug('control point id: ' + control_pt_id)
	return control_pt_id

# Takes in a thinknode id for a rt_plan and the index of the beam returns id for the range compensator associated  with that beam
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param plan_id: The thinknode id for the rt_plan to pull the range compensator from
#	param beam_index: The index of the beam to get
#	returns the id of the range compensator from the specified rt_ion_beam
def get_range_compensator_from_beam(iam, plan_id, beam_index):
	dl.debug("get_range_compensator_from_beam")
	beam_array = thinknode.do_calc_item_property(iam, 'beams', thinknode.schema_array_named_type("dosimetry", "rt_ion_beam"), plan_id)

	beam_id = thinknode.do_calc_array_item(iam, beam_index, thinknode.schema_named_type("dosimetry", "rt_ion_beam"), beam_array)

	rt_rcs = thinknode.do_calc_item_property(iam, 'degraders', thinknode.schema_array_named_type("dosimetry", 'rt_ion_rangecompensator'), beam_id)
	rt_rc = thinknode.do_calc_array_item(iam, 0, thinknode.schema_named_type("dosimetry", 'rt_ion_rangecompensator'), rt_rcs)
	return rt_rc

# Takes in a thinknode id for a rt_plan and returns id for the patient_position_type for the first patient setup sequence
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param plan_id: The thinknode id for the rt_plan to pull the patient position from
#	returns the id of the patient_position_type from the first patient setup sequence
def get_patient_position(iam, plan_id):
	dl.debug("get_patient_position")
	setups_array = thinknode.do_calc_item_property(iam, 'patient_setups', thinknode.schema_array_named_type("dosimetry", 'rt_patient_setup'), plan_id)
	setup = thinknode.do_calc_array_item(iam, 0, thinknode.schema_named_type("dosimetry", 'rt_patient_setup'), setups_array)

	position = thinknode.do_calc_item_property(iam, 'position', thinknode.schema_named_type("dosimetry", 'patient_position_type'), setup)
	dl.debug('Patient Position: ' + str(position))
	return position

# Takes in a thinknode id for a dicom_patient and returns id for the rt_structure_set
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param patient_id: The thinknode id for the dicom_patient to pull the structure set from
#	returns the id of the rt_structure_set from the patient
def get_structure_set(iam, patient_id):
	dl.debug("get_structure_set")
	dd_array = thinknode.do_calc_item_property(iam, 'patient', thinknode.schema_array_named_type("dosimetry", "dicom_data"), patient_id)
	dl.debug('dd_array: ' + dd_array)

	dd_index = 0
	not_found = True

	while not_found:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dosimetry", "dicom_data"), dd_array)
		dl.debug('dd: ' + dd)

		dd_obj = thinknode.do_calc_item_property(iam, 'dicom_obj', thinknode.schema_named_type("dosimetry", "dicom_object"), dd)
		dl.debug('dd_obj: ' + dd_obj)

		ss = thinknode.do_calc_item_property(iam, 'structure_set', thinknode.schema_named_type("dosimetry", "rt_structure_set"), dd_obj)
		if not ss:
			dl.debug('dd object was not a structure_set object!!')
			dd_index = dd_index + 1
		else:
			dl.debug('ss: ' + ss)
			return ss

# Takes in a thinknode id for a rt_structure_set and the index of the structure returns id for the rt_structure
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param ss_id: The thinknode id for the rt_structure_set to pull the structure from
#	param index: The index of the structure to pull out from the structure set
#	returns the id of the rt_structure 
def get_structure_by_index(iam, ss_id, index):
	dl.debug("get_structure_by_index")
	structures = thinknode.do_calc_item_property(iam, 'structures', thinknode.schema_array_named_type("dosimetry", "rt_structure"), ss_id)
	structure = thinknode.do_calc_array_item(iam, index, thinknode.schema_named_type("dosimetry", "rt_structure"), structures)

	return structure

# Takes in a thinknode id for a rt_structure and returns id for the structure_geometry for the structure
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param s_id: The thinknode id for the rt_structure to pull the structure_geometry from
#	returns the id of the structure_geometry from the given rt_structure
def get_structure_geometry_from_structure(iam, s_id):
	dl.debug("get_structure_geometry_from_structure")
	calc = \
		thinknode.function("dicom", "get_geometry_from_structure",
			[
				thinknode.reference(s_id)
			])
	res = thinknode.post_calculation(iam, calc)
	return res

# Takes in a thinknode id for a dicom_patient and returns id for the rt_dose
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param patient_id: The thinknode id for the dicom_patient to pull the dose from
#	returns the id of the rt_dose from the patient
def get_dose(iam, patient_id):
	dl.debug("get_dose")
	dd_array = thinknode.do_calc_item_property(iam, 'patient', thinknode.schema_array_named_type("dosimetry", "dicom_data"), patient_id)
	dl.debug('dd_array: ' + dd_array)

	dd_index = 0
	not_found = True

	while not_found:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dosimetry", "dicom_data"), dd_array)
		dl.debug('dd: ' + dd)

		dd_obj = thinknode.do_calc_item_property(iam, 'dicom_obj', thinknode.schema_named_type("dosimetry", "dicom_object"), dd)
		dl.debug('dd_obj: ' + dd_obj)

		dose = thinknode.do_calc_item_property(iam, 'dose', thinknode.schema_named_type("dosimetry", "rt_dose"), dd_obj)
		if not dose:
			dl.debug('dd object was not a dose object!!')
			dd_index = dd_index + 1
		else:
			dl.debug('dose: ' + dose)
			return dose

# Gets a stopping power image from a dicom study
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param study_id: rt_study iss id
def get_stopping_power_img(iam, study_id):
	dl.debug("get_stopping_power_img")
	ct_img_data = thinknode.do_calc_item_property(iam, 'ct', thinknode.schema_named_type("dosimetry", "ct_image"), study_id)
	ct_img = thinknode.do_calc_item_property(iam, 'image_set', thinknode.schema_named_type("dosimetry", "ct_image_set"), ct_img_data)
	img = thinknode.do_calc_item_property(iam, 'image', thinknode.schema_named_type("dosimetry", "image_3d"), ct_img)

	calc = \
		thinknode.function(iam["account_name"], "dosimetry", "hu_to_stopping_power",
			[
				thinknode.reference(img)
			])
	res = thinknode.post_calculation(iam, calc)
	return res

# Takes in a thinknode id for a dicom_patient and returns id for the ct_image_set
#   param iam: connection settings (url, user token, and ids for context and realm)
#	param patient_id: The thinknode id for the dicom_patient to pull the CT image set from
#	returns the id of the ct_image_set from the patient
def get_ct_image_set(iam, patient_id):
	dl.debug("get_ct_image_set")
	dd_array = thinknode.do_calc_item_property(iam, 'patient', thinknode.schema_array_named_type("dosimetry", "dicom_data"), patient_id)
	dl.debug('dd_array: ' + dd_array)

	dd_index = 0
	not_found = True

	while not_found:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dosimetry", "dicom_data"), dd_array)
		dl.debug('dd: ' + dd)

		dd_obj = thinknode.do_calc_item_property(iam, 'dicom_obj', thinknode.schema_named_type("dosimetry", "dicom_object"), dd)
		dl.debug('dd_obj: ' + dd_obj)

		ct_img = thinknode.do_calc_item_property(iam, 'ct_image_set', thinknode.schema_named_type("dosimetry", "ct_image_set"), dd_obj)
		if not ct_img:
			dl.debug('dd object was not a ct_img object!!')
			dd_index = dd_index + 1
		else:
			dl.debug('ct_img: ' + ct_img)
			return ct_img

# Posts a DICOM SS file object as a referenced type
def structure_geometry_refs(iam, dicom_obj_id):
    obj = thinknode.get_immutable(iam, 'dosimetry', dicom_obj_id)
    ss_id = thinknode.do_calc_item_property(iam, 'structure_set', thinknode.schema_named_type("dosimetry", "rt_structure_set"), dicom_obj_id)
    ss_list_id = thinknode.do_calc_item_property(iam, 'structures', thinknode.schema_named_type("dosimetry", "rt_structure_list"), ss_id)
    structure_list_id = thinknode.do_calc_item_property(iam, 'structure_list', thinknode.schema_array_named_type("dosimetry", "rt_structure"), ss_list_id)
    
    list_of_refs = get_property_array_item_ids(iam, structure_list_id, "rt_structure")

    list_of_ref_iss_ids = []
    print("starting list")
    for ref in list_of_refs:
        print(ref)
        ref_data = thinknode.get_immutable(iam, 'dosimetry', ref)
        list_of_ref_iss_ids.append(json.loads(thinknode.post_immutable_named(iam, "dosimetry", ref_data, 'rt_structure').text)['id'])

    obj['structure_set']['structures']['ref_structure_list'] = list_of_ref_iss_ids
    del obj['structure_set']['structures']['structure_list']

    dicom_obj_ref_id = json.loads(thinknode.post_immutable_named(iam, "dosimetry", obj, 'dicom_object', True).text)['id']
    print('dicom_obj_ref_id: ' + dicom_obj_ref_id)
    return dicom_obj_ref_id
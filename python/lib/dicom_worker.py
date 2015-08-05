# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown
# Date:     07/10/2015
# Desc:     Worker to perform common dicom calculations and pull common dicom objects

import os.path
import binascii
from lib import thinknode_worker as thinknode
from lib import decimal_logging as dl
from lib import rt_types as rt_types
import requests
import json

app_name = "dicom"
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))
dicom_filetypes = [".img", ".dcm"]

#####################################################################
# functions to make a dicom_patient from a file directory
#####################################################################

# Takes in a file name and returns true if its extension is valid, otherwise returns false
# 	param filename: The name of the file to check
def valid_dicom_filetype(filename):
	for ext in dicom_filetypes:
		if filename[len(filename)-len(ext):] == ext:
			return True;
	dl.error('Invalid filetype found: ' + filename)
	return False

# Posts a filesystem_item to iss in thinknode and returns the id of the item
#	param item: The filesystem_item to be posted to thinknode
def post_filesystem_item(item):
	res = thinknode.post_dependency_immutable(iam, "rt_types", item, 'filesystem_item')
	obj = json.loads(res.text)
	return obj['id']

# Posts a filesystem_item_contents to iss in thinknode and returns the id of the item
#	param item: The filesystem_item_contents to be posted to thinknode
def post_filesystem_item_contents(item):
	res = thinknode.post_dependency_immutable(iam, "rt_types", item, 'filesystem_item_contents')
	obj = json.loads(res.text)
	return obj['id']

# Takes in a filename and reads in file in binary mode
#	param filename: The name of the file to read in to a blob
# 	returns a blob of the file
def read_file(filename):
	fp = open(filename, 'rb')
	output_string = ''
	bytes_read = fp.read()
	output_string = binascii.b2a_base64(bytes_read)
	o_s = output_string[:len(output_string)-1]
	s = str(o_s)
	blob_data = s[2:len(s)-1]
	b = rt_types.blob_type()
	b.blob = blob_data
	return b

# Takes in a filename, reads in the file to a blob and uploads to thinknode as filesystem_item
#	param filename: The name of the file to be uploaded to thinknode
#	returns the id of teh filesystem_item
def upload_file(filename):
	dl.event('Reading file: ' + filename)

	if valid_dicom_filetype(filename) == True:
		b = read_file(filename)		
		
		fsic = rt_types.filesystem_item_contents()
		fsic.type = "file"
		fsic.file = b
		fsi = rt_types.filesystem_item()
		fsi.name = filename
		fsi.contents = fsic

		obj_id = post_filesystem_item(thinknode.to_json(fsi))
		dl.debug('Filesystem item: ' + obj_id)
		
		return obj_id
	else:
		return 'bad filetype'

# Takes in a directory path and uploads all the files in the path to thinknode as filesystem_items
#	param dirname: The name of the directory to be uploaded to thinknode
# 	returns id of the filesystem_item that holds a directory of the files
def upload_dir(dirname):
	dl.event('Uploading directory: ' + dirname)
	
	tn_dir = rt_types.filesystem_item_contents()
	tn_dir.type = "directory"

	for fi in os.listdir(dirname):
		filename = dirname + '/' + fi
		obj_id = upload_file(filename)
		if (obj_id != 'bad filetype'):
			tn_dir.directory.append(obj_id)

	fsi = rt_types.filesystem_item()
	fsi.name = dirname
	fsi.contents = tn_dir

	obj_id = post_filesystem_item(thinknode.to_json(fsi))
	dl.debug('Directory id: ' + obj_id)	
	return obj_id

# def get_dicom_dir_by_id(dir_id):
# 	res = thinknode.get_immutable(iam, dir_id)
# 	dir_obj = json.loads(res)
# 	return dir_obj

# Takes in a thinknode id for a directory of dicom files and processes the files into a dicom_patient
#	param dir_id: thinknode id for the directory of files
#	returns the id of the dicom_patient
def make_patient_from_dir_id(dir_id):
	res = thinknode.get_immutable(iam, dir_id)
	dir_obj = json.loads(res)
	dicom_ids = []
	for file_id in dir_obj["contents"]["directory"]:
		dl.debug("File id: " + file_id)
		dicom_id = run_calc_parse_dicom_filesystem(file_id)
		dicom_ids.append(thinknode.reference(dicom_id))
	dicom_patient_array = thinknode.array_named_type('rt_types', 'dicom_data', dicom_ids)

	calc_id = run_calc_make_patient(dicom_patient_array)
	dl.debug('Make patient calc id: ' + calc_id)
	return calc_id

# Takes in a directory name and then uploads the directory to thinknode as filesystem_items and then
# 	runs the calculation to make a dicom_paitnet
#	param dir_name: Name of the directory to turn into a dicom_patient
#	returns the thinknode id of the dicom_patient
def make_patient_from_dir(dir_name):
	dir_id = upload_dir(dir_name)
	print (dir_id)
	calc_id = make_patient_from_dir_id(dir_id)
	dl.debug('Make patient calc id: ' + calc_id)
	return calc_id

# Run a calcuation to turn a filesytem_item in to a dicom_data object
#	param filesytem_item_id: The thinknode id for the filesystem_item
#	returns the id of the dicom_data object
def run_calc_parse_dicom_filesystem(filesytem_item_id):	
	dl.event('run_calc_parse_dicom_filesystem')
	calc = \
		thinknode.function(app_name, "parse_dicom_filesystem_item",
			[
				thinknode.reference(filesytem_item_id)
			])

	res = thinknode.do_calculation(iam, calc, False)
	return res

# Run a calcuation to turn an array of dicom_data objects into a dicom_patient
#	param dicom_objs: The array of thinknode ids for the dicom_data objects
#	returns the id of the dicom_patient object
def run_calc_make_patient(dicom_objs):
	dl.event("run_calc_make_patient")
	calc = \
		thinknode.function(app_name, "make_patient",
			[
				dicom_objs
			])

	res = thinknode.do_calculation(iam, calc, False)
	return res

#####################################################################
# functions to pull data out of a dicom_patient
#####################################################################

# Takes in a thinknode id for a dicom_patient and returns id for the rt_plan
#	param patient_id: The thinknode id for the dicom_patient to pull the plan from
#	returns the id of the rt_plan from the patient
def get_plan(patient_id):
	dd_array = thinknode.do_calc_item_property(iam, 'patient', thinknode.schema_array_named_type("dicom_data"), patient_id)
	dl.debug('dd_array: ' + dd_array)

	dd_index = 0
	not_found = True

	while not_found:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dicom_data"), dd_array)
		dl.debug('dd: ' + dd)

		dd_obj = thinknode.do_calc_item_property(iam, 'dicom_obj', thinknode.schema_named_type("dicom_object"), dd)
		dl.debug('dd_obj: ' + dd_obj)

		plan = thinknode.do_calc_item_property(iam, 'plan', thinknode.schema_named_type("rt_plan"), dd_obj)
		if not plan:
			dl.debug('dd object was not a plan object!!')
			dd_index = dd_index + 1
		else:
			dl.debug('plan: ' + plan)
			return plan

# Takes in a thinknode id for a rt_plan and the index of the beam returns id for the rt_ion_beam
#	param plan_id: The thinknode id for the rt_plan to pull the rt_ion_beam from
#	param beam_index: The index of the beam to get
#	returns the id of the rt_ion_beam from the rt_plan
def get_beam_by_index(plan_id, beam_index):
	beam_array = thinknode.do_calc_item_property(iam, 'beams', thinknode.schema_array_named_type("rt_ion_beam"), plan_id)
	print ('beam_array: ' + beam_array)

	beam = thinknode.do_calc_array_item(iam, beam_index, thinknode.schema_named_type("rt_ion_beam"), beam_array)
	print ('beam: ' + beam)
	return beam

# Takes in a thinknode id for a rt_plan and the index of the beam returns id for the aperture associated  with that beam
#	param plan_id: The thinknode id for the rt_plan to pull the aperture from
#	param beam_index: The index of the beam to get
#	returns the id of the aperture from the specified rt_ion_beam
def get_aperture_from_beam(plan_id, beam_index):
	beam_array = thinknode.do_calc_item_property(iam, 'beams', thinknode.schema_array_named_type("rt_ion_beam"), plan_id)
	print ('beam_array: ' + beam_array)

	beam_id = thinknode.do_calc_array_item(iam, beam_index, thinknode.schema_named_type("rt_ion_beam"), beam_array)
	print ('beam_id: ' + beam_id)

	rt_ap = thinknode.do_calc_item_property(iam, 'block', thinknode.schema_named_type('rt_ion_block'), beam_id)
	ap_poly = thinknode.do_calc_item_property(iam, 'data', thinknode.schema_named_type('polyset'), rt_ap)
	ap_ds_edge = thinknode.do_calc_item_property(iam, 'downstream_edge', thinknode.schema_standard_type('number_type'), rt_ap)

	struct_calc = \
		thinknode.structure(thinknode.schema_named_type('aperture'),
			{
				"downstream_edge": thinknode.reference(ap_ds_edge), 
				"shape": thinknode.reference(ap_poly)
			})
	aperture = thinknode.do_calculation(iam, struct_calc, False)
	dl.debug('aperture: ' + aperture)
	return aperture

def get_pbs_spots_from_beam(beam_id):
	spots_calc = \
		thinknode.function('dicom', 'get_weighted_spot_list_from_beam',
			{
				thinknode.reference(beam_id)
			})
	spots = thinknode.do_calculation(iam, spots_calc, False)
	dl.debug('spots_calc: ' + spots)
	return spots

# Takes in a thinknode id for a rt_plan and the index of the beam returns id for the range compensator associated  with that beam
#	param plan_id: The thinknode id for the rt_plan to pull the range compensator from
#	param beam_index: The index of the beam to get
#	returns the id of the range compensator from the specified rt_ion_beam
def get_range_compensator_from_beam(plan_id, beam_index):
	beam_array = thinknode.do_calc_item_property(iam, 'beams', thinknode.schema_array_named_type("rt_ion_beam"), plan_id)
	print ('beam_array: ' + beam_array)

	beam_id = thinknode.do_calc_array_item(iam, beam_index, thinknode.schema_named_type("rt_ion_beam"), beam_array)
	print ('beam_id: ' + beam_id)

	rt_rcs = thinknode.do_calc_item_property(iam, 'degraders', thinknode.schema_array_named_type('rt_ion_rangecompensator'), beam_id)
	rt_rc = thinknode.do_calc_array_item(iam, 0, thinknode.schema_named_type('rt_ion_rangecompensator'), rt_rcs)
	print ('RC: ' + rt_rc)
	return rt_rc

# Takes in a thinknode id for a rt_plan and returns id for the patient_position_type for the first patient setup sequence
#	param plan_id: The thinknode id for the rt_plan to pull the patient position from
#	returns the id of the patient_position_type from the first patient setup sequence
def get_patient_position(plan_id):
	print ('get_patient_position')
	setups_array = thinknode.do_calc_item_property(iam, 'patient_setups', thinknode.schema_array_named_type('rt_patient_setup'), plan_id)
	setup = thinknode.do_calc_array_item(iam, 0, thinknode.schema_named_type('rt_patient_setup'), setups_array)

	position = thinknode.do_calc_item_property(iam, 'position', thinknode.schema_named_type('patient_position_type'), setup)
	dl.debug('Patient Position: ' + str(position))
	return position

# Takes in a thinknode id for a dicom_patient and returns id for the rt_structure_set
#	param patient_id: The thinknode id for the dicom_patient to pull the structure set from
#	returns the id of the rt_structure_set from the patient
def get_structure_set(patient_id):
	dd_array = thinknode.do_calc_item_property(iam, 'patient', thinknode.schema_array_named_type("dicom_data"), patient_id)
	dl.debug('dd_array: ' + dd_array)

	dd_index = 0
	not_found = True

	while not_found:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dicom_data"), dd_array)
		dl.debug('dd: ' + dd)

		dd_obj = thinknode.do_calc_item_property(iam, 'dicom_obj', thinknode.schema_named_type("dicom_object"), dd)
		dl.debug('dd_obj: ' + dd_obj)

		ss = thinknode.do_calc_item_property(iam, 'structure_set', thinknode.schema_named_type("rt_structure_set"), dd_obj)
		if not ss:
			dl.debug('dd object was not a structure_set object!!')
			dd_index = dd_index + 1
		else:
			dl.debug('ss: ' + ss)
			return ss

# Takes in a thinknode id for a rt_structure_set and the index of the structure returns id for the rt_structure
#	param ss_id: The thinknode id for the rt_structure_set to pull the structure from
#	param index: The index of the structure to pull out from the structure set
#	returns the id of the rt_structure 
def get_structure_by_index(ss_id, index):
	structures = thinknode.do_calc_item_property(iam, 'structures', thinknode.schema_array_named_type("rt_structure"), ss_id)
	print('structures: ' + structures)
	structure = thinknode.do_calc_array_item(iam, index, thinknode.schema_named_type("rt_structure"), structures)

	return structure

# Takes in a thinknode id for a rt_structure and returns id for the structure_geometry for the structure
#	param s_id: The thinknode id for the rt_structure to pull the structure_geometry from
#	returns the id of the structure_geometry from the given rt_structure
def get_structure_geometry_from_structure(s_id):
	calc = \
		thinknode.function("dicom", "get_geometry_from_structure",
			[
				thinknode.reference(s_id)
			])
	res = thinknode.do_calculation(iam, calc, False)
	return res

# Takes in a thinknode id for a dicom_patient and returns id for the rt_dose
#	param patient_id: The thinknode id for the dicom_patient to pull the dose from
#	returns the id of the rt_dose from the patient
def get_dose(patient_id):
	dd_array = thinknode.do_calc_item_property(iam, 'patient', thinknode.schema_array_named_type("dicom_data"), patient_id)
	dl.debug('dd_array: ' + dd_array)

	dd_index = 0
	not_found = True

	while not_found:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dicom_data"), dd_array)
		dl.debug('dd: ' + dd)

		dd_obj = thinknode.do_calc_item_property(iam, 'dicom_obj', thinknode.schema_named_type("dicom_object"), dd)
		dl.debug('dd_obj: ' + dd_obj)

		dose = thinknode.do_calc_item_property(iam, 'dose', thinknode.schema_named_type("rt_dose"), dd_obj)
		if not dose:
			dl.debug('dd object was not a dose object!!')
			dd_index = dd_index + 1
		else:
			dl.debug('dose: ' + dose)
			return dose

# Takes in a thinknode id for a dicom_patient and returns id for the ct_image_set
#	param patient_id: The thinknode id for the dicom_patient to pull the CT image set from
#	returns the id of the ct_image_set from the patient
def get_ct_image_set(patient_id):
	dd_array = thinknode.do_calc_item_property(iam, 'patient', thinknode.schema_array_named_type("dicom_data"), patient_id)
	dl.debug('dd_array: ' + dd_array)

	dd_index = 0
	not_found = True

	while not_found:
		dd = thinknode.do_calc_array_item(iam, dd_index, thinknode.schema_named_type("dicom_data"), dd_array)
		dl.debug('dd: ' + dd)

		dd_obj = thinknode.do_calc_item_property(iam, 'dicom_obj', thinknode.schema_named_type("dicom_object"), dd)
		dl.debug('dd_obj: ' + dd_obj)

		ct_img = thinknode.do_calc_item_property(iam, 'ct_image_set', thinknode.schema_named_type("ct_image_set"), dd_obj)
		if not ct_img:
			dl.debug('dd object was not a ct_img object!!')
			dd_index = dd_index + 1
		else:
			dl.debug('ct_img: ' + ct_img)
			return ct_img
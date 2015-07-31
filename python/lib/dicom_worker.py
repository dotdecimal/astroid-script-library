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

def valid_dicom_filetype(filename):
	for ext in dicom_filetypes:
		if filename[len(filename)-len(ext):] == ext:
			return True;
	dl.error('Invalid filetype found: ' + filename)
	return False

def post_filesystem_item(item):
	res = thinknode.post_dependency_immutable(iam, "rt_types", item, 'filesystem_item')
	obj = json.loads(res.text)
	return obj['id']

def post_filesystem_item_contents(item):
	res = thinknode.post_dependency_immutable(iam, "rt_types", item, 'filesystem_item_contents')
	obj = json.loads(res.text)
	return obj['id']

# Takes in a filename and reads in file in binary mode
# returns a blob of the file
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

# Takes in a filename and uploads to thinknode as filesystem_item
# Returns the id of teh filesystem_item
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
# Returns id of the filesystem_item that holds a directory of the files
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
	# dl.debug(obj_id)
	
	return obj_id

def get_dicom_dir_by_id(dir_id):
	res = thinknode.get_immutable(iam, dir_id)
	dir_obj = json.loads(res)
	return dir_obj

def make_patient_from_dir_id(dir_id):
	dir_obj = get_dicom_dir_by_id(dir_id)
	dicom_ids = []
	for file_id in dir_obj["contents"]["directory"]:
		dl.debug("File id: " + file_id)
		dicom_id = run_calc_parse_dicom_filesystem(file_id)
		dicom_ids.append(thinknode.reference(dicom_id))
	dicom_patient_array = thinknode.array_named_type('rt_types', 'dicom_data', dicom_ids)

	calc_id = run_calc_make_patient(dicom_patient_array)
	dl.debug('Make patient calc id: ' + calc_id)
	return calc_id

def make_patient_from_dir(dir_name):
	dir_id = upload_dir(dir_name)
	calc_id = make_patient_from_dir_id(dir_id)
	dl.debug('Make patient calc id: ' + calc_id)
	return calc_id

def run_calc_parse_dicom_filesystem(data_id):	
	dl.event('run_calc_parse_dicom_filesystem')
	calc = \
		thinknode.function(app_name, "parse_dicom_filesystem_item",
			[
				thinknode.reference(data_id)
			])

	res = thinknode.do_calculation(iam, calc, False)
	# dl.debug_data('run_calc_parse_dicom_filesystem results', res)
	return res

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

def get_structure_by_index(ss_id, index):
	structures = thinknode.do_calc_item_property(iam, 'structures', thinknode.schema_array_named_type("rt_structure"), ss_id)

	structure = thinknode.do_calc_array_item(iam, index, thinknode.schema_named_type("rt_structure"), structures)

	return structure

def get_structure_geometry_from_structure(s_id):
	print ("s_id: " + s_id)
	# vol_obj = thinknode.do_calc_item_property(iam, 'volume', thinknode.schema_named_type("dicom_structure_geometry"), s_id)
	# sli_obj = thinknode.do_calc_item_property(iam, 'slices', thinknode.schema_array_named_type("dicom_structure_geometry"), vol_obj)
	# sg = thinknode.do_calc_structure(iam, thinknode.schema_named_type("structure_geometry"), 
	# 		{
	# 			"slices": thinknode.reference(res)
	# 		})

	calc = \
		thinknode.function("dicom", "get_geometry_from_structure",
			[
				thinknode.reference(s_id)
			])
	res = thinknode.do_calculation(iam, calc, False)
	return res


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












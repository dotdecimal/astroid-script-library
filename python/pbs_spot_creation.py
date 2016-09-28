# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Kevin Erhart, Andrew Brown
# Date:     09/16/2015
# Desc:     Create a PBS Beam with manually specified spots and Export to DICOM RT Plan

import sys, base64, json
sys.path.append(sys.path[0][0:len(sys.path[0])-13])
from lib import thinknode_worker as thinknode
from lib import dosimetry_worker as dosimetry
from lib import dicom_worker as dicom

# Login/authenticate with thinknode servers
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))
iam["app_name"] = "dosimetry" # ensure app name is set correctly

def read_file(file_name):
	json_data = {}
	with open(file_name) as data_file:
		return json.load(data_file)

# Read the machine file
machine = read_file('../Machine Setup Parser/machine_setups/pbs_machine.json')

# ------ Create the PBS Spot Lists per Energy ------
start_energy = 120.
delta_energy = 3.

# Add a spot along CAX and at corners of a 3x3 box to each energy
spots_by_energy = []
for i in range(0,3):
	e = start_energy + i * delta_energy
	spots_by_energy.append([])
	spots_by_energy[i].append(dosimetry.make_spot([0.,0.], 0.5, e))
	spots_by_energy[i].append(dosimetry.make_spot([-3.,-3.], 0.5, e))
	spots_by_energy[i].append(dosimetry.make_spot([-3., 3.], 0.5, e))
	spots_by_energy[i].append(dosimetry.make_spot([ 3., 3.], 0.5, e))
	spots_by_energy[i].append(dosimetry.make_spot([ 3.,-3.], 0.5, e))


# Create Plan will read an existing DICOM Plan file (the first beam will be 
# modified to include the new spot list and meterset_weight, all other items 
# of the beam will remain intact; no ther beams will be modified)
# Set the Directory where file is located
plan_file_path = '../temp/PlanFile/' # Directory, not file
# Set the desired file name (full path) for the output (resulting) plan file
output_file = '../temp/PlanOut/Plan.dcm' # Desired Output File name

# Create a study from a directory, if you already have a study id you can set that here
study_id = dicom.make_rt_study_from_dir(iam, plan_file_path)

# Generate the new plan
res = dosimetry.create_plan(iam, study_id, machine, spots_by_energy)
plan_data = thinknode.get_immutable(iam, "dosimetry", res, False)

stream = open(output_file, 'wb')
stream.write(base64.b64decode(plan_data["blob"]))
stream.close()


print("Done. File written to: " + output_file)
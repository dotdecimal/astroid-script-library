# Copyright (c) 2018 .decimal, LLC. All rights reserved.
# Author:   Christopher Waugh & Kevin Erhart
# Date:     10/11/2018
# Desc:     Copies Astroid Planning App "imported_dicom_file" records from one bucket to another.
#           Also, copies all immutable references contained within these records.

import os.path
import sys
sys.path.append('../lib')
import copy
import thinknode_worker as tn
import dicom_worker as dicom_worker
import rks_worker as rks


src_rks_id = 'RKS ID of record to be copied'
app_name = 'planning'
src_config = tn.read_config('../thinknode.cfg') # Config file with src realm info
dest_realm = 'destination realm name'


# --- Should not need to edit below this line -----

iam_src = tn.authenticate(src_config)
dest_config = copy.deepcopy(src_config)
dest_config['realm_name'] = dest_realm
iam_dest = tn.authenticate(dest_config)

# Main Code
src_bucket = tn.get_bucket_for_realm(iam_src)
dest_bucket = tn.get_bucket_for_realm(iam_dest)
original_record = rks.get_rks_entry(iam_src, src_rks_id, app_name)
print(original_record)
result = rks.copy_record_recursively(iam_src, iam_dest, None, original_record, src_bucket, dest_bucket, app_name)
print('Final RKS ID: ' + str(result))

# Copy the immutable object from the src realm too
record_immutable = tn.get_immutable(iam_src, app_name, original_record['immutable'], False)
dicom_obj_id = record_immutable["dicom_obj"]["some"]
new_obj_id = tn.iss_object_copy(iam_src, dicom_obj_id, src_bucket, dest_bucket)

if record_immutable["meta_data"]["modality"] == "ct":
    ct_obj = tn.get_immutable(iam_src, app_name, dicom_obj_id, False)
    i = 0
    for s in ct_obj["ct_image"]["image_slices"]:
        orig_id = s["slice"]["content"]["img"]["pixel_ref"]
        new_id = tn.iss_object_copy(iam_src, orig_id, src_bucket, dest_bucket)
        i += 1
    print("Copied CT slices: " + str(i))
elif record_immutable["meta_data"]["modality"] == "rtstruct":
    ss_obj = tn.get_immutable(iam_src, app_name, dicom_obj_id, False)
    i = 0
    for s in ss_obj["structure_set"]["structures"]["ref_structure_list"]:
        new_id = tn.iss_object_copy(iam_src, s, src_bucket, dest_bucket)
        i += 1
    print("Copied Structures: " + str(i))
# Copyright (c) 2018 .decimal, LLC. All rights reserved.
# Author:   Christopher Waugh
# Date:     10/11/2018
# Desc:     Copy a record and its object from one realm to another. Does the same for its 
#           child records and their data recursively
#           (does NOT copy obj_references with record data).

import os.path
import sys
import requests
import copy
import lib.thinknode_worker as tn
import lib.dicom_worker as dicom_worker
import lib.rks_worker as rks


src_rks_id = 'RKS ID of record to be copied'
app_name = 'planning'
src_config = tn.read_config('thinknode.cfg') # Config file with src realm info
dest_realm = 'destination realm name'


# --- Should not need to edit below this line -----

iam_src = tn.authenticate(src_config)
dest_config = copy.deepcopy(src_config)
dest_config['realm_name'] = dest_realm
iam_dest = tn.authenticate(dest_config)

# Copies a record and its object from one realm to another. Does the same for its 
#   child records recursively.
def record_copy_helper(iam_src, iam_dest, parent_id, original_record, a, b):
    # Create a copy of the original object for the new record
    duplicate_object_id = tn.iss_object_copy(iam_src, original_record['immutable'],  a, b)
    print('Copied object: ' + str(duplicate_object_id))
    # Create the new record based on the old record and the copied immutable
    rks_id = rks.write_rks_entry(iam_dest, original_record['record']['name'], duplicate_object_id, original_record['name'], parent_id)
    print('New RKS ID: ' + str(rks_id))
    # Recursively copy the children
    children = rks.get_rks_entry_children(iam_src, original_record['id'], app_name, "false")
    for child in children:
        record_copy_helper(iam_src, iam_dest, rks_id, child, a, b)
    return duplicate_object_id


# Main Code
src_bucket = tn.get_bucket_for_realm(iam_src)
dest_bucket = tn.get_bucket_for_realm(iam_dest)
original_record = rks.get_rks_entry(iam_src, src_rks_id, app_name)
print(original_record)
result = record_copy_helper(iam_src, iam_dest, None, original_record, src_bucket, dest_bucket)
print('Final RKS ID: ' + str(result))

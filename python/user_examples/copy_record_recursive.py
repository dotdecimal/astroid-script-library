# Copyright (c) 2018 .decimal, LLC. All rights reserved.
# Author:   Christopher Waugh
# Date:     10/11/2018
# Desc:     Copy a record and its object from one realm to another. Does the same for its 
#           child records and their data recursively
#           (does NOT copy obj_references with record data).

import os.path
import sys
sys.path.append('../lib')
import copy
import thinknode_worker as tn
import dicom_worker as dicom_worker
import rks_worker as rks


# src_rks_id = 'RKS ID of record to be copied'
# app_name = 'planning'
# src_config = tn.read_config('../thinknode.cfg') # Config file with src realm info
# dest_realm = 'destination realm name'


src_rks_id = '5b7d65cb01807ff0332ab01801974fcf' #'RKS ID of record to be copied'
app_name = 'planning'
src_config = tn.read_config('../thinknode.cfg') # Config file with src realm info
dest_realm = 'z-kburnett'# 'destination realm name'

# --- Should not need to edit below this line -----

iam_src = tn.authenticate(src_config)
dest_config = copy.deepcopy(src_config)
dest_config['realm_name'] = dest_realm
iam_dest = tn.authenticate(dest_config)

src_bucket = tn.get_bucket_for_realm(iam_src)
dest_bucket = tn.get_bucket_for_realm(iam_dest)
original_record = rks.get_rks_entry(iam_src, src_rks_id, app_name)
print(original_record)
result = rks.copy_record_recursively(iam_src, iam_dest, None, original_record, src_bucket, dest_bucket, app_name)
print('Final RKS ID: ' + str(result))

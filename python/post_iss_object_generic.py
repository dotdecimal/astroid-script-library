# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Bottomley
# Date:     01/09/2015
# Desc:     Post an immutable json object to the thinknode framework


import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import json

iss_dir = "iss_files"
json_iss_file = "lucite.json"
obj_name = "proton_material_properties"

# Get IAM ids
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))
 
# App object to post to iss
with open(iss_dir + '/' + json_iss_file) as data_file:
    json_data = json.load(data_file)

# Post immutable object to ISS
res = thinknode.post_immutable_named(iam, "dosimetry", json_data, obj_name, False)


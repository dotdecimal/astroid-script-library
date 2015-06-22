# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Bottomley
# Date:     01/09/2015
# Desc:     Post an immutable json object to the thinknode framework

from lib import thinknode_worker as thinknode
from lib import decimal_logging as dl
import requests
import json

iss_dir = "iss_files"
json_iss_file = "aperture_creation_params.json"
obj_name = "aperture_creation_params"

# Get IAM ids
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))
 
# App object to post to iss
with open(iss_dir + '/' + json_iss_file) as data_file:
    json_data = json.load(data_file)

# Post immutable object to ISS
res = thinknode.post_immutable(iam, json_data, obj_name)    
dl.data("Immutable id: ", res.text)


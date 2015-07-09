# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Bottomley
# Date:     01/09/2015
# Desc:     Post a json calculation request to the thinknode framework

from lib import thinknode_worker as thinknode
from lib import decimal_logging as dl
import requests
import json

request_dir = "request_files"
json_calc_file = "compute_aperture.json"

# Get IAM ids
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

# App calculation request
with open(request_dir + '/' + json_calc_file) as data_file:
    json_data = json.load(data_file)

# Send calc request and wait for answer
res = thinknode.do_calculation(iam, json_data, True)
# dl.data("Calculation Result: ", res.text)

# thinknode.clear_calculations()
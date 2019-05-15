# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Bottomley
# Date:     01/09/2015
# Desc:     Post a json calculation request to the thinknode framework
import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import dosimetry_worker as dosimetry
import decimal_logging as dl
import json
import rt_types as rt

# Get IAM ids
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))
box = rt.box_3d()

box.size = [10.,10.,10.]
box.corner = [0.,0.,0.]

input_list = [(1.23, 1.54, 1.1234124),(100., 100., 100.),(10., 10., 10.),(1., 11., 15.),(2., 2., 2.),(3., 3., 3.)]

#json_box = json.dumps(box)
#print(json_box)

run_json = \
	thinknode.function(iam["account_name"], "dosimetry", "filter_points_by_box",
        [
            thinknode.value(box.expand_data()),
            thinknode.value(input_list),
            
        ])


# App calculation request
#with open(request_dir + '/' + json_calc_file) as data_file:
#   json_data = json.load(data_file)

# Send calc request and wait for answer
#thinknode.do_calculation
res = thinknode.do_calculation(iam, run_json)
print(type(res))
dl.data("Calculation Result: ", str(res))
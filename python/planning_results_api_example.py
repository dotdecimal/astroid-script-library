# Copyright (c) 2017 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     07/18/2017
# Desc:     Example script for calling a Planning Results API meta function

import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import decimal_logging as dl


iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

plan_iss_id = "Paste_Example_Plan_ISS_ID_Here"

# Make the meta generator request for the planning Results API
generator_request = thinknode.function(iam["account_name"], "planning", "generate_plan_summary_request", 
    [
            thinknode.reference(plan_iss_id)
    ])

# Post the meta generator request
generator_id = thinknode.do_calculation(iam, generator_request, False)

# Post the meta calculation
result_id = thinknode.do_calculation(iam, thinknode.meta(iam["account_name"], "planning", "plan_summary", generator_id), False)

# Get the calculation result from ISS
plan_summary = thinknode.get_immutable(iam, "planning", result_id, False)

dl.data("Calculation Result: ", str(plan_summary))
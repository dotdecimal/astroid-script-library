# Copyright (c) 2017 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     07/18/2017
# Desc:     Example script for calling a Planning Results API meta function

import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import decimal_logging as dl

# Login, authenticate, and capture the Apps and Context IDs in the current realm.
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

plan_iss_id = "Paste_Example_Plan_ISS_ID_Here"

# Capture the Thinknode context ID for the currently installed Planning App
current_planning_context_id = iam["apps"]["planning"]["context_id"]

# Get the original treatment_plan from Thinknode at the current Planning App version, ignoring data upgrades
orig_plan = thinknode.get_immutable(iam, "planning", plan_iss_id, False, True)

# Submit the request to the ResultsAPI for the currently installed Planning App function and get its result
api_request = thinknode.function(iam["account_name"], "planning", "api_generate_plan_summary_request",
     [
         thinknode.value(orig_plan)
     ])
api_request_result = thinknode.do_calculation(iam, api_request, True, False, False, "planning")

# Check if the Results API was able to return a request for the Planning version that published the treatment_plan. This
# means the request could be generated for the ResultsAPI version captured in the treatment_plan.
if api_request_result["request"] != {"none": None}:
    # Set the context ID to the one returned by the Results API
    iam["apps"]["planning"]["context_id"] = api_request_result["context_id"]

    # Submit the ResultsAPI's returned request using the context ID returned by the ResultsAPI to ensure compatibility
    # with the Planning App version the treatment_plan captured.
    generator_request = api_request_result["request"]["some"]
    generator_id = thinknode.do_calculation(iam, generator_request, False, False, False, "planning")
    result_id = thinknode.do_calculation(iam, thinknode.meta_named_type(iam["account_name"], "planning", "plan_summary",
                    generator_id), False, False, False, "planning")

    # Reset the context ID to the current one in the realm
    iam["apps"]["planning"]["context_id"] = current_planning_context_id

    # Get the final useful data returned by the generated ResultsAPI request
    plan_summary = thinknode.get_immutable(iam, "planning", result_id, False)
    dl.data("Calculation Result: ", str(plan_summary))

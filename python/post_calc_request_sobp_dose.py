# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     06/09/2015
# Desc:     Post a sobp calculation request to the .decimal Dosimetry App on the thinknode framework

import json
from lib import thinknode_worker as thinknode
from lib import dosimetry_worker as dosimetry
from lib import decimal_logging as dl

# Get IAM ids
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

def make_dose_points(pointCount):
    dose_points = []
    ps = 90.0
    pe = -90.0
    delta = (pe - ps) / (pointCount - 1)
    for i in range(pointCount):
        dose_points.append([0.0, ps + i * delta, 0.0])
    return dose_points

# Manual aperture creation
def make_aperture(downstream_edge, mill_radius):
    aperture_points = []
    aperture_points.append([50.,50.])
    aperture_points.append([50.,-50.])
    aperture_points.append([-50.,-50.])
    aperture_points.append([-50.,50.])
    return dosimetry.make_aperture(iam, aperture_points, downstream_edge, mill_radius)
    
def make_target():
    return \
        thinknode.function(iam["account_name"], "dosimetry", "make_cube",
            [      
                thinknode.value([-32, -20.897, -30]),
                thinknode.value([16, -10, 30])
            ])

beam_geometry = \
    thinknode.value({
        "image_to_beam": [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], 
        "sad": [2270, 2270]
    })

def compute_aperture():
    return dosimetry.compute_aperture(iam, make_target(), beam_geometry, 20.0, 0.0, 250.5)

# Call compute_sobp_pb_dose2
dose_calc = \
    thinknode.function(iam["account_name"], "dosimetry", "compute_sobp_pb_dose2",
        [
            dosimetry.make_image_3d(iam, [-100, -100, -100], [200, 200, 200], [2, 2, 2], 1), #stopping_power_image
            thinknode.value(make_dose_points(181)), # dose_points
            beam_geometry, #beam_geometry
            dosimetry.make_grid(iam, [-75, -75], [150, 150], [2, 2]), # bixel_grid
            dosimetry.make_sobp_layers(iam, 2270.6, 152.0, 38.0),
            compute_aperture(), # aperture based on targets
            # make_aperture(100, 0), # geometric aperture
            thinknode.value([]) # degraders
        ])

# Write calc request to json file (debugging)
# with open('dump_request.json', 'w') as outfile:
#    json.dump(dose_calc, outfile)

## Perform calculation
res = thinknode.do_calculation(iam, dose_calc)
dl.data("Calculation Result: ", res)
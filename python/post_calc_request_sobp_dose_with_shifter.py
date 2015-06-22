# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Bottomley, Kevin Erhart
# Date:     06/09/2015
# Desc:     Post a sobp calculation request with a degrader to the .decimal Dosimetry App on the thinknode framework

import json
from collections import OrderedDict
from lib import thinknode_worker as thinknode
from lib import decimal_logging as dl
from lib import dosimetry_types as dt

# Get IAM ids
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

def make_grid(corner, size, spacing):
    return \
        thinknode.function("dosimetry", "make_grid_for_box_" + str(len(corner)) + "d",
            [
                thinknode.value({"corner": corner, "size": size}),
                thinknode.value(spacing)
            ])

def make_water_phantom(corner, size, spacing):
    return \
        thinknode.function("dosimetry", "create_uniform_image_on_grid_3d",
            [
                make_grid(corner, size, spacing),
                thinknode.value(1),
                thinknode.value("relative_stopping_power")
            ])

def make_dose_points(pointCount):
    dose_points = []
    ps = 90.0
    pe = -90.0
    delta = (pe - ps) / (pointCount - 1)
    for i in range(pointCount):
        dose_points.append([0.0, ps + i * delta, 0.0])
    return dose_points

def get_example_sobp_machine(id):
    return \
        thinknode.function("dosimetry", "get_example_sobp_machine",
            [
                thinknode.value(id),
            ])

def make_layers(sad, range, mod):
    return \
        thinknode.function("dosimetry", "compute_double_scattering_layers",
            [
                #get_example_sobp_machine(0),
                thinknode.reference("557b40b1ee000020000c"),
                thinknode.value(sad),
                thinknode.value(range),
                thinknode.value(mod)
            ])

# Manual aperture creation
def make_aperture(downstream_edge, mill_radius):
    aperture_points = []
    aperture_points.append([50.,50.])
    aperture_points.append([50.,-50.])
    aperture_points.append([-50.,-50.])
    aperture_points.append([-50.,50.])
    return \
        thinknode.function("dosimetry", "make_aperture",
            [
                thinknode.value(aperture_points),
                thinknode.value(downstream_edge),
                thinknode.value(mill_radius)
            ])

def make_target():
    return \
        thinknode.function("dosimetry", "make_cube",
            [      
                thinknode.value([-32, -20, -30]),
                thinknode.value([16, -10, 30])
            ])

def make_view():
    mv = dt.multiple_source_view()
    ds = {}
    ds['corner'] = [-100, -100]
    ds['size'] = [200, 200]
    mv.display_surface = ds
    mv.center = [0, 0, 0]
    mv.direction = [0, 1, 0]
    mv.distance = [2270, 2270]
    mv.up = [0, 0, 1]

    return mv.out()

def compute_aperture():
    ap_params = dt.aperture_creation_params()

    ap_params.targets.append(make_target())
    ap_params.target_margin = 20.0
    ap_params.view = make_view()
    ap_params.mill_radius = 0.0
    ap_params.downstream_edge = 250.0

    # Make aperture_creation_params
    args = {}
    args["targets"] = thinknode.array_named_type("dosimetry", "triangle_mesh", ap_params.targets)
    args["target_margin"] = thinknode.value(ap_params.target_margin)
    args["view"] = thinknode.value(ap_params.view)
    args["mill_radius"] = thinknode.value(ap_params.mill_radius)
    args["organs"] = thinknode.value(ap_params.organs)
    args["half_planes"] = thinknode.value(ap_params.half_planes)
    args["corner_planes"] = thinknode.value(ap_params.corner_planes)
    args["centerlines"] = thinknode.value(ap_params.centerlines)
    args["overrides"] = thinknode.value(ap_params.overrides)
    args["downstream_edge"] = thinknode.value(ap_params.downstream_edge)

    return \
        thinknode.function("dosimetry", "compute_aperture",
            [
                thinknode.structure_named_type("dosimetry", "aperture_creation_params", args)
            ])

beam_geometry = \
    thinknode.value({
        "image_to_beam": [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], 
        "sad": [2270, 2270]
    })

# Lucite
material = \
    {
       "density": 1.150,
       "theta_curve": {
          "outside_domain_policy": "extend_with_copies",
          "samples": {
             "blob": "bvDPVm8eaD8AMxOxLaj0PtQWMrK/R2g/AIEV8ecl8D7WQRSCC2hoPwBEHOviNuo+Gl7/ZEKCaD8Ax+4CJQXmPuFMAopHmGg/AJ43XzZL4z5/hGHAkqtoPwDTizW3neE+UhCXdzC9aD8AHlVNEHXfPuG6vf/qzGg/AKInZVJD2z6yTvCojNpoPwC8UdCSbNo+kHdY8sLnaD8ADNARVOjXPpZfYRy382g/AFxOUxVk1T7EBgsnaf5oPwBq44i1+NQ+eXjPgeUIaT8AnjdfNkvTPkgU/xyLEmk/ALhhynZ00j4kRWRYxRtpPwDgIGtXMtE+lNUZhF4kaT8A/ErWl1vQPhL7BFCMLGk/ACjqgrAJzz6ctSW8TjRpPwBgPlkxXM0+NAV8yKU7aT8AfGjEcYXMPlMf7STHQmk/AMjmBTMByj4Fma5xR0lpPwCwvJry18o+MUhVbv1PaT8AADvcs1PIPvFWTFsSVmk/ABhlR/R8xz43MF6Y8VtpPwAYZUf0fMc+fQlw1dBhaT8AULkddc/FPtF3t7JEZ2k/AGjjiLX4xD6rsBnggmxpPwCEDfT1IcQ+DLSWXYtxaT8AhA309SHEPm23E9uTdmk/AJw3XzZLwz5UhauoZntpPwC8Ycp2dMI+wx1exgOAaT8A0Is1t53BPreAKzRrhGk/APC1oPfGwD4zrhPynIhpPwDQizW3ncE+JxHhXwSNaT8A8LWg98bAPqM+yR02kWk/AEAU7vAyvj4rAed7/JRpPwAQwBdw4L8+LfnpifiYaT8ASBTu8DK+Pra7B+i+nGk/AEgU7vAyvj4/fiVGhaBpPwCwvJry17o+1dV4ROCjaT8AeGjEcYW8Pg==",
             "type": "base64-encoded-blob"
          },
          "x0": 2.0,
          "x_spacing": 1.0
       },
       "water_equivalent_ratio": 1.0
    }

degrade_geom = \
    thinknode.function("dosimetry", "make_shifter", 
        [
            thinknode.value(18), # thickness
            thinknode.value("mm"), # units
            thinknode.value(200) # downstream edge
        ])

res1 = thinknode.do_calculation(iam, degrade_geom, True)

proton_degr = \
    {
        "geometry": json.loads(res1.text),
        "material": material
    }

# Call compute_sobp_pb_dose2
dose_calc = \
    thinknode.function("dosimetry", "compute_sobp_pb_dose2",
        [
            make_water_phantom([-100, -100, -100], [200, 200, 200], [2, 2, 2]), #stopping_power_image
            thinknode.value(make_dose_points(181)), # dose_points
            beam_geometry, #beam_geometry
            make_grid([-75, -75], [150, 150], [2, 2]), # bixel_grid
            make_layers(2270.0, 152.0, 38.0),
            compute_aperture(), # aperture based on targets
            thinknode.value([proton_degr]) # degraders
        ])

## Write calc request to json file (debugging)
# with open('dump_request.json', 'w') as outfile:
#    json.dump(dose_calc, outfile)

## Load existing json calc request (debugging)
# file = open('test.json')
# calc = json.load(file)
# file.close()

## Perform calculation
res = thinknode.do_calculation(iam, dose_calc, id)
dl.data("Calculation Result: ", res.text)
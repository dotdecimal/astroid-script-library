# Copyright (c) 2018 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     05/25/2018
# Desc:     Compute pbs layers and spots for a water phantom
import json
import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import dosimetry_worker as dosimetry
import rt_types as rt
import decimal_logging as dl

# Get Identify Access Management configuration
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

# Get the pbs machine spec and post it to Thinknode Immutable Storage Service (ISS)
with open("C:/machine_R1.json") as machine_data_file:
    machine_data = json.load(machine_data_file)
machine_id = json.loads(thinknode.post_immutable_named(iam, "dosimetry", machine_data, "pbs_machine_spec", False).text)['id']

# Patient Image
water_phantom = dosimetry.make_image_3d(iam, [-100, -100, -100], [200, 200, 200], [2, 2, 2], 1)

# Construct the Beam target using the rt_types classes (this types are consistent with dosimetry app types in Thinknode)
target_box = rt.box_3d()
target_box.corner = [-30., -30., -30.]
target_box.size = [60., 60., 60.]
target = \
    thinknode.function(iam["account_name"], "dosimetry", "make_sliced_box",
        [
            thinknode.value(target_box.expand_data()),
            thinknode.value(2),
            thinknode.value(0.1),
        ])

# Calculate the Beam Geometry
beam_geometry_calc = \
    thinknode.function(iam["account_name"], "dosimetry", "construct_beam_geometry",
        [
           thinknode.value([2270, 2270]),       # SAD
           thinknode.value([0., 0., 0.]),       # Isocenter
           thinknode.value(0.),                 # Gantry Angle
           thinknode.value(0.),                 # Couch Angle
           thinknode.value("hfs")               # Patient Position
        ])
beam_geometry_result = thinknode.do_calculation(iam, beam_geometry_calc, True)
# print(beam_geometry_result)

# Calculate the Range Analysis Context
range_analysis_context = \
    thinknode.function(iam["account_name"], "dosimetry", "make_range_analysis_context",
        [
            water_phantom,
            beam_geometry_calc,
            thinknode.value([]),
        ])

# Calculate the Range Extents (this value is a dosimetry::min_max, which could be manually created from the rt_types instead of computed)
range_extents = \
    thinknode.function(iam["account_name"], "dosimetry", "compute_range_extents_from_structure_geometry",
        [
            range_analysis_context,
            target,
            thinknode.value(1),
        ])

# Compute PBS layers
layers_calc = thinknode.function(iam["account_name"], 'dosimetry', "create_pbs_layers_for_target",
    [
        thinknode.reference(machine_id),                        # Machine
        water_phantom,                                          # Patient Image
        thinknode.value([]),                                    # Degraders
        target,                                                 # Target
        thinknode.value(beam_geometry_result["image_to_beam"]), # Beam Matrix
        range_extents,                                          # Range Extents
        thinknode.value(0.8),                                   # Layer Spacing
        thinknode.value("distal_w80"),                          # Layer Strategy
        thinknode.value(1.),                                    # Flixel Spacing
        thinknode.value("sigma"),                               # Flixel Strategy
        thinknode.value(10.),                                   # Lateral Margin
        thinknode.value(10.),                                   # Distal Margin
        thinknode.value(0)                                      # Gantry Angle
    ])
# print(layers_calc)
layers_calc_id = thinknode.do_calculation(iam, layers_calc, False) # Submit the calculation, but don't wait for it to finish

# Get spots from the pbs layers
spots_calc = thinknode.function(iam["account_name"], 'dosimetry', "extract_calculation_spots",
    [
        thinknode.reference(layers_calc_id),
    ])

# Method 1 and 2 below are equivalent. Method 1 posts the calculation, waits for the result, and returns the result data.
# The second method posts the calc, gets the calculation ID and then manually pulls the immutable object down using the
# resulting calc ID. They are added separately for a more granular example of the functionality provided in the scripts.
# Note: calculation resuslts are 'cached' locally in the 'calculations' folder. The results of each calculation are stored by
# the Thinknode calc ID. So instead of having to manually write the results to file file, you can grab the file from the
# cached calculations folder.

# Method 1
# spots_result = thinknode.do_calculation(iam, spots_calc, True)

# Method 2
spot_calc_id = thinknode.do_calculation(iam, spots_calc, False)
dl.alert("Spot Calc ID: " + spot_calc_id)
spots_result = thinknode.get_immutable(iam, "dosimetry", spot_calc_id, True)

print(spots_result[0])
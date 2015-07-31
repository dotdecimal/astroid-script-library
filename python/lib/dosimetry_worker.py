# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown
# Date:     07/10/2015
# Desc:     Worker to perform common dosimetry calculations

import os.path
import binascii
import lib.thinknode_worker as thinknode
import lib.decimal_logging as dl
import lib.rt_types as rt_types



# Makes a funciton representation of an grid at the given location with given size and spacing
#   param corner: lower left corner of the grid
#   param size: size of the grid
#   param spacing: spacing between the points in the grid
def make_grid(corner, size, spacing):
    return \
        thinknode.function("dosimetry", "make_grid_for_box_" + str(len(corner)) + "d",
            [
                thinknode.value({"corner": corner, "size": size}),
                thinknode.value(spacing)
            ])

# Makes a funciton representation of an image_3d at the given location with given size and pixel spacing and pixel value
#   param corner: lower left corner of the image
#   param size: size of the image
#   param spacing: spacing between the points in the image
#   param v: value for the pixels in the image
def make_image_3d(corner, size, spacing, v):
    return \
        thinknode.function("dosimetry", "create_uniform_image_on_grid_3d",
            [
                make_grid(corner, size, spacing),
                thinknode.value(v),
                thinknode.value("relative_stopping_power")
            ])

# Computes a gamma index values to compare 2 doses
#   param dose_id: thinknode id of dose
#   param ref_dose_id: thinknode id of the reference dose
#   param value_tolerance: Allowable dose difference between matching points on the actual and reference image
#   param spatial_tolerance: Allowable distance-to-agreement (DTA) value, where DTA is the distance from a 
#									reference point to the nearest point in the actual image the has the same 
#									dose as the reference point
def dose_comparison(dose_id, ref_dose_id, value_tolerance, spatial_tolerance):
	dose_compare_calc = \
	    thinknode.function("dosimetry", "compute_gamma_index_values_3d ",
	        [
	        	thinknode.reference(dose_id),
	        	thinknode.reference(ref_dose_id),
	        	thinknode.value(value_tolerance),
	        	thinknode.value(spatial_tolerance)
	    	])
	return dose_compare_calc












# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown, Kevin Erhart, Daniel Patenaude
# Date:     07/10/2015
# Modified: 09/25/2015
# Desc:     Worker to perform common dosimetry calculations

import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import decimal_logging as dl
import rt_types as rt_types
import json, copy, math

#####################################################################
# Device functions
#####################################################################

# Makes a funciton representation to constructs an aperture for a given target structure mesh
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param target: triangle_mesh object defining the beam target structure (must be thinknode ready, as ref, value, or function)
#   param beam: beam_geometry object defining the beam position information (must be thinknode ready, as ref, value, or function)
#   param margin: distance for aperture target structure margin (mm)
#   param mill_radius: radial size of the milling tool that will be used to machine the aperture (mm)
#   param downstream_edge: distance from the aperture downstream face to the isocenter (mm)
def compute_aperture(iam, target, beam, margin, mill_radius, downstream_edge):
    dl.debug("compute_aperture")
    # Make aperture_creation_params
    ap_params = rt_types.aperture_creation_params()
    ap_params.targets.append(target)
    args = {}
    args["targets"] = thinknode.array_named_type("dosimetry", "triangle_mesh", ap_params.targets)
    args["target_margin"] = thinknode.value(margin)
    args["mill_radius"] = thinknode.value(mill_radius)
    args["organs"] = thinknode.value(ap_params.organs)
    args["half_planes"] = thinknode.value(ap_params.half_planes)
    args["corner_planes"] = thinknode.value(ap_params.corner_planes)
    args["centerlines"] = thinknode.value(ap_params.centerlines)
    args["overrides"] = thinknode.value(ap_params.overrides)
    args["downstream_edge"] = thinknode.value(downstream_edge)

    return \
        thinknode.function(iam["account_name"], "dosimetry", "compute_aperture",
            [
                thinknode.structure_named_type("dosimetry", "aperture_creation_params", args),
                beam
            ])

# Makes a function representation to construct an aperture for a given target structure mesh reference list
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param target: triangle_mesh reference defining the beam target structure (must be thinknode ready, as ref, value, or function)
#   param beam: beam_geometry object defining the beam position information (must be thinknode ready, as ref, value, or function)
#   param margin: distance for aperture target structure margin (mm)
#   param mill_radius: radial size of the milling tool that will be used to machine the aperture (mm)
#   param downstream_edge: distance from the aperture downstream face to the isocenter (mm)
def compute_aperture_ref(iam, target, beam, margin, mill_radius, downstream_edge):
    dl.debug("compute_aperture_ref")
    ap_params = rt_types.aperture_creation_params()
    ap_params.targets.append(target)
    args = {}
    args["targets"] = thinknode.array_referenced_named_type("dosimetry", "triangle_mesh", ap_params.targets)
    args["target_margin"] = thinknode.value(margin)
    args["mill_radius"] = thinknode.value(mill_radius)
    args["organs"] = thinknode.value([])
    args["half_planes"] = thinknode.value([])
    args["corner_planes"] = thinknode.value([])
    args["centerlines"] = thinknode.value([])
    args["overrides"] = thinknode.value([])
    args["downstream_edge"] = thinknode.value(downstream_edge)

    aper_calc = \
        thinknode.function(iam["account_name"], "dosimetry", "compute_aperture",
            [
                thinknode.structure_named_type("dosimetry", "aperture_creation_params", args),
                beam
            ])
    print("Compute Aperture2: " + str(aper_calc))
    res = thinknode.do_calculation(iam, aper_calc)
    # print("COmpute Aperture2: " + str(res))
    return res 

# Makes a structure representation of a beam_properties data_type
def make_beam_properties(geometry, field_size, ssd, bixel_grid, r90, index):
    dl.debug("make_beam_properties")
    args = {}
    args["geometry"] = geometry
    args["field"] = field_size
    args["ssd"] = ssd
    args["bixel_grid"] = bixel_grid
    args["range"] = r90
    args["beam_index"] = index
    return args

# Makes a structure representation of a rc_opt_properties data_type
def make_rc_opt_properties(target_distal, target_inner, iter_count, smear_w, smear_s, shift_direction):
    dl.debug("make_rc_opt_properties")
    args = {}
    args["target_distal_dose"] = target_distal
    args["target_inner_border"] = target_inner
    args["iteration_count"] = iter_count
    args["smear_weight"] = smear_w
    args["smear_span"] = smear_s
    args["shift_direction"] = shift_direction
    args["dose_grid"] = {'none': None}
    args["current_dose"] = {'none': None}
    args["patch_distal_dose"] = {'none': None}
    return args

# Manual aperture creation based on a list of points
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param points: array of points to construct the aperture polyset from
#   param downstream_edge: distance from the aperture downstream face to the isocenter (mm)
#   param mill_radius: radial size of the milling tool that will be used to machine the aperture (mm)
def make_aperture(iam, points, downstream_edge, mill_radius):
    dl.debug("make_aperture")
    return \
        thinknode.function(iam["account_name"], "dosimetry", "make_aperture",
            [
                thinknode.value(points),
                thinknode.value(downstream_edge),
                thinknode.value(mill_radius)
            ])

#####################################################################
# Image functions
#####################################################################

# Makes a funciton representation for computing gamma index values to compare 2 doses
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param dose_id: thinknode id of dose
#   param ref_dose_id: thinknode id of the reference dose
#   param value_tolerance: Allowable dose difference between matching points on the actual and reference image
#   param spatial_tolerance: Allowable distance-to-agreement (DTA) value, where DTA is the distance from a 
#                                   reference point to the nearest point in the actual image the has the same 
#                                   dose as the reference point
def dose_comparison(iam, dose_id, ref_dose_id, value_tolerance, spatial_tolerance):
    dl.debug("dose_comparision")
    dose_compare_calc = \
        thinknode.function(iam["account_name"], 'dosimetry', "compute_gamma_index_values_3d",
            [
                thinknode.reference(dose_id),
                thinknode.reference(ref_dose_id),
                thinknode.value(value_tolerance),
                thinknode.value(spatial_tolerance)
            ])
    return dose_compare_calc

# Makes a function representation of an grid at the given location with given size and spacing
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param corner: lower left corner of the grid
#   param size: size of the grid
#   param spacing: spacing between the points in the grid
def make_grid(iam, corner, size, spacing):
    dl.debug("make_grid")
    return \
        thinknode.function(iam["account_name"], 'dosimetry', "make_grid_for_box_" + str(len(corner)) + "d",
            [
                thinknode.value({"corner": corner, "size": size}),
                thinknode.value(spacing)
            ])

# Defines a grid at the given location with given size and spacing
#   param p0: lower left point of the grid (position of the first grid point)
#   param n_points: number of  points in the grid
#   param spacing: spacing between the points in the grid
def define_grid(p0, n_points, spacing):
    dl.debug("define_grid")
    return {"p0": p0, "n_points": n_points, "spacing": spacing}

# Make a 2d grid about the origin and spanning the size of the stopping image.
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param stopping_img: stopping image, origin and size of are used for grid
#   param spacing: spacing between the points in the grid
#   returns: 2d grid matching stopping image origin and size
def get_grid_on_image_2d(iam, stopping_img, spacing):
    dl.debug("get_grid_on_image")
    # Get image origin
    origin_id = thinknode.do_calc_item_property(iam, 'origin', thinknode.schema_array_standard_type("float_type"), stopping_img)
    origin = thinknode.get_immutable(iam, 'dicom', origin_id)
    # Get image size
    size_id = thinknode.do_calc_item_property(iam, 'size', thinknode.schema_array_standard_type("integer_type"), stopping_img)
    size = thinknode.get_immutable(iam, 'dicom', size_id)
    # Get image axes
    axes_id = thinknode.do_calc_item_property(iam, 'axes', thinknode.schema_array_array_standard_type("float_type"), stopping_img)
    axes = thinknode.get_immutable(iam, 'dicom', axes_id)
    dl.debug("image axes: " + str(axes))

    grid = make_grid(iam, [origin[0], origin[1]], [axes[0][0]*size[0], axes[1][1]*size[1]], [spacing, spacing])
    res = thinknode.do_calculation(iam, grid, False)
    return res

# Make a grid about the origin and spanning the size of the stopping image.
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param stopping_img: stopping image, origin and size of are used for grid
#   param spacing: spacing between the points in the grid
#   returns: 3d dose grid matching stopping image origin and size
def get_dose_grid(iam, stopping_img, spacing):
    dl.debug("get_dose_grid")
    # Get image origin
    origin_id = thinknode.do_calc_item_property(iam, 'origin', thinknode.schema_array_standard_type("float_type"), stopping_img, True)
    origin = thinknode.get_immutable(iam, 'dicom', origin_id)
    dl.debug("image origin: " + str(origin))
    # Get image size
    size_id = thinknode.do_calc_item_property(iam, 'size', thinknode.schema_array_standard_type("integer_type"), stopping_img, True)
    size = thinknode.get_immutable(iam, 'dicom', size_id)
    dl.debug("image size: " + str(size))
    # Get image axes
    axes_id = thinknode.do_calc_item_property(iam, 'axes', thinknode.schema_array_array_standard_type("float_type"), stopping_img, True)
    axes = thinknode.get_immutable(iam, 'dicom', axes_id)
    dl.debug("image axes: " + str(axes))

    dose_grid = make_grid(iam, origin, [axes[0][0]*size[0], axes[1][1]*size[1], axes[2][2]*size[2]], [spacing, spacing, spacing])
    res = thinknode.post_calculation(iam, dose_grid)
    return res

# Makes a funciton representation of an grid at the given location with given size and spacing
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param corner: lower left corner of the grid
#   param size: size of the grid
#   param counts: count of items for each dim
def make_grid_covering_box(iam, corner, size, counts):
    dl.debug("make_grid_covering_box")
    return \
        thinknode.function(iam["account_name"], 'dosimetry', "make_grid_covering_box_3d",
            [
                thinknode.value({"corner": corner, "size": size}),
                thinknode.value(counts)
            ])

# Makes a funciton representation of an image_3d at the given location with given size and pixel spacing and pixel value
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param corner: lower left corner of the image
#   param size: size of the image
#   param spacing: spacing between the points in the image
#   param v: value for the pixels in the image
def make_image_3d(iam, corner, size, spacing, v):
    dl.debug("make_image_3d")
    return \
        thinknode.function(iam["account_name"], 'dosimetry', "create_uniform_image_on_grid_3d",
            [
                make_grid(iam, corner, size, spacing),
                thinknode.value(v),
                thinknode.value("relative_stopping_power")
            ])

#####################################################################
# SOBP functions
#####################################################################

def make_sobp_layers(iam, sad, range, mod):
    dl.debug("make_sobp_layers")
    return \
        thinknode.function(iam["account_name"], "dosimetry", "compute_double_scattering_layers",
            [
                thinknode.reference(tn_id.sobp_machine()), # SOBP Machine from ISS
                thinknode.value(sad),
                thinknode.value(range),
                thinknode.value(mod)
            ])

#####################################################################
# PBS functions
#####################################################################

# Spot builder function
#   param position: [x,y] position pair specified at the isocenter plane
#   param fluence: weight of this spot
#   param energy: energy of this spot
def make_spot(position, fluence, energy):
    dl.debug("make_spot")
    spot = {}
    spot["energy"] = energy
    spot["position"] = position
    spot["fluence"] = fluence
    return spot

# Sort pbs spots by energy ascending
#   param data: dictionary of pbs spots to sort
def sort_spots_by_energy(data):
    dl.debug("sort_spots_by_energy")
    d = {}
    out = []
    # Sort the data
    for i in range(0, len(data)):
        if d.get(data[i]["energy"], "") == "":
            d[data[i]["energy"]] = []
        d[data[i]["energy"]].append(data[i])
        # Combine back into single array
        ky = sorted(d.keys())
        for j in ky:
            for i in d[j]:
                out.append(i)
    return out

def get_spot_size(machine, energy):
    dl.debug("get_spot_size")
    e = 0
    i = 0
    sigmax = 100
    sigmay = 100
    while e < energy:
        e = machine["modeled_energies"][i]["energy"]
        sigmax = machine["modeled_energies"][i]["sigma"]["x"]["c"]
        sigmay = machine["modeled_energies"][i]["sigma"]["y"]["c"]
        i += 1
    return [math.sqrt(sigmax / 2), math.sqrt(sigmay / 2)]

# Get the bounding box of a specific spot
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param spot_id: spot iss id
#   returns: box_2d bounding box of the spot
def get_spot_bounding_box(spots):
    dl.debug("get_spot_bounding_box")

    x_min = 9999
    x_max = -9999
    y_min = 9999
    y_max = -9999

    for spot in spots:
        if (spot['position'][0] < x_min):
            x_min = spot['position'][0]
        if (spot['position'][1] < y_min):
            y_min = spot['position'][1]
        if (spot['position'][0] > x_max):
            x_max = spot['position'][0]
        if (spot['position'][1] > y_max):
            y_max = spot['position'][1]

    x_size = x_max-x_min
    y_size = y_max-y_min

    box = rt_types.box_2d()
    box.corner = [x_min, y_min]
    box.size = [x_size, y_size]
    print(str(box.expand_data()))

    return box.expand_data()

# Make a bixel grid over the spot spot bounding box
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param spots: spot iss id
#   param spacing: spacing between the points in the grid
def get_pbs_bixel_grid(iam, spot_id, spacing):
    dl.debug("get_pbs_bixel_grid")
    spots = thinknode.get_immutable(iam, 'dicom', spot_id)
    box = get_spot_bounding_box(spots)

    bixel_grid = thinknode.function(iam["account_name"], "dosimetry", "make_grid_for_box_2d",
            [
                thinknode.value(box),
                thinknode.value([spacing, spacing])
            ])
    res = thinknode.do_calculation(iam, bixel_grid, False)
    return res  

# Makes a structure representation of a dose_objective with the given data_type
def make_dose_objective(data_type, voxel_list):
    dl.debug("make_dose_objective")
    args = {}
    args[data_type] = voxel_list
    return args

# Makes a structure representation of a given dose_constraint data_type
def make_dose_constraint(data_type, voxel_list, dose_level):
    dl.debug("make_dose_constraint")
    sdc = {}
    sdc["voxels"] = voxel_list
    sdc["dose_level"] = dose_level
    sdc["beams"] = [1,1]
    args = {}
    args[data_type] = sdc
    return args

# Create a plan with custom defined pbs spots by energy
#   param iam: connection settings (url, user token, and ids for context and realm)
#   param study_id: thinknode id for the study that the plan will be added to
#   param machine: pbs machine config
#   param spots_by_energy: an array of energies that each contain an array of spots
#   returns: the id for a plan that contains a beam with the created spots
def create_plan(iam, study_id, machine, spots_by_energy):

    study = thinknode.get_immutable(iam, "dosimetry", study_id)

    cp = study["plan"]["beams"][0]['control_points'][0]
    cp["layer"]["spots"] = []

    cnt_pts = []
    msw = 0
    n = 0
    for spot_list in spots_by_energy:
        n += 1
        cp["layer"]["spots"] = []
        cp["layer"]["num_spot_positions"] = len(spot_list)
        cp["layer"]["num_paintings"] = 1
        cp["layer"]["spot_size"] = get_spot_size(machine, spot_list[0]["energy"])
        ms = 0
        for spot in spot_list:
            ms += spot["fluence"]
            cp["layer"]["spots"].append(spot)
        msw += ms
        cp["number"] = n
        cp["meterset_weight"] = msw
        cp["nominal_beam_energy"] = spot_list[0]["energy"]
        cnt_pts.append(copy.deepcopy(cp))

    # Overwrite the first beam control point list
    study["plan"]["beams"][0]['final_meterset_weight'] = msw
    study["plan"]["beams"][0]['control_points'] = cnt_pts


    study_res = json.loads(thinknode.post_immutable_named(iam, "dicom", study, "rt_study").text)

    # Write plan back to file
    plan_calc = thinknode.function(iam["account_name"], "dicom", "write_plan", 
        [thinknode.reference(study_res['id']), 
        thinknode.none])

    print(plan_calc)

    res = thinknode.do_calculation(iam, plan_calc, False)
    return res

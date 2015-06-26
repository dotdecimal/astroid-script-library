# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:	Travis DeMint
# Date:		06/26/2015
# Desc:		Provides access to cradle type usage for all types
# Dosimetry Version:		1.0.1.10

from collections import OrderedDict

class blob_type:

	def __init__(self):
		self.blob = ""
		self.type = "base64-encoded-blob"

	def toStr(self):
		values = OrderedDict([("blob", self.blob), 
								("type", self.type)
			])
		return values

class aperture:

	#Initialize
	def __init__(self):
		self.shape = polyset()
		self.downstream_edge = 0.0 

	def toStr(self):
		values = OrderedDict([("shape", self.shape.toStr()),
								("downstream_edge", self.downstream_edge)
			]) 
		return values 

class aperture_target:

	#Initialize
	def __init__(self):
		self.structure = triangle_mesh()
		self.margin = 0.0 

	def toStr(self):
		values = OrderedDict([("structure", self.structure.toStr()),
								("margin", self.margin)
			]) 
		return values 

class aperture_organ:

	#Initialize
	def __init__(self):
		self.structure = triangle_mesh()
		self.margin = 0.0 
		self.occlude_by_target = False 

	def toStr(self):
		values = OrderedDict([("structure", self.structure.toStr()),
								("margin", self.margin),
								("occlude_by_target", self.occlude_by_target)
			]) 
		return values 

class aperture_centerline:

	#Initialize
	def __init__(self):
		self.structure = triangle_mesh()
		self.margin = 0.0 

	def toStr(self):
		values = OrderedDict([("structure", self.structure.toStr()),
								("margin", self.margin)
			]) 
		return values 

class aperture_half_plane:

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.direction = 0.0 

	def toStr(self):
		values = OrderedDict([("origin", self.origin),
								("direction", self.direction)
			]) 
		return values 

class aperture_corner_plane:

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.first_direction = 0.0 
		self.second_direction = 0.0 

	def toStr(self):
		values = OrderedDict([("origin", self.origin),
								("first_direction", self.first_direction),
								("second_direction", self.second_direction)
			]) 
		return values 

class aperture_manual_override:

	#Initialize
	def __init__(self):
		self.shape = polyset()
		self.add_shape_to_opening = False 

	def toStr(self):
		values = OrderedDict([("shape", self.shape.toStr()),
								("add_shape_to_opening", self.add_shape_to_opening)
			]) 
		return values 

class aperture_creation_params:

	#Initialize
	def __init__(self):
		self.targets = [] 
		self.target_margin = 0.0 
		self.view = multiple_source_view()
		self.mill_radius = 0.0 
		self.organs = [] 
		self.half_planes = [] 
		self.corner_planes = [] 
		self.centerlines = [] 
		self.overrides = [] 
		self.downstream_edge = 0.0 

	def toStr(self):
		values = OrderedDict([("targets", self.targets),
								("target_margin", self.target_margin),
								("view", self.view.toStr()),
								("mill_radius", self.mill_radius),
								("organs", self.organs),
								("half_planes", self.half_planes),
								("corner_planes", self.corner_planes),
								("centerlines", self.centerlines),
								("overrides", self.overrides),
								("downstream_edge", self.downstream_edge)
			]) 
		return values 

class shifter_geometry:

	#Initialize
	def __init__(self):
		self.thickness = 0.0 

	def toStr(self):
		values = OrderedDict([("thickness", self.thickness),
			]) 
		return values 

class block_geometry:

	#Initialize
	def __init__(self):
		self.shape = polyset()
		self.thickness = 0.0 

	def toStr(self):
		values = OrderedDict([("shape", self.shape.toStr()),
								("thickness", self.thickness)
			]) 
		return values 

class rc_geometry:

	#Initialize
	def __init__(self):
		self.thickness = image_2d()

	def toStr(self):
		values = OrderedDict([("thickness", self.thickness.toStr()),
			]) 
		return values 

class rc_nurb_geometry:

	#Initialize
	def __init__(self):
		self.surface = nurb_surface()

	def toStr(self):
		values = OrderedDict([("surface", self.surface.toStr()),
			]) 
		return values 

class degrader_shape:

	#Initialize
	def __init__(self):
		self.type = ""
		self.shifter = shifter_geometry.toStr()
		self.block = block_geometry.toStr()
		self.rc = rc_geometry.toStr()
		self.rc_nurb = rc_nurb_geometry.toStr()

	def toStr(self):
		if (self.type == 'shifter'):
			values = OrderedDict([("shifter", self.shifter.toStr()),
									("type", self.type)
				]) 
			return values 
		elif (self.type == 'block'):
			values = OrderedDict([("block", self.block.toStr()),
									("type", self.type)
				]) 
			return values 
		elif (self.type == 'rc'):
			values = OrderedDict([("rc", self.rc.toStr()),
									("type", self.type)
				]) 
			return values 
		elif (self.type == 'rc_nurb'):
			values = OrderedDict([("rc_nurb", self.rc_nurb.toStr()),
									("type", self.type)
				]) 
			return values 
		else:
			return "Type not Set" 

class degrader_geometry:

	#Initialize
	def __init__(self):
		self.downstream_edge = 0.0 
		self.thickness_units = "" 
		self.scale_factor = 0.0 
		self.shape = degrader_shape()

	def toStr(self):
		values = OrderedDict([("downstream_edge", self.downstream_edge),
								("thickness_units", self.thickness_units),
								("scale_factor", self.scale_factor),
								("shape", self.shape.toStr())
			]) 
		return values 

class dij_row:

	#Initialize
	def __init__(self):
		self.offset = 0.0 
		self.n_entries = 0.0 

	def toStr(self):
		values = OrderedDict([("offset", self.offset),
								("n_entries", self.n_entries)
			]) 
		return values 

class dij_entry:

	#Initialize
	def __init__(self):
		self.beamlet_index = 0.0 
		self.dose = 0.0 

	def toStr(self):
		values = OrderedDict([("beamlet_index", self.beamlet_index),
								("dose", self.dose)
			]) 
		return values 

class dij_matrix:

	#Initialize
	def __init__(self):
		self.n_points = 0.0 
		self.n_beamlets = 0.0 
		blob = blob_type()
		self.rows = blob.toStr()
		blob = blob_type()
		self.entries = blob.toStr()

	def toStr(self):
		values = OrderedDict([("n_points", self.n_points),
								("n_beamlets", self.n_beamlets),
								("rows", self.rows),
								("entries", self.entries)
			]) 
		return values 

class projected_isocentric_vector:

	#Initialize
	def __init__(self):
		self.at_iso = [] 
		self.delta = [] 

	def toStr(self):
		values = OrderedDict([("at_iso", self.at_iso),
								("delta", self.delta)
			]) 
		return values 

class bixel_geometry:

	#Initialize
	def __init__(self):
		self.axis = projected_isocentric_vector()
		self.size = projected_isocentric_vector()

	def toStr(self):
		values = OrderedDict([("axis", self.axis.toStr()),
								("size", self.size.toStr())
			]) 
		return values 

class weighted_bixel:

	#Initialize
	def __init__(self):
		self.geometry = bixel_geometry()
		self.weight = 0.0 

	def toStr(self):
		values = OrderedDict([("geometry", self.geometry.toStr()),
								("weight", self.weight)
			]) 
		return values 

class beam_geometry:

	#Initialize
	def __init__(self):
		self.sad = [] 
		self.image_to_beam = [] 

	def toStr(self):
		values = OrderedDict([("sad", self.sad),
								("image_to_beam", self.image_to_beam)
			]) 
		return values 

class proton_material_properties:

	#Initialize
	def __init__(self):
		self.theta_curve = interpolated_function()
		self.density = 0.0 
		self.water_equivalent_ratio = 0.0 

	def toStr(self):
		values = OrderedDict([("theta_curve", self.theta_curve.toStr()),
								("density", self.density),
								("water_equivalent_ratio", self.water_equivalent_ratio)
			]) 
		return values 

class proton_degrader:

	#Initialize
	def __init__(self):
		self.geometry = degrader_geometry()
		self.material = proton_material_properties()

	def toStr(self):
		values = OrderedDict([("geometry", self.geometry.toStr()),
								("material", self.material.toStr())
			]) 
		return values 

class beam_properties:

	#Initialize
	def __init__(self):
		self.geometry = beam_geometry()
		self.field = box_2d()
		self.ssd = 0.0 
		self.bixel_grid = regular_grid_2d()
		self.range = 0.0 

	def toStr(self):
		values = OrderedDict([("geometry", self.geometry.toStr()),
								("field", self.field.toStr()),
								("ssd", self.ssd),
								("bixel_grid", self.bixel_grid.toStr()),
								("range", self.range)
			]) 
		return values 

class rc_opt_properties:

	#Initialize
	def __init__(self):
		self.target_distal_dose = 0.0 
		self.target_inner_border = 0.0 
		self.iteration_count = 0.0 
		self.smear_weight = 0.0 
		self.smear_span = 0.0 
		self.shift_direction = 0.0 

	def toStr(self):
		values = OrderedDict([("target_distal_dose", self.target_distal_dose),
								("target_inner_border", self.target_inner_border),
								("iteration_count", self.iteration_count),
								("smear_weight", self.smear_weight),
								("smear_span", self.smear_span),
								("shift_direction", self.shift_direction)
								("dose_grid", self.dose_grid),
								("current_dose", self.current_dose),
								("patch_distal_dose", self.patch_distal_dose),
			]) 
		return values 

class double_scattering_step:

	#Initialize
	def __init__(self):
		self.theta = 0.0 
		self.weight = 0.0 
		self.dR = 0.0 

	def toStr(self):
		values = OrderedDict([("theta", self.theta),
								("weight", self.weight),
								("dR", self.dR)
			]) 
		return values 

class double_scattering_option:

	#Initialize
	def __init__(self):
		self.name = "" 
		self.id = "" 
		self.min_range = 0.0 
		self.max_range = 0.0 
		self.max_mod = 0.0 
		self.wts1 = 0.0 
		self.track_length = 0.0 
		self.penumbral_source_size = 0.0 
		self.source_size_on_track = 0.0 
		self.sdm = [] 
		self.mod_correction = [] 
		self.steps = [] 
		self.bcm = [] 
		self.pristine_peak = irregularly_sampled_function()

	def toStr(self):
		values = OrderedDict([("name", self.name),
								("id", self.id),
								("min_range", self.min_range),
								("max_range", self.max_range),
								("max_mod", self.max_mod),
								("wts1", self.wts1),
								("track_length", self.track_length),
								("penumbral_source_size", self.penumbral_source_size),
								("source_size_on_track", self.source_size_on_track),
								("sdm", self.sdm),
								("mod_correction", self.mod_correction),
								("steps", self.steps),
								("bcm", self.bcm),
								("pristine_peak", self.pristine_peak.toStr())
			]) 
		return values 

class double_scattering_machine_spec:

	#Initialize
	def __init__(self):
		self.options = [] 

	def toStr(self):
		values = OrderedDict([("options", self.options),
			]) 
		return values 

class sobp_calculation_layer:

	#Initialize
	def __init__(self):
		self.depth_dose_curve = interpolated_function()
		self.initial_range = 0.0 
		self.initial_sigma = 0.0 
		self.weight = 0.0 
		self.sad = 0.0 
		self.pdd_shift = 0.0 

	def toStr(self):
		values = OrderedDict([("depth_dose_curve", self.depth_dose_curve.toStr()),
								("initial_range", self.initial_range),
								("initial_sigma", self.initial_sigma),
								("weight", self.weight),
								("sad", self.sad),
								("pdd_shift", self.pdd_shift)
			]) 
		return values 

class range_analysis_context:

	#Initialize
	def __init__(self):
		self.patient_image = image_3d()
		self.sad = [] 
		self.image_to_beam = [] 
		self.beam_to_image = [] 
		self.degraders = [] 

	def toStr(self):
		values = OrderedDict([("patient_image", self.patient_image.toStr()),
								("sad", self.sad),
								("image_to_beam", self.image_to_beam),
								("beam_to_image", self.beam_to_image),
								("degraders", self.degraders)
			]) 
		return values 

class image_1d:

	#Initialize
	def __init__(self):
		self.type_info = variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = linear_function()
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()

	def toStr(self):
		values = OrderedDict([("type_info", self.type_info.toStr()),
								("size", self.size),
								("origin", self.origin),
								("axes", self.axes),
								("value_mapping", self.value_mapping.toStr()),
								("units", self.units),
								("pixels", self.pixels)
			]) 
		return values 

class image_2d:

	#Initialize
	def __init__(self):
		self.type_info = variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = linear_function()
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()

	def toStr(self):
		values = OrderedDict([("type_info", self.type_info.toStr()),
								("size", self.size),
								("origin", self.origin),
								("axes", self.axes),
								("value_mapping", self.value_mapping.toStr()),
								("units", self.units),
								("pixels", self.pixels)
			]) 
		return values 

class image_3d:

	#Initialize
	def __init__(self):
		self.type_info = variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = linear_function()
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()

	def toStr(self):
		values = OrderedDict([("type_info", self.type_info.toStr()),
								("size", self.size),
								("origin", self.origin),
								("axes", self.axes),
								("value_mapping", self.value_mapping.toStr()),
								("units", self.units),
								("pixels", self.pixels)
			]) 
		return values 

class rgb:

	#Initialize
	def __init__(self):
		self.r = 0.0 
		self.g = 0.0 
		self.b = 0.0 

	def toStr(self):
		values = OrderedDict([("r", self.r),
								("g", self.g),
								("b", self.b)
			]) 
		return values 

class rgba:

	#Initialize
	def __init__(self):
		self.r = 0.0 
		self.g = 0.0 
		self.b = 0.0 
		self.a = 0.0 

	def toStr(self):
		values = OrderedDict([("r", self.r),
								("g", self.g),
								("b", self.b),
								("a", self.a)
			]) 
		return values 

class structure_geometry:

	#Initialize
	def __init__(self):
		self.slices = [] 

	def toStr(self):
		values = OrderedDict([("slices", self.slices),
			]) 
		return values 

class box_2d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

	def toStr(self):
		values = OrderedDict([("corner", self.corner),
								("size", self.size)
			]) 
		return values 

class regular_grid_2d:

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

	def toStr(self):
		values = OrderedDict([("p0", self.p0),
								("spacing", self.spacing),
								("n_points", self.n_points)
			]) 
		return values 

class regular_grid_3d:

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

	def toStr(self):
		values = OrderedDict([("p0", self.p0),
								("spacing", self.spacing),
								("n_points", self.n_points)
			]) 
		return values 

class triangle_mesh:

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.vertices = blob.toStr()
		blob = blob_type()
		self.faces = blob.toStr()

	def toStr(self):
		values = OrderedDict([("vertices", self.vertices),
								("faces", self.faces)
			]) 
		return values 

class min_max:

	#Initialize
	def __init__(self):
		self.min = 0.0 
		self.max = 0.0 

	def toStr(self):
		values = OrderedDict([("min", self.min),
								("max", self.max)
			]) 
		return values 

class polyset:

	#Initialize
	def __init__(self):
		self.polygons = [] 
		self.holes = [] 

	def toStr(self):
		values = OrderedDict([("polygons", self.polygons),
								("holes", self.holes)
			]) 
		return values 

class adaptive_grid:

	#Initialize
	def __init__(self):
		self.extents = box_3d()
		blob = blob_type()
		self.voxels = blob.toStr()
		blob = blob_type()
		self.volumes = blob.toStr()

	def toStr(self):
		values = OrderedDict([("extents", self.extents.toStr()),
								("voxels", self.voxels),
								("volumes", self.volumes)
			]) 
		return values 

class nurb_surface:

	#Initialize
	def __init__(self):
		self.order = [] 
		self.point_counts = [] 
		self.knots = [] 
		self.heights = [] 
		self.weights = [] 
		self.box = box_2d()

	def toStr(self):
		values = OrderedDict([("order", self.order),
								("point_counts", self.point_counts),
								("knots", self.knots),
								("heights", self.heights),
								("weights", self.weights),
								("box", self.box.toStr())
			]) 
		return values 

class triangle_mesh_with_normals:

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.vertex_positions = blob.toStr()
		blob = blob_type()
		self.vertex_normals = blob.toStr()
		blob = blob_type()
		self.face_position_indices = blob.toStr()
		blob = blob_type()
		self.face_normal_indices = blob.toStr()

	def toStr(self):
		values = OrderedDict([("vertex_positions", self.vertex_positions),
								("vertex_normals", self.vertex_normals),
								("face_position_indices", self.face_position_indices),
								("face_normal_indices", self.face_normal_indices)
			]) 
		return values 

class interpolated_function:

	#Initialize
	def __init__(self):
		self.x0 = 0.0 
		self.x_spacing = 0.0 
		blob = blob_type()
		self.samples = blob.toStr()
		self.outside_domain_policy = outside_domain_policy()

	def toStr(self):
		values = OrderedDict([("x0", self.x0),
								("x_spacing", self.x_spacing),
								("samples", self.samples),
								("outside_domain_policy", self.outside_domain_policy.toStr())
			]) 
		return values 

class polygon2:

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.vertices = blob.toStr()

	def toStr(self):
		values = OrderedDict([("vertices", self.vertices),
			]) 
		return values 

class set_operation:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# union
		# intersection
		# difference
		# xor

	def toStr(self):
		return self.name 

class slice_description:

	#Initialize
	def __init__(self):
		self.position = 0.0 
		self.thickness = 0.0 

	def toStr(self):
		values = OrderedDict([("position", self.position),
								("thickness", self.thickness)
			]) 
		return values 

class box_3d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

	def toStr(self):
		values = OrderedDict([("corner", self.corner),
								("size", self.size)
			]) 
		return values 

class regular_grid_1d:

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

	def toStr(self):
		values = OrderedDict([("p0", self.p0),
								("spacing", self.spacing),
								("n_points", self.n_points)
			]) 
		return values 

class optimized_triangle_mesh:

	#Initialize
	def __init__(self):
		self.mesh = triangle_mesh()
		self.bin_collection = bin_collection_3d()

	def toStr(self):
		values = OrderedDict([("mesh", self.mesh.toStr()),
								("bin_collection", self.bin_collection.toStr())
			]) 
		return values 

class image_geometry_1d:

	#Initialize
	def __init__(self):
		self.slicing = [] 
		self.regular_grid = regular_grid_1d()

	def toStr(self):
		values = OrderedDict([("slicing", self.slicing),
								("out_of_plane_info", self.out_of_plane_info)
								("regular_grid", self.regular_grid.toStr()),
			]) 
		return values 

class box_1d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

	def toStr(self):
		values = OrderedDict([("corner", self.corner),
								("size", self.size)
			]) 
		return values 

class image_geometry_2d:

	#Initialize
	def __init__(self):
		self.slicing = [] 
		self.regular_grid = regular_grid_2d()

	def toStr(self):
		values = OrderedDict([("slicing", self.slicing),
								("out_of_plane_info", self.out_of_plane_info)
								("regular_grid", self.regular_grid.toStr()),
			]) 
		return values 

class image_geometry_3d:

	#Initialize
	def __init__(self):
		self.slicing = [] 
		self.regular_grid = regular_grid_3d()

	def toStr(self):
		values = OrderedDict([("slicing", self.slicing),
								("out_of_plane_info", self.out_of_plane_info)
								("regular_grid", self.regular_grid.toStr()),
			]) 
		return values 

class multiple_source_view:

	#Initialize
	def __init__(self):
		self.center = [] 
		self.display_surface = box_2d()
		self.direction = [] 
		self.distance = [] 
		self.up = [] 

	def toStr(self):
		values = OrderedDict([("center", self.center),
								("display_surface", self.display_surface.toStr()),
								("direction", self.direction),
								("distance", self.distance),
								("up", self.up)
			]) 
		return values 

class irregularly_sampled_function:

	#Initialize
	def __init__(self):
		self.samples = [] 
		self.outside_domain_policy = outside_domain_policy()

	def toStr(self):
		values = OrderedDict([("samples", self.samples),
								("outside_domain_policy", self.outside_domain_policy.toStr())
			]) 
		return values 

class linear_function:

	#Initialize
	def __init__(self):
		self.intercept = 0.0 
		self.slope = 0.0 

	def toStr(self):
		values = OrderedDict([("intercept", self.intercept),
								("slope", self.slope)
			]) 
		return values 

class variant_type_info:

	#Initialize
	def __init__(self):
		self.format = pixel_format()
		self.type = channel_type()

	def toStr(self):
		values = OrderedDict([("format", self.format.toStr()),
								("type", self.type.toStr())
			]) 
		return values 

class structure_geometry_slice:

	#Initialize
	def __init__(self):
		self.position = 0.0 
		self.thickness = 0.0 
		self.region = polyset()

	def toStr(self):
		values = OrderedDict([("position", self.position),
								("thickness", self.thickness),
								("region", self.region.toStr())
			]) 
		return values 

class outside_domain_policy:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# always_zero
		# extend_with_copies

	def toStr(self):
		return self.name 

class bin_collection_3d:

	#Initialize
	def __init__(self):
		self.bounds = box_3d()
		self.grid_size = [] 
		blob = blob_type()
		self.offsets = blob.toStr()
		blob = blob_type()
		self.counts = blob.toStr()
		blob = blob_type()
		self.bins = blob.toStr()

	def toStr(self):
		values = OrderedDict([("bounds", self.bounds.toStr()),
								("grid_size", self.grid_size),
								("offsets", self.offsets),
								("counts", self.counts),
								("bins", self.bins)
			]) 
		return values 

class pixel_format:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# gray
		# rgb
		# rgba

	def toStr(self):
		return self.name 

class channel_type:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# int8
		# uint8
		# int16
		# uint16
		# int32
		# uint32
		# int64
		# uint64
		# float
		# double

	def toStr(self):
		return self.name 

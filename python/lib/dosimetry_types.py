# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:	Travis DeMint
# Date:		06/30/2015
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

class aperture_target:

	#Initialize
	def __init__(self):
		self.structure = triangle_mesh()
		self.margin = 0.0 

class aperture_organ:

	#Initialize
	def __init__(self):
		self.structure = triangle_mesh()
		self.margin = 0.0 
		self.occlude_by_target = False 

class aperture_centerline:

	#Initialize
	def __init__(self):
		self.structure = triangle_mesh()
		self.margin = 0.0 

class aperture_half_plane:

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.direction = 0.0 

class aperture_corner_plane:

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.first_direction = 0.0 
		self.second_direction = 0.0 

class aperture_manual_override:

	#Initialize
	def __init__(self):
		self.shape = polyset()
		self.add_shape_to_opening = False 

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

class shifter_geometry:

	#Initialize
	def __init__(self):
		self.thickness = 0.0 

class block_geometry:

	#Initialize
	def __init__(self):
		self.shape = polyset()
		self.thickness = 0.0 

class rc_geometry:

	#Initialize
	def __init__(self):
		self.thickness = image_2d()

class rc_nurb_geometry:

	#Initialize
	def __init__(self):
		self.surface = nurb_surface()

class degrader_shape:

	#Initialize
	def __init__(self):
		self.type = ""
		self.shifter = shifter_geometry.toStr()
		self.block = block_geometry.toStr()
		self.rc = rc_geometry.toStr()
		self.rc_nurb = rc_nurb_geometry.toStr()

class degrader_geometry:

	#Initialize
	def __init__(self):
		self.downstream_edge = 0.0 
		self.thickness_units = "" 
		self.scale_factor = 0.0 
		self.shape = degrader_shape()

class dij_row:

	#Initialize
	def __init__(self):
		self.offset = 0.0 
		self.n_entries = 0.0 

class dij_entry:

	#Initialize
	def __init__(self):
		self.beamlet_index = 0.0 
		self.dose = 0.0 

class dij_matrix:

	#Initialize
	def __init__(self):
		self.n_points = 0.0 
		self.n_beamlets = 0.0 
		blob = blob_type()
		self.rows = blob.toStr()
		blob = blob_type()
		self.entries = blob.toStr()

class projected_isocentric_vector:

	#Initialize
	def __init__(self):
		self.at_iso = [] 
		self.delta = [] 

class bixel_geometry:

	#Initialize
	def __init__(self):
		self.axis = projected_isocentric_vector()
		self.size = projected_isocentric_vector()

class weighted_bixel:

	#Initialize
	def __init__(self):
		self.geometry = bixel_geometry()
		self.weight = 0.0 

class beam_geometry:

	#Initialize
	def __init__(self):
		self.sad = [] 
		self.image_to_beam = [] 

class proton_material_properties:

	#Initialize
	def __init__(self):
		self.theta_curve = interpolated_function()
		self.density = 0.0 
		self.water_equivalent_ratio = 0.0 

class proton_degrader:

	#Initialize
	def __init__(self):
		self.geometry = degrader_geometry()
		self.material = proton_material_properties()

class beam_properties:

	#Initialize
	def __init__(self):
		self.geometry = beam_geometry()
		self.field = box_2d()
		self.ssd = 0.0 
		self.bixel_grid = regular_grid_2d()
		self.range = 0.0 

class rc_opt_properties:

	#Initialize
	def __init__(self):
		self.target_distal_dose = 0.0 
		self.target_inner_border = 0.0 
		self.iteration_count = 0.0 
		self.smear_weight = 0.0 
		self.smear_span = 0.0 
		self.shift_direction = 0.0 

class double_scattering_step:

	#Initialize
	def __init__(self):
		self.theta = 0.0 
		self.weight = 0.0 
		self.dR = 0.0 

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

class double_scattering_machine_spec:

	#Initialize
	def __init__(self):
		self.options = [] 

class sobp_calculation_layer:

	#Initialize
	def __init__(self):
		self.depth_dose_curve = interpolated_function()
		self.initial_range = 0.0 
		self.initial_sigma = 0.0 
		self.weight = 0.0 
		self.sad = 0.0 
		self.pdd_shift = 0.0 

class range_analysis_context:

	#Initialize
	def __init__(self):
		self.patient_image = image_3d()
		self.sad = [] 
		self.image_to_beam = [] 
		self.beam_to_image = [] 
		self.degraders = [] 

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

class rgb:

	#Initialize
	def __init__(self):
		self.r = 0.0 
		self.g = 0.0 
		self.b = 0.0 

class rgba:

	#Initialize
	def __init__(self):
		self.r = 0.0 
		self.g = 0.0 
		self.b = 0.0 
		self.a = 0.0 

class structure_geometry:

	#Initialize
	def __init__(self):
		self.slices = [] 

class box_2d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

class regular_grid_2d:

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

class regular_grid_3d:

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

class triangle_mesh:

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.vertices = blob.toStr()
		blob = blob_type()
		self.faces = blob.toStr()

class min_max:

	#Initialize
	def __init__(self):
		self.min = 0.0 
		self.max = 0.0 

class polyset:

	#Initialize
	def __init__(self):
		self.polygons = [] 
		self.holes = [] 

class adaptive_grid:

	#Initialize
	def __init__(self):
		self.extents = box_3d()
		blob = blob_type()
		self.voxels = blob.toStr()
		blob = blob_type()
		self.volumes = blob.toStr()

class nurb_surface:

	#Initialize
	def __init__(self):
		self.order = [] 
		self.point_counts = [] 
		self.knots = [] 
		self.heights = [] 
		self.weights = [] 
		self.box = box_2d()

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

class interpolated_function:

	#Initialize
	def __init__(self):
		self.x0 = 0.0 
		self.x_spacing = 0.0 
		blob = blob_type()
		self.samples = blob.toStr()
		self.outside_domain_policy = outside_domain_policy()

class polygon2:

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.vertices = blob.toStr()

class set_operation:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# union
		# intersection
		# difference
		# xor

class slice_description:

	#Initialize
	def __init__(self):
		self.position = 0.0 
		self.thickness = 0.0 

class box_3d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

class regular_grid_1d:

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

class optimized_triangle_mesh:

	#Initialize
	def __init__(self):
		self.mesh = triangle_mesh()
		self.bin_collection = bin_collection_3d()

class image_geometry_1d:

	#Initialize
	def __init__(self):
		self.slicing = [] 
		self.regular_grid = regular_grid_1d()

class box_1d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

class image_geometry_2d:

	#Initialize
	def __init__(self):
		self.slicing = [] 
		self.regular_grid = regular_grid_2d()

class image_geometry_3d:

	#Initialize
	def __init__(self):
		self.slicing = [] 
		self.regular_grid = regular_grid_3d()

class multiple_source_view:

	#Initialize
	def __init__(self):
		self.center = [] 
		self.display_surface = box_2d()
		self.direction = [] 
		self.distance = [] 
		self.up = [] 

class irregularly_sampled_function:

	#Initialize
	def __init__(self):
		self.samples = [] 
		self.outside_domain_policy = outside_domain_policy()

class linear_function:

	#Initialize
	def __init__(self):
		self.intercept = 0.0 
		self.slope = 0.0 

class variant_type_info:

	#Initialize
	def __init__(self):
		self.format = pixel_format()
		self.type = channel_type()

class structure_geometry_slice:

	#Initialize
	def __init__(self):
		self.position = 0.0 
		self.thickness = 0.0 
		self.region = polyset()

class outside_domain_policy:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# always_zero
		# extend_with_copies

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

class pixel_format:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# gray
		# rgb
		# rgba

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

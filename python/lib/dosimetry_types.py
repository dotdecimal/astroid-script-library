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

class filesystem_item_contents:

	#Initialize
	def __init__(self):
		self.type = ""
		self.directory = []
		self.file = blob_type()

class filesystem_item:

	#Initialize
	def __init__(self):
		self.name = "" 
		self.contents = filesystem_item_contents()

class dicom_element:

	#Initialize
	def __init__(self):
		self.name = "" 
		self.value = "" 
		self.g = 0.0 
		self.e = 0.0 

class dicom_sequence:

	#Initialize
	def __init__(self):
		self.items = [] 
		self.g = 0.0 
		self.e = 0.0 

class dicom_item:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 

class rt_study:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.study_date = "" 
		self.description = "" 
		self.physician_name = "" 
		self.id = "" 
		self.accession_number = "" 

class patient_position_type:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# HFS
		# HFP
		# FFS
		# FFP
		# HFDR
		# HFDL
		# FFDR
		# FFDL

class person_name:

	#Initialize
	def __init__(self):
		self.family_name = "" 
		self.given_name = "" 
		self.middle_name = "" 
		self.prefix = "" 
		self.suffix = "" 

class patient_sex:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# M
		# F
		# O

class patient:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.name = person_name()
		self.id = "" 
		self.sex = patient_sex()
		self.other_names = [] 
		self.other_ids = [] 
		self.ethnic_group = "" 
		self.comments = "" 

class rt_control_point:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.number = 0.0 
		self.meterset_weight = 0.0 
		self.nominal_beam_energy = 0.0 
		self.gantry_angle = 0.0 
		self.gantry_pitch_angle = 0.0 
		self.beam_limiting_device_angle = 0.0 
		self.patient_support_angle = 0.0 
		self.meterset_rate = 0.0 
		self.source_to_surface_distance = 0.0 
		self.snout_position = 0.0 
		self.iso_center_position = [] 
		self.surface_entry_point = [] 
		self.gantry_rotation_direction = "" 
		self.gantry_pitch_direction = "" 
		self.beam_limiting_direction = "" 
		self.patient_support_direction = "" 
		self.table_top_pitch_angle = 0.0 
		self.table_top_roll_angle = 0.0 
		self.table_top_pitch_direction = "" 
		self.table_top_roll_direction = "" 

class rt_mounting_position:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# PATIENT_SIDE
		# SOURCE_SIDE
		# DOUBLE_SIDED

class rt_ion_rangecompensator:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.name = "" 
		self.number = 0.0 
		self.material = "" 
		self.divergent = False 
		self.mounting_position = rt_mounting_position()
		self.downstream_edge = 0.0 
		self.column_offset = 0.0 
		self.relative_stopping_power = 0.0 
		self.position = [] 
		self.pixelSpacing = [] 
		self.data = image_2d()

class rt_ion_block_type:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# APERTURE
		# SHIELDING

class rt_ion_block:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.name = "" 
		self.description = "" 
		self.material = "" 
		self.number = 0.0 
		self.divergent = False 
		self.downstream_edge = 0.0 
		self.thinkness = 0.0 
		self.position = rt_mounting_position()
		self.block_type = rt_ion_block_type()
		self.data = polyset()

class rt_snout:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.id = "" 
		self.accessoryCode = "" 

class rt_radiation_type:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# PROTON
		# PHOTON
		# ELECTRON
		# NEUTRON

class rt_ion_beam_type:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# STATIC
		# DYNAMIC

class rt_ion_beam:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.beam_number = 0.0 
		self.name = "" 
		self.description = "" 
		self.treatment_machine = "" 
		self.primary_dosimeter_unit = "" 
		self.treatment_delivery_type = "" 
		self.beam_type = rt_ion_beam_type()
		self.radiation_type = rt_radiation_type()
		self.referenced_patient_setup = 0.0 
		self.referenced_tolerance_table = 0.0 
		self.virtual_sad = [] 
		self.final_meterset_weight = 0.0 
		self.snouts = [] 
		self.block = rt_ion_block()
		self.degraders = [] 
		self.control_points = [] 

class rt_dose_reference:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.number = 0.0 
		self.uid = "" 
		self.structure_type = "" 
		self.description = "" 
		self.type = "" 
		self.delivery_max_dose = 0.0 
		self.target_rx_dose = 0.0 
		self.target_min_dose = 0.0 
		self.target_max_dose = 0.0 
		self.point_coordinates = [] 

class rt_tolerance_table:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.number = 0.0 
		self.gantry_angle = 0.0 
		self.beam_limiting_angle = 0.0 
		self.patient_support_angle = 0.0 
		self.table_top_vert_position = 0.0 
		self.table_top_long_position = 0.0 
		self.table_top_lat_position = 0.0 
		self.label = "" 
		self.limiting_device_position = [] 
		self.limiting_device_type = [] 

class rt_patient_setup:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.setup_number = 0.0 
		self.position = patient_position_type()
		self.setup_description = "" 

class rt_fraction:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.number = 0.0 
		self.number_planned_fractions = 0.0 
		self.number_beams = 0.0 
		self.referenced_beam_numbers = [] 
		self.referenced_beam_dose = [] 

class rt_ref_beam:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.beam_dose = 0.0 
		self.beam_number = 0.0 

class rt_plan:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.plan_date = "" 
		self.name = "" 
		self.description = "" 
		self.label = "" 
		self.uid = "" 
		self.geometry = "" 
		self.frame_of_ref_uid = "" 
		self.patient_data = patient()
		self.study = rt_study()
		self.dose = [] 
		self.fractions = [] 
		self.ref_beam = [] 
		self.tolerance_table = [] 
		self.patient_setups = [] 
		self.beams = [] 

class rt_image_conversion_type:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# DV
		# DI
		# DF
		# WSD

class rt_image_type:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# DRR
		# PORTAL
		# SIMULATOR
		# RADIOGRAPH
		# BLANK
		# FLUENCE

class rt_structure_type:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# point
		# closed_planar

class dicom_modality:

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# RTPLAN
		# RTSTRUCTURESET
		# RTSTRUCT
		# CT
		# RTDOSE

class dicom_structure_geometry_slice:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.position = 0.0 
		self.thickness = 0.0 
		self.region = polyset()

class dicom_structure_geometry:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.slices = [] 

class rt_structure:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.name = "" 
		self.description = "" 
		self.number = 0.0 
		self.color = rgb()
		self.type = rt_structure_type()
		self.point = [] 
		self.volume = dicom_structure_geometry()

class rt_structure_set:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.name = "" 
		self.description = "" 
		self.structures = [] 
		self.patient_position = patient_position_type()
		self.contour_image_sequence = [] 
		self.frame_of_ref_uid = "" 
		self.series_uid = "" 
		self.study = rt_study()

class rt_dose:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.dose = rt_image_slice_3d()
		self.number_frames = 0.0 
		self.frame_spacing = [] 
		self.frame_increment_pointer = "" 
		self.study = rt_study()

class ct_image_slice:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.slice = rt_image_slice_2d()
		self.patient_position = patient_position_type()
		self.study = rt_study()

class ct_image_set:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.image = image_3d()
		self.patient_position = patient_position_type()
		self.study = rt_study()

class dicom_metadata:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.creationDate = "" 
		self.patient_metadata = patient()
		self.modality = dicom_modality()

class dicom_object:

	#Initialize
	def __init__(self):
		self.type = ""
		self.structure_set = rt_structure_set.toStr()
		self.ct_image = ct_image_slice.toStr()
		self.ct_image_set = ct_image_set.toStr()
		self.dose = rt_dose.toStr()
		self.plan = rt_plan.toStr()

class dicom_data:

	#Initialize
	def __init__(self):
		self.meta_data = dicom_metadata()
		self.dicom_obj = dicom_object()

class dicom_patient:

	#Initialize
	def __init__(self):
		self.patient = [] 

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

class box_3d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

class slice_description:

	#Initialize
	def __init__(self):
		self.position = 0.0 
		self.thickness = 0.0 

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

class box_1d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

class image_geometry_1d:

	#Initialize
	def __init__(self):
		self.slicing = [] 
		self.regular_grid = regular_grid_1d()

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

class rt_image_slice_3d:

	#Initialize
	def __init__(self):
		self.content = rt_image_3d()
		self.axis = 0.0 
		self.position = 0.0 
		self.thickness = 0.0 
		self.instance_number = 0.0 
		self.samples_per_pixel = 0.0 
		self.pixel_rep = 0.0 
		self.pixel_spacing = [] 
		self.image_position = [] 
		self.image_orientation = [] 
		self.photometric_interpretation = "" 

class rt_image_slice_2d:

	#Initialize
	def __init__(self):
		self.content = rt_image_2d()
		self.axis = 0.0 
		self.position = 0.0 
		self.thickness = 0.0 
		self.instance_number = 0.0 
		self.samples_per_pixel = 0.0 
		self.pixel_rep = 0.0 
		self.pixel_spacing = [] 
		self.image_position = [] 
		self.image_orientation = [] 
		self.photometric_interpretation = "" 

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

class rt_image_3d:

	#Initialize
	def __init__(self):
		self.img = image_3d()
		self.bits_allocated = 0.0 
		self.bits_stored = 0.0 
		self.high_bit = 0.0 
		self.rescale_intercept = 0.0 
		self.rescale_slope = 0.0 
		self.cols = 0.0 
		self.rows = 0.0 

class rt_image_2d:

	#Initialize
	def __init__(self):
		self.img = image_2d()
		self.bits_allocated = 0.0 
		self.bits_stored = 0.0 
		self.high_bit = 0.0 
		self.rescale_intercept = 0.0 
		self.rescale_slope = 0.0 
		self.cols = 0.0 
		self.rows = 0.0 

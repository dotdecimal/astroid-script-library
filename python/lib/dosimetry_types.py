# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:	Travis DeMint
# Date:		06/24/2015
# Desc:		Provides access to cradle type usage for all types
# Dosimetry Version:		1.0.5.1

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

class adaptive_grid_region:

	#Initialize
	def __init__(self):
		self.region = optimized_triangle_mesh()
		self.maximum_spacing = 0.0 

	def toStr(self):
		values = OrderedDict([("region", self.region.toStr()),
								("maximum_spacing", self.maximum_spacing)
			]) 
		return values 

class adaptive_grid_voxel:

	#Initialize
	def __init__(self):
		self.index = 0.0 
		self.volume_offset = 0.0 
		self.inside_count = 0.0 
		self.surface_count = 0.0 

	def toStr(self):
		values = OrderedDict([("index", self.index),
								("volume_offset", self.volume_offset),
								("inside_count", self.inside_count),
								("surface_count", self.surface_count)
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

class box_4d:

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

	def toStr(self):
		values = OrderedDict([("corner", self.corner),
								("size", self.size)
			]) 
		return values 

class circle:

	#Initialize
	def __init__(self):
		self.center = [] 
		self.radius = 0.0 

	def toStr(self):
		values = OrderedDict([("center", self.center),
								("radius", self.radius)
			]) 
		return values 

class plane:

	#Initialize
	def __init__(self):
		self.point = [] 
		self.normal = [] 

	def toStr(self):
		values = OrderedDict([("point", self.point),
								("normal", self.normal)
			]) 
		return values 

class ray_2d:

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.direction = [] 

	def toStr(self):
		values = OrderedDict([("origin", self.origin),
								("direction", self.direction)
			]) 
		return values 

class ray_3d:

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.direction = [] 

	def toStr(self):
		values = OrderedDict([("origin", self.origin),
								("direction", self.direction)
			]) 
		return values 

class ray_points:

	#Initialize
	def __init__(self):
		self.n_points = 0.0 
		self.offset = 0.0 

	def toStr(self):
		values = OrderedDict([("n_points", self.n_points),
								("offset", self.offset)
			]) 
		return values 

class divergent_grid:

	#Initialize
	def __init__(self):
		self.isUniform = False 
		self.z_position = 0.0 
		self.source_dist = 0.0 
		self.cax_length = 0.0 
		self.grid = regular_grid_2d()
		blob = blob_type()
		self.rays = blob.toStr()
		blob = blob_type()
		self.data = blob.toStr()

	def toStr(self):
		values = OrderedDict([("isUniform", self.isUniform),
								("z_position", self.z_position),
								("source_dist", self.source_dist),
								("cax_length", self.cax_length),
								("grid", self.grid.toStr()),
								("rays", self.rays),
								("data", self.data)
			]) 
		return values 

class ray_box_intersection_2d:

	#Initialize
	def __init__(self):
		self.n_intersections = 0.0 
		self.entrance_distance = 0.0 
		self.exit_distance = 0.0 

	def toStr(self):
		values = OrderedDict([("n_intersections", self.n_intersections),
								("entrance_distance", self.entrance_distance),
								("exit_distance", self.exit_distance)
			]) 
		return values 

class ray_box_intersection_3d:

	#Initialize
	def __init__(self):
		self.n_intersections = 0.0 
		self.entrance_distance = 0.0 
		self.exit_distance = 0.0 

	def toStr(self):
		values = OrderedDict([("n_intersections", self.n_intersections),
								("entrance_distance", self.entrance_distance),
								("exit_distance", self.exit_distance)
			]) 
		return values 

class levelset2:

	#Initialize
	def __init__(self):
		self.values = image_2d()

	def toStr(self):
		values = OrderedDict([("values", self.values.toStr()),
			]) 
		return values 

class line_strip:

	#Initialize
	def __init__(self):
		self.vertices = [] 

	def toStr(self):
		values = OrderedDict([("vertices", self.vertices),
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

class polygon2:

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.vertices = blob.toStr()

	def toStr(self):
		values = OrderedDict([("vertices", self.vertices),
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

class set_operation:

	#Initialize
	def __init__(self):
		self.union = 0
		self.intersection = 1
		self.difference = 2
		self.xor = 3

	def toStr(self):
		values = OrderedDict([("union", self.union),
								("intersection", self.intersection),
								("difference", self.difference),
								("xor", self.xor)
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

class structure_geometry:

	#Initialize
	def __init__(self):
		self.slices = [] 

	def toStr(self):
		values = OrderedDict([("slices", self.slices),
			]) 
		return values 

class weighted_grid_index:

	#Initialize
	def __init__(self):
		self.index = 0.0 
		self.weight = 0.0 

	def toStr(self):
		values = OrderedDict([("index", self.index),
								("weight", self.weight)
			]) 
		return values 

class sliced_scene_geometry_2d:

	#Initialize
	def __init__(self):
		self.slicing = [] 

	def toStr(self):
		values = OrderedDict([("slicing", self.slicing),
			]) 
		return values 

class sliced_scene_geometry_3d:

	#Initialize
	def __init__(self):
		self.slicing = [] 

	def toStr(self):
		values = OrderedDict([("slicing", self.slicing),
			]) 
		return values 

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

class id_and_type:

	#Initialize
	def __init__(self):
		self.id = "" 
		self.type = "" 

	def toStr(self):
		values = OrderedDict([("id", self.id),
								("type", self.type)
			]) 
		return values 

class gui_task_state:

	#Initialize
	def __init__(self):
		self.type = "" 
		self.completed_subtask_count = 0.0 
		self.canceled_subtask_count = 0.0 
		self.open_subtask_count = 0.0 

	def toStr(self):
		values = OrderedDict([("type", self.type),
								("state", self.state),
								("active_subtask", self.active_subtask),
								("completed_subtask_count", self.completed_subtask_count)
								("canceled_subtask_count", self.canceled_subtask_count),
								("open_subtask_count", self.open_subtask_count),
			]) 
		return values 

class app_level_page:

	#Initialize
	def __init__(self):
		self.app_contents = 0
		self.app_info = 1
		self.settings = 2
		self.notifications = 3

	def toStr(self):
		values = OrderedDict([("app_contents", self.app_contents),
								("app_info", self.app_info),
								("settings", self.settings),
								("notifications", self.notifications)
			]) 
		return values 

class base_zoom_type:

	#Initialize
	def __init__(self):
		self.stretch_to_fit = 0
		self.fit_scene = 1
		self.fit_scene_width = 2
		self.fit_scene_height = 3
		self.fill_canvas = 4

	def toStr(self):
		values = OrderedDict([("stretch_to_fit", self.stretch_to_fit),
								("fit_scene", self.fit_scene),
								("fit_scene_width", self.fit_scene_width),
								("fit_scene_height", self.fit_scene_height),
								("fill_canvas", self.fill_canvas)
			]) 
		return values 

class camera:

	#Initialize
	def __init__(self):
		self.zoom = 0.0 
		self.position = [] 

	def toStr(self):
		values = OrderedDict([("zoom", self.zoom),
								("position", self.position)
			]) 
		return values 

class simple_2d_image_view_state:

	#Initialize
	def __init__(self):
		self.camera = camera()
		self.measurement = simple_2d_view_measurement_state()

	def toStr(self):
		values = OrderedDict([("camera", self.camera.toStr()),
								("measurement", self.measurement.toStr())
			]) 
		return values 

class sliced_3d_image_view_state:

	#Initialize
	def __init__(self):
		self.view_axis = 0.0 

	def toStr(self):
		values = OrderedDict([("view_axis", self.view_axis),
			]) 
		return values 

class sliced_3d_structure_view_state:

	#Initialize
	def __init__(self):
		self.view_axis = 0.0 

	def toStr(self):
		values = OrderedDict([("view_axis", self.view_axis),
			]) 
		return values 

class sliced_3d_structure_set_view_state:

	#Initialize
	def __init__(self):
		self.view_axis = 0.0 

	def toStr(self):
		values = OrderedDict([("view_axis", self.view_axis),
			]) 
		return values 

class display_layout_type:

	#Initialize
	def __init__(self):
		self.main_plus_row = 0
		self.main_plus_column = 1
		self.two_rows = 2
		self.two_columns = 3
		self.squares = 4

	def toStr(self):
		values = OrderedDict([("main_plus_row", self.main_plus_row),
								("main_plus_column", self.main_plus_column),
								("two_rows", self.two_rows),
								("two_columns", self.two_columns),
								("squares", self.squares)
			]) 
		return values 

class display_view_instance:

	#Initialize
	def __init__(self):
		self.instance_id = "" 
		self.type_id = "" 

	def toStr(self):
		values = OrderedDict([("instance_id", self.instance_id),
								("type_id", self.type_id)
			]) 
		return values 

class display_view_composition:

	#Initialize
	def __init__(self):
		self.id = "" 
		self.label = "" 
		self.views = [] 
		self.layout = display_layout_type()

	def toStr(self):
		values = OrderedDict([("id", self.id),
								("label", self.label),
								("views", self.views),
								("layout", self.layout.toStr())
			]) 
		return values 

class display_state:

	#Initialize
	def __init__(self):
		self.controls_expanded = False 

	def toStr(self):
		values = OrderedDict([("selected_composition", self.selected_composition),
								("focused_view", self.focused_view),
								("controls_expanded", self.controls_expanded),
			]) 
		return values 

class dose_level:

	#Initialize
	def __init__(self):
		self.level = 0.0 
		self.color = rgb()

	def toStr(self):
		values = OrderedDict([("level", self.level),
								("color", self.color.toStr())
			]) 
		return values 

class dose_display_type:

	#Initialize
	def __init__(self):
		self.off = 0
		self.isodose_lines = 1
		self.color_wash = 2

	def toStr(self):
		values = OrderedDict([("off", self.off),
								("isodose_lines", self.isodose_lines),
								("color_wash", self.color_wash)
			]) 
		return values 

class dose_display_style:

	#Initialize
	def __init__(self):
		self.display_type = dose_display_type()
		self.isodose_display = spatial_region_display_options()
		self.color_wash_opacity = 0.0 

	def toStr(self):
		values = OrderedDict([("display_type", self.display_type.toStr()),
								("isodose_display", self.isodose_display.toStr()),
								("color_wash_opacity", self.color_wash_opacity)
			]) 
		return values 

class dose_display_options:

	#Initialize
	def __init__(self):
		self.levels = [] 
		self.style = dose_display_style()

	def toStr(self):
		values = OrderedDict([("levels", self.levels),
								("style", self.style.toStr())
			]) 
		return values 

class dose_level_ui_mode:

	#Initialize
	def __init__(self):
		self.relative = 0
		self.absolute = 1

	def toStr(self):
		values = OrderedDict([("relative", self.relative),
								("absolute", self.absolute)
			]) 
		return values 

class preset_dose_level:

	#Initialize
	def __init__(self):
		self.color = rgb()
		self.is_fixed = False 

	def toStr(self):
		values = OrderedDict([("color", self.color.toStr()),
								("is_fixed", self.is_fixed)
								("absolute_level", self.absolute_level),
								("relative_level", self.relative_level),
			]) 
		return values 

class line_stipple:

	#Initialize
	def __init__(self):
		self.factor = 0.0 
		self.pattern = 0.0 

	def toStr(self):
		values = OrderedDict([("factor", self.factor),
								("pattern", self.pattern)
			]) 
		return values 

class line_style:

	#Initialize
	def __init__(self):
		self.width = 0.0 
		self.stipple = line_stipple()

	def toStr(self):
		values = OrderedDict([("width", self.width),
								("stipple", self.stipple.toStr())
			]) 
		return values 

class gray_image_display_options:

	#Initialize
	def __init__(self):
		self.level = 0.0 
		self.window = 0.0 

	def toStr(self):
		values = OrderedDict([("level", self.level),
								("window", self.window)
			]) 
		return values 

class line_stipple_type:

	#Initialize
	def __init__(self):
		self.none = 0
		self.solid = 1
		self.dashed = 2
		self.dotted = 3

	def toStr(self):
		values = OrderedDict([("none", self.none),
								("solid", self.solid),
								("dashed", self.dashed),
								("dotted", self.dotted)
			]) 
		return values 

class spatial_region_fill_options:

	#Initialize
	def __init__(self):
		self.enabled = False 
		self.opacity = 0.0 

	def toStr(self):
		values = OrderedDict([("enabled", self.enabled),
								("opacity", self.opacity)
			]) 
		return values 

class spatial_region_outline_options:

	#Initialize
	def __init__(self):
		self.type = line_stipple_type()
		self.width = 0.0 
		self.opacity = 0.0 

	def toStr(self):
		values = OrderedDict([("type", self.type.toStr()),
								("width", self.width),
								("opacity", self.opacity)
			]) 
		return values 

class spatial_region_display_options:

	#Initialize
	def __init__(self):
		self.fill = spatial_region_fill_options()
		self.outline = spatial_region_outline_options()

	def toStr(self):
		values = OrderedDict([("fill", self.fill.toStr()),
								("outline", self.outline.toStr())
			]) 
		return values 

class point_rendering_options:

	#Initialize
	def __init__(self):
		self.size = 0.0 
		self.line_type = line_stipple_type()
		self.line_thickness = 0.0 

	def toStr(self):
		values = OrderedDict([("size", self.size),
								("line_type", self.line_type.toStr()),
								("line_thickness", self.line_thickness)
			]) 
		return values 

class notable_data_point:

	#Initialize
	def __init__(self):
		self.label = "" 
		self.color = rgb()
		self.position = [] 

	def toStr(self):
		values = OrderedDict([("label", self.label),
								("color", self.color.toStr()),
								("position", self.position)
			]) 
		return values 

class data_reporting_parameters:

	#Initialize
	def __init__(self):
		self.label = "" 
		self.units = "" 
		self.digits = 0.0 

	def toStr(self):
		values = OrderedDict([("label", self.label),
								("units", self.units),
								("digits", self.digits)
			]) 
		return values 

class graph_line_style_info:

	#Initialize
	def __init__(self):
		self.color = rgba()

	def toStr(self):
		values = OrderedDict([("color", self.color.toStr()),
			]) 
		return values 

class out_of_plane_information:

	#Initialize
	def __init__(self):
		self.axis = 0.0 
		self.thickness = 0.0 
		self.position = 0.0 

	def toStr(self):
		values = OrderedDict([("axis", self.axis),
								("thickness", self.thickness),
								("position", self.position)
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

class image_geometry_4d:

	#Initialize
	def __init__(self):
		self.slicing = [] 
		self.regular_grid = regular_grid_4d()

	def toStr(self):
		values = OrderedDict([("slicing", self.slicing),
								("out_of_plane_info", self.out_of_plane_info)
								("regular_grid", self.regular_grid.toStr()),
			]) 
		return values 

class drr_options:

	#Initialize
	def __init__(self):
		self.image_display_options = gray_image_display_options()
		self.min_z = 0.0 
		self.max_z = 0.0 
		self.min_value = 0.0 
		self.max_value = 0.0 
		self.image_z = 0.0 
		self.sizing = regular_grid_2d()

	def toStr(self):
		values = OrderedDict([("image_display_options", self.image_display_options.toStr()),
								("min_z", self.min_z),
								("max_z", self.max_z),
								("min_value", self.min_value),
								("max_value", self.max_value),
								("image_z", self.image_z),
								("sizing", self.sizing.toStr())
			]) 
		return values 

class camera3:

	#Initialize
	def __init__(self):
		self.zoom = 0.0 
		self.position = [] 
		self.direction = [] 
		self.up = [] 

	def toStr(self):
		values = OrderedDict([("zoom", self.zoom),
								("position", self.position),
								("direction", self.direction),
								("up", self.up)
			]) 
		return values 

class sliced_3d_view_state:

	#Initialize
	def __init__(self):
		self.slice_positions = [] 

	def toStr(self):
		values = OrderedDict([("slice_positions", self.slice_positions),
			]) 
		return values 

class point_sample_2d:

	#Initialize
	def __init__(self):
		self.position = [] 
		self.color = rgb()

	def toStr(self):
		values = OrderedDict([("position", self.position),
								("color", self.color.toStr())
			]) 
		return values 

class line_profile:

	#Initialize
	def __init__(self):
		self.axis = 0.0 
		self.position = 0.0 
		self.color = rgb()

	def toStr(self):
		values = OrderedDict([("axis", self.axis),
								("position", self.position),
								("color", self.color.toStr())
			]) 
		return values 

class simple_2d_view_measurement_state:

	#Initialize
	def __init__(self):
		self.profiles = [] 
		self.point_samples = [] 

	def toStr(self):
		values = OrderedDict([("profiles", self.profiles),
								("point_samples", self.point_samples)
			]) 
		return values 

class subtask_event_type:

	#Initialize
	def __init__(self):
		self.task_completed = 0
		self.value_produced = 1
		self.task_canceled = 2

	def toStr(self):
		values = OrderedDict([("task_completed", self.task_completed),
								("value_produced", self.value_produced),
								("task_canceled", self.task_canceled)
			]) 
		return values 

class subtask_event:

	#Initialize
	def __init__(self):
		self.type = subtask_event_type()
		self.task_id = "" 

	def toStr(self):
		values = OrderedDict([("type", self.type.toStr()),
								("task_id", self.task_id)
								("value", self.value),
			]) 
		return values 

class tristate_expansion:

	#Initialize
	def __init__(self):
		self.closed = 0
		self.halfway = 1
		self.open = 2

	def toStr(self):
		values = OrderedDict([("closed", self.closed),
								("halfway", self.halfway),
								("open", self.open)
			]) 
		return values 

class color_map_level:

	#Initialize
	def __init__(self):
		self.level = 0.0 
		self.color = rgba()

	def toStr(self):
		values = OrderedDict([("level", self.level),
								("color", self.color.toStr())
			]) 
		return values 

class grid_cell_inclusion_info:

	#Initialize
	def __init__(self):
		self.cells_inside = [] 

	def toStr(self):
		values = OrderedDict([("cells_inside", self.cells_inside),
			]) 
		return values 

class colored_vertex_2d:

	#Initialize
	def __init__(self):
		self.position = [] 
		self.color = rgba()

	def toStr(self):
		values = OrderedDict([("position", self.position),
								("color", self.color.toStr())
			]) 
		return values 

class image_slice_1d:

	#Initialize
	def __init__(self):
		self.axis = 0.0 
		self.position = 0.0 
		self.thickness = 0.0 
		self.content = image_1d()

	def toStr(self):
		values = OrderedDict([("axis", self.axis),
								("position", self.position),
								("thickness", self.thickness),
								("content", self.content.toStr())
			]) 
		return values 

class image_slice_2d:

	#Initialize
	def __init__(self):
		self.axis = 0.0 
		self.position = 0.0 
		self.thickness = 0.0 
		self.content = image_2d()

	def toStr(self):
		values = OrderedDict([("axis", self.axis),
								("position", self.position),
								("thickness", self.thickness),
								("content", self.content.toStr())
			]) 
		return values 

class image_slice_3d:

	#Initialize
	def __init__(self):
		self.axis = 0.0 
		self.position = 0.0 
		self.thickness = 0.0 
		self.content = image_3d()

	def toStr(self):
		values = OrderedDict([("axis", self.axis),
								("position", self.position),
								("thickness", self.thickness),
								("content", self.content.toStr())
			]) 
		return values 

class pixel_format:

	#Initialize
	def __init__(self):
		self.gray = 0
		self.rgb = 1
		self.rgba = 2

	def toStr(self):
		values = OrderedDict([("gray", self.gray),
								("rgb", self.rgb),
								("rgba", self.rgba)
			]) 
		return values 

class channel_type:

	#Initialize
	def __init__(self):
		self.int8 = 0
		self.uint8 = 1
		self.int16 = 2
		self.uint16 = 3
		self.int32 = 4
		self.uint32 = 5
		self.int64 = 6
		self.uint64 = 7
		self.float = 8
		self.double = 9

	def toStr(self):
		values = OrderedDict([("int8", self.int8),
								("uint8", self.uint8),
								("int16", self.int16),
								("uint16", self.uint16),
								("int32", self.int32),
								("uint32", self.uint32),
								("int64", self.int64),
								("uint64", self.uint64),
								("float", self.float),
								("double", self.double)
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

class unboxed_image_2d:

	#Initialize
	def __init__(self):
		self.size = [] 
		self.pixels = [] 
		self.origin = [] 
		self.axes = [] 

	def toStr(self):
		values = OrderedDict([("size", self.size),
								("pixels", self.pixels),
								("origin", self.origin),
								("axes", self.axes)
			]) 
		return values 

class unboxed_image_3d:

	#Initialize
	def __init__(self):
		self.size = [] 
		self.pixels = [] 
		self.origin = [] 
		self.axes = [] 

	def toStr(self):
		values = OrderedDict([("size", self.size),
								("pixels", self.pixels),
								("origin", self.origin),
								("axes", self.axes)
			]) 
		return values 

class filesystem_item_contents:

	#Initialize
	def __init__(self):
		self.type = ""
		self.directory = []
		self.file = blob_type()

	def toStr(self):
		if (self.type == 'directory'):
			values = OrderedDict([("directory", self.directory),
									("type", self.type)
				]) 
			return values 
		elif (self.type == 'file'):
			values = OrderedDict([("file", self.file.toStr()),
									("type", self.type)
				]) 
			return values 
		else:
			return "Type not Set" 

class filesystem_item:

	#Initialize
	def __init__(self):
		self.name = "" 
		self.contents = filesystem_item_contents()

	def toStr(self):
		values = OrderedDict([("name", self.name),
								("contents", self.contents.toStr())
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

class statistics:

	#Initialize
	def __init__(self):
		self.n_samples = 0.0 

	def toStr(self):
		values = OrderedDict([("min", self.min),
								("max", self.max),
								("mean", self.mean),
								("n_samples", self.n_samples),
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

class quadratic_function:

	#Initialize
	def __init__(self):
		self.a = 0.0 
		self.b = 0.0 
		self.c = 0.0 

	def toStr(self):
		values = OrderedDict([("a", self.a),
								("b", self.b),
								("c", self.c)
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

class regular_grid_4d:

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

class outside_domain_policy:

	#Initialize
	def __init__(self):
		self.always_zero = 0
		self.extend_with_copies = 1

	def toStr(self):
		values = OrderedDict([("always_zero", self.always_zero),
								("extend_with_copies", self.extend_with_copies)
			]) 
		return values 

class function_sample:

	#Initialize
	def __init__(self):
		self.value = 0.0 
		self.delta = 0.0 

	def toStr(self):
		values = OrderedDict([("value", self.value),
								("delta", self.delta)
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

class regularly_sampled_function:

	#Initialize
	def __init__(self):
		self.x0 = 0.0 
		self.x_spacing = 0.0 
		self.samples = [] 
		self.outside_domain_policy = outside_domain_policy()

	def toStr(self):
		values = OrderedDict([("x0", self.x0),
								("x_spacing", self.x_spacing),
								("samples", self.samples),
								("outside_domain_policy", self.outside_domain_policy.toStr())
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

class gaussian_sample_point:

	#Initialize
	def __init__(self):
		self.point = [] 
		self.weight = 0.0 

	def toStr(self):
		values = OrderedDict([("point", self.point),
								("weight", self.weight)
			]) 
		return values 

class mco_navigation_objective:

	#Initialize
	def __init__(self):
		self.is_maximization = False 
		self.range = min_max()

	def toStr(self):
		values = OrderedDict([("is_maximization", self.is_maximization),
								("range", self.range.toStr())
			]) 
		return values 

class mco_navigation_system:

	#Initialize
	def __init__(self):
		self.plan_count = 0.0 
		self.objectives = [] 
		self.p_matrix = [] 

	def toStr(self):
		values = OrderedDict([("plan_count", self.plan_count),
								("objectives", self.objectives),
								("p_matrix", self.p_matrix)
			]) 
		return values 

class dicom_element:

	#Initialize
	def __init__(self):
		self.name = "" 
		self.value = "" 
		self.g = 0.0 
		self.e = 0.0 

	def toStr(self):
		values = OrderedDict([("name", self.name),
								("value", self.value),
								("g", self.g),
								("e", self.e)
			]) 
		return values 

class dicom_sequence:

	#Initialize
	def __init__(self):
		self.items = [] 
		self.g = 0.0 
		self.e = 0.0 

	def toStr(self):
		values = OrderedDict([("items", self.items),
								("g", self.g),
								("e", self.e)
			]) 
		return values 

class dicom_item:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("study_date", self.study_date),
								("study_time", self.study_time),
								("description", self.description),
								("physician_name", self.physician_name),
								("id", self.id)
								("accession_number", self.accession_number),
			]) 
		return values 

class patient_position_type:

	#Initialize
	def __init__(self):
		self.HFS = 0
		self.HFP = 1
		self.FFS = 2
		self.FFP = 3
		self.HFDR = 4
		self.HFDL = 5
		self.FFDR = 6
		self.FFDL = 7

	def toStr(self):
		values = OrderedDict([("HFS", self.HFS),
								("HFP", self.HFP),
								("FFS", self.FFS),
								("FFP", self.FFP),
								("HFDR", self.HFDR),
								("HFDL", self.HFDL),
								("FFDR", self.FFDR),
								("FFDL", self.FFDL)
			]) 
		return values 

class person_name:

	#Initialize
	def __init__(self):
		self.family_name = "" 
		self.given_name = "" 
		self.middle_name = "" 
		self.prefix = "" 
		self.suffix = "" 

	def toStr(self):
		values = OrderedDict([("family_name", self.family_name),
								("given_name", self.given_name),
								("middle_name", self.middle_name),
								("prefix", self.prefix),
								("suffix", self.suffix)
			]) 
		return values 

class patient_sex:

	#Initialize
	def __init__(self):
		self.M = 0
		self.F = 1
		self.O = 2

	def toStr(self):
		values = OrderedDict([("M", self.M),
								("F", self.F),
								("O", self.O)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("name", self.name.toStr()),
								("id", self.id),
								("sex", self.sex.toStr()),
								("birth_date", self.birth_date),
								("other_names", self.other_names),
								("other_ids", self.other_ids),
								("ethnic_group", self.ethnic_group)
								("comments", self.comments),
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("number", self.number),
								("meterset_weight", self.meterset_weight),
								("nominal_beam_energy", self.nominal_beam_energy),
								("gantry_angle", self.gantry_angle),
								("gantry_pitch_angle", self.gantry_pitch_angle),
								("beam_limiting_device_angle", self.beam_limiting_device_angle),
								("patient_support_angle", self.patient_support_angle),
								("meterset_rate", self.meterset_rate),
								("source_to_surface_distance", self.source_to_surface_distance),
								("snout_position", self.snout_position),
								("iso_center_position", self.iso_center_position),
								("surface_entry_point", self.surface_entry_point),
								("gantry_rotation_direction", self.gantry_rotation_direction),
								("gantry_pitch_direction", self.gantry_pitch_direction),
								("beam_limiting_direction", self.beam_limiting_direction),
								("patient_support_direction", self.patient_support_direction),
								("table_top_pitch_angle", self.table_top_pitch_angle),
								("table_top_roll_angle", self.table_top_roll_angle),
								("table_top_pitch_direction", self.table_top_pitch_direction),
								("table_top_roll_direction", self.table_top_roll_direction)
			]) 
		return values 

class rt_mounting_position:

	#Initialize
	def __init__(self):
		self.PATIENT_SIDE = 0
		self.SOURCE_SIDE = 1
		self.DOUBLE_SIDED = 2

	def toStr(self):
		values = OrderedDict([("PATIENT_SIDE", self.PATIENT_SIDE),
								("SOURCE_SIDE", self.SOURCE_SIDE),
								("DOUBLE_SIDED", self.DOUBLE_SIDED)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("name", self.name),
								("number", self.number),
								("material", self.material),
								("divergent", self.divergent),
								("mounting_position", self.mounting_position.toStr()),
								("downstream_edge", self.downstream_edge),
								("column_offset", self.column_offset),
								("relative_stopping_power", self.relative_stopping_power),
								("position", self.position),
								("pixelSpacing", self.pixelSpacing),
								("data", self.data.toStr())
			]) 
		return values 

class rt_ion_block_type:

	#Initialize
	def __init__(self):
		self.APERTURE = 0
		self.SHIELDING = 1

	def toStr(self):
		values = OrderedDict([("APERTURE", self.APERTURE),
								("SHIELDING", self.SHIELDING)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("name", self.name),
								("description", self.description),
								("material", self.material),
								("number", self.number),
								("divergent", self.divergent),
								("downstream_edge", self.downstream_edge),
								("thinkness", self.thinkness),
								("position", self.position.toStr()),
								("block_type", self.block_type.toStr()),
								("data", self.data.toStr())
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("id", self.id),
								("accessoryCode", self.accessoryCode)
			]) 
		return values 

class rt_radiation_type:

	#Initialize
	def __init__(self):
		self.PROTON = 0
		self.PHOTON = 1
		self.ELECTRON = 2
		self.NEUTRON = 3

	def toStr(self):
		values = OrderedDict([("PROTON", self.PROTON),
								("PHOTON", self.PHOTON),
								("ELECTRON", self.ELECTRON),
								("NEUTRON", self.NEUTRON)
			]) 
		return values 

class rt_ion_beam_type:

	#Initialize
	def __init__(self):
		self.STATIC = 0
		self.DYNAMIC = 1

	def toStr(self):
		values = OrderedDict([("STATIC", self.STATIC),
								("DYNAMIC", self.DYNAMIC)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("beam_number", self.beam_number),
								("name", self.name),
								("description", self.description),
								("treatment_machine", self.treatment_machine),
								("primary_dosimeter_unit", self.primary_dosimeter_unit),
								("treatment_delivery_type", self.treatment_delivery_type),
								("beam_type", self.beam_type.toStr()),
								("radiation_type", self.radiation_type.toStr()),
								("referenced_patient_setup", self.referenced_patient_setup),
								("referenced_tolerance_table", self.referenced_tolerance_table),
								("virtual_sad", self.virtual_sad),
								("final_meterset_weight", self.final_meterset_weight),
								("snouts", self.snouts),
								("block", self.block.toStr()),
								("degraders", self.degraders),
								("control_points", self.control_points)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("number", self.number),
								("uid", self.uid),
								("structure_type", self.structure_type),
								("description", self.description),
								("type", self.type),
								("delivery_max_dose", self.delivery_max_dose),
								("target_rx_dose", self.target_rx_dose),
								("target_min_dose", self.target_min_dose),
								("target_max_dose", self.target_max_dose),
								("point_coordinates", self.point_coordinates)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("number", self.number),
								("gantry_angle", self.gantry_angle),
								("beam_limiting_angle", self.beam_limiting_angle),
								("patient_support_angle", self.patient_support_angle),
								("table_top_vert_position", self.table_top_vert_position),
								("table_top_long_position", self.table_top_long_position),
								("table_top_lat_position", self.table_top_lat_position),
								("label", self.label),
								("limiting_device_position", self.limiting_device_position),
								("limiting_device_type", self.limiting_device_type)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("setup_number", self.setup_number),
								("position", self.position.toStr()),
								("setup_description", self.setup_description)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("number", self.number),
								("number_planned_fractions", self.number_planned_fractions),
								("number_beams", self.number_beams),
								("referenced_beam_numbers", self.referenced_beam_numbers),
								("referenced_beam_dose", self.referenced_beam_dose)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("beam_dose", self.beam_dose),
								("beam_number", self.beam_number)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("plan_date", self.plan_date),
								("plan_time", self.plan_time),
								("name", self.name),
								("description", self.description),
								("label", self.label),
								("uid", self.uid),
								("geometry", self.geometry),
								("frame_of_ref_uid", self.frame_of_ref_uid),
								("patient_data", self.patient_data.toStr()),
								("study", self.study.toStr()),
								("dose", self.dose),
								("fractions", self.fractions),
								("ref_beam", self.ref_beam),
								("tolerance_table", self.tolerance_table),
								("patient_setups", self.patient_setups)
								("beams", self.beams),
			]) 
		return values 

class rt_image_conversion_type:

	#Initialize
	def __init__(self):
		self.DV = 0
		self.DI = 1
		self.DF = 2
		self.WSD = 3

	def toStr(self):
		values = OrderedDict([("DV", self.DV),
								("DI", self.DI),
								("DF", self.DF),
								("WSD", self.WSD)
			]) 
		return values 

class rt_image_type:

	#Initialize
	def __init__(self):
		self.DRR = 0
		self.PORTAL = 1
		self.SIMULATOR = 2
		self.RADIOGRAPH = 3
		self.BLANK = 4
		self.FLUENCE = 5

	def toStr(self):
		values = OrderedDict([("DRR", self.DRR),
								("PORTAL", self.PORTAL),
								("SIMULATOR", self.SIMULATOR),
								("RADIOGRAPH", self.RADIOGRAPH),
								("BLANK", self.BLANK),
								("FLUENCE", self.FLUENCE)
			]) 
		return values 

class rt_structure_type:

	#Initialize
	def __init__(self):
		self.point = 0
		self.closed_planar = 1

	def toStr(self):
		values = OrderedDict([("point", self.point),
								("closed_planar", self.closed_planar)
			]) 
		return values 

class dicom_modality:

	#Initialize
	def __init__(self):
		self.RTPLAN = 0
		self.RTSTRUCTURESET = 1
		self.RTSTRUCT = 2
		self.CT = 3
		self.RTDOSE = 4

	def toStr(self):
		values = OrderedDict([("RTPLAN", self.RTPLAN),
								("RTSTRUCTURESET", self.RTSTRUCTURESET),
								("RTSTRUCT", self.RTSTRUCT),
								("CT", self.CT),
								("RTDOSE", self.RTDOSE)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("position", self.position),
								("thickness", self.thickness),
								("region", self.region.toStr())
			]) 
		return values 

class dicom_structure_geometry:

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.slices = [] 

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("slices", self.slices)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("name", self.name),
								("description", self.description),
								("number", self.number),
								("color", self.color.toStr()),
								("type", self.type.toStr()),
								("point", self.point),
								("volume", self.volume.toStr())
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("name", self.name),
								("description", self.description),
								("structures", self.structures),
								("patient_position", self.patient_position.toStr()),
								("contour_image_sequence", self.contour_image_sequence),
								("frame_of_ref_uid", self.frame_of_ref_uid),
								("series_uid", self.series_uid),
								("study", self.study.toStr())
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("img", self.img.toStr()),
								("bits_allocated", self.bits_allocated),
								("bits_stored", self.bits_stored),
								("high_bit", self.high_bit),
								("rescale_intercept", self.rescale_intercept),
								("rescale_slope", self.rescale_slope),
								("cols", self.cols),
								("rows", self.rows)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("img", self.img.toStr()),
								("bits_allocated", self.bits_allocated),
								("bits_stored", self.bits_stored),
								("high_bit", self.high_bit),
								("rescale_intercept", self.rescale_intercept),
								("rescale_slope", self.rescale_slope),
								("cols", self.cols),
								("rows", self.rows)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("content", self.content.toStr()),
								("axis", self.axis),
								("position", self.position),
								("thickness", self.thickness),
								("instance_number", self.instance_number),
								("samples_per_pixel", self.samples_per_pixel),
								("pixel_rep", self.pixel_rep),
								("pixel_spacing", self.pixel_spacing),
								("image_position", self.image_position),
								("image_orientation", self.image_orientation),
								("photometric_interpretation", self.photometric_interpretation)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("content", self.content.toStr()),
								("axis", self.axis),
								("position", self.position),
								("thickness", self.thickness),
								("instance_number", self.instance_number),
								("samples_per_pixel", self.samples_per_pixel),
								("pixel_rep", self.pixel_rep),
								("pixel_spacing", self.pixel_spacing),
								("image_position", self.image_position),
								("image_orientation", self.image_orientation),
								("photometric_interpretation", self.photometric_interpretation)
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("dose", self.dose.toStr()),
								("number_frames", self.number_frames),
								("frame_spacing", self.frame_spacing),
								("frame_increment_pointer", self.frame_increment_pointer),
								("study", self.study.toStr())
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("slice", self.slice.toStr()),
								("patient_position", self.patient_position.toStr()),
								("study", self.study.toStr())
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("image", self.image.toStr()),
								("patient_position", self.patient_position.toStr()),
								("study", self.study.toStr())
			]) 
		return values 

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

	def toStr(self):
		values = OrderedDict([("class_uid", self.class_uid),
								("instance_uid", self.instance_uid),
								("series_uid", self.series_uid),
								("elements", self.elements),
								("sequences", self.sequences),
								("creationDate", self.creationDate),
								("creationTime", self.creationTime),
								("patient_metadata", self.patient_metadata.toStr())
								("modality", self.modality.toStr()),
			]) 
		return values 

class dicom_object:

	#Initialize
	def __init__(self):
		self.type = ""
		self.structure_set = rt_structure_set.toStr()
		self.ct_image = ct_image_slice.toStr()
		self.ct_image_set = ct_image_set.toStr()
		self.dose = rt_dose.toStr()
		self.plan = rt_plan.toStr()

	def toStr(self):
		if (self.type == 'structure_set'):
			values = OrderedDict([("structure_set", self.structure_set.toStr()),
									("type", self.type)
				]) 
			return values 
		elif (self.type == 'ct_image'):
			values = OrderedDict([("ct_image", self.ct_image.toStr()),
									("type", self.type)
				]) 
			return values 
		elif (self.type == 'ct_image_set'):
			values = OrderedDict([("ct_image_set", self.ct_image_set.toStr()),
									("type", self.type)
				]) 
			return values 
		elif (self.type == 'dose'):
			values = OrderedDict([("dose", self.dose.toStr()),
									("type", self.type)
				]) 
			return values 
		elif (self.type == 'plan'):
			values = OrderedDict([("plan", self.plan.toStr()),
									("type", self.type)
				]) 
			return values 
		else:
			return "Type not Set" 

class dicom_data:

	#Initialize
	def __init__(self):
		self.meta_data = dicom_metadata()
		self.dicom_obj = dicom_object()

	def toStr(self):
		values = OrderedDict([("meta_data", self.meta_data.toStr()),
								("dicom_obj", self.dicom_obj.toStr())
			]) 
		return values 

class dicom_patient:

	#Initialize
	def __init__(self):
		self.patient = [] 

	def toStr(self):
		values = OrderedDict([("patient", self.patient),
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

class pbs_deliverable_energy:

	#Initialize
	def __init__(self):
		self.r90 = 0.0 
		self.energy = 0.0 

	def toStr(self):
		values = OrderedDict([("r90", self.r90),
								("energy", self.energy)
								("r80", self.r80),
			]) 
		return values 

class pbs_modeled_energy:

	#Initialize
	def __init__(self):
		self.r90 = 0.0 
		self.w80 = 0.0 
		self.energy = 0.0 
		self.sigma = pbs_optical_sigma()
		self.pristine_peak = irregularly_sampled_function()

	def toStr(self):
		values = OrderedDict([("r90", self.r90),
								("w80", self.w80),
								("energy", self.energy),
								("r100", self.r100),
								("sigma", self.sigma.toStr())
								("pristine_peak", self.pristine_peak.toStr()),
			]) 
		return values 

class pbs_machine_spec:

	#Initialize
	def __init__(self):
		self.modeled_energies = [] 
		self.deliverable_energies = [] 
		self.source_rotation_function = linear_function()
		self.aperture_sad = [] 
		self.sad = [] 
		self.halo_sigma_sq_function = quadratic_function()
		self.sigma_v = 0.0 

	def toStr(self):
		values = OrderedDict([("modeled_energies", self.modeled_energies),
								("deliverable_energies", self.deliverable_energies),
								("source_rotation_function", self.source_rotation_function.toStr()),
								("aperture_sad", self.aperture_sad),
								("sad", self.sad),
								("halo_sigma_sq_function", self.halo_sigma_sq_function.toStr()),
								("sigma_v", self.sigma_v)
			]) 
		return values 

class pbs_layer_spacing_strategy:

	#Initialize
	def __init__(self):
		self.constant = 0
		self.distal_w80 = 1
		self.variable_w80 = 2

	def toStr(self):
		values = OrderedDict([("constant", self.constant),
								("distal_w80", self.distal_w80),
								("variable_w80", self.variable_w80)
			]) 
		return values 

class spot_spacing_strategy:

	#Initialize
	def __init__(self):
		self.constant = 0
		self.sigma = 1

	def toStr(self):
		values = OrderedDict([("constant", self.constant),
								("sigma", self.sigma)
			]) 
		return values 

class pbs_optical_sigma:

	#Initialize
	def __init__(self):
		self.x = quadratic_function()
		self.y = quadratic_function()

	def toStr(self):
		values = OrderedDict([("x", self.x.toStr()),
								("y", self.y.toStr())
			]) 
		return values 

class pbs_pb_calculation_layer:

	#Initialize
	def __init__(self):
		self.flixels = [] 
		self.r90 = 0.0 
		self.energy = 0.0 
		self.sigma = pbs_optical_sigma()
		self.flixel_rotation = 0.0 
		self.pristine_peak = interpolated_function()

	def toStr(self):
		values = OrderedDict([("flixels", self.flixels),
								("r90", self.r90),
								("energy", self.energy),
								("sigma", self.sigma.toStr()),
								("flixel_rotation", self.flixel_rotation),
								("pristine_peak", self.pristine_peak.toStr())
			]) 
		return values 

class pbs_pb_aperture_model:

	#Initialize
	def __init__(self):
		self.aperture = aperture()
		self.sad = [] 

	def toStr(self):
		values = OrderedDict([("aperture", self.aperture.toStr()),
								("sad", self.sad)
			]) 
		return values 

class spot_placement:

	#Initialize
	def __init__(self):
		self.energy = 0.0 
		self.position = [] 

	def toStr(self):
		values = OrderedDict([("energy", self.energy),
								("position", self.position)
			]) 
		return values 

class weighted_spot:

	#Initialize
	def __init__(self):
		self.energy = 0.0 
		self.position = [] 
		self.fluence = 0.0 

	def toStr(self):
		values = OrderedDict([("energy", self.energy),
								("position", self.position),
								("fluence", self.fluence)
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

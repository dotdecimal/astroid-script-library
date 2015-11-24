# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:	Travis DeMint & Daniel Patenaude
# Date:		11/19/2015
# Desc:		Provides access to type usage for all types
# RT_Types Version:		1.0.0-beta10

from collections import OrderedDict
import base64
import struct as st

def parse_bytes_i(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('i',buf,offset)
		data.append(tmp[0])
		offset += 4
	return data

def parse_bytes_1i(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('i',buf,offset)
		data.append([tmp[0]])
		offset += 4
	return data

def parse_bytes_2i(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('ii',buf,offset)
		data.append([tmp[0],tmp[1]])
		offset += 8
	return data

def parse_bytes_3i(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('iii',buf,offset)
		data.append([tmp[0],tmp[1],tmp[2]])
		offset += 12
	return data

def parse_bytes_d(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('d',buf,offset)
		data.append(tmp[0])
		offset += 8
	return data

def parse_bytes_1d(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('d',buf,offset)
		data.append([tmp[0]])
		offset += 8
	return data

def parse_bytes_2d(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('dd',buf,offset)
		data.append([tmp[0],tmp[1]])
		offset += 16
	return data

def parse_bytes_3d(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('ddd',buf,offset)
		data.append([tmp[0],tmp[1],tmp[2]])
		offset += 24
	return data

def parse_bytes_ul(buf, offset=0):
	tmp = st.unpack_from('Q',buf,offset)
	return tmp[0]

def parse_bytes_u(buf, offset=0):
	tmp = st.unpack_from('I',buf,offset)
	return tmp[0]

def parse_bytes_f(buf, offset=0):
	tmp = st.unpack_from('f',buf,offset)
	return tmp[0]

def parse_array(obj, buf, offset=0):
	data = []
	while len(buf) - offset >= obj.get_offset():
		data.append(obj.parse_self(buf,offset))
		offset += obj.get_offset()
	return data

def parse_bytes_not_defined(buf, offset=0):
	print("Parse Bytes Function Not Defined, Contact .decimal")
	sys.exit()

class blob_type(object):

	def __init__(self):
		self.blob = ""
		self.type = "base64-encoded-blob"

	def toStr(self):
		values = OrderedDict([("blob", self.blob), 
								("type", self.type)
			])
		return values

class adaptive_grid(object):

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.voxels = blob.toStr()
		self.extents = box_3d()
		blob = blob_type()
		self.volumes = blob.toStr()

	def expand_data(self):
		data = {}
		data['voxels'] = parse_bytes_daptive_grid_voxel(base64.b64decode(self.voxels['blob']))
		data['extents'] = self.extents.expand_data()
		data['volumes'] = parse_bytes_i(base64.b64decode(self.volumes['blob']))
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'extents':
					self.extents.from_json(v)
				else:
					setattr(self, k, v)

class adaptive_grid_region(object):

	#Initialize
	def __init__(self):
		self.region = optimized_triangle_mesh()
		self.maximum_spacing = 0.0 

	def expand_data(self):
		data = {}
		data['region'] = self.region.expand_data()
		data['maximum_spacing'] = self.maximum_spacing
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'region':
					self.region.from_json(v)
				else:
					setattr(self, k, v)

class adaptive_grid_voxel(object):

	#Initialize
	def __init__(self):
		self.index = 0 
		self.surface_count = 0 
		self.volume_offset = 0 
		self.inside_count = 0 

	def expand_data(self):
		data = {}
		data['index'] = self.index
		data['surface_count'] = self.surface_count
		data['volume_offset'] = self.volume_offset
		data['inside_count'] = self.inside_count
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class aperture(object):

	#Initialize
	def __init__(self):
		self.shape = polyset()
		self.downstream_edge = 0.0 

	def expand_data(self):
		data = {}
		data['shape'] = self.shape.expand_data()
		data['downstream_edge'] = self.downstream_edge
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'shape':
					self.shape.from_json(v)
				else:
					setattr(self, k, v)

class aperture_centerline(object):

	#Initialize
	def __init__(self):
		self.margin = 0.0 
		self.structure = triangle_mesh()

	def expand_data(self):
		data = {}
		data['margin'] = self.margin
		data['structure'] = self.structure.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'structure':
					self.structure.from_json(v)
				else:
					setattr(self, k, v)

class aperture_corner_plane(object):

	#Initialize
	def __init__(self):
		self.second_direction = 0.0 
		self.first_direction = 0.0 
		self.origin = [] 

	def expand_data(self):
		data = {}
		data['second_direction'] = self.second_direction
		data['first_direction'] = self.first_direction
		data['origin'] = self.origin
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class aperture_creation_params(object):

	#Initialize
	def __init__(self):
		self.half_planes = [] 
		self.organs = [] 
		self.downstream_edge = 0.0 
		self.targets = [] 
		self.overrides = [] 
		self.target_margin = 0.0 
		self.centerlines = [] 
		self.mill_radius = 0.0 
		self.corner_planes = [] 

	def expand_data(self):
		data = {}
		half_plane = []
		for x in self.half_planes:
			s = aperture_half_plane()
			s.from_json(x)
			half_plane.append(s.expand_data())
		data['half_planes'] = half_plane
		organ = []
		for x in self.organs:
			s = aperture_organ()
			s.from_json(x)
			organ.append(s.expand_data())
		data['organs'] = organ
		data['downstream_edge'] = self.downstream_edge
		target = []
		for x in self.targets:
			s = triangle_mesh()
			s.from_json(x)
			target.append(s.expand_data())
		data['targets'] = target
		override = []
		for x in self.overrides:
			s = aperture_manual_override()
			s.from_json(x)
			override.append(s.expand_data())
		data['overrides'] = override
		data['target_margin'] = self.target_margin
		centerline = []
		for x in self.centerlines:
			s = aperture_centerline()
			s.from_json(x)
			centerline.append(s.expand_data())
		data['centerlines'] = centerline
		data['mill_radius'] = self.mill_radius
		corner_plane = []
		for x in self.corner_planes:
			s = aperture_corner_plane()
			s.from_json(x)
			corner_plane.append(s.expand_data())
		data['corner_planes'] = corner_plane
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class aperture_half_plane(object):

	#Initialize
	def __init__(self):
		self.direction = 0.0 
		self.origin = [] 

	def expand_data(self):
		data = {}
		data['direction'] = self.direction
		data['origin'] = self.origin
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class aperture_manual_override(object):

	#Initialize
	def __init__(self):
		self.shape = polyset()
		self.add_shape_to_opening = False 

	def expand_data(self):
		data = {}
		data['shape'] = self.shape.expand_data()
		data['add_shape_to_opening'] = self.add_shape_to_opening
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'shape':
					self.shape.from_json(v)
				else:
					setattr(self, k, v)

class aperture_organ(object):

	#Initialize
	def __init__(self):
		self.margin = 0.0 
		self.occlude_by_target = False 
		self.structure = triangle_mesh()

	def expand_data(self):
		data = {}
		data['margin'] = self.margin
		data['occlude_by_target'] = self.occlude_by_target
		data['structure'] = self.structure.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'structure':
					self.structure.from_json(v)
				else:
					setattr(self, k, v)

class aperture_target(object):

	#Initialize
	def __init__(self):
		self.margin = 0.0 
		self.structure = triangle_mesh()

	def expand_data(self):
		data = {}
		data['margin'] = self.margin
		data['structure'] = self.structure.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'structure':
					self.structure.from_json(v)
				else:
					setattr(self, k, v)

class app_level_page(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# settings
		# app_contents
		# app_info
		# notifications

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class arithmetic_operation(object):

	#Initialize
	def __init__(self):
		self.op = arithmetic_operator()
		self.right = machine_expression()
		self.left = machine_expression()

	def expand_data(self):
		data = {}
		data['op'] = self.op.expand_data()
		data['right'] = self.right.expand_data()
		data['left'] = self.left.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'op':
					self.op.from_json(v)
				elif k == 'right':
					self.right.from_json(v)
				elif k == 'left':
					self.left.from_json(v)
				else:
					setattr(self, k, v)

class arithmetic_operator(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# subtraction
		# multiplication
		# addition
		# division

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class base_zoom_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# fit_scene
		# fit_scene_width
		# stretch_to_fit
		# fill_canvas
		# fit_scene_height

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class beam_geometry(object):

	#Initialize
	def __init__(self):
		self.image_to_beam = [] 
		self.sad = [] 

	def expand_data(self):
		data = {}
		data['image_to_beam'] = self.image_to_beam
		data['sad'] = self.sad
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class beam_model(object):

	#Initialize
	def __init__(self):
		self.name = "" 
		self.data = radiation_machine_data()

	def expand_data(self):
		data = {}
		data['name'] = self.name
		data['data'] = self.data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'data':
					self.data.from_json(v)
				else:
					setattr(self, k, v)

class beam_properties(object):

	#Initialize
	def __init__(self):
		self.field = box_2d()
		self.geometry = beam_geometry()
		self.range = 0.0 
		self.bixel_grid = regular_grid_2d()
		self.ssd = 0.0 

	def expand_data(self):
		data = {}
		data['field'] = self.field.expand_data()
		data['geometry'] = self.geometry.expand_data()
		data['range'] = self.range
		data['bixel_grid'] = self.bixel_grid.expand_data()
		data['ssd'] = self.ssd
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'field':
					self.field.from_json(v)
				elif k == 'geometry':
					self.geometry.from_json(v)
				elif k == 'bixel_grid':
					self.bixel_grid.from_json(v)
				else:
					setattr(self, k, v)

class bin_collection_3d(object):

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.bins = blob.toStr()
		blob = blob_type()
		self.counts = blob.toStr()
		self.bounds = box_3d()
		blob = blob_type()
		self.offsets = blob.toStr()
		self.grid_size = [] 

	def expand_data(self):
		data = {}
		data['bins'] = parse_bytes_temType(base64.b64decode(self.bins['blob']))
		data['counts'] = parse_bytes_u(base64.b64decode(self.counts['blob']))
		data['bounds'] = self.bounds.expand_data()
		data['offsets'] = parse_bytes_u(base64.b64decode(self.offsets['blob']))
		data['grid_size'] = self.grid_size
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'bounds':
					self.bounds.from_json(v)
				else:
					setattr(self, k, v)

class biological_structure_parameters(object):

	#Initialize
	def __init__(self):
		self.a = 0.0 
		self.alphabeta = 0.0 
		self.cutoff = 0.0 
		self.gamma50 = 0.0 
		self.d50 = 0.0 

	def expand_data(self):
		data = {}
		data['a'] = self.a
		data['alphabeta'] = self.alphabeta
		data['cutoff'] = self.cutoff
		data['gamma50'] = self.gamma50
		data['d50'] = self.d50
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class bixel_geometry(object):

	#Initialize
	def __init__(self):
		self.axis = projected_isocentric_vector()
		self.size = projected_isocentric_vector()

	def expand_data(self):
		data = {}
		data['axis'] = self.axis.expand_data()
		data['size'] = self.size.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'axis':
					self.axis.from_json(v)
				elif k == 'size':
					self.size.from_json(v)
				else:
					setattr(self, k, v)

class block_geometry(object):

	#Initialize
	def __init__(self):
		self.shape = polyset()
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['shape'] = self.shape.expand_data()
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'shape':
					self.shape.from_json(v)
				else:
					setattr(self, k, v)

class box_1d(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.corner = [] 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['corner'] = self.corner
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class box_2d(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.corner = [] 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['corner'] = self.corner
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class box_3d(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.corner = [] 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['corner'] = self.corner
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class box_4d(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.corner = [] 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['corner'] = self.corner
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class camera(object):

	#Initialize
	def __init__(self):
		self.position = [] 
		self.zoom = 0.0 

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['zoom'] = self.zoom
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class camera3(object):

	#Initialize
	def __init__(self):
		self.position = [] 
		self.up = [] 
		self.direction = [] 
		self.zoom = 0.0 

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['up'] = self.up
		data['direction'] = self.direction
		data['zoom'] = self.zoom
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class channel_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# double
		# uint8
		# int64
		# float
		# uint64
		# int8
		# uint16
		# int32
		# uint32
		# int16

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class circle(object):

	#Initialize
	def __init__(self):
		self.radius = 0.0 
		self.center = [] 

	def expand_data(self):
		data = {}
		data['radius'] = self.radius
		data['center'] = self.center
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class color_map_level(object):

	#Initialize
	def __init__(self):
		self.level = 0.0 
		self.color = rgba8()

	def expand_data(self):
		data = {}
		data['level'] = self.level
		data['color'] = self.color.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				else:
					setattr(self, k, v)

class colored_vertex_2d(object):

	#Initialize
	def __init__(self):
		self.position = [] 
		self.color = rgba8()

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['color'] = self.color.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				else:
					setattr(self, k, v)

class ct_image_data(object):

	#Initialize
	def __init__(self):
		self.image_set = ct_image_set.toStr()
		self.image_slices = []

class ct_image_set(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.sequences = [] 
		self.class_uid = "" 
		self.patient_position = patient_position_type()
		self.image = image_3d()
		self.meta_data = dicom_metadata()
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['patient_position'] = self.patient_position.expand_data()
		data['image'] = self.image.expand_data()
		data['meta_data'] = self.meta_data.expand_data()
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_position':
					self.patient_position.from_json(v)
				elif k == 'image':
					self.image.from_json(v)
				elif k == 'meta_data':
					self.meta_data.from_json(v)
				else:
					setattr(self, k, v)

class ct_image_slice(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.sequences = [] 
		self.referenced_ids = [] 
		self.class_uid = "" 
		self.patient_position = patient_position_type()
		self.slice = rt_image_slice_2d()
		self.instance_uid = "" 
		self.meta_data = dicom_metadata()

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		referenced_id = []
		for x in self.referenced_ids:
			s = ref_dicom_item()
			s.from_json(x)
			referenced_id.append(s.expand_data())
		data['referenced_ids'] = referenced_id
		data['class_uid'] = self.class_uid
		data['patient_position'] = self.patient_position.expand_data()
		data['slice'] = self.slice.expand_data()
		data['instance_uid'] = self.instance_uid
		data['meta_data'] = self.meta_data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_position':
					self.patient_position.from_json(v)
				elif k == 'slice':
					self.slice.from_json(v)
				elif k == 'meta_data':
					self.meta_data.from_json(v)
				else:
					setattr(self, k, v)

class data_reporting_parameters(object):

	#Initialize
	def __init__(self):
		self.units = "" 
		self.digits = 0 
		self.label = "" 

	def expand_data(self):
		data = {}
		data['units'] = self.units
		data['digits'] = self.digits
		data['label'] = self.label
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class degrader_geometry(object):

	#Initialize
	def __init__(self):
		self.shape = degrader_shape()
		self.downstream_edge = 0.0 
		self.thickness_units = "" 
		self.scale_factor = 0.0 

	def expand_data(self):
		data = {}
		data['shape'] = self.shape.expand_data()
		data['downstream_edge'] = self.downstream_edge
		data['thickness_units'] = self.thickness_units
		data['scale_factor'] = self.scale_factor
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'shape':
					self.shape.from_json(v)
				else:
					setattr(self, k, v)

class degrader_shape(object):

	#Initialize
	def __init__(self):
		self.rc_nurb = rc_nurb_geometry.toStr()
		self.shifter = shifter_geometry.toStr()
		self.block = block_geometry.toStr()
		self.rc = rc_geometry.toStr()

class department(object):

	#Initialize
	def __init__(self):
		self.description = "" 
		self.machines = [] 
		self.name = "" 

	def expand_data(self):
		data = {}
		data['description'] = self.description
		machine = []
		for x in self.machines:
			s = treatment_machine()
			s.from_json(x)
			machine.append(s.expand_data())
		data['machines'] = machine
		data['name'] = self.name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_data(object):

	#Initialize
	def __init__(self):
		self.dicom_obj = "" 
		self.meta_data = dicom_metadata()

	def expand_data(self):
		data = {}
		data['dicom_obj'] = self.dicom_obj
		data['meta_data'] = self.meta_data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'meta_data':
					self.meta_data.from_json(v)
				else:
					setattr(self, k, v)

class dicom_element(object):

	#Initialize
	def __init__(self):
		self.g = 0 
		self.value = "" 
		self.e = 0 
		self.name = "" 

	def expand_data(self):
		data = {}
		data['g'] = self.g
		data['value'] = self.value
		data['e'] = self.e
		data['name'] = self.name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_file(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.class_uid = "" 
		self.ref_instance_uid = "" 
		self.instance_uid = "" 
		self.meta_data = dicom_metadata()

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['instance_uid'] = self.instance_uid
		data['meta_data'] = self.meta_data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'meta_data':
					self.meta_data.from_json(v)
				else:
					setattr(self, k, v)

class dicom_item(object):

	#Initialize
	def __init__(self):
		self.elements = [] 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_metadata(object):

	#Initialize
	def __init__(self):
		self.elements = [] 
		self.modality = dicom_modality()
		self.creationDate = "" 
		self.class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.patient_metadata = patient()
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['modality'] = self.modality.expand_data()
		data['creationDate'] = self.creationDate
		data['class_uid'] = self.class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		data['patient_metadata'] = self.patient_metadata.expand_data()
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'modality':
					self.modality.from_json(v)
				elif k == 'patient_metadata':
					self.patient_metadata.from_json(v)
				else:
					setattr(self, k, v)

class dicom_modality(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# rtstruct
		# rtdose
		# ct
		# rtplan

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class dicom_object(object):

	#Initialize
	def __init__(self):
		self.dose = rt_dose.toStr()
		self.structure_set = rt_structure_set.toStr()
		self.ct_image = ct_image_data.toStr()
		self.plan = rt_plan.toStr()

class dicom_patient(object):

	#Initialize
	def __init__(self):
		self.studies = [] 

	def expand_data(self):
		data = {}
		studie = []
		for x in self.studies:
			s = rt_study()
			s.from_json(x)
			studie.append(s.expand_data())
		data['studies'] = studie
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_sequence(object):

	#Initialize
	def __init__(self):
		self.g = 0 
		self.e = 0 
		self.items = [] 

	def expand_data(self):
		data = {}
		data['g'] = self.g
		data['e'] = self.e
		item = []
		for x in self.items:
			s = dicom_item()
			s.from_json(x)
			item.append(s.expand_data())
		data['items'] = item
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_structure_geometry(object):

	#Initialize
	def __init__(self):
		self.elements = [] 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.slices = [] 
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		slice = []
		for x in self.slices:
			s = dicom_structure_geometry_slice()
			s.from_json(x)
			slice.append(s.expand_data())
		data['slices'] = slice
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_structure_geometry_slice(object):

	#Initialize
	def __init__(self):
		self.elements = [] 
		self.ref_class_uid = "" 
		self.region = polyset()
		self.class_uid = "" 
		self.ref_instance_uid = "" 
		self.thickness = 0.0 
		self.series_uid = "" 
		self.position = 0.0 
		self.sequences = [] 
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['region'] = self.region.expand_data()
		data['class_uid'] = self.class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['thickness'] = self.thickness
		data['series_uid'] = self.series_uid
		data['position'] = self.position
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'region':
					self.region.from_json(v)
				else:
					setattr(self, k, v)

class dij_entry(object):

	#Initialize
	def __init__(self):
		self.dose = 0.0 
		self.beamlet_index = 0 

	def parse_self(self, buf, offset):
		self.beamlet_index = parse_bytes_u(buf, offset)
		self.dose = parse_bytes_f(buf, offset + 4)
		return self.expand_data()

	def get_offset(self):
		return 8

	def expand_data(self):
		data = {}
		data['dose'] = self.dose
		data['beamlet_index'] = self.beamlet_index
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dij_matrix(object):

	#Initialize
	def __init__(self):
		self.n_beamlets = 0 
		blob = blob_type()
		self.rows = blob.toStr()
		blob = blob_type()
		self.entries = blob.toStr()
		self.n_points = 0 

	def expand_data(self):
		data = {}
		data['n_beamlets'] = self.n_beamlets
		dijrow = dij_row()
		data['rows'] = parse_array(dijrow, base64.b64decode(self.rows['blob']))
		dijentry = dij_entry()
		data['entries'] = parse_array(dijentry, base64.b64decode(self.entries['blob']))
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dij_row(object):

	#Initialize
	def __init__(self):
		self.n_entries = 0 
		self.offset = 0 

	def parse_self(self, buf, offset):
		self.offset = parse_bytes_ul(buf, offset)
		self.n_entries = parse_bytes_u(buf, offset + 8)
		return self.expand_data()

	def get_offset(self):
		return 16

	def expand_data(self):
		data = {}
		data['n_entries'] = self.n_entries
		data['offset'] = self.offset
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class display_layout_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# squares
		# two_rows
		# main_plus_column
		# main_plus_row
		# two_columns

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class display_state(object):

	#Initialize
	def __init__(self):
		self.selected_composition = "" 
		self.focused_view = "" 
		self.controls_expanded = False 

	def expand_data(self):
		data = {}
		data['selected_composition'] = self.selected_composition
		data['focused_view'] = self.focused_view
		data['controls_expanded'] = self.controls_expanded
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class display_view_composition(object):

	#Initialize
	def __init__(self):
		self.id = "" 
		self.label = "" 
		self.layout = display_layout_type()
		self.views = [] 

	def expand_data(self):
		data = {}
		data['id'] = self.id
		data['label'] = self.label
		data['layout'] = self.layout.expand_data()
		view = []
		for x in self.views:
			s = display_view_instance()
			s.from_json(x)
			view.append(s.expand_data())
		data['views'] = view
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'layout':
					self.layout.from_json(v)
				else:
					setattr(self, k, v)

class display_view_instance(object):

	#Initialize
	def __init__(self):
		self.instance_id = "" 
		self.type_id = "" 

	def expand_data(self):
		data = {}
		data['instance_id'] = self.instance_id
		data['type_id'] = self.type_id
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class divergent_grid(object):

	#Initialize
	def __init__(self):
		self.cax_length = 0.0 
		blob = blob_type()
		self.rays = blob.toStr()
		blob = blob_type()
		self.data = blob.toStr()
		self.grid = regular_grid_2d()
		self.source_dist = 0.0 
		self.z_position = 0.0 
		self.isUniform = False 

	def expand_data(self):
		data = {}
		data['cax_length'] = self.cax_length
		data['rays'] = parse_bytes_not_defined(base64.b64decode(self.rays['blob']))
		data['data'] = parse_bytes_not_defined(base64.b64decode(self.data['blob']))
		data['grid'] = self.grid.expand_data()
		data['source_dist'] = self.source_dist
		data['z_position'] = self.z_position
		data['isUniform'] = self.isUniform
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'grid':
					self.grid.from_json(v)
				else:
					setattr(self, k, v)

class dose_constraint(object):

	#Initialize
	def __init__(self):
		self.max = simple_dose_constraint.toStr()
		self.max_mean = simple_dose_constraint.toStr()
		self.min = simple_dose_constraint.toStr()
		self.min_mean = simple_dose_constraint.toStr()

class dose_objective(object):

	#Initialize
	def __init__(self):
		self.minimize_max = []
		self.minimize_overdose = ramp_dose_objective.toStr()
		self.maximize_min = []
		self.minimize_underdose = ramp_dose_objective.toStr()
		self.minimize_mean = []
		self.maximize_mean = []

class dose_summation_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# beam
		# plan
		# fraction

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class dose_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# physical
		# error
		# effective

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class double_scattering_machine_spec(object):

	#Initialize
	def __init__(self):
		self.options = [] 

	def expand_data(self):
		data = {}
		option = []
		for x in self.options:
			s = double_scattering_option()
			s.from_json(x)
			option.append(s.expand_data())
		data['options'] = option
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class double_scattering_option(object):

	#Initialize
	def __init__(self):
		self.track_length = 0 
		self.steps = [] 
		self.min_range = 0.0 
		self.penumbral_source_size = 0.0 
		self.sdm = [] 
		self.wts1 = 0.0 
		self.id = "" 
		self.bcm = [] 
		self.source_size_on_track = 0.0 
		self.max_range = 0.0 
		self.max_mod = 0.0 
		self.name = "" 
		self.pristine_peak = irregularly_sampled_function()
		self.mod_correction = [] 

	def expand_data(self):
		data = {}
		data['track_length'] = self.track_length
		step = []
		for x in self.steps:
			s = double_scattering_step()
			s.from_json(x)
			step.append(s.expand_data())
		data['steps'] = step
		data['min_range'] = self.min_range
		data['penumbral_source_size'] = self.penumbral_source_size
		data['sdm'] = self.sdm
		data['wts1'] = self.wts1
		data['id'] = self.id
		data['bcm'] = self.bcm
		data['source_size_on_track'] = self.source_size_on_track
		data['max_range'] = self.max_range
		data['max_mod'] = self.max_mod
		data['name'] = self.name
		data['pristine_peak'] = self.pristine_peak.expand_data()
		data['mod_correction'] = self.mod_correction
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'pristine_peak':
					self.pristine_peak.from_json(v)
				else:
					setattr(self, k, v)

class double_scattering_step(object):

	#Initialize
	def __init__(self):
		self.theta = 0.0 
		self.dR = 0.0 
		self.weight = 0.0 

	def expand_data(self):
		data = {}
		data['theta'] = self.theta
		data['dR'] = self.dR
		data['weight'] = self.weight
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class drr_options(object):

	#Initialize
	def __init__(self):
		self.max_value = 0.0 
		self.image_display_options = gray_image_display_options()
		self.min_value = 0.0 
		self.image_z = 0.0 
		self.sizing = regular_grid_2d()
		self.max_z = 0.0 
		self.min_z = 0.0 

	def expand_data(self):
		data = {}
		data['max_value'] = self.max_value
		data['image_display_options'] = self.image_display_options.expand_data()
		data['min_value'] = self.min_value
		data['image_z'] = self.image_z
		data['sizing'] = self.sizing.expand_data()
		data['max_z'] = self.max_z
		data['min_z'] = self.min_z
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'image_display_options':
					self.image_display_options.from_json(v)
				elif k == 'sizing':
					self.sizing.from_json(v)
				else:
					setattr(self, k, v)

class facility(object):

	#Initialize
	def __init__(self):
		self.description = "" 
		self.departments = [] 
		self.name = "" 

	def expand_data(self):
		data = {}
		data['description'] = self.description
		department = []
		for x in self.departments:
			s = department()
			s.from_json(x)
			department.append(s.expand_data())
		data['departments'] = department
		data['name'] = self.name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class filesystem_item(object):

	#Initialize
	def __init__(self):
		self.name = "" 
		self.contents = filesystem_item_contents()

	def expand_data(self):
		data = {}
		data['name'] = self.name
		data['contents'] = self.contents.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'contents':
					self.contents.from_json(v)
				else:
					setattr(self, k, v)

class filesystem_item_contents(object):

	#Initialize
	def __init__(self):
		self.directory = []
		self.file = blob_type()

class function_sample(object):

	#Initialize
	def __init__(self):
		self.value = 0.0 
		self.delta = 0.0 

	def expand_data(self):
		data = {}
		data['value'] = self.value
		data['delta'] = self.delta
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class gaussian_sample_point(object):

	#Initialize
	def __init__(self):
		self.point = [] 
		self.weight = 0.0 

	def expand_data(self):
		data = {}
		data['point'] = self.point
		data['weight'] = self.weight
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class graph_line_style_info(object):

	#Initialize
	def __init__(self):
		self.color = rgba8()

	def expand_data(self):
		data = {}
		data['color'] = self.color.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				else:
					setattr(self, k, v)

class gray_image_display_options(object):

	#Initialize
	def __init__(self):
		self.level = 0.0 
		self.window = 0.0 

	def expand_data(self):
		data = {}
		data['level'] = self.level
		data['window'] = self.window
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class grid_cell_inclusion_info(object):

	#Initialize
	def __init__(self):
		self.cells_inside = [] 

	def expand_data(self):
		data = {}
		cells_insid = []
		for x in self.cells_inside:
			s = weighted_grid_index()
			s.from_json(x)
			cells_insid.append(s.expand_data())
		data['cells_inside'] = cells_insid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class gui_task_state(object):

	#Initialize
	def __init__(self):
		self.open_subtask_count = 0 
		self.canceled_subtask_count = 0 
		self.active_subtask = "" 
		self.type = "" 
		self.completed_subtask_count = 0 

	def expand_data(self):
		data = {}
		data['open_subtask_count'] = self.open_subtask_count
		data['canceled_subtask_count'] = self.canceled_subtask_count
		data['active_subtask'] = self.active_subtask
		data['type'] = self.type
		data['completed_subtask_count'] = self.completed_subtask_count
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class id_and_type(object):

	#Initialize
	def __init__(self):
		self.id = "" 
		self.type = "" 

	def expand_data(self):
		data = {}
		data['id'] = self.id
		data['type'] = self.type
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class image_1d(object):

	#Initialize
	def __init__(self):
		self.axes = [] 
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()
		self.size = [] 
		self.type_info = variant_type_info()
		self.origin = [] 
		self.value_mapping = linear_function()

	def expand_data(self):
		data = {}
		data['axes'] = self.axes
		data['units'] = self.units
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['origin'] = self.origin
		data['value_mapping'] = self.value_mapping.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type_info':
					self.type_info.from_json(v)
				elif k == 'value_mapping':
					self.value_mapping.from_json(v)
				else:
					setattr(self, k, v)

class image_2d(object):

	#Initialize
	def __init__(self):
		self.axes = [] 
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()
		self.size = [] 
		self.type_info = variant_type_info()
		self.origin = [] 
		self.value_mapping = linear_function()

	def expand_data(self):
		data = {}
		data['axes'] = self.axes
		data['units'] = self.units
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['origin'] = self.origin
		data['value_mapping'] = self.value_mapping.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type_info':
					self.type_info.from_json(v)
				elif k == 'value_mapping':
					self.value_mapping.from_json(v)
				else:
					setattr(self, k, v)

class image_3d(object):

	#Initialize
	def __init__(self):
		self.axes = [] 
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()
		self.size = [] 
		self.type_info = variant_type_info()
		self.origin = [] 
		self.value_mapping = linear_function()

	def expand_data(self):
		data = {}
		data['axes'] = self.axes
		data['units'] = self.units
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['origin'] = self.origin
		data['value_mapping'] = self.value_mapping.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type_info':
					self.type_info.from_json(v)
				elif k == 'value_mapping':
					self.value_mapping.from_json(v)
				else:
					setattr(self, k, v)

class image_geometry_1d(object):

	#Initialize
	def __init__(self):
		self.out_of_plane_info = linear_function()
		self.slicing = [] 
		self.regular_grid = regular_grid_1d()

	def expand_data(self):
		data = {}
		data['out_of_plane_info'] = self.out_of_plane_info.expand_data()
		data['slicing'] = self.slicing
		data['regular_grid'] = self.regular_grid.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'regular_grid':
					self.regular_grid.from_json(v)
				else:
					setattr(self, k, v)

class image_geometry_2d(object):

	#Initialize
	def __init__(self):
		self.out_of_plane_info = regular_grid_1d()
		self.slicing = [] 
		self.regular_grid = regular_grid_2d()

	def expand_data(self):
		data = {}
		data['out_of_plane_info'] = self.out_of_plane_info.expand_data()
		data['slicing'] = self.slicing
		data['regular_grid'] = self.regular_grid.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'regular_grid':
					self.regular_grid.from_json(v)
				else:
					setattr(self, k, v)

class image_geometry_3d(object):

	#Initialize
	def __init__(self):
		self.out_of_plane_info = regular_grid_2d()
		self.slicing = [] 
		self.regular_grid = regular_grid_3d()

	def expand_data(self):
		data = {}
		data['out_of_plane_info'] = self.out_of_plane_info.expand_data()
		data['slicing'] = self.slicing
		data['regular_grid'] = self.regular_grid.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'regular_grid':
					self.regular_grid.from_json(v)
				else:
					setattr(self, k, v)

class image_geometry_4d(object):

	#Initialize
	def __init__(self):
		self.out_of_plane_info = regular_grid_3d()
		self.slicing = [] 
		self.regular_grid = regular_grid_4d()

	def expand_data(self):
		data = {}
		data['out_of_plane_info'] = self.out_of_plane_info.expand_data()
		data['slicing'] = self.slicing
		data['regular_grid'] = self.regular_grid.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'regular_grid':
					self.regular_grid.from_json(v)
				else:
					setattr(self, k, v)

class image_slice_1d(object):

	#Initialize
	def __init__(self):
		self.axis = 0 
		self.position = 0.0 
		self.content = image_1d()
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['position'] = self.position
		data['content'] = self.content.expand_data()
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'content':
					self.content.from_json(v)
				else:
					setattr(self, k, v)

class image_slice_2d(object):

	#Initialize
	def __init__(self):
		self.axis = 0 
		self.position = 0.0 
		self.content = image_2d()
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['position'] = self.position
		data['content'] = self.content.expand_data()
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'content':
					self.content.from_json(v)
				else:
					setattr(self, k, v)

class image_slice_3d(object):

	#Initialize
	def __init__(self):
		self.axis = 0 
		self.position = 0.0 
		self.content = image_3d()
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['position'] = self.position
		data['content'] = self.content.expand_data()
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'content':
					self.content.from_json(v)
				else:
					setattr(self, k, v)

class interpolated_function(object):

	#Initialize
	def __init__(self):
		self.outside_domain_policy = outside_domain_policy()
		blob = blob_type()
		self.samples = blob.toStr()
		self.x_spacing = 0.0 
		self.x0 = 0.0 

	def expand_data(self):
		data = {}
		data['outside_domain_policy'] = self.outside_domain_policy.expand_data()
		data['samples'] = parse_bytes_unction_sample(base64.b64decode(self.samples['blob']))
		data['x_spacing'] = self.x_spacing
		data['x0'] = self.x0
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'outside_domain_policy':
					self.outside_domain_policy.from_json(v)
				else:
					setattr(self, k, v)

class irregularly_sampled_function(object):

	#Initialize
	def __init__(self):
		self.outside_domain_policy = outside_domain_policy()
		self.samples = [] 

	def expand_data(self):
		data = {}
		data['outside_domain_policy'] = self.outside_domain_policy.expand_data()
		data['samples'] = self.samples
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'outside_domain_policy':
					self.outside_domain_policy.from_json(v)
				else:
					setattr(self, k, v)

class item_list_view_mode(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# collapsed
		# compact
		# detailed

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class levelset2(object):

	#Initialize
	def __init__(self):
		self.values = image_2d()

	def expand_data(self):
		data = {}
		data['values'] = self.values.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'values':
					self.values.from_json(v)
				else:
					setattr(self, k, v)

class line_profile(object):

	#Initialize
	def __init__(self):
		self.axis = 0 
		self.position = 0.0 
		self.color = rgb8()

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['position'] = self.position
		data['color'] = self.color.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				else:
					setattr(self, k, v)

class line_stipple(object):

	#Initialize
	def __init__(self):
		self.pattern = 0 
		self.factor = 0 

	def expand_data(self):
		data = {}
		data['pattern'] = self.pattern
		data['factor'] = self.factor
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class line_stipple_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# none
		# dashed
		# dotted
		# solid

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class line_strip(object):

	#Initialize
	def __init__(self):
		self.vertices = [] 

	def expand_data(self):
		data = {}
		data['vertices'] = self.vertices
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class line_style(object):

	#Initialize
	def __init__(self):
		self.width = 0.0 
		self.stipple = line_stipple()

	def expand_data(self):
		data = {}
		data['width'] = self.width
		data['stipple'] = self.stipple.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'stipple':
					self.stipple.from_json(v)
				else:
					setattr(self, k, v)

class linear_function(object):

	#Initialize
	def __init__(self):
		self.slope = 0.0 
		self.intercept = 0.0 

	def expand_data(self):
		data = {}
		data['slope'] = self.slope
		data['intercept'] = self.intercept
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class list_item_mode(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# normal
		# editing
		# deleting

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class machine_expression(object):

	#Initialize
	def __init__(self):
		self.setting = ""
		self.operation = arithmetic_operation.toStr()

class machine_frame_of_reference(object):

	#Initialize
	def __init__(self):
		self.tags = [] 
		self.id = "" 
		self.label = "" 
		self.transformation = machine_transformation()
		self.nested = [] 

	def expand_data(self):
		data = {}
		tag = []
		for x in self.tags:
			s = machine_frame_tag()
			s.from_json(x)
			tag.append(s.expand_data())
		data['tags'] = tag
		data['id'] = self.id
		data['label'] = self.label
		data['transformation'] = self.transformation.expand_data()
		neste = []
		for x in self.nested:
			s = machine_frame_of_reference()
			s.from_json(x)
			neste.append(s.expand_data())
		data['nested'] = neste
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'transformation':
					self.transformation.from_json(v)
				else:
					setattr(self, k, v)

class machine_frame_tag(object):

	#Initialize
	def __init__(self):
		self.room = ""
		self.imaging = ""
		self.beam = ""
		self.couch = ""

class machine_geometry(object):

	#Initialize
	def __init__(self):
		self.frame_of_reference = machine_frame_of_reference()
		self.name = "" 

	def expand_data(self):
		data = {}
		data['frame_of_reference'] = self.frame_of_reference.expand_data()
		data['name'] = self.name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'frame_of_reference':
					self.frame_of_reference.from_json(v)
				else:
					setattr(self, k, v)

class machine_rotation(object):

	#Initialize
	def __init__(self):
		self.axis = [] 
		self.angle = machine_expression()

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['angle'] = self.angle.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'angle':
					self.angle.from_json(v)
				else:
					setattr(self, k, v)

class machine_setting(object):

	#Initialize
	def __init__(self):
		self.description = "" 
		self.units = "" 
		self.precision = 0 
		self.id = "" 
		self.range = min_max()
		self.label = "" 

	def expand_data(self):
		data = {}
		data['description'] = self.description
		data['units'] = self.units
		data['precision'] = self.precision
		data['id'] = self.id
		data['range'] = self.range.expand_data()
		data['label'] = self.label
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'range':
					self.range.from_json(v)
				else:
					setattr(self, k, v)

class machine_snout(object):

	#Initialize
	def __init__(self):
		self.slabs = min_max()
		self.field_size = [] 
		self.rc_info = min_max()
		self.shape = snout_shape()
		self.shifters = snout_shape()
		self.name = "" 
		self.extention = min_max()

	def expand_data(self):
		data = {}
		data['slabs'] = self.slabs.expand_data()
		data['field_size'] = self.field_size
		data['rc_info'] = self.rc_info.expand_data()
		data['shape'] = self.shape.expand_data()
		data['shifters'] = self.shifters.expand_data()
		data['name'] = self.name
		data['extention'] = self.extention.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'shape':
					self.shape.from_json(v)
				elif k == 'extention':
					self.extention.from_json(v)
				else:
					setattr(self, k, v)

class machine_transformation(object):

	#Initialize
	def __init__(self):
		self.rotation = machine_rotation.toStr()
		self.translation = machine_translation.toStr()

class machine_translation(object):

	#Initialize
	def __init__(self):
		self.vector = [] 

	def expand_data(self):
		data = {}
		vecto = []
		for x in self.vector:
			s = machine_expression()
			s.from_json(x)
			vecto.append(s.expand_data())
		data['vector'] = vecto
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class mco_navigation_objective(object):

	#Initialize
	def __init__(self):
		self.is_maximization = False 
		self.range = min_max()

	def expand_data(self):
		data = {}
		data['is_maximization'] = self.is_maximization
		data['range'] = self.range.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'range':
					self.range.from_json(v)
				else:
					setattr(self, k, v)

class mco_navigation_system(object):

	#Initialize
	def __init__(self):
		self.objectives = [] 
		self.plan_count = 0 
		self.p_matrix = [] 

	def expand_data(self):
		data = {}
		objective = []
		for x in self.objectives:
			s = mco_navigation_objective()
			s.from_json(x)
			objective.append(s.expand_data())
		data['objectives'] = objective
		data['plan_count'] = self.plan_count
		data['p_matrix'] = self.p_matrix
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class min_max(object):

	#Initialize
	def __init__(self):
		self.max = 0.0 
		self.min = 0.0 

	def expand_data(self):
		data = {}
		data['max'] = self.max
		data['min'] = self.min
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class multiple_source_view(object):

	#Initialize
	def __init__(self):
		self.up = [] 
		self.distance = [] 
		self.direction = [] 
		self.center = [] 
		self.display_surface = box_2d()

	def expand_data(self):
		data = {}
		data['up'] = self.up
		data['distance'] = self.distance
		data['direction'] = self.direction
		data['center'] = self.center
		data['display_surface'] = self.display_surface.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'display_surface':
					self.display_surface.from_json(v)
				else:
					setattr(self, k, v)

class notable_data_point(object):

	#Initialize
	def __init__(self):
		self.position = [] 
		self.label = "" 
		self.color = rgb8()

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['label'] = self.label
		data['color'] = self.color.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				else:
					setattr(self, k, v)

class nurb_surface(object):

	#Initialize
	def __init__(self):
		self.heights = [] 
		self.knots = [] 
		self.box = box_2d()
		self.order = [] 
		self.point_counts = [] 
		self.weights = [] 

	def expand_data(self):
		data = {}
		data['heights'] = self.heights
		data['knots'] = self.knots
		data['box'] = self.box.expand_data()
		data['order'] = self.order
		data['point_counts'] = self.point_counts
		data['weights'] = self.weights
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'box':
					self.box.from_json(v)
				else:
					setattr(self, k, v)

class optimized_triangle_mesh(object):

	#Initialize
	def __init__(self):
		self.bin_collection = bin_collection_3d()
		self.mesh = triangle_mesh()

	def expand_data(self):
		data = {}
		data['bin_collection'] = self.bin_collection.expand_data()
		data['mesh'] = self.mesh.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'bin_collection':
					self.bin_collection.from_json(v)
				elif k == 'mesh':
					self.mesh.from_json(v)
				else:
					setattr(self, k, v)

class out_of_plane_information(object):

	#Initialize
	def __init__(self):
		self.axis = 0 
		self.position = 0.0 
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['position'] = self.position
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class outside_domain_policy(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# extend_with_copies
		# always_zero

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class patient(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.other_ids = [] 
		self.comments = "" 
		self.other_names = [] 
		self.sequences = [] 
		self.ethnic_group = "" 
		self.class_uid = "" 
		self.id = "" 
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.birth_date = "" 
		self.ref_instance_uid = "" 
		self.name = person_name()
		self.sex = patient_sex()

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		data['comments'] = self.comments
		other_name = []
		for x in self.other_names:
			s = person_name()
			s.from_json(x)
			other_name.append(s.expand_data())
		data['other_names'] = other_name
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['ethnic_group'] = self.ethnic_group
		data['class_uid'] = self.class_uid
		data['id'] = self.id
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['birth_date'] = self.birth_date
		data['ref_instance_uid'] = self.ref_instance_uid
		data['name'] = self.name.expand_data()
		data['sex'] = self.sex.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'name':
					self.name.from_json(v)
				elif k == 'sex':
					self.sex.from_json(v)
				else:
					setattr(self, k, v)

class patient_position_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# hfdl
		# hfs
		# hfdr
		# ffp
		# hfp
		# ffdr
		# ffdl
		# ffs

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class patient_sex(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# o
		# f
		# m

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class pbs_deliverable_energy(object):

	#Initialize
	def __init__(self):
		self.r80 = 0.0 
		self.r90 = 0.0 
		self.energy = 0.0 

	def expand_data(self):
		data = {}
		data['r80'] = self.r80
		data['r90'] = self.r90
		data['energy'] = self.energy
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class pbs_layer_spacing_strategy(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# constant
		# distal_w80
		# variable_w80

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class pbs_machine_spec(object):

	#Initialize
	def __init__(self):
		self.sad = [] 
		self.modeled_energies = [] 
		self.halo_sigma_sq_function = quadratic_function()
		self.deliverable_energies = [] 
		self.aperture_sad = [] 
		self.source_rotation_function = linear_function()

	def expand_data(self):
		data = {}
		data['sad'] = self.sad
		modeled_energie = []
		for x in self.modeled_energies:
			s = pbs_modeled_energy()
			s.from_json(x)
			modeled_energie.append(s.expand_data())
		data['modeled_energies'] = modeled_energie
		data['halo_sigma_sq_function'] = self.halo_sigma_sq_function.expand_data()
		deliverable_energie = []
		for x in self.deliverable_energies:
			s = pbs_deliverable_energy()
			s.from_json(x)
			deliverable_energie.append(s.expand_data())
		data['deliverable_energies'] = deliverable_energie
		data['aperture_sad'] = self.aperture_sad
		data['source_rotation_function'] = self.source_rotation_function.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'halo_sigma_sq_function':
					self.halo_sigma_sq_function.from_json(v)
				elif k == 'source_rotation_function':
					self.source_rotation_function.from_json(v)
				else:
					setattr(self, k, v)

class pbs_modeled_energy(object):

	#Initialize
	def __init__(self):
		self.w80 = 0.0 
		self.sigma = pbs_optical_sigma()
		self.energy = 0.0 
		self.r90 = 0.0 
		self.pristine_peak = irregularly_sampled_function()
		self.r100 = 0.0 

	def expand_data(self):
		data = {}
		data['w80'] = self.w80
		data['sigma'] = self.sigma.expand_data()
		data['energy'] = self.energy
		data['r90'] = self.r90
		data['pristine_peak'] = self.pristine_peak.expand_data()
		data['r100'] = self.r100
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'sigma':
					self.sigma.from_json(v)
				elif k == 'pristine_peak':
					self.pristine_peak.from_json(v)
				else:
					setattr(self, k, v)

class pbs_optical_sigma(object):

	#Initialize
	def __init__(self):
		self.x = quadratic_function()
		self.y = quadratic_function()

	def expand_data(self):
		data = {}
		data['x'] = self.x.expand_data()
		data['y'] = self.y.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'x':
					self.x.from_json(v)
				elif k == 'y':
					self.y.from_json(v)
				else:
					setattr(self, k, v)

class pbs_pb_aperture_model(object):

	#Initialize
	def __init__(self):
		self.sad = [] 
		self.aperture = aperture()

	def expand_data(self):
		data = {}
		data['sad'] = self.sad
		data['aperture'] = self.aperture.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'aperture':
					self.aperture.from_json(v)
				else:
					setattr(self, k, v)

class pbs_pb_calculation_layer(object):

	#Initialize
	def __init__(self):
		self.sigma = pbs_optical_sigma()
		self.energy = 0.0 
		self.flixel_rotation = 0.0 
		self.r90 = 0.0 
		self.pristine_peak = interpolated_function()
		self.flixels = [] 

	def expand_data(self):
		data = {}
		data['sigma'] = self.sigma.expand_data()
		data['energy'] = self.energy
		data['flixel_rotation'] = self.flixel_rotation
		data['r90'] = self.r90
		data['pristine_peak'] = self.pristine_peak.expand_data()
		flixel = []
		for x in self.flixels:
			s = projected_isocentric_vector()
			s.from_json(x)
			flixel.append(s.expand_data())
		data['flixels'] = flixel
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'sigma':
					self.sigma.from_json(v)
				elif k == 'pristine_peak':
					self.pristine_peak.from_json(v)
				else:
					setattr(self, k, v)

class pbs_spot_layer(object):

	#Initialize
	def __init__(self):
		self.spot_tune_id = 0.0 
		self.num_spot_positions = 0 
		self.num_paintings = 0 
		self.spots = [] 
		self.spot_size = [] 

	def expand_data(self):
		data = {}
		data['spot_tune_id'] = self.spot_tune_id
		data['num_spot_positions'] = self.num_spot_positions
		data['num_paintings'] = self.num_paintings
		spot = []
		for x in self.spots:
			s = weighted_spot()
			s.from_json(x)
			spot.append(s.expand_data())
		data['spots'] = spot
		data['spot_size'] = self.spot_size
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class person_name(object):

	#Initialize
	def __init__(self):
		self.prefix = "" 
		self.given_name = "" 
		self.suffix = "" 
		self.family_name = "" 
		self.middle_name = "" 

	def expand_data(self):
		data = {}
		data['prefix'] = self.prefix
		data['given_name'] = self.given_name
		data['suffix'] = self.suffix
		data['family_name'] = self.family_name
		data['middle_name'] = self.middle_name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class pixel_format(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# rgba
		# gray
		# rgb

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class plane(object):

	#Initialize
	def __init__(self):
		self.normal = [] 
		self.point = [] 

	def expand_data(self):
		data = {}
		data['normal'] = self.normal
		data['point'] = self.point
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class point_rendering_options(object):

	#Initialize
	def __init__(self):
		self.line_thickness = 0.0 
		self.size = 0.0 
		self.line_type = line_stipple_type()

	def expand_data(self):
		data = {}
		data['line_thickness'] = self.line_thickness
		data['size'] = self.size
		data['line_type'] = self.line_type.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'line_type':
					self.line_type.from_json(v)
				else:
					setattr(self, k, v)

class point_sample_2d(object):

	#Initialize
	def __init__(self):
		self.position = [] 
		self.color = rgb8()

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['color'] = self.color.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				else:
					setattr(self, k, v)

class polygon2(object):

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.vertices = blob.toStr()

	def expand_data(self):
		data = {}
		data['vertices'] = parse_bytes_2d(base64.b64decode(self.vertices['blob']))
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class polyset(object):

	#Initialize
	def __init__(self):
		self.polygons = [] 
		self.holes = [] 

	def expand_data(self):
		data = {}
		polygon = []
		for x in self.polygons:
			s = polygon2()
			s.from_json(x)
			polygon.append(s.expand_data())
		data['polygons'] = polygon
		hole = []
		for x in self.holes:
			s = polygon2()
			s.from_json(x)
			hole.append(s.expand_data())
		data['holes'] = hole
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class projected_isocentric_vector(object):

	#Initialize
	def __init__(self):
		self.delta = [] 
		self.at_iso = [] 

	def expand_data(self):
		data = {}
		data['delta'] = self.delta
		data['at_iso'] = self.at_iso
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class proton_degrader(object):

	#Initialize
	def __init__(self):
		self.material = proton_material_properties()
		self.geometry = degrader_geometry()

	def expand_data(self):
		data = {}
		data['material'] = self.material.expand_data()
		data['geometry'] = self.geometry.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'material':
					self.material.from_json(v)
				elif k == 'geometry':
					self.geometry.from_json(v)
				else:
					setattr(self, k, v)

class proton_device_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# aperture
		# shifter
		# compensator

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class proton_material_properties(object):

	#Initialize
	def __init__(self):
		self.water_equivalent_ratio = 0.0 
		self.theta_curve = interpolated_function()
		self.density = 0.0 

	def expand_data(self):
		data = {}
		data['water_equivalent_ratio'] = self.water_equivalent_ratio
		data['theta_curve'] = self.theta_curve.expand_data()
		data['density'] = self.density
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'theta_curve':
					self.theta_curve.from_json(v)
				else:
					setattr(self, k, v)

class quadratic_function(object):

	#Initialize
	def __init__(self):
		self.a = 0.0 
		self.c = 0.0 
		self.b = 0.0 

	def expand_data(self):
		data = {}
		data['a'] = self.a
		data['c'] = self.c
		data['b'] = self.b
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class radiation_machine_data(object):

	#Initialize
	def __init__(self):
		self.ds_machine = ""
		self.pbs_machine = ""

class radiation_mode(object):

	#Initialize
	def __init__(self):
		self.optional_devices = [] 
		self.name = "" 
		self.required_devices = [] 
		self.snout_names = [] 
		self.radiation_type = rt_radiation_type()
		self.mode_type = "" 

	def expand_data(self):
		data = {}
		optional_device = []
		for x in self.optional_devices:
			s = proton_device_type()
			s.from_json(x)
			optional_device.append(s.expand_data())
		data['optional_devices'] = optional_device
		data['name'] = self.name
		required_device = []
		for x in self.required_devices:
			s = proton_device_type()
			s.from_json(x)
			required_device.append(s.expand_data())
		data['required_devices'] = required_device
		data['radiation_type'] = self.radiation_type.expand_data()
		data['mode_type'] = self.mode_type
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'radiation_type':
					self.radiation_type.from_json(v)
				else:
					setattr(self, k, v)

class ramp_dose_objective(object):

	#Initialize
	def __init__(self):
		self.voxels = [] 
		self.dose_level = 0.0 

	def expand_data(self):
		data = {}
		voxel = []
		for x in self.voxels:
			s = weighted_grid_index()
			s.from_json(x)
			voxel.append(s.expand_data())
		data['voxels'] = voxel
		data['dose_level'] = self.dose_level
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class range_analysis_context(object):

	#Initialize
	def __init__(self):
		self.image_to_beam = [] 
		self.sad = [] 
		self.degraders = [] 
		self.patient_image = image_3d()
		self.beam_to_image = [] 

	def expand_data(self):
		data = {}
		data['image_to_beam'] = self.image_to_beam
		data['sad'] = self.sad
		degrader = []
		for x in self.degraders:
			s = degrader_geometry()
			s.from_json(x)
			degrader.append(s.expand_data())
		data['degraders'] = degrader
		data['patient_image'] = self.patient_image.expand_data()
		data['beam_to_image'] = self.beam_to_image
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_image':
					self.patient_image.from_json(v)
				else:
					setattr(self, k, v)

class range_compensator_info(object):

	#Initialize
	def __init__(self):
		self.extents = box_2d()
		self.material_ref = "" 
		self.thickness = min_max()

	def expand_data(self):
		data = {}
		data['extents'] = self.extents.expand_data()
		data['material_ref'] = self.material_ref
		data['thickness'] = self.thickness.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'extents':
					self.extents.from_json(v)
				elif k == 'thickness':
					self.thickness.from_json(v)
				else:
					setattr(self, k, v)

class range_shifter_list(object):

	#Initialize
	def __init__(self):
		self.extents = box_2d()
		self.thicknesses = [] 
		self.material_ref = "" 

	def expand_data(self):
		data = {}
		data['extents'] = self.extents.expand_data()
		data['thicknesses'] = self.thicknesses
		data['material_ref'] = self.material_ref
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'extents':
					self.extents.from_json(v)
				else:
					setattr(self, k, v)

class ray_2d(object):

	#Initialize
	def __init__(self):
		self.direction = [] 
		self.origin = [] 

	def expand_data(self):
		data = {}
		data['direction'] = self.direction
		data['origin'] = self.origin
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_3d(object):

	#Initialize
	def __init__(self):
		self.direction = [] 
		self.origin = [] 

	def expand_data(self):
		data = {}
		data['direction'] = self.direction
		data['origin'] = self.origin
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_box_intersection_2d(object):

	#Initialize
	def __init__(self):
		self.n_intersections = 0 
		self.exit_distance = 0.0 
		self.entrance_distance = 0.0 

	def expand_data(self):
		data = {}
		data['n_intersections'] = self.n_intersections
		data['exit_distance'] = self.exit_distance
		data['entrance_distance'] = self.entrance_distance
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_box_intersection_3d(object):

	#Initialize
	def __init__(self):
		self.n_intersections = 0 
		self.exit_distance = 0.0 
		self.entrance_distance = 0.0 

	def expand_data(self):
		data = {}
		data['n_intersections'] = self.n_intersections
		data['exit_distance'] = self.exit_distance
		data['entrance_distance'] = self.entrance_distance
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_points(object):

	#Initialize
	def __init__(self):
		self.offset = 0 
		self.n_points = 0 

	def expand_data(self):
		data = {}
		data['offset'] = self.offset
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rc_geometry(object):

	#Initialize
	def __init__(self):
		self.thickness = image_2d()

	def expand_data(self):
		data = {}
		data['thickness'] = self.thickness.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'thickness':
					self.thickness.from_json(v)
				else:
					setattr(self, k, v)

class rc_nurb_geometry(object):

	#Initialize
	def __init__(self):
		self.surface = nurb_surface()

	def expand_data(self):
		data = {}
		data['surface'] = self.surface.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'surface':
					self.surface.from_json(v)
				else:
					setattr(self, k, v)

class rc_opt_properties(object):

	#Initialize
	def __init__(self):
		self.shift_direction = 0 
		self.target_inner_border = 0.0 
		self.current_dose = nurb_surface()
		self.smear_span = 0 
		self.patch_distal_dose = 0.0 
		self.target_distal_dose = 0.0 
		self.dose_grid = nurb_surface()
		self.smear_weight = 0.0 
		self.iteration_count = 0 

	def expand_data(self):
		data = {}
		data['shift_direction'] = self.shift_direction
		data['target_inner_border'] = self.target_inner_border
		data['current_dose'] = self.current_dose.expand_data()
		data['smear_span'] = self.smear_span
		data['patch_distal_dose'] = self.patch_distal_dose
		data['target_distal_dose'] = self.target_distal_dose
		data['dose_grid'] = self.dose_grid.expand_data()
		data['smear_weight'] = self.smear_weight
		data['iteration_count'] = self.iteration_count
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ref_dicom_item(object):

	#Initialize
	def __init__(self):
		self.elements = [] 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.type = dicom_modality()
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		data['type'] = self.type.expand_data()
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type':
					self.type.from_json(v)
				else:
					setattr(self, k, v)

class regular_grid_1d(object):

	#Initialize
	def __init__(self):
		self.spacing = [] 
		self.p0 = [] 
		self.n_points = [] 

	def expand_data(self):
		data = {}
		data['spacing'] = self.spacing
		data['p0'] = self.p0
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regular_grid_2d(object):

	#Initialize
	def __init__(self):
		self.spacing = [] 
		self.p0 = [] 
		self.n_points = [] 

	def expand_data(self):
		data = {}
		data['spacing'] = self.spacing
		data['p0'] = self.p0
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regular_grid_3d(object):

	#Initialize
	def __init__(self):
		self.spacing = [] 
		self.p0 = [] 
		self.n_points = [] 

	def expand_data(self):
		data = {}
		data['spacing'] = self.spacing
		data['p0'] = self.p0
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regular_grid_4d(object):

	#Initialize
	def __init__(self):
		self.spacing = [] 
		self.p0 = [] 
		self.n_points = [] 

	def expand_data(self):
		data = {}
		data['spacing'] = self.spacing
		data['p0'] = self.p0
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regularly_sampled_function(object):

	#Initialize
	def __init__(self):
		self.outside_domain_policy = outside_domain_policy()
		self.samples = [] 
		self.x_spacing = 0.0 
		self.x0 = 0.0 

	def expand_data(self):
		data = {}
		data['outside_domain_policy'] = self.outside_domain_policy.expand_data()
		data['samples'] = self.samples
		data['x_spacing'] = self.x_spacing
		data['x0'] = self.x0
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'outside_domain_policy':
					self.outside_domain_policy.from_json(v)
				else:
					setattr(self, k, v)

class rgb8(object):

	#Initialize
	def __init__(self):
		self.g = 0 
		self.b = 0 
		self.r = 0 

	def expand_data(self):
		data = {}
		data['g'] = self.g
		data['b'] = self.b
		data['r'] = self.r
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rgba8(object):

	#Initialize
	def __init__(self):
		self.g = 0 
		self.a = 0 
		self.b = 0 
		self.r = 0 

	def expand_data(self):
		data = {}
		data['g'] = self.g
		data['a'] = self.a
		data['b'] = self.b
		data['r'] = self.r
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_control_point(object):

	#Initialize
	def __init__(self):
		self.patient_support_direction = "" 
		self.sequences = [] 
		self.table_top_pitch_angle = 0.0 
		self.patient_support_angle = 0.0 
		self.table_top_roll_angle = 0.0 
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.table_top_roll_direction = "" 
		self.beam_limiting_device_angle = 0.0 
		self.table_top_pitch_direction = "" 
		self.series_uid = "" 
		self.nominal_beam_energy_unit = "" 
		self.gantry_angle = 0.0 
		self.nominal_beam_energy = 0.0 
		self.gantry_pitch_angle = 0.0 
		self.meterset_weight = 0.0 
		self.meterset_rate = 0.0 
		self.surface_entry_point = [] 
		self.class_uid = "" 
		self.source_to_surface_distance = 0.0 
		self.layer = pbs_spot_layer()
		self.gantry_pitch_direction = "" 
		self.gantry_rotation_direction = "" 
		self.iso_center_position = [] 
		self.snout_position = 0.0 
		self.beam_limiting_direction = "" 
		self.number = 0 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['patient_support_direction'] = self.patient_support_direction
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['table_top_pitch_angle'] = self.table_top_pitch_angle
		data['patient_support_angle'] = self.patient_support_angle
		data['table_top_roll_angle'] = self.table_top_roll_angle
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['table_top_roll_direction'] = self.table_top_roll_direction
		data['beam_limiting_device_angle'] = self.beam_limiting_device_angle
		data['table_top_pitch_direction'] = self.table_top_pitch_direction
		data['series_uid'] = self.series_uid
		data['nominal_beam_energy_unit'] = self.nominal_beam_energy_unit
		data['gantry_angle'] = self.gantry_angle
		data['nominal_beam_energy'] = self.nominal_beam_energy
		data['gantry_pitch_angle'] = self.gantry_pitch_angle
		data['meterset_weight'] = self.meterset_weight
		data['meterset_rate'] = self.meterset_rate
		data['surface_entry_point'] = self.surface_entry_point
		data['class_uid'] = self.class_uid
		data['source_to_surface_distance'] = self.source_to_surface_distance
		data['layer'] = self.layer.expand_data()
		data['gantry_pitch_direction'] = self.gantry_pitch_direction
		data['gantry_rotation_direction'] = self.gantry_rotation_direction
		data['iso_center_position'] = self.iso_center_position
		data['snout_position'] = self.snout_position
		data['beam_limiting_direction'] = self.beam_limiting_direction
		data['number'] = self.number
		data['ref_instance_uid'] = self.ref_instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'layer':
					self.layer.from_json(v)
				else:
					setattr(self, k, v)

class rt_dose(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.frame_spacing = [] 
		self.sequences = [] 
		self.referenced_ids = [] 
		self.class_uid = "" 
		self.type = dose_type()
		self.ref_fraction_num = "" 
		self.instance_uid = "" 
		self.dose = rt_image_slice_3d()
		self.elements = [] 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.frame_of_ref_uid = "" 
		self.frame_increment_pointer = "" 
		self.ref_beam_num = "" 
		self.summation_type = dose_summation_type()
		self.number_frames = 0 
		self.meta_data = dicom_metadata()

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		data['frame_spacing'] = self.frame_spacing
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		referenced_id = []
		for x in self.referenced_ids:
			s = ref_dicom_item()
			s.from_json(x)
			referenced_id.append(s.expand_data())
		data['referenced_ids'] = referenced_id
		data['class_uid'] = self.class_uid
		data['type'] = self.type.expand_data()
		data['ref_fraction_num'] = self.ref_fraction_num
		data['instance_uid'] = self.instance_uid
		data['dose'] = self.dose.expand_data()
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		data['frame_increment_pointer'] = self.frame_increment_pointer
		data['ref_beam_num'] = self.ref_beam_num
		data['summation_type'] = self.summation_type.expand_data()
		data['number_frames'] = self.number_frames
		data['meta_data'] = self.meta_data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type':
					self.type.from_json(v)
				elif k == 'dose':
					self.dose.from_json(v)
				elif k == 'summation_type':
					self.summation_type.from_json(v)
				elif k == 'meta_data':
					self.meta_data.from_json(v)
				else:
					setattr(self, k, v)

class rt_dose_reference(object):

	#Initialize
	def __init__(self):
		self.uid = "" 
		self.description = "" 
		self.sequences = [] 
		self.structure_type = "" 
		self.class_uid = "" 
		self.target_min_dose = 0.0 
		self.number = 0 
		self.target_underdose_vol_fraction = 0.0 
		self.target_rx_dose = 0.0 
		self.point_coordinates = [] 
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.target_max_dose = 0.0 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.type = "" 
		self.ref_roi_number = 0 
		self.delivery_max_dose = 0.0 

	def expand_data(self):
		data = {}
		data['uid'] = self.uid
		data['description'] = self.description
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['structure_type'] = self.structure_type
		data['class_uid'] = self.class_uid
		data['target_min_dose'] = self.target_min_dose
		data['number'] = self.number
		data['target_underdose_vol_fraction'] = self.target_underdose_vol_fraction
		data['target_rx_dose'] = self.target_rx_dose
		data['point_coordinates'] = self.point_coordinates
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['target_max_dose'] = self.target_max_dose
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		data['type'] = self.type
		data['ref_roi_number'] = self.ref_roi_number
		data['delivery_max_dose'] = self.delivery_max_dose
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_fraction(object):

	#Initialize
	def __init__(self):
		self.elements = [] 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.sequences = [] 
		self.class_uid = "" 
		self.number_beams = 0 
		self.number = 0 
		self.number_planned_fractions = 0 
		self.series_uid = "" 
		self.ref_beam = [] 
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['number_beams'] = self.number_beams
		data['number'] = self.number
		data['number_planned_fractions'] = self.number_planned_fractions
		data['series_uid'] = self.series_uid
		ref_bea = []
		for x in self.ref_beam:
			s = rt_ref_beam()
			s.from_json(x)
			ref_bea.append(s.expand_data())
		data['ref_beam'] = ref_bea
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_image_2d(object):

	#Initialize
	def __init__(self):
		self.rows = 0 
		self.rescale_slope = 0.0 
		self.bits_stored = 0 
		self.rescale_intercept = 0.0 
		self.high_bit = 0 
		self.cols = 0 
		self.img = image_2d()
		self.bits_allocated = 0 

	def expand_data(self):
		data = {}
		data['rows'] = self.rows
		data['rescale_slope'] = self.rescale_slope
		data['bits_stored'] = self.bits_stored
		data['rescale_intercept'] = self.rescale_intercept
		data['high_bit'] = self.high_bit
		data['cols'] = self.cols
		data['img'] = self.img.expand_data()
		data['bits_allocated'] = self.bits_allocated
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'img':
					self.img.from_json(v)
				else:
					setattr(self, k, v)

class rt_image_3d(object):

	#Initialize
	def __init__(self):
		self.rows = 0 
		self.rescale_slope = 0.0 
		self.bits_stored = 0 
		self.rescale_intercept = 0.0 
		self.high_bit = 0 
		self.cols = 0 
		self.img = image_3d()
		self.bits_allocated = 0 

	def expand_data(self):
		data = {}
		data['rows'] = self.rows
		data['rescale_slope'] = self.rescale_slope
		data['bits_stored'] = self.bits_stored
		data['rescale_intercept'] = self.rescale_intercept
		data['high_bit'] = self.high_bit
		data['cols'] = self.cols
		data['img'] = self.img.expand_data()
		data['bits_allocated'] = self.bits_allocated
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'img':
					self.img.from_json(v)
				else:
					setattr(self, k, v)

class rt_image_conversion_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# dv
		# wsd
		# di
		# df

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_image_slice_2d(object):

	#Initialize
	def __init__(self):
		self.image_position = [] 
		self.pixel_spacing = [] 
		self.content = rt_image_2d()
		self.samples_per_pixel = 0 
		self.axis = 0 
		self.thickness = 0.0 
		self.image_orientation = [] 
		self.position = 0.0 
		self.photometric_interpretation = "" 
		self.instance_number = 0 
		self.pixel_rep = 0 

	def expand_data(self):
		data = {}
		data['image_position'] = self.image_position
		data['pixel_spacing'] = self.pixel_spacing
		data['content'] = self.content.expand_data()
		data['samples_per_pixel'] = self.samples_per_pixel
		data['axis'] = self.axis
		data['thickness'] = self.thickness
		data['image_orientation'] = self.image_orientation
		data['position'] = self.position
		data['photometric_interpretation'] = self.photometric_interpretation
		data['instance_number'] = self.instance_number
		data['pixel_rep'] = self.pixel_rep
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'content':
					self.content.from_json(v)
				else:
					setattr(self, k, v)

class rt_image_slice_3d(object):

	#Initialize
	def __init__(self):
		self.image_position = [] 
		self.pixel_spacing = [] 
		self.content = rt_image_3d()
		self.samples_per_pixel = 0 
		self.axis = 0 
		self.thickness = 0.0 
		self.image_orientation = [] 
		self.position = 0.0 
		self.photometric_interpretation = "" 
		self.instance_number = 0 
		self.pixel_rep = 0 

	def expand_data(self):
		data = {}
		data['image_position'] = self.image_position
		data['pixel_spacing'] = self.pixel_spacing
		data['content'] = self.content.expand_data()
		data['samples_per_pixel'] = self.samples_per_pixel
		data['axis'] = self.axis
		data['thickness'] = self.thickness
		data['image_orientation'] = self.image_orientation
		data['position'] = self.position
		data['photometric_interpretation'] = self.photometric_interpretation
		data['instance_number'] = self.instance_number
		data['pixel_rep'] = self.pixel_rep
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'content':
					self.content.from_json(v)
				else:
					setattr(self, k, v)

class rt_image_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# simulator
		# blank
		# portal
		# drr
		# fluence
		# radiograph

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_ion_beam(object):

	#Initialize
	def __init__(self):
		self.referenced_patient_setup = 0 
		self.sequences = [] 
		self.primary_dosimeter_unit = "" 
		self.radiation_type = rt_radiation_type()
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.control_points = [] 
		self.block = rt_ion_block()
		self.final_meterset_weight = 0.0 
		self.name = "" 
		self.beam_scan_mode = rt_ion_beam_scan_mode()
		self.description = "" 
		self.beam_type = rt_ion_beam_type()
		self.virtual_sad = [] 
		self.class_uid = "" 
		self.degraders = [] 
		self.beam_number = 0 
		self.series_uid = "" 
		self.treatment_machine = "" 
		self.referenced_tolerance_table = 0 
		self.snouts = [] 
		self.ref_instance_uid = "" 
		self.treatment_delivery_type = "" 
		self.shifters = [] 

	def expand_data(self):
		data = {}
		data['referenced_patient_setup'] = self.referenced_patient_setup
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['primary_dosimeter_unit'] = self.primary_dosimeter_unit
		data['radiation_type'] = self.radiation_type.expand_data()
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		control_point = []
		for x in self.control_points:
			s = rt_control_point()
			s.from_json(x)
			control_point.append(s.expand_data())
		data['control_points'] = control_point
		data['block'] = self.block.expand_data()
		data['final_meterset_weight'] = self.final_meterset_weight
		data['name'] = self.name
		data['beam_scan_mode'] = self.beam_scan_mode.expand_data()
		data['description'] = self.description
		data['beam_type'] = self.beam_type.expand_data()
		data['virtual_sad'] = self.virtual_sad
		data['class_uid'] = self.class_uid
		degrader = []
		for x in self.degraders:
			s = rt_ion_rangecompensator()
			s.from_json(x)
			degrader.append(s.expand_data())
		data['degraders'] = degrader
		data['beam_number'] = self.beam_number
		data['series_uid'] = self.series_uid
		data['treatment_machine'] = self.treatment_machine
		data['referenced_tolerance_table'] = self.referenced_tolerance_table
		snout = []
		for x in self.snouts:
			s = rt_snout()
			s.from_json(x)
			snout.append(s.expand_data())
		data['snouts'] = snout
		data['ref_instance_uid'] = self.ref_instance_uid
		data['treatment_delivery_type'] = self.treatment_delivery_type
		shifter = []
		for x in self.shifters:
			s = rt_ion_range_shifter()
			s.from_json(x)
			shifter.append(s.expand_data())
		data['shifters'] = shifter
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'radiation_type':
					self.radiation_type.from_json(v)
				elif k == 'block':
					self.block.from_json(v)
				elif k == 'beam_scan_mode':
					self.beam_scan_mode.from_json(v)
				elif k == 'beam_type':
					self.beam_type.from_json(v)
				else:
					setattr(self, k, v)

class rt_ion_beam_scan_mode(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# none
		# uniform
		# modulated

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_ion_beam_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# static
		# dynamic

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_ion_block(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.description = "" 
		self.downstream_edge = 0.0 
		self.sequences = [] 
		self.class_uid = "" 
		self.number = 0 
		self.thickness = 0.0 
		self.instance_uid = "" 
		self.material = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.block_type = rt_ion_block_type()
		self.name = "" 
		self.position = rt_mounting_position()
		self.divergent = False 
		self.data = polyset()

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		data['description'] = self.description
		data['downstream_edge'] = self.downstream_edge
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['number'] = self.number
		data['thickness'] = self.thickness
		data['instance_uid'] = self.instance_uid
		data['material'] = self.material
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['block_type'] = self.block_type.expand_data()
		data['name'] = self.name
		data['position'] = self.position.expand_data()
		data['divergent'] = self.divergent
		data['data'] = self.data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'block_type':
					self.block_type.from_json(v)
				elif k == 'position':
					self.position.from_json(v)
				elif k == 'data':
					self.data.from_json(v)
				else:
					setattr(self, k, v)

class rt_ion_block_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# aperture
		# shielding

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_ion_range_shifter(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.id = "" 
		self.ref_instance_uid = "" 
		self.number = 0 
		self.class_uid = "" 
		self.type = rt_range_shifter_type()
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['id'] = self.id
		data['ref_instance_uid'] = self.ref_instance_uid
		data['number'] = self.number
		data['class_uid'] = self.class_uid
		data['type'] = self.type.expand_data()
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type':
					self.type.from_json(v)
				else:
					setattr(self, k, v)

class rt_ion_rangecompensator(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.downstream_edge = 0.0 
		self.sequences = [] 
		self.class_uid = "" 
		self.pixelSpacing = [] 
		self.number = 0 
		self.relative_stopping_power = 0.0 
		self.ref_class_uid = "" 
		self.instance_uid = "" 
		self.material = "" 
		self.elements = [] 
		self.mounting_position = rt_mounting_position()
		self.ref_instance_uid = "" 
		self.divergent = False 
		self.name = "" 
		self.position = [] 
		self.column_offset = 0.0 
		self.data = image_2d()

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		data['downstream_edge'] = self.downstream_edge
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['pixelSpacing'] = self.pixelSpacing
		data['number'] = self.number
		data['relative_stopping_power'] = self.relative_stopping_power
		data['ref_class_uid'] = self.ref_class_uid
		data['instance_uid'] = self.instance_uid
		data['material'] = self.material
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['mounting_position'] = self.mounting_position.expand_data()
		data['ref_instance_uid'] = self.ref_instance_uid
		data['divergent'] = self.divergent
		data['name'] = self.name
		data['position'] = self.position
		data['column_offset'] = self.column_offset
		data['data'] = self.data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'mounting_position':
					self.mounting_position.from_json(v)
				elif k == 'data':
					self.data.from_json(v)
				else:
					setattr(self, k, v)

class rt_mounting_position(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# patient_side
		# double_sided
		# source_side

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_patient_setup(object):

	#Initialize
	def __init__(self):
		self.table_top_vert_setup_dis = 0.0 
		self.sequences = [] 
		self.class_uid = "" 
		self.series_uid = "" 
		self.setup_description = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.setup_number = 0 
		self.ref_instance_uid = "" 
		self.table_top_lateral_setup_dis = 0.0 
		self.instance_uid = "" 
		self.position = patient_position_type()
		self.table_top_long_setup_dis = 0.0 

	def expand_data(self):
		data = {}
		data['table_top_vert_setup_dis'] = self.table_top_vert_setup_dis
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['series_uid'] = self.series_uid
		data['setup_description'] = self.setup_description
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['setup_number'] = self.setup_number
		data['ref_instance_uid'] = self.ref_instance_uid
		data['table_top_lateral_setup_dis'] = self.table_top_lateral_setup_dis
		data['instance_uid'] = self.instance_uid
		data['position'] = self.position.expand_data()
		data['table_top_long_setup_dis'] = self.table_top_long_setup_dis
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'position':
					self.position.from_json(v)
				else:
					setattr(self, k, v)

class rt_plan(object):

	#Initialize
	def __init__(self):
		self.tolerance_table = [] 
		self.plan_date = "" 
		self.sequences = [] 
		self.referenced_ids = [] 
		self.dose = [] 
		self.beams = [] 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.patient_setups = [] 
		self.geometry = "" 
		self.name = "" 
		self.meta_data = dicom_metadata()
		self.uid = "" 
		self.description = "" 
		self.patient_data = patient()
		self.label = "" 
		self.class_uid = "" 
		self.series_uid = "" 
		self.instance_uid = "" 
		self.fractions = [] 
		self.ref_instance_uid = "" 
		self.frame_of_ref_uid = "" 

	def expand_data(self):
		data = {}
		tolerance_tabl = []
		for x in self.tolerance_table:
			s = rt_tolerance_table()
			s.from_json(x)
			tolerance_tabl.append(s.expand_data())
		data['tolerance_table'] = tolerance_tabl
		data['plan_date'] = self.plan_date
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		referenced_id = []
		for x in self.referenced_ids:
			s = ref_dicom_item()
			s.from_json(x)
			referenced_id.append(s.expand_data())
		data['referenced_ids'] = referenced_id
		dos = []
		for x in self.dose:
			s = rt_dose_reference()
			s.from_json(x)
			dos.append(s.expand_data())
		data['dose'] = dos
		beam = []
		for x in self.beams:
			s = rt_ion_beam()
			s.from_json(x)
			beam.append(s.expand_data())
		data['beams'] = beam
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		patient_setup = []
		for x in self.patient_setups:
			s = rt_patient_setup()
			s.from_json(x)
			patient_setup.append(s.expand_data())
		data['patient_setups'] = patient_setup
		data['geometry'] = self.geometry
		data['name'] = self.name
		data['meta_data'] = self.meta_data.expand_data()
		data['uid'] = self.uid
		data['description'] = self.description
		data['patient_data'] = self.patient_data.expand_data()
		data['label'] = self.label
		data['class_uid'] = self.class_uid
		data['series_uid'] = self.series_uid
		data['instance_uid'] = self.instance_uid
		fraction = []
		for x in self.fractions:
			s = rt_fraction()
			s.from_json(x)
			fraction.append(s.expand_data())
		data['fractions'] = fraction
		data['ref_instance_uid'] = self.ref_instance_uid
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'meta_data':
					self.meta_data.from_json(v)
				elif k == 'patient_data':
					self.patient_data.from_json(v)
				else:
					setattr(self, k, v)

class rt_radiation_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# neutron
		# photon
		# proton
		# electron

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_range_shifter_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# analog
		# binary

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_ref_beam(object):

	#Initialize
	def __init__(self):
		self.elements = [] 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.sequences = [] 
		self.class_uid = "" 
		self.beam_meterset = 0.0 
		self.beam_dose = 0.0 
		self.series_uid = "" 
		self.dose_specification_point = [] 
		self.beam_number = 0 
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['beam_meterset'] = self.beam_meterset
		data['beam_dose'] = self.beam_dose
		data['series_uid'] = self.series_uid
		data['dose_specification_point'] = self.dose_specification_point
		data['beam_number'] = self.beam_number
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_snout(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.id = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.accessoryCode = "" 
		self.instance_uid = "" 

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		data['id'] = self.id
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		data['class_uid'] = self.class_uid
		data['accessoryCode'] = self.accessoryCode
		data['instance_uid'] = self.instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_structure(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.description = "" 
		self.color = rgb8()
		self.sequences = [] 
		self.class_uid = "" 
		self.number = 0 
		self.point = [] 
		self.volume = dicom_structure_geometry()
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.name = "" 
		self.type = rt_structure_type()

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		data['description'] = self.description
		data['color'] = self.color.expand_data()
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['number'] = self.number
		data['point'] = self.point
		data['volume'] = self.volume.expand_data()
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['name'] = self.name
		data['type'] = self.type.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				elif k == 'volume':
					self.volume.from_json(v)
				elif k == 'type':
					self.type.from_json(v)
				else:
					setattr(self, k, v)

class rt_structure_set(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.description = "" 
		self.structures = [] 
		self.sequences = [] 
		self.contour_image_sequence = [] 
		self.class_uid = "" 
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.frame_of_ref_uid = "" 
		self.name = "" 
		self.patient_position = patient_position_type()
		self.meta_data = dicom_metadata()

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		data['description'] = self.description
		structure = []
		for x in self.structures:
			s = rt_structure()
			s.from_json(x)
			structure.append(s.expand_data())
		data['structures'] = structure
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		contour_image_sequenc = []
		for x in self.contour_image_sequence:
			s = dicom_item()
			s.from_json(x)
			contour_image_sequenc.append(s.expand_data())
		data['contour_image_sequence'] = contour_image_sequenc
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		data['name'] = self.name
		data['patient_position'] = self.patient_position.expand_data()
		data['meta_data'] = self.meta_data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_position':
					self.patient_position.from_json(v)
				elif k == 'meta_data':
					self.meta_data.from_json(v)
				else:
					setattr(self, k, v)

class rt_structure_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# point
		# closed_planar

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_study(object):

	#Initialize
	def __init__(self):
		self.accession_number = "" 
		self.description = "" 
		self.plan = rt_plan()
		self.class_uid = "" 
		self.series_uid = "" 
		self.structure_set = rt_structure_set()
		self.ct_image = ct_image_data()
		self.id = "" 
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.doses = [] 
		self.physician_name = "" 
		self.ref_instance_uid = "" 
		self.name = "" 
		self.study_date = "" 
		self.sequences = [] 

	def expand_data(self):
		data = {}
		data['accession_number'] = self.accession_number
		data['description'] = self.description
		data['plan'] = self.plan.expand_data()
		data['class_uid'] = self.class_uid
		data['series_uid'] = self.series_uid
		data['structure_set'] = self.structure_set.expand_data()
		data['ct_image'] = self.ct_image.expand_data()
		data['id'] = self.id
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		dose = []
		for x in self.doses:
			s = rt_dose()
			s.from_json(x)
			dose.append(s.expand_data())
		data['doses'] = dose
		data['physician_name'] = self.physician_name
		data['ref_instance_uid'] = self.ref_instance_uid
		data['name'] = self.name
		data['study_date'] = self.study_date
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'plan':
					self.plan.from_json(v)
				elif k == 'structure_set':
					self.structure_set.from_json(v)
				elif k == 'ct_image':
					self.ct_image.from_json(v)
				else:
					setattr(self, k, v)

class rt_tolerance_table(object):

	#Initialize
	def __init__(self):
		self.series_uid = "" 
		self.table_top_long_position = 0.0 
		self.sequences = [] 
		self.class_uid = "" 
		self.number = 0 
		self.patient_support_angle = 0.0 
		self.table_top_lat_position = 0.0 
		self.instance_uid = "" 
		self.limiting_device_type = [] 
		self.elements = [] 
		self.ref_class_uid = "" 
		self.table_top_vert_position = 0.0 
		self.limiting_device_position = [] 
		self.ref_instance_uid = "" 
		self.label = "" 
		self.beam_limiting_angle = 0.0 
		self.gantry_angle = 0.0 

	def expand_data(self):
		data = {}
		data['series_uid'] = self.series_uid
		data['table_top_long_position'] = self.table_top_long_position
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['class_uid'] = self.class_uid
		data['number'] = self.number
		data['patient_support_angle'] = self.patient_support_angle
		data['table_top_lat_position'] = self.table_top_lat_position
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_class_uid'] = self.ref_class_uid
		data['table_top_vert_position'] = self.table_top_vert_position
		data['limiting_device_position'] = self.limiting_device_position
		data['ref_instance_uid'] = self.ref_instance_uid
		data['label'] = self.label
		data['beam_limiting_angle'] = self.beam_limiting_angle
		data['gantry_angle'] = self.gantry_angle
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class set_operation(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# difference
		# xor
		# intersection
		# union

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class shifter_geometry(object):

	#Initialize
	def __init__(self):
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class simple_2d_image_view_state(object):

	#Initialize
	def __init__(self):
		self.camera = camera()
		self.measurement = simple_2d_view_measurement_state()

	def expand_data(self):
		data = {}
		data['camera'] = self.camera.expand_data()
		data['measurement'] = self.measurement.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'camera':
					self.camera.from_json(v)
				elif k == 'measurement':
					self.measurement.from_json(v)
				else:
					setattr(self, k, v)

class simple_2d_view_measurement_state(object):

	#Initialize
	def __init__(self):
		self.profiles = [] 
		self.point_samples = [] 

	def expand_data(self):
		data = {}
		profile = []
		for x in self.profiles:
			s = line_profile()
			s.from_json(x)
			profile.append(s.expand_data())
		data['profiles'] = profile
		point_sample = []
		for x in self.point_samples:
			s = point_sample_2d()
			s.from_json(x)
			point_sample.append(s.expand_data())
		data['point_samples'] = point_sample
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class simple_dose_constraint(object):

	#Initialize
	def __init__(self):
		self.voxels = [] 
		self.dose_level = 0.0 

	def expand_data(self):
		data = {}
		voxel = []
		for x in self.voxels:
			s = weighted_grid_index()
			s.from_json(x)
			voxel.append(s.expand_data())
		data['voxels'] = voxel
		data['dose_level'] = self.dose_level
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class slab_info(object):

	#Initialize
	def __init__(self):
		self.count = 0 
		self.range = 0.0 
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['count'] = self.count
		data['range'] = self.range
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class slab_info_list(object):

	#Initialize
	def __init__(self):
		self.info = [] 
		self.extents = box_2d()

	def expand_data(self):
		data = {}
		inf = []
		for x in self.info:
			s = slab_info()
			s.from_json(x)
			inf.append(s.expand_data())
		data['info'] = inf
		data['extents'] = self.extents.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'extents':
					self.extents.from_json(v)
				else:
					setattr(self, k, v)

class slice_description(object):

	#Initialize
	def __init__(self):
		self.position = 0.0 
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class sliced_3d_image_view_state(object):

	#Initialize
	def __init__(self):
		self.view_axis = 0 

	def expand_data(self):
		data = {}
		data['view_axis'] = self.view_axis
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class sliced_3d_view_state(object):

	#Initialize
	def __init__(self):
		self.slice_positions = [] 

	def expand_data(self):
		data = {}
		data['slice_positions'] = self.slice_positions
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class sliced_scene_geometry_2d(object):

	#Initialize
	def __init__(self):
		self.slicing = [] 

	def expand_data(self):
		data = {}
		data['slicing'] = self.slicing
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class sliced_scene_geometry_3d(object):

	#Initialize
	def __init__(self):
		self.slicing = [] 

	def expand_data(self):
		data = {}
		data['slicing'] = self.slicing
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class snout_shape(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# circular
		# rectangular

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class sobp_calculation_layer(object):

	#Initialize
	def __init__(self):
		self.weight = 0.0 
		self.depth_dose_curve = interpolated_function()
		self.sad = 0.0 
		self.initial_sigma = 0.0 
		self.initial_range = 0.0 
		self.pdd_shift = 0.0 

	def expand_data(self):
		data = {}
		data['weight'] = self.weight
		data['depth_dose_curve'] = self.depth_dose_curve.expand_data()
		data['sad'] = self.sad
		data['initial_sigma'] = self.initial_sigma
		data['initial_range'] = self.initial_range
		data['pdd_shift'] = self.pdd_shift
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'depth_dose_curve':
					self.depth_dose_curve.from_json(v)
				else:
					setattr(self, k, v)

class spatial_region_display_options(object):

	#Initialize
	def __init__(self):
		self.outline = spatial_region_outline_options()
		self.fill = spatial_region_fill_options()

	def expand_data(self):
		data = {}
		data['outline'] = self.outline.expand_data()
		data['fill'] = self.fill.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'outline':
					self.outline.from_json(v)
				elif k == 'fill':
					self.fill.from_json(v)
				else:
					setattr(self, k, v)

class spatial_region_fill_options(object):

	#Initialize
	def __init__(self):
		self.opacity = 0.0 
		self.enabled = False 

	def expand_data(self):
		data = {}
		data['opacity'] = self.opacity
		data['enabled'] = self.enabled
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class spatial_region_outline_options(object):

	#Initialize
	def __init__(self):
		self.width = 0.0 
		self.opacity = 0.0 
		self.type = line_stipple_type()

	def expand_data(self):
		data = {}
		data['width'] = self.width
		data['opacity'] = self.opacity
		data['type'] = self.type.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type':
					self.type.from_json(v)
				else:
					setattr(self, k, v)

class spot_placement(object):

	#Initialize
	def __init__(self):
		self.position = [] 
		self.energy = 0.0 

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['energy'] = self.energy
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class spot_rendering_options(object):

	#Initialize
	def __init__(self):
		self.energy_list = [] 
		self.selected_energy = "" 

	def expand_data(self):
		data = {}
		data['selected_energy'] = self.selected_energy
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class spot_spacing_strategy(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# constant
		# sigma

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class statistics(object):

	#Initialize
	def __init__(self):
		self.max = 0.0 
		self.n_samples = 0.0 
		self.min = 0.0 
		self.mean = 0.0 

	def expand_data(self):
		data = {}
		data['max'] = self.max
		data['n_samples'] = self.n_samples
		data['min'] = self.min
		data['mean'] = self.mean
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class structure_geometry(object):

	#Initialize
	def __init__(self):
		self.slices = [] 

	def expand_data(self):
		data = {}
		slice = []
		for x in self.slices:
			s = structure_geometry_slice()
			s.from_json(x)
			slice.append(s.expand_data())
		data['slices'] = slice
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class structure_geometry_slice(object):

	#Initialize
	def __init__(self):
		self.region = polyset()
		self.position = 0.0 
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['region'] = self.region.expand_data()
		data['position'] = self.position
		data['thickness'] = self.thickness
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'region':
					self.region.from_json(v)
				else:
					setattr(self, k, v)

class subtask_event(object):

	#Initialize
	def __init__(self):
		self.task_id = "" 
		self.type = subtask_event_type()

	def expand_data(self):
		data = {}
		data['task_id'] = self.task_id
		data['type'] = self.type.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type':
					self.type.from_json(v)
				else:
					setattr(self, k, v)

class subtask_event_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# task_canceled
		# value_produced
		# task_completed

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class treatment_machine(object):

	#Initialize
	def __init__(self):
		self.manufacturer = "" 
		self.description = "" 
		self.serial = "" 
		self.rooms = [] 
		self.settings = [] 
		self.name = "" 
		self.location = "" 

	def expand_data(self):
		data = {}
		data['manufacturer'] = self.manufacturer
		data['description'] = self.description
		data['serial'] = self.serial
		room = []
		for x in self.rooms:
			s = treatment_room()
			s.from_json(x)
			room.append(s.expand_data())
		data['rooms'] = room
		setting = []
		for x in self.settings:
			s = machine_setting()
			s.from_json(x)
			setting.append(s.expand_data())
		data['settings'] = setting
		data['name'] = self.name
		data['location'] = self.location
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class treatment_room(object):

	#Initialize
	def __init__(self):
		self.name = "" 
		self.machine_geometry_name = "" 
		self.snout_names = [] 

	def expand_data(self):
		data = {}
		data['name'] = self.name
		data['machine_geometry_name'] = self.machine_geometry_name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class triangle_mesh(object):

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.faces = blob.toStr()
		blob = blob_type()
		self.vertices = blob.toStr()

	def expand_data(self):
		data = {}
		data['faces'] = parse_bytes_3i(base64.b64decode(self.faces['blob']))
		data['vertices'] = parse_bytes_3d(base64.b64decode(self.vertices['blob']))
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class triangle_mesh_with_normals(object):

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.face_normal_indices = blob.toStr()
		blob = blob_type()
		self.vertex_normals = blob.toStr()
		blob = blob_type()
		self.vertex_positions = blob.toStr()
		blob = blob_type()
		self.face_position_indices = blob.toStr()

	def expand_data(self):
		data = {}
		data['face_normal_indices'] = parse_bytes_3i(base64.b64decode(self.face_normal_indices['blob']))
		data['vertex_normals'] = parse_bytes_3d(base64.b64decode(self.vertex_normals['blob']))
		data['vertex_positions'] = parse_bytes_3d(base64.b64decode(self.vertex_positions['blob']))
		data['face_position_indices'] = parse_bytes_3i(base64.b64decode(self.face_position_indices['blob']))
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class tristate_expansion(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# closed
		# open
		# halfway

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class unboxed_image_2d(object):

	#Initialize
	def __init__(self):
		self.axes = [] 
		self.pixels = [] 
		self.size = [] 
		self.origin = [] 

	def expand_data(self):
		data = {}
		data['axes'] = self.axes
		data['pixels'] = self.pixels
		data['size'] = self.size
		data['origin'] = self.origin
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class unboxed_image_3d(object):

	#Initialize
	def __init__(self):
		self.axes = [] 
		self.pixels = [] 
		self.size = [] 
		self.origin = [] 

	def expand_data(self):
		data = {}
		data['axes'] = self.axes
		data['pixels'] = self.pixels
		data['size'] = self.size
		data['origin'] = self.origin
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class variant_type_info(object):

	#Initialize
	def __init__(self):
		self.format = pixel_format()
		self.type = channel_type()

	def expand_data(self):
		data = {}
		data['format'] = self.format.expand_data()
		data['type'] = self.type.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'format':
					self.format.from_json(v)
				elif k == 'type':
					self.type.from_json(v)
				else:
					setattr(self, k, v)

class weighted_bixel(object):

	#Initialize
	def __init__(self):
		self.geometry = bixel_geometry()
		self.weight = 0.0 

	def expand_data(self):
		data = {}
		data['geometry'] = self.geometry.expand_data()
		data['weight'] = self.weight
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'geometry':
					self.geometry.from_json(v)
				else:
					setattr(self, k, v)

class weighted_grid_index(object):

	#Initialize
	def __init__(self):
		self.index = 0 
		self.weight = 0.0 

	def expand_data(self):
		data = {}
		data['index'] = self.index
		data['weight'] = self.weight
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class weighted_spot(object):

	#Initialize
	def __init__(self):
		self.position = [] 
		self.fluence = 0.0 
		self.energy = 0.0 

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['fluence'] = self.fluence
		data['energy'] = self.energy
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

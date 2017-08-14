# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:	Travis DeMint & Daniel Patenaude
# Date:		03/24/2016
# Desc:		Provides access to type usage for all types
# RT_Types Version:		1.0.0-beta10

from collections import OrderedDict
import base64
import struct as st

def parse_bytes_u(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('H',buf,offset)
		data.append(tmp[0])
		offset += 2
	return data

def parse_bytes_1u(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('H',buf,offset)
		data.append([tmp[0]])
		offset += 2
	return data

def parse_bytes_2u(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('HH',buf,offset)
		data.append([tmp[0],tmp[1]])
		offset += 4
	return data

def parse_bytes_3u(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('HHH',buf,offset)
		data.append([tmp[0],tmp[1],tmp[2]])
		offset += 6
	return data

def parse_bytes_f(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('f',buf,offset)
		data.append(tmp[0])
		offset += 4
	return data

def parse_bytes_1f(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('f',buf,offset)
		data.append([tmp[0]])
		offset += 4
	return data

def parse_bytes_2f(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('ff',buf,offset)
		data.append([tmp[0],tmp[1]])
		offset += 8
	return data

def parse_bytes_3f(buf, offset=0):
	data = []
	while offset < len(buf):
		tmp = st.unpack_from('fff',buf,offset)
		data.append([tmp[0],tmp[1],tmp[2]])
		offset += 12
	return data

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

def parse_byte_ul(buf, offset=0):
	tmp = st.unpack_from('Q',buf,offset)
	return tmp[0]

def parse_byte_u(buf, offset=0):
	tmp = st.unpack_from('I',buf,offset)
	return tmp[0]

def parse_byte_f(buf, offset=0):
	tmp = st.unpack_from('f',buf,offset)
	return tmp[0]

def parse_byte_d(buf, offset=0):
	tmp = st.unpack_from('d',buf,offset)
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

class abbreviated_task_info(object):

	#Initialize
	def __init__(self):
		self.id = "" 
		self.type = "" 
		self.group_index = 0 

	def expand_data(self):
		data = {}
		data['id'] = self.id
		data['type'] = self.type
		data['group_index'] = self.group_index
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class adaptive_grid(object):

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.volumes = blob.toStr()
		blob = blob_type()
		self.voxels = blob.toStr()
		self.extents = box_3d()

	def expand_data(self):
		data = {}
		data['volumes'] = parse_bytes_i(base64.b64decode(self.volumes['blob']))
		adaptivegridvoxel = adaptive_grid_voxel()
		data['voxels'] = parse_array(adaptivegridvoxel, base64.b64decode(self.voxels['blob']))
		data['extents'] = self.extents.expand_data()
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

	def parse_self(self, buf, offset):
		self.inside_count = parse_bytes_i(buf, offset)
		self.surface_count = parse_byte_i(buff, offset + 4)
		self.index = parse_byte_i(buff, offset + 8)
		self.volume_offset = parse_byte_i(buff, offset + 12)
		return self.expand_data()

	def get_offset(self):
		return 16

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
		self.downstream_edge = 0.0 
		self.shape = polyset()

	def expand_data(self):
		data = {}
		data['downstream_edge'] = self.downstream_edge
		data['shape'] = self.shape.expand_data()
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
		self.origin = [] 
		self.second_direction = 0.0 
		self.first_direction = 0.0 

	def expand_data(self):
		data = {}
		data['origin'] = self.origin
		data['second_direction'] = self.second_direction
		data['first_direction'] = self.first_direction
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class aperture_creation_params(object):

	#Initialize
	def __init__(self):
		self.downstream_edge = 0.0 
		self.half_planes = [] 
		self.target_margin = 0.0 
		self.corner_planes = [] 
		self.mill_radius = 0.0 
		self.overrides = [] 
		self.centerlines = [] 
		self.targets = [] 
		self.organs = [] 

	def expand_data(self):
		data = {}
		data['downstream_edge'] = self.downstream_edge
		half_plane = []
		for x in self.half_planes:
			s = aperture_half_plane()
			s.from_json(x)
			half_plane.append(s.expand_data())
		data['half_planes'] = half_plane
		data['target_margin'] = self.target_margin
		corner_plane = []
		for x in self.corner_planes:
			s = aperture_corner_plane()
			s.from_json(x)
			corner_plane.append(s.expand_data())
		data['corner_planes'] = corner_plane
		data['mill_radius'] = self.mill_radius
		override = []
		for x in self.overrides:
			s = aperture_manual_override()
			s.from_json(x)
			override.append(s.expand_data())
		data['overrides'] = override
		centerline = []
		for x in self.centerlines:
			s = aperture_centerline()
			s.from_json(x)
			centerline.append(s.expand_data())
		data['centerlines'] = centerline
		target = []
		for x in self.targets:
			s = triangle_mesh()
			s.from_json(x)
			target.append(s.expand_data())
		data['targets'] = target
		organ = []
		for x in self.organs:
			s = aperture_organ()
			s.from_json(x)
			organ.append(s.expand_data())
		data['organs'] = organ
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
		self.add_shape_to_opening = False 
		self.shape = polyset()

	def expand_data(self):
		data = {}
		data['add_shape_to_opening'] = self.add_shape_to_opening
		data['shape'] = self.shape.expand_data()
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
		self.occlude_by_target = False 
		self.margin = 0.0 
		self.structure = triangle_mesh()

	def expand_data(self):
		data = {}
		data['occlude_by_target'] = self.occlude_by_target
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
		# notifications
		# app_info
		# app_contents
		# settings

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
		self.left = machine_expression()
		self.right = machine_expression()
		self.op = arithmetic_operator()

	def expand_data(self):
		data = {}
		data['left'] = self.left.expand_data()
		data['right'] = self.right.expand_data()
		data['op'] = self.op.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'left':
					self.left.from_json(v)
				elif k == 'right':
					self.right.from_json(v)
				elif k == 'op':
					self.op.from_json(v)
				else:
					setattr(self, k, v)

class arithmetic_operator(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# multiplication
		# addition
		# division
		# subtraction

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
		# fit_scene_height
		# fit_scene_width
		# fill_canvas
		# stretch_to_fit
		# fit_scene

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
		self.beam_index = 0 
		self.bixel_grid = regular_grid_2d()
		self.geometry = beam_geometry()
		self.ssd = 0.0 
		self.range = 0.0 
		self.field = box_2d()

	def expand_data(self):
		data = {}
		data['beam_index'] = self.beam_index
		data['bixel_grid'] = self.bixel_grid.expand_data()
		data['geometry'] = self.geometry.expand_data()
		data['ssd'] = self.ssd
		data['range'] = self.range
		data['field'] = self.field.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'bixel_grid':
					self.bixel_grid.from_json(v)
				elif k == 'geometry':
					self.geometry.from_json(v)
				elif k == 'field':
					self.field.from_json(v)
				else:
					setattr(self, k, v)

class bin_collection_3d(object):

	#Initialize
	def __init__(self):
		self.bounds = box_3d()
		blob = blob_type()
		self.counts = blob.toStr()
		blob = blob_type()
		self.offsets = blob.toStr()
		blob = blob_type()
		self.bins = blob.toStr()
		self.grid_size = [] 

	def expand_data(self):
		data = {}
		data['bounds'] = self.bounds.expand_data()
		data['counts'] = parse_bytes_u(base64.b64decode(self.counts['blob']))
		data['offsets'] = parse_bytes_u(base64.b64decode(self.offsets['blob']))
		data['bins'] = parse_bytes_3d(base64.b64decode(self.bins['blob']))
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
		self.gamma50 = 0.0 
		self.d50 = 0.0 
		self.cutoff = 0.0 
		self.a = 0.0 
		self.alphabeta = 0.0 

	def expand_data(self):
		data = {}
		data['gamma50'] = self.gamma50
		data['d50'] = self.d50
		data['cutoff'] = self.cutoff
		data['a'] = self.a
		data['alphabeta'] = self.alphabeta
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class bixel_geometry(object):

	#Initialize
	def __init__(self):
		self.size = projected_isocentric_vector()
		self.axis = projected_isocentric_vector()

	def expand_data(self):
		data = {}
		data['size'] = self.size.expand_data()
		data['axis'] = self.axis.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'size':
					self.size.from_json(v)
				elif k == 'axis':
					self.axis.from_json(v)
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
		self.zoom = 0.0 
		self.position = [] 

	def expand_data(self):
		data = {}
		data['zoom'] = self.zoom
		data['position'] = self.position
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class camera3(object):

	#Initialize
	def __init__(self):
		self.direction = [] 
		self.up = [] 
		self.zoom = 0.0 
		self.position = [] 

	def expand_data(self):
		data = {}
		data['direction'] = self.direction
		data['up'] = self.up
		data['zoom'] = self.zoom
		data['position'] = self.position
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
		# int16
		# float
		# uint16
		# int32
		# uint8
		# uint32
		# uint64
		# int8
		# int64

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
		self.center = [] 
		self.radius = 0.0 

	def expand_data(self):
		data = {}
		data['center'] = self.center
		data['radius'] = self.radius
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class color_map_level(object):

	#Initialize
	def __init__(self):
		self.color = rgba8()
		self.level = 0.0 

	def expand_data(self):
		data = {}
		data['color'] = self.color.expand_data()
		data['level'] = self.level
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
		self.color = rgba8()
		self.position = [] 

	def expand_data(self):
		data = {}
		data['color'] = self.color.expand_data()
		data['position'] = self.position
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				else:
					setattr(self, k, v)

class ct_image(object):

	#Initialize
	def __init__(self):
		self.image_slices = []
		self.image_set = ct_image_set.toStr()

	def expand_data(self):
		data = {}
		slices = []
		for x in self.image_slices:
			s = ct_image_slice()
			s.from_json(x)
			slices.append(s.expand_data())
		data['image_slices'] = slices
		data['image_set'] = self.image_set
		return data

class ct_image_data(object):

	#Initialize
	def __init__(self):
		self.pixel_ref = ""
		self.img = image_2d.toStr()
		self.pixel = pixel_blob.toStr()

class ct_image_set(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.patient_position = patient_position_type()
		self.sequences = [] 
		self.series_uid = "" 
		self.elements = [] 
		self.instance_uid = "" 
		self.meta_data = dicom_metadata()
		self.ref_class_uid = "" 
		self.image = image_3d()
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['patient_position'] = self.patient_position.expand_data()
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['instance_uid'] = self.instance_uid
		data['meta_data'] = self.meta_data.expand_data()
		data['ref_class_uid'] = self.ref_class_uid
		data['image'] = self.image.expand_data()
		data['ref_instance_uid'] = self.ref_instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_position':
					self.patient_position.from_json(v)
				elif k == 'meta_data':
					self.meta_data.from_json(v)
				elif k == 'image':
					self.image.from_json(v)
				else:
					setattr(self, k, v)

class ct_image_slice(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.patient_position = patient_position_type()
		self.sequences = [] 
		self.series_uid = "" 
		self.instance_uid = "" 
		self.referenced_ids = [] 
		self.slice = ct_image_slice_content()
		self.meta_data = dicom_metadata()
		self.ref_class_uid = "" 
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['patient_position'] = self.patient_position.expand_data()
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['instance_uid'] = self.instance_uid
		referenced_id = []
		for x in self.referenced_ids:
			s = ref_dicom_item()
			s.from_json(x)
			referenced_id.append(s.expand_data())
		data['referenced_ids'] = referenced_id
		data['slice'] = self.slice.expand_data()
		data['meta_data'] = self.meta_data.expand_data()
		data['ref_class_uid'] = self.ref_class_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
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

class ct_image_slice_content(object):

	#Initialize
	def __init__(self):
		self.image_orientation = [] 
		self.thickness = 0.0 
		self.axis = 0 
		self.pixel_rep = 0 
		self.pixel_spacing = [] 
		self.content = ct_image_slice_data()
		self.photometric_interpretation = "" 
		self.instance_number = 0 
		self.image_position = [] 
		self.samples_per_pixel = 0 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['image_orientation'] = self.image_orientation
		data['thickness'] = self.thickness
		data['axis'] = self.axis
		data['pixel_rep'] = self.pixel_rep
		data['pixel_spacing'] = self.pixel_spacing
		data['content'] = self.content.expand_data()
		data['photometric_interpretation'] = self.photometric_interpretation
		data['instance_number'] = self.instance_number
		data['image_position'] = self.image_position
		data['samples_per_pixel'] = self.samples_per_pixel
		data['position'] = self.position
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'content':
					self.content.from_json(v)
				else:
					setattr(self, k, v)

class ct_image_slice_data(object):

	#Initialize
	def __init__(self):
		self.bits_stored = 0 
		self.rescale_intercept = 0.0 
		self.bits_allocated = 0 
		self.rescale_slope = 0.0 
		self.cols = 0 
		self.high_bit = 0 
		self.rows = 0 
		self.img = ct_image_data()

	def expand_data(self):
		data = {}
		data['bits_stored'] = self.bits_stored
		data['rescale_intercept'] = self.rescale_intercept
		data['bits_allocated'] = self.bits_allocated
		data['rescale_slope'] = self.rescale_slope
		data['cols'] = self.cols
		data['high_bit'] = self.high_bit
		data['rows'] = self.rows
		data['img'] = self.img.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'img':
					self.img.from_json(v)
				else:
					setattr(self, k, v)

class data_reporting_parameters(object):

	#Initialize
	def __init__(self):
		self.units = "" 
		self.label = "" 
		self.digits = 0 

	def expand_data(self):
		data = {}
		data['units'] = self.units
		data['label'] = self.label
		data['digits'] = self.digits
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class degrader_geometry(object):

	#Initialize
	def __init__(self):
		self.downstream_edge = 0.0 
		self.scale_factor = 0.0 
		self.thickness_units = "" 
		self.shape = degrader_shape()

	def expand_data(self):
		data = {}
		data['downstream_edge'] = self.downstream_edge
		data['scale_factor'] = self.scale_factor
		data['thickness_units'] = self.thickness_units
		data['shape'] = self.shape.expand_data()
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
		self.shifter = shifter_geometry.toStr()
		self.block = block_geometry.toStr()
		self.rc_nurb = rc_nurb_geometry.toStr()
		self.rc = rc_geometry.toStr()

class department(object):

	#Initialize
	def __init__(self):
		self.name = "" 
		self.description = "" 
		self.machines = [] 

	def expand_data(self):
		data = {}
		data['name'] = self.name
		data['description'] = self.description
		machine = []
		for x in self.machines:
			s = treatment_machine()
			s.from_json(x)
			machine.append(s.expand_data())
		data['machines'] = machine
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
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.instance_uid = "" 
		self.meta_data = dicom_metadata()
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['instance_uid'] = self.instance_uid
		data['meta_data'] = self.meta_data.expand_data()
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
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
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_metadata(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.modality = dicom_modality()
		self.instance_uid = "" 
		self.creationDate = "" 
		self.patient_metadata = patient()
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['modality'] = self.modality.expand_data()
		data['instance_uid'] = self.instance_uid
		data['creationDate'] = self.creationDate
		data['patient_metadata'] = self.patient_metadata.expand_data()
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
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
		# ct
		# rtplan
		# rtdose

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
		self.plan = rt_plan.toStr()
		self.dose = rt_dose.toStr()
		self.structure_set = rt_structure_set.toStr()
		self.ct_image = ct_image.toStr()

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
		self.items = [] 
		self.e = 0 

	def expand_data(self):
		data = {}
		data['g'] = self.g
		item = []
		for x in self.items:
			s = dicom_item()
			s.from_json(x)
			item.append(s.expand_data())
		data['items'] = item
		data['e'] = self.e
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_structure_geometry(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.instance_uid = "" 
		self.slices = [] 
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['instance_uid'] = self.instance_uid
		slice = []
		for x in self.slices:
			s = dicom_structure_geometry_slice()
			s.from_json(x)
			slice.append(s.expand_data())
		data['slices'] = slice
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_structure_geometry_slice(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.thickness = 0.0 
		self.instance_uid = "" 
		self.region = polyset()
		self.ref_instance_uid = "" 
		self.elements = [] 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['thickness'] = self.thickness
		data['instance_uid'] = self.instance_uid
		data['region'] = self.region.expand_data()
		data['ref_instance_uid'] = self.ref_instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['position'] = self.position
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
		self.dose = parse_byte_f(buf, offset + 4)
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
		self.n_points = 0 
		blob = blob_type()
		self.entries = blob.toStr()

	def expand_data(self):
		data = {}
		data['n_beamlets'] = self.n_beamlets
		dijrow = dij_row()
		data['rows'] = parse_array(dijrow, base64.b64decode(self.rows['blob']))
		data['n_points'] = self.n_points
		dijentry = dij_entry()
		data['entries'] = parse_array(dijentry, base64.b64decode(self.entries['blob']))
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dij_row(object):

	#Initialize
	def __init__(self):
		self.offset = 0 
		self.n_entries = 0 

	def parse_self(self, buf, offset):
		self.offset = parse_bytes_ul(buf, offset)
		self.n_entries = parse_byte_u(buf, offset + 8)
		return self.expand_data()

	def get_offset(self):
		return 16

	def expand_data(self):
		data = {}
		data['offset'] = self.offset
		data['n_entries'] = self.n_entries
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
		# two_rows
		# squares
		# main_plus_row
		# main_plus_column
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
		self.controls_expanded = False 
		self.focused_view = "" 

	def expand_data(self):
		data = {}
		data['selected_composition'] = self.selected_composition
		data['controls_expanded'] = self.controls_expanded
		data['focused_view'] = self.focused_view
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class display_view_composition(object):

	#Initialize
	def __init__(self):
		self.id = "" 
		self.views = [] 
		self.label = "" 
		self.layout = display_layout_type()

	def expand_data(self):
		data = {}
		data['id'] = self.id
		view = []
		for x in self.views:
			s = display_view_instance()
			s.from_json(x)
			view.append(s.expand_data())
		data['views'] = view
		data['label'] = self.label
		data['layout'] = self.layout.expand_data()
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
		self.grid = regular_grid_2d()
		blob = blob_type()
		self.rays = blob.toStr()
		self.z_position = 0.0 
		blob = blob_type()
		self.data = blob.toStr()
		self.isUniform = False 
		self.cax_length = 0.0 
		self.source_dist = 0.0 

	def expand_data(self):
		data = {}
		data['grid'] = self.grid.expand_data()
		data['rays'] = parse_bytes_not_defined(base64.b64decode(self.rays['blob']))
		data['z_position'] = self.z_position
		data['data'] = parse_bytes_not_defined(base64.b64decode(self.data['blob']))
		data['isUniform'] = self.isUniform
		data['cax_length'] = self.cax_length
		data['source_dist'] = self.source_dist
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
		self.min_mean = simple_dose_constraint.toStr()
		self.min = simple_dose_constraint.toStr()
		self.max = simple_dose_constraint.toStr()
		self.max_mean = simple_dose_constraint.toStr()

class dose_objective(object):

	#Initialize
	def __init__(self):
		self.minimize_max = []
		self.minimize_underdose = ramp_dose_objective.toStr()
		self.maximize_mean = []
		self.maximize_min = []
		self.minimize_overdose = ramp_dose_objective.toStr()
		self.minimize_mean = []

class dose_summation_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# plan
		# beam
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
		# error
		# effective
		# physical

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
		self.max_range = 0.0 
		self.id = "" 
		self.track_length = 0 
		self.max_mod = 0.0 
		self.bcm = [] 
		self.sdm = [] 
		self.source_size_on_track = 0.0 
		self.min_range = 0.0 
		self.steps = [] 
		self.mod_correction = [] 
		self.pristine_peak = irregularly_sampled_function()
		self.penumbral_source_size = 0.0 
		self.wts1 = 0.0 
		self.name = "" 

	def expand_data(self):
		data = {}
		data['max_range'] = self.max_range
		data['id'] = self.id
		data['track_length'] = self.track_length
		data['max_mod'] = self.max_mod
		data['bcm'] = self.bcm
		data['sdm'] = self.sdm
		data['source_size_on_track'] = self.source_size_on_track
		data['min_range'] = self.min_range
		step = []
		for x in self.steps:
			s = double_scattering_step()
			s.from_json(x)
			step.append(s.expand_data())
		data['steps'] = step
		data['mod_correction'] = self.mod_correction
		data['pristine_peak'] = self.pristine_peak.expand_data()
		data['penumbral_source_size'] = self.penumbral_source_size
		data['wts1'] = self.wts1
		data['name'] = self.name
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
		self.dR = 0.0 
		self.weight = 0.0 
		self.theta = 0.0 

	def expand_data(self):
		data = {}
		data['dR'] = self.dR
		data['weight'] = self.weight
		data['theta'] = self.theta
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class drr_options(object):

	#Initialize
	def __init__(self):
		self.image_display_options = gray_image_display_options()
		self.min_z = 0.0 
		self.max_value = 0.0 
		self.max_z = 0.0 
		self.sizing = regular_grid_2d()
		self.show = False 
		self.min_value = 0.0 
		self.image_z = 0.0 

	def expand_data(self):
		data = {}
		data['image_display_options'] = self.image_display_options.expand_data()
		data['min_z'] = self.min_z
		data['max_value'] = self.max_value
		data['max_z'] = self.max_z
		data['sizing'] = self.sizing.expand_data()
		data['show'] = self.show
		data['min_value'] = self.min_value
		data['image_z'] = self.image_z
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
		self.name = "" 
		self.departments = [] 

	def expand_data(self):
		data = {}
		data['description'] = self.description
		data['name'] = self.name
		department = []
		for x in self.departments:
			s = department()
			s.from_json(x)
			department.append(s.expand_data())
		data['departments'] = department
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class filesystem_item(object):

	#Initialize
	def __init__(self):
		self.contents = filesystem_item_contents()
		self.name = "" 

	def expand_data(self):
		data = {}
		data['contents'] = self.contents.expand_data()
		data['name'] = self.name
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

	def parse_self(self, buf, offset):
		self.value = parse_byte_d(buf, offset)
		self.delta = parse_byte_d(buf, offset + 8)
		return self.expand_data()

	def get_offset(self):
		return 16

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
		self.weight = 0.0 
		self.point = [] 

	def expand_data(self):
		data = {}
		data['weight'] = self.weight
		data['point'] = self.point
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
		self.window = 0.0 
		self.level = 0.0 

	def expand_data(self):
		data = {}
		data['window'] = self.window
		data['level'] = self.level
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

class gui_task_group_state(object):

	#Initialize
	def __init__(self):
		self.root_id = "" 

	def expand_data(self):
		data = {}
		data['root_id'] = self.root_id
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class gui_task_state(object):

	#Initialize
	def __init__(self):
		self.completed_subtask_count = 0 
		self.open_subtask_count = 0 
		self.canceled_subtask_count = 0 
		self.active_subtask = "" 
		self.type = "" 

	def expand_data(self):
		data = {}
		data['completed_subtask_count'] = self.completed_subtask_count
		data['open_subtask_count'] = self.open_subtask_count
		data['canceled_subtask_count'] = self.canceled_subtask_count
		data['active_subtask'] = self.active_subtask
		data['type'] = self.type
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class image_1d(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.type_info = variant_type_info()
		blob = blob_type()
		self.pixels = blob.toStr()
		self.value_mapping = linear_function()
		self.origin = [] 
		self.axes = [] 
		self.units = "" 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
		data['value_mapping'] = self.value_mapping.expand_data()
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['units'] = self.units
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
		self.size = [] 
		self.type_info = variant_type_info()
		blob = blob_type()
		self.pixels = blob.toStr()
		self.value_mapping = linear_function()
		self.origin = [] 
		self.axes = [] 
		self.units = "" 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
		data['value_mapping'] = self.value_mapping.expand_data()
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['units'] = self.units
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
		self.size = [] 
		self.type_info = variant_type_info()
		blob = blob_type()
		self.pixels = blob.toStr()
		self.value_mapping = linear_function()
		self.origin = [] 
		self.axes = [] 
		self.units = "" 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
		data['value_mapping'] = self.value_mapping.expand_data()
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['units'] = self.units
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

class image_1f(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.type_info = variant_type_info()
		blob = blob_type()
		self.pixels = blob.toStr()
		self.value_mapping = linear_function()
		self.origin = [] 
		self.axes = [] 
		self.units = "" 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['pixels'] = parse_bytes_f(base64.b64decode(self.pixels['blob']))
		data['value_mapping'] = self.value_mapping.expand_data()
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['units'] = self.units
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

class image_2f(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.type_info = variant_type_info()
		blob = blob_type()
		self.pixels = blob.toStr()
		self.value_mapping = linear_function()
		self.origin = [] 
		self.axes = [] 
		self.units = "" 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['pixels'] = parse_bytes_f(base64.b64decode(self.pixels['blob']))
		data['value_mapping'] = self.value_mapping.expand_data()
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['units'] = self.units
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

class image_3f(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.type_info = variant_type_info()
		blob = blob_type()
		self.pixels = blob.toStr()
		self.value_mapping = linear_function()
		self.origin = [] 
		self.axes = [] 
		self.units = "" 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['type_info'] = self.type_info.expand_data()
		data['pixels'] = parse_bytes_f(base64.b64decode(self.pixels['blob']))
		data['value_mapping'] = self.value_mapping.expand_data()
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['units'] = self.units
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
		self.grid = regular_grid_1d()
		self.slicing = [] 
		self.out_of_plane_info = regular_grid_1d()

	def expand_data(self):
		data = {}
		data['grid'] = self.grid.expand_data()
		data['slicing'] = self.slicing
		data['out_of_plane_info'] = self.out_of_plane_info.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'grid':
					self.grid.from_json(v)
				else:
					setattr(self, k, v)

class image_geometry_2d(object):

	#Initialize
	def __init__(self):
		self.grid = regular_grid_2d()
		self.slicing = [] 
		self.out_of_plane_info = regular_grid_2d()

	def expand_data(self):
		data = {}
		data['grid'] = self.grid.expand_data()
		data['slicing'] = self.slicing
		data['out_of_plane_info'] = self.out_of_plane_info.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'grid':
					self.grid.from_json(v)
				else:
					setattr(self, k, v)

class image_geometry_3d(object):

	#Initialize
	def __init__(self):
		self.grid = regular_grid_3d()
		self.slicing = [] 
		self.out_of_plane_info = regular_grid_3d()

	def expand_data(self):
		data = {}
		data['grid'] = self.grid.expand_data()
		data['slicing'] = self.slicing
		data['out_of_plane_info'] = self.out_of_plane_info.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'grid':
					self.grid.from_json(v)
				else:
					setattr(self, k, v)

class image_geometry_4d(object):

	#Initialize
	def __init__(self):
		self.grid = regular_grid_4d()
		self.slicing = [] 
		self.out_of_plane_info = regular_grid_4d()

	def expand_data(self):
		data = {}
		data['grid'] = self.grid.expand_data()
		data['slicing'] = self.slicing
		data['out_of_plane_info'] = self.out_of_plane_info.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'grid':
					self.grid.from_json(v)
				else:
					setattr(self, k, v)

class image_slice_1d(object):

	#Initialize
	def __init__(self):
		self.content = image_1d()
		self.axis = 0 
		self.thickness = 0.0 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['content'] = self.content.expand_data()
		data['axis'] = self.axis
		data['thickness'] = self.thickness
		data['position'] = self.position
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
		self.content = image_2d()
		self.axis = 0 
		self.thickness = 0.0 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['content'] = self.content.expand_data()
		data['axis'] = self.axis
		data['thickness'] = self.thickness
		data['position'] = self.position
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
		self.content = image_3d()
		self.axis = 0 
		self.thickness = 0.0 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['content'] = self.content.expand_data()
		data['axis'] = self.axis
		data['thickness'] = self.thickness
		data['position'] = self.position
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
		self.x_spacing = 0.0 
		self.x0 = 0.0 
		blob = blob_type()
		self.samples = blob.toStr()
		self.outside_domain_policy = outside_domain_policy()

	def expand_data(self):
		data = {}
		data['x_spacing'] = self.x_spacing
		data['x0'] = self.x0
		functionsample = function_sample()
		data['samples'] = parse_array(functionsample, base64.b64decode(self.samples['blob']))
		data['outside_domain_policy'] = self.outside_domain_policy.expand_data()
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
		self.samples = [] 
		self.outside_domain_policy = outside_domain_policy()

	def expand_data(self):
		data = {}
		data['samples'] = self.samples
		data['outside_domain_policy'] = self.outside_domain_policy.expand_data()
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
		# detailed
		# compact

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
		self.color = rgb8()
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['color'] = self.color.expand_data()
		data['position'] = self.position
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
		# dotted
		# none
		# solid
		# dashed

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
		self.stipple = line_stipple()
		self.width = 0.0 

	def expand_data(self):
		data = {}
		data['stipple'] = self.stipple.expand_data()
		data['width'] = self.width
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
		self.intercept = 0.0 
		self.slope = 0.0 

	def expand_data(self):
		data = {}
		data['intercept'] = self.intercept
		data['slope'] = self.slope
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
		# editing
		# normal
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
		self.operation = arithmetic_operation.toStr()
		self.setting = ""

class machine_frame_of_reference(object):

	#Initialize
	def __init__(self):
		self.id = "" 
		self.transformation = machine_transformation()
		self.tags = [] 
		self.nested = [] 
		self.label = "" 

	def expand_data(self):
		data = {}
		data['id'] = self.id
		data['transformation'] = self.transformation.expand_data()
		tag = []
		for x in self.tags:
			s = machine_frame_tag()
			s.from_json(x)
			tag.append(s.expand_data())
		data['tags'] = tag
		neste = []
		for x in self.nested:
			s = machine_frame_of_reference()
			s.from_json(x)
			neste.append(s.expand_data())
		data['nested'] = neste
		data['label'] = self.label
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
		self.couch = ""
		self.imaging = ""
		self.beam = ""

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
		self.angle = machine_expression()
		self.axis = [] 

	def expand_data(self):
		data = {}
		data['angle'] = self.angle.expand_data()
		data['axis'] = self.axis
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
		self.id = "" 
		self.precision = 0 
		self.description = "" 
		self.label = "" 
		self.range = min_max()
		self.units = "" 

	def expand_data(self):
		data = {}
		data['id'] = self.id
		data['precision'] = self.precision
		data['description'] = self.description
		data['label'] = self.label
		data['range'] = self.range.expand_data()
		data['units'] = self.units
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
		self.shifters = min_max()
		self.extention = min_max()
		self.shape = snout_shape()
		self.rc_info = snout_shape()
		self.slabs = snout_shape()
		self.field_size = [] 
		self.name = "" 

	def expand_data(self):
		data = {}
		data['shifters'] = self.shifters.expand_data()
		data['extention'] = self.extention.expand_data()
		data['shape'] = self.shape.expand_data()
		data['rc_info'] = self.rc_info.expand_data()
		data['slabs'] = self.slabs.expand_data()
		data['field_size'] = self.field_size
		data['name'] = self.name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'extention':
					self.extention.from_json(v)
				elif k == 'shape':
					self.shape.from_json(v)
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
		self.p_matrix = [] 
		self.objectives = [] 
		self.plan_count = 0 

	def expand_data(self):
		data = {}
		data['p_matrix'] = self.p_matrix
		objective = []
		for x in self.objectives:
			s = mco_navigation_objective()
			s.from_json(x)
			objective.append(s.expand_data())
		data['objectives'] = objective
		data['plan_count'] = self.plan_count
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class min_max(object):

	#Initialize
	def __init__(self):
		self.min = 0.0 
		self.max = 0.0 

	def expand_data(self):
		data = {}
		data['min'] = self.min
		data['max'] = self.max
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class multiple_source_view(object):

	#Initialize
	def __init__(self):
		self.direction = [] 
		self.display_surface = box_2d()
		self.up = [] 
		self.center = [] 
		self.distance = [] 

	def expand_data(self):
		data = {}
		data['direction'] = self.direction
		data['display_surface'] = self.display_surface.expand_data()
		data['up'] = self.up
		data['center'] = self.center
		data['distance'] = self.distance
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
		self.label = "" 
		self.color = rgb8()
		self.position = [] 

	def expand_data(self):
		data = {}
		data['label'] = self.label
		data['color'] = self.color.expand_data()
		data['position'] = self.position
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
		self.knots = [] 
		self.box = box_2d()
		self.heights = [] 
		self.weights = [] 
		self.order = [] 
		self.point_counts = [] 

	def expand_data(self):
		data = {}
		data['knots'] = self.knots
		data['box'] = self.box.expand_data()
		data['heights'] = self.heights
		data['weights'] = self.weights
		data['order'] = self.order
		data['point_counts'] = self.point_counts
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
		self.thickness = 0.0 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['thickness'] = self.thickness
		data['position'] = self.position
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
		# always_zero
		# extend_with_copies

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
		self.comments = "" 
		self.sex = patient_sex()
		self.instance_uid = "" 
		self.id = "" 
		self.sequences = [] 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.other_ids = [] 
		self.series_uid = "" 
		self.name = person_name()
		self.ethnic_group = "" 
		self.other_names = [] 
		self.birth_date = "" 

	def expand_data(self):
		data = {}
		data['comments'] = self.comments
		data['sex'] = self.sex.expand_data()
		data['instance_uid'] = self.instance_uid
		data['id'] = self.id
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
		data['ref_class_uid'] = self.ref_class_uid
		data['series_uid'] = self.series_uid
		data['name'] = self.name.expand_data()
		data['ethnic_group'] = self.ethnic_group
		other_name = []
		for x in self.other_names:
			s = person_name()
			s.from_json(x)
			other_name.append(s.expand_data())
		data['other_names'] = other_name
		data['birth_date'] = self.birth_date
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'sex':
					self.sex.from_json(v)
				elif k == 'name':
					self.name.from_json(v)
				else:
					setattr(self, k, v)

class patient_position_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# hfs
		# hfdr
		# ffs
		# hfdl
		# hfp
		# ffp
		# ffdl
		# ffdr

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
		self.r90 = 0.0 
		self.r80 = 0.0 
		self.energy = 0.0 

	def expand_data(self):
		data = {}
		data['r90'] = self.r90
		data['r80'] = self.r80
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
		# distal_w80
		# variable_w80
		# constant

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
		self.source_rotation_function = linear_function()
		self.aperture_sad = [] 
		self.halo_sigma_sq_function = quadratic_function()
		self.deliverable_energies = [] 

	def expand_data(self):
		data = {}
		data['sad'] = self.sad
		modeled_energie = []
		for x in self.modeled_energies:
			s = pbs_modeled_energy()
			s.from_json(x)
			modeled_energie.append(s.expand_data())
		data['modeled_energies'] = modeled_energie
		data['source_rotation_function'] = self.source_rotation_function.expand_data()
		data['aperture_sad'] = self.aperture_sad
		data['halo_sigma_sq_function'] = self.halo_sigma_sq_function.expand_data()
		deliverable_energie = []
		for x in self.deliverable_energies:
			s = pbs_deliverable_energy()
			s.from_json(x)
			deliverable_energie.append(s.expand_data())
		data['deliverable_energies'] = deliverable_energie
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'source_rotation_function':
					self.source_rotation_function.from_json(v)
				elif k == 'halo_sigma_sq_function':
					self.halo_sigma_sq_function.from_json(v)
				else:
					setattr(self, k, v)

class pbs_modeled_energy(object):

	#Initialize
	def __init__(self):
		self.r90 = 0.0 
		self.sigma = pbs_optical_sigma()
		self.energy = 0.0 
		self.pristine_peak = irregularly_sampled_function()
		self.w80 = 0.0 
		self.r100 = 0.0 

	def expand_data(self):
		data = {}
		data['r90'] = self.r90
		data['sigma'] = self.sigma.expand_data()
		data['energy'] = self.energy
		data['pristine_peak'] = self.pristine_peak.expand_data()
		data['w80'] = self.w80
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
		self.r90 = 0.0 
		self.sigma = pbs_optical_sigma()
		self.energy = 0.0 
		self.flixels = [] 
		self.flixel_rotation = 0.0 
		self.pristine_peak = interpolated_function()

	def expand_data(self):
		data = {}
		data['r90'] = self.r90
		data['sigma'] = self.sigma.expand_data()
		data['energy'] = self.energy
		flixel = []
		for x in self.flixels:
			s = projected_isocentric_vector()
			s.from_json(x)
			flixel.append(s.expand_data())
		data['flixels'] = flixel
		data['flixel_rotation'] = self.flixel_rotation
		data['pristine_peak'] = self.pristine_peak.expand_data()
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
		self.spots = [] 
		self.spot_size = [] 
		self.num_paintings = 0 
		self.spot_tune_id = 0.0 
		self.num_spot_positions = 0 

	def expand_data(self):
		data = {}
		spot = []
		for x in self.spots:
			s = weighted_spot()
			s.from_json(x)
			spot.append(s.expand_data())
		data['spots'] = spot
		data['spot_size'] = self.spot_size
		data['num_paintings'] = self.num_paintings
		data['spot_tune_id'] = self.spot_tune_id
		data['num_spot_positions'] = self.num_spot_positions
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class person_name(object):

	#Initialize
	def __init__(self):
		self.suffix = "" 
		self.given_name = "" 
		self.family_name = "" 
		self.prefix = "" 
		self.middle_name = "" 

	def expand_data(self):
		data = {}
		data['suffix'] = self.suffix
		data['given_name'] = self.given_name
		data['family_name'] = self.family_name
		data['prefix'] = self.prefix
		data['middle_name'] = self.middle_name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class pixel_blob(object):

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.blob = blob.toStr()

	def expand_data(self):
		data = {}
		data['blob'] = parse_bytes_at(base64.b64decode(self.blob['blob']))
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
		# rgb
		# gray

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
		self.size = 0.0 
		self.line_type = line_stipple_type()
		self.line_thickness = 0.0 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['line_type'] = self.line_type.expand_data()
		data['line_thickness'] = self.line_thickness
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
		self.color = rgb8()
		self.position = [] 

	def expand_data(self):
		data = {}
		data['color'] = self.color.expand_data()
		data['position'] = self.position
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
		self.holes = [] 
		self.polygons = [] 

	def expand_data(self):
		data = {}
		hole = []
		for x in self.holes:
			s = polygon2()
			s.from_json(x)
			hole.append(s.expand_data())
		data['holes'] = hole
		polygon = []
		for x in self.polygons:
			s = polygon2()
			s.from_json(x)
			polygon.append(s.expand_data())
		data['polygons'] = polygon
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
		# shifter
		# compensator
		# aperture

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
		self.theta_curve = interpolated_function()
		self.water_equivalent_ratio = 0.0 
		self.density = 0.0 

	def expand_data(self):
		data = {}
		data['theta_curve'] = self.theta_curve.expand_data()
		data['water_equivalent_ratio'] = self.water_equivalent_ratio
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
		self.c = 0.0 
		self.b = 0.0 
		self.a = 0.0 

	def expand_data(self):
		data = {}
		data['c'] = self.c
		data['b'] = self.b
		data['a'] = self.a
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class radiation_machine_data(object):

	#Initialize
	def __init__(self):
		self.pbs_machine = ""
		self.ds_machine = ""

class radiation_mode(object):

	#Initialize
	def __init__(self):
		self.required_devices = [] 
		self.mode_type = "" 
		self.snout_names = [] 
		self.radiation_type = rt_radiation_type()
		self.name = "" 
		self.optional_devices = [] 

	def expand_data(self):
		data = {}
		required_device = []
		for x in self.required_devices:
			s = proton_device_type()
			s.from_json(x)
			required_device.append(s.expand_data())
		data['required_devices'] = required_device
		data['mode_type'] = self.mode_type
		data['radiation_type'] = self.radiation_type.expand_data()
		data['name'] = self.name
		optional_device = []
		for x in self.optional_devices:
			s = proton_device_type()
			s.from_json(x)
			optional_device.append(s.expand_data())
		data['optional_devices'] = optional_device
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
		self.patient_image = image_3d()
		self.beam_to_image = [] 
		self.sad = [] 
		self.degraders = [] 

	def expand_data(self):
		data = {}
		data['image_to_beam'] = self.image_to_beam
		data['patient_image'] = self.patient_image.expand_data()
		data['beam_to_image'] = self.beam_to_image
		data['sad'] = self.sad
		degrader = []
		for x in self.degraders:
			s = degrader_geometry()
			s.from_json(x)
			degrader.append(s.expand_data())
		data['degraders'] = degrader
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
		self.thickness = min_max()
		self.material_ref = "" 
		self.extents = box_2d()

	def expand_data(self):
		data = {}
		data['thickness'] = self.thickness.expand_data()
		data['material_ref'] = self.material_ref
		data['extents'] = self.extents.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'thickness':
					self.thickness.from_json(v)
				elif k == 'extents':
					self.extents.from_json(v)
				else:
					setattr(self, k, v)

class range_shifter_list(object):

	#Initialize
	def __init__(self):
		self.thicknesses = [] 
		self.material_ref = "" 
		self.extents = box_2d()

	def expand_data(self):
		data = {}
		data['thicknesses'] = self.thicknesses
		data['material_ref'] = self.material_ref
		data['extents'] = self.extents.expand_data()
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
		self.exit_distance = 0.0 
		self.n_intersections = 0 
		self.entrance_distance = 0.0 

	def expand_data(self):
		data = {}
		data['exit_distance'] = self.exit_distance
		data['n_intersections'] = self.n_intersections
		data['entrance_distance'] = self.entrance_distance
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_box_intersection_3d(object):

	#Initialize
	def __init__(self):
		self.exit_distance = 0.0 
		self.n_intersections = 0 
		self.entrance_distance = 0.0 

	def expand_data(self):
		data = {}
		data['exit_distance'] = self.exit_distance
		data['n_intersections'] = self.n_intersections
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
		self.patch_distal_dose = 0.0 
		self.iteration_count = 0 
		self.smear_weight = 0.0 
		self.target_distal_dose = 0.0 
		self.current_dose = nurb_surface()
		self.target_inner_border = 0.0 
		self.dose_grid = nurb_surface()
		self.smear_span = 0 
		self.shift_direction = 0 

	def expand_data(self):
		data = {}
		data['patch_distal_dose'] = self.patch_distal_dose
		data['iteration_count'] = self.iteration_count
		data['smear_weight'] = self.smear_weight
		data['target_distal_dose'] = self.target_distal_dose
		data['current_dose'] = self.current_dose.expand_data()
		data['target_inner_border'] = self.target_inner_border
		data['dose_grid'] = self.dose_grid.expand_data()
		data['smear_span'] = self.smear_span
		data['shift_direction'] = self.shift_direction
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ref_dicom_item(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.instance_uid = "" 
		self.type = dicom_modality()
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['instance_uid'] = self.instance_uid
		data['type'] = self.type.expand_data()
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
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
		self.x_spacing = 0.0 
		self.x0 = 0.0 
		self.samples = [] 
		self.outside_domain_policy = outside_domain_policy()

	def expand_data(self):
		data = {}
		data['x_spacing'] = self.x_spacing
		data['x0'] = self.x0
		data['samples'] = self.samples
		data['outside_domain_policy'] = self.outside_domain_policy.expand_data()
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
		self.r = 0 
		self.b = 0 

	def expand_data(self):
		data = {}
		data['g'] = self.g
		data['r'] = self.r
		data['b'] = self.b
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rgba8(object):

	#Initialize
	def __init__(self):
		self.g = 0 
		self.r = 0 
		self.b = 0 
		self.a = 0 

	def expand_data(self):
		data = {}
		data['g'] = self.g
		data['r'] = self.r
		data['b'] = self.b
		data['a'] = self.a
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_control_point(object):

	#Initialize
	def __init__(self):
		self.gantry_pitch_direction = "" 
		self.beam_limiting_device_angle = 0.0 
		self.table_top_roll_angle = 0.0 
		self.nominal_beam_energy_unit = "" 
		self.layer = pbs_spot_layer()
		self.ref_instance_uid = "" 
		self.ref_class_uid = "" 
		self.patient_support_angle = 0.0 
		self.number = 0 
		self.iso_center_position = [] 
		self.table_top_pitch_direction = "" 
		self.snout_position = 0.0 
		self.gantry_pitch_angle = 0.0 
		self.surface_entry_point = [] 
		self.sequences = [] 
		self.table_top_pitch_angle = 0.0 
		self.meterset_weight = 0.0 
		self.source_to_surface_distance = 0.0 
		self.instance_uid = "" 
		self.patient_support_direction = "" 
		self.beam_limiting_direction = "" 
		self.elements = [] 
		self.class_uid = "" 
		self.gantry_angle = 0.0 
		self.meterset_rate = 0.0 
		self.gantry_rotation_direction = "" 
		self.table_top_roll_direction = "" 
		self.series_uid = "" 
		self.nominal_beam_energy = 0.0 

	def expand_data(self):
		data = {}
		data['gantry_pitch_direction'] = self.gantry_pitch_direction
		data['beam_limiting_device_angle'] = self.beam_limiting_device_angle
		data['table_top_roll_angle'] = self.table_top_roll_angle
		data['nominal_beam_energy_unit'] = self.nominal_beam_energy_unit
		data['layer'] = self.layer.expand_data()
		data['ref_instance_uid'] = self.ref_instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['patient_support_angle'] = self.patient_support_angle
		data['number'] = self.number
		data['iso_center_position'] = self.iso_center_position
		data['table_top_pitch_direction'] = self.table_top_pitch_direction
		data['snout_position'] = self.snout_position
		data['gantry_pitch_angle'] = self.gantry_pitch_angle
		data['surface_entry_point'] = self.surface_entry_point
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['table_top_pitch_angle'] = self.table_top_pitch_angle
		data['meterset_weight'] = self.meterset_weight
		data['source_to_surface_distance'] = self.source_to_surface_distance
		data['instance_uid'] = self.instance_uid
		data['patient_support_direction'] = self.patient_support_direction
		data['beam_limiting_direction'] = self.beam_limiting_direction
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['class_uid'] = self.class_uid
		data['gantry_angle'] = self.gantry_angle
		data['meterset_rate'] = self.meterset_rate
		data['gantry_rotation_direction'] = self.gantry_rotation_direction
		data['table_top_roll_direction'] = self.table_top_roll_direction
		data['series_uid'] = self.series_uid
		data['nominal_beam_energy'] = self.nominal_beam_energy
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
		self.number_frames = 0 
		self.ref_fraction_num = "" 
		self.summation_type = dose_summation_type()
		self.instance_uid = "" 
		self.type = dose_type()
		self.ref_instance_uid = "" 
		self.meta_data = dicom_metadata()
		self.frame_spacing = [] 
		self.ref_beam_num = "" 
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.dose = rt_image_data()
		self.elements = [] 
		self.referenced_ids = [] 
		self.frame_of_ref_uid = "" 
		self.frame_increment_pointer = "" 

	def expand_data(self):
		data = {}
		data['number_frames'] = self.number_frames
		data['ref_fraction_num'] = self.ref_fraction_num
		data['summation_type'] = self.summation_type.expand_data()
		data['instance_uid'] = self.instance_uid
		data['type'] = self.type.expand_data()
		data['ref_instance_uid'] = self.ref_instance_uid
		data['meta_data'] = self.meta_data.expand_data()
		data['frame_spacing'] = self.frame_spacing
		data['ref_beam_num'] = self.ref_beam_num
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['dose'] = self.dose.expand_data()
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		referenced_id = []
		for x in self.referenced_ids:
			s = ref_dicom_item()
			s.from_json(x)
			referenced_id.append(s.expand_data())
		data['referenced_ids'] = referenced_id
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		data['frame_increment_pointer'] = self.frame_increment_pointer
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'summation_type':
					self.summation_type.from_json(v)
				elif k == 'type':
					self.type.from_json(v)
				elif k == 'meta_data':
					self.meta_data.from_json(v)
				elif k == 'dose':
					self.dose.from_json(v)
				else:
					setattr(self, k, v)

class rt_dose_reference(object):

	#Initialize
	def __init__(self):
		self.type = "" 
		self.target_min_dose = 0.0 
		self.instance_uid = "" 
		self.structure_type = "" 
		self.target_underdose_vol_fraction = 0.0 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.description = "" 
		self.sequences = [] 
		self.ref_roi_number = 0 
		self.number = 0 
		self.target_max_dose = 0.0 
		self.point_coordinates = [] 
		self.uid = "" 
		self.delivery_max_dose = 0.0 
		self.series_uid = "" 
		self.ref_class_uid = "" 
		self.target_rx_dose = 0.0 

	def expand_data(self):
		data = {}
		data['type'] = self.type
		data['target_min_dose'] = self.target_min_dose
		data['instance_uid'] = self.instance_uid
		data['structure_type'] = self.structure_type
		data['target_underdose_vol_fraction'] = self.target_underdose_vol_fraction
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		data['class_uid'] = self.class_uid
		data['description'] = self.description
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['ref_roi_number'] = self.ref_roi_number
		data['number'] = self.number
		data['target_max_dose'] = self.target_max_dose
		data['point_coordinates'] = self.point_coordinates
		data['uid'] = self.uid
		data['delivery_max_dose'] = self.delivery_max_dose
		data['series_uid'] = self.series_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['target_rx_dose'] = self.target_rx_dose
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_fraction(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.ref_beam = [] 
		self.number = 0 
		self.number_beams = 0 
		self.number_planned_fractions = 0 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		ref_bea = []
		for x in self.ref_beam:
			s = rt_ref_beam()
			s.from_json(x)
			ref_bea.append(s.expand_data())
		data['ref_beam'] = ref_bea
		data['number'] = self.number
		data['number_beams'] = self.number_beams
		data['number_planned_fractions'] = self.number_planned_fractions
		data['instance_uid'] = self.instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_image_2d(object):

	#Initialize
	def __init__(self):
		self.bits_stored = 0 
		self.rescale_intercept = 0.0 
		self.bits_allocated = 0 
		self.rescale_slope = 0.0 
		self.cols = 0 
		self.high_bit = 0 
		self.rows = 0 
		self.img = image_2d()

	def expand_data(self):
		data = {}
		data['bits_stored'] = self.bits_stored
		data['rescale_intercept'] = self.rescale_intercept
		data['bits_allocated'] = self.bits_allocated
		data['rescale_slope'] = self.rescale_slope
		data['cols'] = self.cols
		data['high_bit'] = self.high_bit
		data['rows'] = self.rows
		data['img'] = self.img.expand_data()
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
		self.bits_stored = 0 
		self.rescale_intercept = 0.0 
		self.bits_allocated = 0 
		self.rescale_slope = 0.0 
		self.cols = 0 
		self.high_bit = 0 
		self.rows = 0 
		self.img = image_3d()

	def expand_data(self):
		data = {}
		data['bits_stored'] = self.bits_stored
		data['rescale_intercept'] = self.rescale_intercept
		data['bits_allocated'] = self.bits_allocated
		data['rescale_slope'] = self.rescale_slope
		data['cols'] = self.cols
		data['high_bit'] = self.high_bit
		data['rows'] = self.rows
		data['img'] = self.img.expand_data()
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

class rt_image_data(object):

	#Initialize
	def __init__(self):
		self.image_orientation = [] 
		self.thickness = 0.0 
		self.axis = 0 
		self.pixel_rep = 0 
		self.pixel_spacing = [] 
		self.content = rt_image_3d()
		self.photometric_interpretation = "" 
		self.instance_number = 0 
		self.image_position = [] 
		self.samples_per_pixel = 0 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['image_orientation'] = self.image_orientation
		data['thickness'] = self.thickness
		data['axis'] = self.axis
		data['pixel_rep'] = self.pixel_rep
		data['pixel_spacing'] = self.pixel_spacing
		data['content'] = self.content.expand_data()
		data['photometric_interpretation'] = self.photometric_interpretation
		data['instance_number'] = self.instance_number
		data['image_position'] = self.image_position
		data['samples_per_pixel'] = self.samples_per_pixel
		data['position'] = self.position
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
		# drr
		# portal
		# radiograph
		# fluence
		# blank
		# simulator

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
		self.beam_type = rt_ion_beam_type()
		self.referenced_patient_setup = 0 
		self.virtual_sad = [] 
		self.control_points = [] 
		self.snouts = [] 
		self.treatment_delivery_type = "" 
		self.ref_instance_uid = "" 
		self.primary_dosimeter_unit = "" 
		self.radiation_type = rt_radiation_type()
		self.beam_number = 0 
		self.beam_scan_mode = rt_ion_beam_scan_mode()
		self.ref_class_uid = "" 
		self.degraders = [] 
		self.treatment_machine = "" 
		self.block = rt_ion_block()
		self.shifters = [] 
		self.final_meterset_weight = 0.0 
		self.instance_uid = "" 
		self.sequences = [] 
		self.elements = [] 
		self.class_uid = "" 
		self.series_uid = "" 
		self.name = "" 
		self.description = "" 
		self.referenced_tolerance_table = 0 

	def expand_data(self):
		data = {}
		data['beam_type'] = self.beam_type.expand_data()
		data['referenced_patient_setup'] = self.referenced_patient_setup
		data['virtual_sad'] = self.virtual_sad
		control_point = []
		for x in self.control_points:
			s = rt_control_point()
			s.from_json(x)
			control_point.append(s.expand_data())
		data['control_points'] = control_point
		snout = []
		for x in self.snouts:
			s = rt_snout()
			s.from_json(x)
			snout.append(s.expand_data())
		data['snouts'] = snout
		data['treatment_delivery_type'] = self.treatment_delivery_type
		data['ref_instance_uid'] = self.ref_instance_uid
		data['primary_dosimeter_unit'] = self.primary_dosimeter_unit
		data['radiation_type'] = self.radiation_type.expand_data()
		data['beam_number'] = self.beam_number
		data['beam_scan_mode'] = self.beam_scan_mode.expand_data()
		data['ref_class_uid'] = self.ref_class_uid
		degrader = []
		for x in self.degraders:
			s = rt_ion_rangecompensator()
			s.from_json(x)
			degrader.append(s.expand_data())
		data['degraders'] = degrader
		data['treatment_machine'] = self.treatment_machine
		data['block'] = self.block.expand_data()
		shifter = []
		for x in self.shifters:
			s = rt_ion_range_shifter()
			s.from_json(x)
			shifter.append(s.expand_data())
		data['shifters'] = shifter
		data['final_meterset_weight'] = self.final_meterset_weight
		data['instance_uid'] = self.instance_uid
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
		data['class_uid'] = self.class_uid
		data['series_uid'] = self.series_uid
		data['name'] = self.name
		data['description'] = self.description
		data['referenced_tolerance_table'] = self.referenced_tolerance_table
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'beam_type':
					self.beam_type.from_json(v)
				elif k == 'radiation_type':
					self.radiation_type.from_json(v)
				elif k == 'beam_scan_mode':
					self.beam_scan_mode.from_json(v)
				elif k == 'block':
					self.block.from_json(v)
				else:
					setattr(self, k, v)

class rt_ion_beam_scan_mode(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# modulated
		# none
		# uniform

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
		self.downstream_edge = 0.0 
		self.material = "" 
		self.instance_uid = "" 
		self.divergent = False 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.number = 0 
		self.thickness = 0.0 
		self.data = polyset()
		self.description = "" 
		self.block_type = rt_ion_block_type()
		self.name = "" 
		self.position = rt_mounting_position()

	def expand_data(self):
		data = {}
		data['downstream_edge'] = self.downstream_edge
		data['material'] = self.material
		data['instance_uid'] = self.instance_uid
		data['divergent'] = self.divergent
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['number'] = self.number
		data['thickness'] = self.thickness
		data['data'] = self.data.expand_data()
		data['description'] = self.description
		data['block_type'] = self.block_type.expand_data()
		data['name'] = self.name
		data['position'] = self.position.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'data':
					self.data.from_json(v)
				elif k == 'block_type':
					self.block_type.from_json(v)
				elif k == 'position':
					self.position.from_json(v)
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
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.number = 0 
		self.instance_uid = "" 
		self.id = "" 
		self.type = rt_range_shifter_type()
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['number'] = self.number
		data['instance_uid'] = self.instance_uid
		data['id'] = self.id
		data['type'] = self.type.expand_data()
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
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
		self.downstream_edge = 0.0 
		self.material = "" 
		self.relative_stopping_power = 0.0 
		self.instance_uid = "" 
		self.divergent = False 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.number = 0 
		self.column_offset = 0.0 
		self.mounting_position = rt_mounting_position()
		self.pixelSpacing = [] 
		self.data = image_2d()
		self.name = "" 
		self.position = [] 

	def expand_data(self):
		data = {}
		data['downstream_edge'] = self.downstream_edge
		data['material'] = self.material
		data['relative_stopping_power'] = self.relative_stopping_power
		data['instance_uid'] = self.instance_uid
		data['divergent'] = self.divergent
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['number'] = self.number
		data['column_offset'] = self.column_offset
		data['mounting_position'] = self.mounting_position.expand_data()
		data['pixelSpacing'] = self.pixelSpacing
		data['data'] = self.data.expand_data()
		data['name'] = self.name
		data['position'] = self.position
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
		# double_sided
		# patient_side
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
		self.setup_number = 0 
		self.table_top_vert_setup_dis = 0.0 
		self.setup_technique = "" 
		self.instance_uid = "" 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.table_top_long_setup_dis = 0.0 
		self.table_top_lateral_setup_dis = 0.0 
		self.setup_description = "" 
		self.position = patient_position_type()

	def expand_data(self):
		data = {}
		data['setup_number'] = self.setup_number
		data['table_top_vert_setup_dis'] = self.table_top_vert_setup_dis
		data['setup_technique'] = self.setup_technique
		data['instance_uid'] = self.instance_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['table_top_long_setup_dis'] = self.table_top_long_setup_dis
		data['table_top_lateral_setup_dis'] = self.table_top_lateral_setup_dis
		data['setup_description'] = self.setup_description
		data['position'] = self.position.expand_data()
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
		self.plan_date = "" 
		self.tolerance_table = [] 
		self.label = "" 
		self.ref_instance_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.referenced_ids = [] 
		self.patient_data = patient()
		self.name = "" 
		self.class_uid = "" 
		self.beams = [] 
		self.patient_setups = [] 
		self.geometry = "" 
		self.meta_data = dicom_metadata()
		self.elements = [] 
		self.frame_of_ref_uid = "" 
		self.instance_uid = "" 
		self.series_uid = "" 
		self.dose = [] 
		self.description = "" 
		self.uid = "" 
		self.fractions = [] 

	def expand_data(self):
		data = {}
		data['plan_date'] = self.plan_date
		tolerance_tabl = []
		for x in self.tolerance_table:
			s = rt_tolerance_table()
			s.from_json(x)
			tolerance_tabl.append(s.expand_data())
		data['tolerance_table'] = tolerance_tabl
		data['label'] = self.label
		data['ref_instance_uid'] = self.ref_instance_uid
		data['ref_class_uid'] = self.ref_class_uid
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
		data['patient_data'] = self.patient_data.expand_data()
		data['name'] = self.name
		data['class_uid'] = self.class_uid
		beam = []
		for x in self.beams:
			s = rt_ion_beam()
			s.from_json(x)
			beam.append(s.expand_data())
		data['beams'] = beam
		patient_setup = []
		for x in self.patient_setups:
			s = rt_patient_setup()
			s.from_json(x)
			patient_setup.append(s.expand_data())
		data['patient_setups'] = patient_setup
		data['geometry'] = self.geometry
		data['meta_data'] = self.meta_data.expand_data()
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		data['instance_uid'] = self.instance_uid
		data['series_uid'] = self.series_uid
		dos = []
		for x in self.dose:
			s = rt_dose_reference()
			s.from_json(x)
			dos.append(s.expand_data())
		data['dose'] = dos
		data['description'] = self.description
		data['uid'] = self.uid
		fraction = []
		for x in self.fractions:
			s = rt_fraction()
			s.from_json(x)
			fraction.append(s.expand_data())
		data['fractions'] = fraction
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_data':
					self.patient_data.from_json(v)
				elif k == 'meta_data':
					self.meta_data.from_json(v)
				else:
					setattr(self, k, v)

class rt_radiation_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# neutron
		# electron
		# photon
		# proton

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
		# binary
		# analog

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
		self.beam_dose = 0.0 
		self.class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.beam_meterset = 0.0 
		self.beam_number = 0 
		self.ref_instance_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.elements = [] 
		self.dose_specification_point = [] 

	def expand_data(self):
		data = {}
		data['beam_dose'] = self.beam_dose
		data['class_uid'] = self.class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['beam_meterset'] = self.beam_meterset
		data['beam_number'] = self.beam_number
		data['ref_instance_uid'] = self.ref_instance_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['dose_specification_point'] = self.dose_specification_point
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_snout(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.instance_uid = "" 
		self.id = "" 
		self.accessoryCode = "" 
		self.elements = [] 
		self.ref_instance_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['instance_uid'] = self.instance_uid
		data['id'] = self.id
		data['accessoryCode'] = self.accessoryCode
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_structure(object):

	#Initialize
	def __init__(self):
		self.color = rgb8()
		self.instance_uid = "" 
		self.type = rt_structure_type()
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.number = 0 
		self.volume = dicom_structure_geometry()
		self.description = "" 
		self.point = [] 
		self.name = "" 

	def expand_data(self):
		data = {}
		data['color'] = self.color.expand_data()
		data['instance_uid'] = self.instance_uid
		data['type'] = self.type.expand_data()
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['number'] = self.number
		data['volume'] = self.volume.expand_data()
		data['description'] = self.description
		data['point'] = self.point
		data['name'] = self.name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'color':
					self.color.from_json(v)
				elif k == 'type':
					self.type.from_json(v)
				elif k == 'volume':
					self.volume.from_json(v)
				else:
					setattr(self, k, v)

class rt_structure_set(object):

	#Initialize
	def __init__(self):
		self.structures = [] 
		self.instance_uid = "" 
		self.meta_data = dicom_metadata()
		self.ref_class_uid = "" 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.patient_position = patient_position_type()
		self.sequences = [] 
		self.series_uid = "" 
		self.description = "" 
		self.contour_image_sequence = [] 
		self.frame_of_ref_uid = "" 
		self.name = "" 

	def expand_data(self):
		data = {}
		structure = []
		for x in self.structures:
			s = rt_structure()
			s.from_json(x)
			structure.append(s.expand_data())
		data['structures'] = structure
		data['instance_uid'] = self.instance_uid
		data['meta_data'] = self.meta_data.expand_data()
		data['ref_class_uid'] = self.ref_class_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		data['class_uid'] = self.class_uid
		data['patient_position'] = self.patient_position.expand_data()
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['description'] = self.description
		contour_image_sequenc = []
		for x in self.contour_image_sequence:
			s = dicom_item()
			s.from_json(x)
			contour_image_sequenc.append(s.expand_data())
		data['contour_image_sequence'] = contour_image_sequenc
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		data['name'] = self.name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'meta_data':
					self.meta_data.from_json(v)
				elif k == 'patient_position':
					self.patient_position.from_json(v)
				else:
					setattr(self, k, v)

class rt_structure_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# closed_planar
		# point

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
		self.plan = rt_plan()
		self.study_date = "" 
		self.instance_uid = "" 
		self.id = "" 
		self.doses = [] 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.sequences = [] 
		self.series_uid = "" 
		self.structure_set = rt_structure_set()
		self.description = "" 
		self.ct = ct_image()
		self.physician_name = "" 
		self.accession_number = "" 
		self.name = "" 

	def expand_data(self):
		data = {}
		data['plan'] = self.plan.expand_data()
		data['study_date'] = self.study_date
		data['instance_uid'] = self.instance_uid
		data['id'] = self.id
		dose = []
		for x in self.doses:
			s = rt_dose()
			s.from_json(x)
			dose.append(s.expand_data())
		data['doses'] = dose
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		data['ref_instance_uid'] = self.ref_instance_uid
		data['class_uid'] = self.class_uid
		data['ref_class_uid'] = self.ref_class_uid
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['series_uid'] = self.series_uid
		data['structure_set'] = self.structure_set.expand_data()
		data['description'] = self.description
		data['ct'] = self.ct.expand_data()
		data['physician_name'] = self.physician_name
		data['accession_number'] = self.accession_number
		data['name'] = self.name
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'plan':
					self.plan.from_json(v)
				elif k == 'structure_set':
					self.structure_set.from_json(v)
				elif k == 'ct':
					self.ct.from_json(v)
				else:
					setattr(self, k, v)

class rt_tolerance_table(object):

	#Initialize
	def __init__(self):
		self.table_top_vert_position = 0.0 
		self.table_top_lat_position = 0.0 
		self.limiting_device_type = [] 
		self.label = "" 
		self.instance_uid = "" 
		self.beam_limiting_angle = 0.0 
		self.sequences = [] 
		self.elements = [] 
		self.ref_instance_uid = "" 
		self.class_uid = "" 
		self.ref_class_uid = "" 
		self.patient_support_angle = 0.0 
		self.gantry_angle = 0.0 
		self.number = 0 
		self.table_top_long_position = 0.0 
		self.series_uid = "" 
		self.limiting_device_position = [] 

	def expand_data(self):
		data = {}
		data['table_top_vert_position'] = self.table_top_vert_position
		data['table_top_lat_position'] = self.table_top_lat_position
		data['label'] = self.label
		data['instance_uid'] = self.instance_uid
		data['beam_limiting_angle'] = self.beam_limiting_angle
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
		data['ref_class_uid'] = self.ref_class_uid
		data['patient_support_angle'] = self.patient_support_angle
		data['gantry_angle'] = self.gantry_angle
		data['number'] = self.number
		data['table_top_long_position'] = self.table_top_long_position
		data['series_uid'] = self.series_uid
		data['limiting_device_position'] = self.limiting_device_position
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
		# union
		# intersection
		# xor
		# difference

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
		self.point_samples = [] 
		self.profiles = [] 

	def expand_data(self):
		data = {}
		point_sample = []
		for x in self.point_samples:
			s = point_sample_2d()
			s.from_json(x)
			point_sample.append(s.expand_data())
		data['point_samples'] = point_sample
		profile = []
		for x in self.profiles:
			s = line_profile()
			s.from_json(x)
			profile.append(s.expand_data())
		data['profiles'] = profile
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class simple_dose_constraint(object):

	#Initialize
	def __init__(self):
		self.voxels = [] 
		self.beams = [] 
		self.dose_level = 0.0 

	def expand_data(self):
		data = {}
		voxel = []
		for x in self.voxels:
			s = weighted_grid_index()
			s.from_json(x)
			voxel.append(s.expand_data())
		data['voxels'] = voxel
		data['beams'] = self.beams
		data['dose_level'] = self.dose_level
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class slab_info(object):

	#Initialize
	def __init__(self):
		self.range = 0.0 
		self.count = 0 
		self.thickness = 0.0 

	def expand_data(self):
		data = {}
		data['range'] = self.range
		data['count'] = self.count
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
		self.thickness = 0.0 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['thickness'] = self.thickness
		data['position'] = self.position
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
		# rectangular
		# circular

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
		self.initial_sigma = 0.0 
		self.sad = 0.0 
		self.depth_dose_curve = interpolated_function()
		self.weight = 0.0 
		self.pdd_shift = 0.0 
		self.initial_range = 0.0 

	def expand_data(self):
		data = {}
		data['initial_sigma'] = self.initial_sigma
		data['sad'] = self.sad
		data['depth_dose_curve'] = self.depth_dose_curve.expand_data()
		data['weight'] = self.weight
		data['pdd_shift'] = self.pdd_shift
		data['initial_range'] = self.initial_range
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
		self.fill = spatial_region_fill_options()
		self.outline = spatial_region_outline_options()

	def expand_data(self):
		data = {}
		data['fill'] = self.fill.expand_data()
		data['outline'] = self.outline.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'fill':
					self.fill.from_json(v)
				elif k == 'outline':
					self.outline.from_json(v)
				else:
					setattr(self, k, v)

class spatial_region_fill_options(object):

	#Initialize
	def __init__(self):
		self.enabled = False 
		self.opacity = 0.0 

	def expand_data(self):
		data = {}
		data['enabled'] = self.enabled
		data['opacity'] = self.opacity
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class spatial_region_outline_options(object):

	#Initialize
	def __init__(self):
		self.type = line_stipple_type()
		self.width = 0.0 
		self.opacity = 0.0 

	def expand_data(self):
		data = {}
		data['type'] = self.type.expand_data()
		data['width'] = self.width
		data['opacity'] = self.opacity
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
		self.selected_energy = "" 
		self.energy_list = [] 

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
		# sigma
		# constant

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
		self.min = 0.0 
		self.max = 0.0 
		self.n_samples = 0.0 
		self.mean = 0.0 

	def expand_data(self):
		data = {}
		data['min'] = self.min
		data['max'] = self.max
		data['n_samples'] = self.n_samples
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
		self.thickness = 0.0 
		self.position = 0.0 

	def expand_data(self):
		data = {}
		data['region'] = self.region.expand_data()
		data['thickness'] = self.thickness
		data['position'] = self.position
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
		self.type = subtask_event_type()
		self.task_id = "" 

	def expand_data(self):
		data = {}
		data['type'] = self.type.expand_data()
		data['task_id'] = self.task_id
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
		self.settings = [] 
		self.location = "" 
		self.description = "" 
		self.manufacturer = "" 
		self.rooms = [] 
		self.name = "" 
		self.serial = "" 

	def expand_data(self):
		data = {}
		setting = []
		for x in self.settings:
			s = machine_setting()
			s.from_json(x)
			setting.append(s.expand_data())
		data['settings'] = setting
		data['location'] = self.location
		data['description'] = self.description
		data['manufacturer'] = self.manufacturer
		room = []
		for x in self.rooms:
			s = treatment_room()
			s.from_json(x)
			room.append(s.expand_data())
		data['rooms'] = room
		data['name'] = self.name
		data['serial'] = self.serial
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class treatment_room(object):

	#Initialize
	def __init__(self):
		self.machine_geometry_name = "" 
		self.name = "" 
		self.snout_names = [] 

	def expand_data(self):
		data = {}
		data['machine_geometry_name'] = self.machine_geometry_name
		data['name'] = self.name
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
		self.face_position_indices = blob.toStr()
		blob = blob_type()
		self.face_normal_indices = blob.toStr()
		blob = blob_type()
		self.vertex_normals = blob.toStr()
		blob = blob_type()
		self.vertex_positions = blob.toStr()

	def expand_data(self):
		data = {}
		data['face_position_indices'] = parse_bytes_3i(base64.b64decode(self.face_position_indices['blob']))
		data['face_normal_indices'] = parse_bytes_3i(base64.b64decode(self.face_normal_indices['blob']))
		data['vertex_normals'] = parse_bytes_3d(base64.b64decode(self.vertex_normals['blob']))
		data['vertex_positions'] = parse_bytes_3d(base64.b64decode(self.vertex_positions['blob']))
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
		# open
		# closed
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
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.pixels = [] 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['pixels'] = self.pixels
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class unboxed_image_3d(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.pixels = [] 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['pixels'] = self.pixels
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class variant_type_info(object):

	#Initialize
	def __init__(self):
		self.type = channel_type()
		self.format = pixel_format()

	def expand_data(self):
		data = {}
		data['type'] = self.type.expand_data()
		data['format'] = self.format.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'type':
					self.type.from_json(v)
				elif k == 'format':
					self.format.from_json(v)
				else:
					setattr(self, k, v)

class weighted_bixel(object):

	#Initialize
	def __init__(self):
		self.weight = 0.0 
		self.geometry = bixel_geometry()

	def expand_data(self):
		data = {}
		data['weight'] = self.weight
		data['geometry'] = self.geometry.expand_data()
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

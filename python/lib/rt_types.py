# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:	Travis DeMint & Daniel Patenaude
# Date:		08/28/2015
# Desc:		Provides access to type usage for all types
# RT_Types Version:		1.0.0.2

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
		self.extents = box_3d()
		blob = blob_type()
		self.voxels = blob.toStr()
		blob = blob_type()
		self.volumes = blob.toStr()

	def expand_data(self):
		data = {}
		data['extents'] = self.extents.expand_data()
		data['voxels'] = parse_bytes_daptive_grid_voxel(base64.b64decode(self.voxels['blob']))
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
		self.index = 0.0 
		self.volume_offset = 0.0 
		self.inside_count = 0.0 
		self.surface_count = 0.0 

	def expand_data(self):
		data = {}
		data['index'] = self.index
		data['volume_offset'] = self.volume_offset
		data['inside_count'] = self.inside_count
		data['surface_count'] = self.surface_count
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
		self.structure = triangle_mesh()
		self.margin = 0.0 

	def expand_data(self):
		data = {}
		data['structure'] = self.structure.expand_data()
		data['margin'] = self.margin
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
		self.first_direction = 0.0 
		self.second_direction = 0.0 

	def expand_data(self):
		data = {}
		data['origin'] = self.origin
		data['first_direction'] = self.first_direction
		data['second_direction'] = self.second_direction
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class aperture_creation_params(object):

	#Initialize
	def __init__(self):
		self.targets = [] 
		self.target_margin = 0.0 
		self.mill_radius = 0.0 
		self.organs = [] 
		self.half_planes = [] 
		self.corner_planes = [] 
		self.centerlines = [] 
		self.overrides = [] 
		self.downstream_edge = 0.0 

	def expand_data(self):
		data = {}
		target = []
		for x in self.targets:
			s = triangle_mesh()
			s.from_json(x)
			target.append(s.expand_data())
		data['targets'] = target
		data['target_margin'] = self.target_margin
		data['mill_radius'] = self.mill_radius
		organ = []
		for x in self.organs:
			s = aperture_organ()
			s.from_json(x)
			organ.append(s.expand_data())
		data['organs'] = organ
		half_plane = []
		for x in self.half_planes:
			s = aperture_half_plane()
			s.from_json(x)
			half_plane.append(s.expand_data())
		data['half_planes'] = half_plane
		corner_plane = []
		for x in self.corner_planes:
			s = aperture_corner_plane()
			s.from_json(x)
			corner_plane.append(s.expand_data())
		data['corner_planes'] = corner_plane
		centerline = []
		for x in self.centerlines:
			s = aperture_centerline()
			s.from_json(x)
			centerline.append(s.expand_data())
		data['centerlines'] = centerline
		override = []
		for x in self.overrides:
			s = aperture_manual_override()
			s.from_json(x)
			override.append(s.expand_data())
		data['overrides'] = override
		data['downstream_edge'] = self.downstream_edge
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class aperture_half_plane(object):

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.direction = 0.0 

	def expand_data(self):
		data = {}
		data['origin'] = self.origin
		data['direction'] = self.direction
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
		self.structure = triangle_mesh()
		self.margin = 0.0 
		self.occlude_by_target = False 

	def expand_data(self):
		data = {}
		data['structure'] = self.structure.expand_data()
		data['margin'] = self.margin
		data['occlude_by_target'] = self.occlude_by_target
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
		self.structure = triangle_mesh()
		self.margin = 0.0 

	def expand_data(self):
		data = {}
		data['structure'] = self.structure.expand_data()
		data['margin'] = self.margin
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
		# app_contents
		# app_info
		# settings
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

class base_zoom_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# stretch_to_fit
		# fit_scene
		# fit_scene_width
		# fit_scene_height
		# fill_canvas

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
		self.sad = [] 
		self.image_to_beam = [] 

	def expand_data(self):
		data = {}
		data['sad'] = self.sad
		data['image_to_beam'] = self.image_to_beam
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class beam_properties(object):

	#Initialize
	def __init__(self):
		self.geometry = beam_geometry()
		self.field = box_2d()
		self.ssd = 0.0 
		self.bixel_grid = regular_grid_2d()
		self.range = 0.0 

	def expand_data(self):
		data = {}
		data['geometry'] = self.geometry.expand_data()
		data['field'] = self.field.expand_data()
		data['ssd'] = self.ssd
		data['bixel_grid'] = self.bixel_grid.expand_data()
		data['range'] = self.range
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'geometry':
					self.geometry.from_json(v)
				elif k == 'field':
					self.field.from_json(v)
				elif k == 'bixel_grid':
					self.bixel_grid.from_json(v)
				else:
					setattr(self, k, v)

class bin_collection_3d(object):

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

	def expand_data(self):
		data = {}
		data['bounds'] = self.bounds.expand_data()
		data['grid_size'] = self.grid_size
		data['offsets'] = parse_bytes_u(base64.b64decode(self.offsets['blob']))
		data['counts'] = parse_bytes_u(base64.b64decode(self.counts['blob']))
		data['bins'] = parse_bytes_temType(base64.b64decode(self.bins['blob']))
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'bounds':
					self.bounds.from_json(v)
				else:
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
		self.corner = [] 
		self.size = [] 

	def expand_data(self):
		data = {}
		data['corner'] = self.corner
		data['size'] = self.size
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class box_2d(object):

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

	def expand_data(self):
		data = {}
		data['corner'] = self.corner
		data['size'] = self.size
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class box_3d(object):

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

	def expand_data(self):
		data = {}
		data['corner'] = self.corner
		data['size'] = self.size
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class box_4d(object):

	#Initialize
	def __init__(self):
		self.corner = [] 
		self.size = [] 

	def expand_data(self):
		data = {}
		data['corner'] = self.corner
		data['size'] = self.size
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
		self.zoom = 0.0 
		self.position = [] 
		self.direction = [] 
		self.up = [] 

	def expand_data(self):
		data = {}
		data['zoom'] = self.zoom
		data['position'] = self.position
		data['direction'] = self.direction
		data['up'] = self.up
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
		self.level = 0.0 
		self.color = rgba()

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
		self.color = rgba()

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

class ct_image_set(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.image = image_3d()
		self.patient_position = patient_position_type()
		self.study = rt_study()

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['image'] = self.image.expand_data()
		data['patient_position'] = self.patient_position.expand_data()
		data['study'] = self.study.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'image':
					self.image.from_json(v)
				elif k == 'patient_position':
					self.patient_position.from_json(v)
				elif k == 'study':
					self.study.from_json(v)
				else:
					setattr(self, k, v)

class ct_image_slice(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.slice = rt_image_slice_2d()
		self.patient_position = patient_position_type()
		self.study = rt_study()

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['slice'] = self.slice.expand_data()
		data['patient_position'] = self.patient_position.expand_data()
		data['study'] = self.study.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'slice':
					self.slice.from_json(v)
				elif k == 'patient_position':
					self.patient_position.from_json(v)
				elif k == 'study':
					self.study.from_json(v)
				else:
					setattr(self, k, v)

class data_reporting_parameters(object):

	#Initialize
	def __init__(self):
		self.label = "" 
		self.units = "" 
		self.digits = 0.0 

	def expand_data(self):
		data = {}
		data['label'] = self.label
		data['units'] = self.units
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
		self.thickness_units = "" 
		self.scale_factor = 0.0 
		self.shape = degrader_shape()

	def expand_data(self):
		data = {}
		data['downstream_edge'] = self.downstream_edge
		data['thickness_units'] = self.thickness_units
		data['scale_factor'] = self.scale_factor
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
		self.type = ""
		self.shifter = shifter_geometry.toStr()
		self.block = block_geometry.toStr()
		self.rc = rc_geometry.toStr()
		self.rc_nurb = rc_nurb_geometry.toStr()

class dicom_data(object):

	#Initialize
	def __init__(self):
		self.meta_data = dicom_metadata()
		self.dicom_obj = dicom_object()

	def expand_data(self):
		data = {}
		data['meta_data'] = self.meta_data.expand_data()
		data['dicom_obj'] = self.dicom_obj.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'meta_data':
					self.meta_data.from_json(v)
				elif k == 'dicom_obj':
					self.dicom_obj.from_json(v)
				else:
					setattr(self, k, v)

class dicom_element(object):

	#Initialize
	def __init__(self):
		self.name = "" 
		self.value = "" 
		self.g = 0.0 
		self.e = 0.0 

	def expand_data(self):
		data = {}
		data['name'] = self.name
		data['value'] = self.value
		data['g'] = self.g
		data['e'] = self.e
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_item(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
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
				setattr(self, k, v)

class dicom_metadata(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.creationDate = "" 
		self.patient_metadata = patient()
		self.modality = dicom_modality()

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['creationDate'] = self.creationDate
		data['patient_metadata'] = self.patient_metadata.expand_data()
		data['modality'] = self.modality.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_metadata':
					self.patient_metadata.from_json(v)
				elif k == 'modality':
					self.modality.from_json(v)
				else:
					setattr(self, k, v)

class dicom_modality(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# RTPLAN
		# RTSTRUCTURESET
		# RTSTRUCT
		# CT
		# RTDOSE

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
		self.type = ""
		self.structure_set = rt_structure_set.toStr()
		self.ct_image = ct_image_slice.toStr()
		self.ct_image_set = ct_image_set.toStr()
		self.dose = rt_dose.toStr()
		self.plan = rt_plan.toStr()

class dicom_patient(object):

	#Initialize
	def __init__(self):
		self.patient = [] 

	def expand_data(self):
		data = {}
		patien = []
		for x in self.patient:
			s = dicom_data()
			s.from_json(x)
			patien.append(s.expand_data())
		data['patient'] = patien
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_sequence(object):

	#Initialize
	def __init__(self):
		self.items = [] 
		self.g = 0.0 
		self.e = 0.0 

	def expand_data(self):
		data = {}
		item = []
		for x in self.items:
			s = dicom_item()
			s.from_json(x)
			item.append(s.expand_data())
		data['items'] = item
		data['g'] = self.g
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
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.slices = [] 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		slice = []
		for x in self.slices:
			s = dicom_structure_geometry_slice()
			s.from_json(x)
			slice.append(s.expand_data())
		data['slices'] = slice
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dicom_structure_geometry_slice(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.position = 0.0 
		self.thickness = 0.0 
		self.region = polyset()

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['position'] = self.position
		data['thickness'] = self.thickness
		data['region'] = self.region.expand_data()
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
		self.beamlet_index = 0.0 
		self.dose = 0.0 

	def parse_self(self, buf, offset):
		self.beamlet_index = parse_bytes_u(buf, offset)
		self.dose = parse_bytes_f(buf, offset + 4)
		return self.expand_data()

	def get_offset(self):
		return 8

	def expand_data(self):
		data = {}
		data['beamlet_index'] = self.beamlet_index
		data['dose'] = self.dose
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class dij_matrix(object):

	#Initialize
	def __init__(self):
		self.n_points = 0.0 
		self.n_beamlets = 0.0 
		blob = blob_type()
		self.rows = blob.toStr()
		blob = blob_type()
		self.entries = blob.toStr()

	def expand_data(self):
		data = {}
		data['n_points'] = self.n_points
		data['n_beamlets'] = self.n_beamlets
		dijrow = dij_row()
		data['rows'] = parse_array(dijrow, base64.b64decode(self.rows['blob']))
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
		self.offset = 0.0 
		self.n_entries = 0.0 

	def parse_self(self, buf, offset):
		self.offset = parse_bytes_ul(buf, offset)
		self.n_entries = parse_bytes_u(buf, offset + 8)
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
		# main_plus_row
		# main_plus_column
		# two_rows
		# two_columns
		# squares

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
		self.controls_expanded = False 

	def expand_data(self):
		data = {}
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
		self.views = [] 
		self.layout = display_layout_type()

	def expand_data(self):
		data = {}
		data['id'] = self.id
		data['label'] = self.label
		view = []
		for x in self.views:
			s = display_view_instance()
			s.from_json(x)
			view.append(s.expand_data())
		data['views'] = view
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
		self.isUniform = False 
		self.z_position = 0.0 
		self.source_dist = 0.0 
		self.cax_length = 0.0 
		self.grid = regular_grid_2d()
		blob = blob_type()
		self.rays = blob.toStr()
		blob = blob_type()
		self.data = blob.toStr()

	def expand_data(self):
		data = {}
		data['isUniform'] = self.isUniform
		data['z_position'] = self.z_position
		data['source_dist'] = self.source_dist
		data['cax_length'] = self.cax_length
		data['grid'] = self.grid.expand_data()
		data['rays'] = parse_bytes_not_defined(base64.b64decode(self.rays['blob']))
		data['data'] = parse_bytes_not_defined(base64.b64decode(self.data['blob']))
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'grid':
					self.grid.from_json(v)
				else:
					setattr(self, k, v)

class dose_summation_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# PLAN
		# FRACTION
		# BEAM

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
		# PHYSICAL
		# EFFECTIVE
		# ERROR

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

	def expand_data(self):
		data = {}
		data['name'] = self.name
		data['id'] = self.id
		data['min_range'] = self.min_range
		data['max_range'] = self.max_range
		data['max_mod'] = self.max_mod
		data['wts1'] = self.wts1
		data['track_length'] = self.track_length
		data['penumbral_source_size'] = self.penumbral_source_size
		data['source_size_on_track'] = self.source_size_on_track
		data['sdm'] = self.sdm
		data['mod_correction'] = self.mod_correction
		step = []
		for x in self.steps:
			s = double_scattering_step()
			s.from_json(x)
			step.append(s.expand_data())
		data['steps'] = step
		data['bcm'] = self.bcm
		data['pristine_peak'] = self.pristine_peak.expand_data()
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
		self.weight = 0.0 
		self.dR = 0.0 

	def expand_data(self):
		data = {}
		data['theta'] = self.theta
		data['weight'] = self.weight
		data['dR'] = self.dR
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
		self.max_z = 0.0 
		self.min_value = 0.0 
		self.max_value = 0.0 
		self.image_z = 0.0 
		self.sizing = regular_grid_2d()

	def expand_data(self):
		data = {}
		data['image_display_options'] = self.image_display_options.expand_data()
		data['min_z'] = self.min_z
		data['max_z'] = self.max_z
		data['min_value'] = self.min_value
		data['max_value'] = self.max_value
		data['image_z'] = self.image_z
		data['sizing'] = self.sizing.expand_data()
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
		self.type = ""
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
		self.color = rgba()

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
		self.type = "" 
		self.completed_subtask_count = 0.0 
		self.canceled_subtask_count = 0.0 
		self.open_subtask_count = 0.0 

	def expand_data(self):
		data = {}
		data['type'] = self.type
		data['completed_subtask_count'] = self.completed_subtask_count
		data['canceled_subtask_count'] = self.canceled_subtask_count
		data['open_subtask_count'] = self.open_subtask_count
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
		self.type_info = variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = linear_function()
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
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
		self.type_info = variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = linear_function()
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
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
		self.type_info = variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = linear_function()
		self.units = "" 
		blob = blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
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
		self.slicing = [] 
		self.regular_grid = regular_grid_1d()

	def expand_data(self):
		data = {}
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
		self.slicing = [] 
		self.regular_grid = regular_grid_2d()

	def expand_data(self):
		data = {}
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
		self.slicing = [] 
		self.regular_grid = regular_grid_3d()

	def expand_data(self):
		data = {}
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
		self.slicing = [] 
		self.regular_grid = regular_grid_4d()

	def expand_data(self):
		data = {}
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
		self.axis = 0.0 
		self.position = 0.0 
		self.thickness = 0.0 
		self.content = image_1d()

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['position'] = self.position
		data['thickness'] = self.thickness
		data['content'] = self.content.expand_data()
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
		self.axis = 0.0 
		self.position = 0.0 
		self.thickness = 0.0 
		self.content = image_2d()

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['position'] = self.position
		data['thickness'] = self.thickness
		data['content'] = self.content.expand_data()
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
		self.axis = 0.0 
		self.position = 0.0 
		self.thickness = 0.0 
		self.content = image_3d()

	def expand_data(self):
		data = {}
		data['axis'] = self.axis
		data['position'] = self.position
		data['thickness'] = self.thickness
		data['content'] = self.content.expand_data()
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
		self.x0 = 0.0 
		self.x_spacing = 0.0 
		blob = blob_type()
		self.samples = blob.toStr()
		self.outside_domain_policy = outside_domain_policy()

	def expand_data(self):
		data = {}
		data['x0'] = self.x0
		data['x_spacing'] = self.x_spacing
		data['samples'] = parse_bytes_unction_sample(base64.b64decode(self.samples['blob']))
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
		self.axis = 0.0 
		self.position = 0.0 
		self.color = rgb()

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
		self.factor = 0.0 
		self.pattern = 0.0 

	def expand_data(self):
		data = {}
		data['factor'] = self.factor
		data['pattern'] = self.pattern
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
		# solid
		# dashed
		# dotted

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
		self.plan_count = 0.0 
		self.objectives = [] 
		self.p_matrix = [] 

	def expand_data(self):
		data = {}
		data['plan_count'] = self.plan_count
		objective = []
		for x in self.objectives:
			s = mco_navigation_objective()
			s.from_json(x)
			objective.append(s.expand_data())
		data['objectives'] = objective
		data['p_matrix'] = self.p_matrix
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
		self.center = [] 
		self.display_surface = box_2d()
		self.direction = [] 
		self.distance = [] 
		self.up = [] 

	def expand_data(self):
		data = {}
		data['center'] = self.center
		data['display_surface'] = self.display_surface.expand_data()
		data['direction'] = self.direction
		data['distance'] = self.distance
		data['up'] = self.up
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
		self.color = rgb()
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
		self.order = [] 
		self.point_counts = [] 
		self.knots = [] 
		self.heights = [] 
		self.weights = [] 
		self.box = box_2d()

	def expand_data(self):
		data = {}
		data['order'] = self.order
		data['point_counts'] = self.point_counts
		data['knots'] = self.knots
		data['heights'] = self.heights
		data['weights'] = self.weights
		data['box'] = self.box.expand_data()
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
		self.mesh = triangle_mesh()
		self.bin_collection = bin_collection_3d()

	def expand_data(self):
		data = {}
		data['mesh'] = self.mesh.expand_data()
		data['bin_collection'] = self.bin_collection.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'mesh':
					self.mesh.from_json(v)
				elif k == 'bin_collection':
					self.bin_collection.from_json(v)
				else:
					setattr(self, k, v)

class out_of_plane_information(object):

	#Initialize
	def __init__(self):
		self.axis = 0.0 
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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['name'] = self.name.expand_data()
		data['id'] = self.id
		data['sex'] = self.sex.expand_data()
		other_name = []
		for x in self.other_names:
			s = person_name()
			s.from_json(x)
			other_name.append(s.expand_data())
		data['other_names'] = other_name
		data['ethnic_group'] = self.ethnic_group
		data['comments'] = self.comments
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
		# HFS
		# HFP
		# FFS
		# FFP
		# HFDR
		# HFDL
		# FFDR
		# FFDL

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
		# M
		# F
		# O

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
		self.energy = 0.0 

	def expand_data(self):
		data = {}
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
		self.modeled_energies = [] 
		self.deliverable_energies = [] 
		self.source_rotation_function = linear_function()
		self.aperture_sad = [] 
		self.sad = [] 
		self.halo_sigma_sq_function = quadratic_function()

	def expand_data(self):
		data = {}
		modeled_energie = []
		for x in self.modeled_energies:
			s = pbs_modeled_energy()
			s.from_json(x)
			modeled_energie.append(s.expand_data())
		data['modeled_energies'] = modeled_energie
		deliverable_energie = []
		for x in self.deliverable_energies:
			s = pbs_deliverable_energy()
			s.from_json(x)
			deliverable_energie.append(s.expand_data())
		data['deliverable_energies'] = deliverable_energie
		data['source_rotation_function'] = self.source_rotation_function.expand_data()
		data['aperture_sad'] = self.aperture_sad
		data['sad'] = self.sad
		data['halo_sigma_sq_function'] = self.halo_sigma_sq_function.expand_data()
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
		self.w80 = 0.0 
		self.energy = 0.0 
		self.sigma = pbs_optical_sigma()
		self.pristine_peak = irregularly_sampled_function()

	def expand_data(self):
		data = {}
		data['r90'] = self.r90
		data['w80'] = self.w80
		data['energy'] = self.energy
		data['sigma'] = self.sigma.expand_data()
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
		self.aperture = aperture()
		self.sad = [] 

	def expand_data(self):
		data = {}
		data['aperture'] = self.aperture.expand_data()
		data['sad'] = self.sad
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
		self.flixels = [] 
		self.r90 = 0.0 
		self.energy = 0.0 
		self.sigma = pbs_optical_sigma()
		self.flixel_rotation = 0.0 
		self.pristine_peak = interpolated_function()

	def expand_data(self):
		data = {}
		flixel = []
		for x in self.flixels:
			s = projected_isocentric_vector()
			s.from_json(x)
			flixel.append(s.expand_data())
		data['flixels'] = flixel
		data['r90'] = self.r90
		data['energy'] = self.energy
		data['sigma'] = self.sigma.expand_data()
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
		self.num_spot_positions = 0.0 
		self.spots = [] 
		self.spot_size = [] 
		self.num_paintings = 0.0 
		self.spot_tune_id = 0.0 

	def expand_data(self):
		data = {}
		data['num_spot_positions'] = self.num_spot_positions
		spot = []
		for x in self.spots:
			s = weighted_spot()
			s.from_json(x)
			spot.append(s.expand_data())
		data['spots'] = spot
		data['spot_size'] = self.spot_size
		data['num_paintings'] = self.num_paintings
		data['spot_tune_id'] = self.spot_tune_id
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class person_name(object):

	#Initialize
	def __init__(self):
		self.family_name = "" 
		self.given_name = "" 
		self.middle_name = "" 
		self.prefix = "" 
		self.suffix = "" 

	def expand_data(self):
		data = {}
		data['family_name'] = self.family_name
		data['given_name'] = self.given_name
		data['middle_name'] = self.middle_name
		data['prefix'] = self.prefix
		data['suffix'] = self.suffix
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
		# gray
		# rgb
		# rgba

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
		self.point = [] 
		self.normal = [] 

	def expand_data(self):
		data = {}
		data['point'] = self.point
		data['normal'] = self.normal
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
		self.position = [] 
		self.color = rgb()

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
		self.at_iso = [] 
		self.delta = [] 

	def expand_data(self):
		data = {}
		data['at_iso'] = self.at_iso
		data['delta'] = self.delta
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class proton_degrader(object):

	#Initialize
	def __init__(self):
		self.geometry = degrader_geometry()
		self.material = proton_material_properties()

	def expand_data(self):
		data = {}
		data['geometry'] = self.geometry.expand_data()
		data['material'] = self.material.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'geometry':
					self.geometry.from_json(v)
				elif k == 'material':
					self.material.from_json(v)
				else:
					setattr(self, k, v)

class proton_material_properties(object):

	#Initialize
	def __init__(self):
		self.theta_curve = interpolated_function()
		self.density = 0.0 
		self.water_equivalent_ratio = 0.0 

	def expand_data(self):
		data = {}
		data['theta_curve'] = self.theta_curve.expand_data()
		data['density'] = self.density
		data['water_equivalent_ratio'] = self.water_equivalent_ratio
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
		self.b = 0.0 
		self.c = 0.0 

	def expand_data(self):
		data = {}
		data['a'] = self.a
		data['b'] = self.b
		data['c'] = self.c
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class range_analysis_context(object):

	#Initialize
	def __init__(self):
		self.patient_image = image_3d()
		self.sad = [] 
		self.image_to_beam = [] 
		self.beam_to_image = [] 
		self.degraders = [] 

	def expand_data(self):
		data = {}
		data['patient_image'] = self.patient_image.expand_data()
		data['sad'] = self.sad
		data['image_to_beam'] = self.image_to_beam
		data['beam_to_image'] = self.beam_to_image
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

class ray_2d(object):

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.direction = [] 

	def expand_data(self):
		data = {}
		data['origin'] = self.origin
		data['direction'] = self.direction
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_3d(object):

	#Initialize
	def __init__(self):
		self.origin = [] 
		self.direction = [] 

	def expand_data(self):
		data = {}
		data['origin'] = self.origin
		data['direction'] = self.direction
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_box_intersection_2d(object):

	#Initialize
	def __init__(self):
		self.n_intersections = 0.0 
		self.entrance_distance = 0.0 
		self.exit_distance = 0.0 

	def expand_data(self):
		data = {}
		data['n_intersections'] = self.n_intersections
		data['entrance_distance'] = self.entrance_distance
		data['exit_distance'] = self.exit_distance
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_box_intersection_3d(object):

	#Initialize
	def __init__(self):
		self.n_intersections = 0.0 
		self.entrance_distance = 0.0 
		self.exit_distance = 0.0 

	def expand_data(self):
		data = {}
		data['n_intersections'] = self.n_intersections
		data['entrance_distance'] = self.entrance_distance
		data['exit_distance'] = self.exit_distance
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class ray_points(object):

	#Initialize
	def __init__(self):
		self.n_points = 0.0 
		self.offset = 0.0 

	def expand_data(self):
		data = {}
		data['n_points'] = self.n_points
		data['offset'] = self.offset
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
		self.target_distal_dose = 0.0 
		self.target_inner_border = 0.0 
		self.iteration_count = 0.0 
		self.smear_weight = 0.0 
		self.smear_span = 0.0 
		self.shift_direction = 0.0 

	def expand_data(self):
		data = {}
		data['target_distal_dose'] = self.target_distal_dose
		data['target_inner_border'] = self.target_inner_border
		data['iteration_count'] = self.iteration_count
		data['smear_weight'] = self.smear_weight
		data['smear_span'] = self.smear_span
		data['shift_direction'] = self.shift_direction
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regular_grid_1d(object):

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

	def expand_data(self):
		data = {}
		data['p0'] = self.p0
		data['spacing'] = self.spacing
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regular_grid_2d(object):

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

	def expand_data(self):
		data = {}
		data['p0'] = self.p0
		data['spacing'] = self.spacing
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regular_grid_3d(object):

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

	def expand_data(self):
		data = {}
		data['p0'] = self.p0
		data['spacing'] = self.spacing
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regular_grid_4d(object):

	#Initialize
	def __init__(self):
		self.p0 = [] 
		self.spacing = [] 
		self.n_points = [] 

	def expand_data(self):
		data = {}
		data['p0'] = self.p0
		data['spacing'] = self.spacing
		data['n_points'] = self.n_points
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class regularly_sampled_function(object):

	#Initialize
	def __init__(self):
		self.x0 = 0.0 
		self.x_spacing = 0.0 
		self.samples = [] 
		self.outside_domain_policy = outside_domain_policy()

	def expand_data(self):
		data = {}
		data['x0'] = self.x0
		data['x_spacing'] = self.x_spacing
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

class rgb(object):

	#Initialize
	def __init__(self):
		self.r = 0.0 
		self.g = 0.0 
		self.b = 0.0 

	def expand_data(self):
		data = {}
		data['r'] = self.r
		data['g'] = self.g
		data['b'] = self.b
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rgba(object):

	#Initialize
	def __init__(self):
		self.r = 0.0 
		self.g = 0.0 
		self.b = 0.0 
		self.a = 0.0 

	def expand_data(self):
		data = {}
		data['r'] = self.r
		data['g'] = self.g
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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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
		self.layer = pbs_spot_layer()

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['number'] = self.number
		data['meterset_weight'] = self.meterset_weight
		data['nominal_beam_energy'] = self.nominal_beam_energy
		data['gantry_angle'] = self.gantry_angle
		data['gantry_pitch_angle'] = self.gantry_pitch_angle
		data['beam_limiting_device_angle'] = self.beam_limiting_device_angle
		data['patient_support_angle'] = self.patient_support_angle
		data['meterset_rate'] = self.meterset_rate
		data['source_to_surface_distance'] = self.source_to_surface_distance
		data['snout_position'] = self.snout_position
		data['iso_center_position'] = self.iso_center_position
		data['surface_entry_point'] = self.surface_entry_point
		data['gantry_rotation_direction'] = self.gantry_rotation_direction
		data['gantry_pitch_direction'] = self.gantry_pitch_direction
		data['beam_limiting_direction'] = self.beam_limiting_direction
		data['patient_support_direction'] = self.patient_support_direction
		data['table_top_pitch_angle'] = self.table_top_pitch_angle
		data['table_top_roll_angle'] = self.table_top_roll_angle
		data['table_top_pitch_direction'] = self.table_top_pitch_direction
		data['table_top_roll_direction'] = self.table_top_roll_direction
		data['layer'] = self.layer.expand_data()
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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.dose = rt_image_slice_3d()
		self.number_frames = 0.0 
		self.frame_spacing = [] 
		self.frame_increment_pointer = "" 
		self.study = rt_study()
		self.type = dose_type()
		self.summation_type = dose_summation_type()
		self.frame_of_ref_uid = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['dose'] = self.dose.expand_data()
		data['number_frames'] = self.number_frames
		data['frame_spacing'] = self.frame_spacing
		data['frame_increment_pointer'] = self.frame_increment_pointer
		data['study'] = self.study.expand_data()
		data['type'] = self.type.expand_data()
		data['summation_type'] = self.summation_type.expand_data()
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'dose':
					self.dose.from_json(v)
				elif k == 'study':
					self.study.from_json(v)
				elif k == 'type':
					self.type.from_json(v)
				elif k == 'summation_type':
					self.summation_type.from_json(v)
				else:
					setattr(self, k, v)

class rt_dose_reference(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['number'] = self.number
		data['uid'] = self.uid
		data['structure_type'] = self.structure_type
		data['description'] = self.description
		data['type'] = self.type
		data['delivery_max_dose'] = self.delivery_max_dose
		data['target_rx_dose'] = self.target_rx_dose
		data['target_min_dose'] = self.target_min_dose
		data['target_max_dose'] = self.target_max_dose
		data['point_coordinates'] = self.point_coordinates
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_fraction(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.number = 0.0 
		self.number_planned_fractions = 0.0 
		self.number_beams = 0.0 
		self.referenced_beam_numbers = [] 
		self.referenced_beam_dose = [] 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['number'] = self.number
		data['number_planned_fractions'] = self.number_planned_fractions
		data['number_beams'] = self.number_beams
		data['referenced_beam_numbers'] = self.referenced_beam_numbers
		data['referenced_beam_dose'] = self.referenced_beam_dose
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_image_2d(object):

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

	def expand_data(self):
		data = {}
		data['img'] = self.img.expand_data()
		data['bits_allocated'] = self.bits_allocated
		data['bits_stored'] = self.bits_stored
		data['high_bit'] = self.high_bit
		data['rescale_intercept'] = self.rescale_intercept
		data['rescale_slope'] = self.rescale_slope
		data['cols'] = self.cols
		data['rows'] = self.rows
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
		self.img = image_3d()
		self.bits_allocated = 0.0 
		self.bits_stored = 0.0 
		self.high_bit = 0.0 
		self.rescale_intercept = 0.0 
		self.rescale_slope = 0.0 
		self.cols = 0.0 
		self.rows = 0.0 

	def expand_data(self):
		data = {}
		data['img'] = self.img.expand_data()
		data['bits_allocated'] = self.bits_allocated
		data['bits_stored'] = self.bits_stored
		data['high_bit'] = self.high_bit
		data['rescale_intercept'] = self.rescale_intercept
		data['rescale_slope'] = self.rescale_slope
		data['cols'] = self.cols
		data['rows'] = self.rows
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
		# DV
		# DI
		# DF
		# WSD

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

	def expand_data(self):
		data = {}
		data['content'] = self.content.expand_data()
		data['axis'] = self.axis
		data['position'] = self.position
		data['thickness'] = self.thickness
		data['instance_number'] = self.instance_number
		data['samples_per_pixel'] = self.samples_per_pixel
		data['pixel_rep'] = self.pixel_rep
		data['pixel_spacing'] = self.pixel_spacing
		data['image_position'] = self.image_position
		data['image_orientation'] = self.image_orientation
		data['photometric_interpretation'] = self.photometric_interpretation
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

	def expand_data(self):
		data = {}
		data['content'] = self.content.expand_data()
		data['axis'] = self.axis
		data['position'] = self.position
		data['thickness'] = self.thickness
		data['instance_number'] = self.instance_number
		data['samples_per_pixel'] = self.samples_per_pixel
		data['pixel_rep'] = self.pixel_rep
		data['pixel_spacing'] = self.pixel_spacing
		data['image_position'] = self.image_position
		data['image_orientation'] = self.image_orientation
		data['photometric_interpretation'] = self.photometric_interpretation
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
		# DRR
		# PORTAL
		# SIMULATOR
		# RADIOGRAPH
		# BLANK
		# FLUENCE

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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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
		self.beam_scan_mode = rt_ion_beam_scan_mode()
		self.radiation_type = rt_radiation_type()
		self.referenced_patient_setup = 0.0 
		self.referenced_tolerance_table = 0.0 
		self.virtual_sad = [] 
		self.final_meterset_weight = 0.0 
		self.snouts = [] 
		self.block = rt_ion_block()
		self.degraders = [] 
		self.control_points = [] 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['beam_number'] = self.beam_number
		data['name'] = self.name
		data['description'] = self.description
		data['treatment_machine'] = self.treatment_machine
		data['primary_dosimeter_unit'] = self.primary_dosimeter_unit
		data['treatment_delivery_type'] = self.treatment_delivery_type
		data['beam_type'] = self.beam_type.expand_data()
		data['beam_scan_mode'] = self.beam_scan_mode.expand_data()
		data['radiation_type'] = self.radiation_type.expand_data()
		data['referenced_patient_setup'] = self.referenced_patient_setup
		data['referenced_tolerance_table'] = self.referenced_tolerance_table
		data['virtual_sad'] = self.virtual_sad
		data['final_meterset_weight'] = self.final_meterset_weight
		snout = []
		for x in self.snouts:
			s = rt_snout()
			s.from_json(x)
			snout.append(s.expand_data())
		data['snouts'] = snout
		data['block'] = self.block.expand_data()
		degrader = []
		for x in self.degraders:
			s = rt_ion_rangecompensator()
			s.from_json(x)
			degrader.append(s.expand_data())
		data['degraders'] = degrader
		control_point = []
		for x in self.control_points:
			s = rt_control_point()
			s.from_json(x)
			control_point.append(s.expand_data())
		data['control_points'] = control_point
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'beam_type':
					self.beam_type.from_json(v)
				elif k == 'beam_scan_mode':
					self.beam_scan_mode.from_json(v)
				elif k == 'radiation_type':
					self.radiation_type.from_json(v)
				elif k == 'block':
					self.block.from_json(v)
				else:
					setattr(self, k, v)

class rt_ion_beam_scan_mode(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# NONE
		# UNIFORM
		# MODULATED

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
		# STATIC
		# DYNAMIC

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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.name = "" 
		self.description = "" 
		self.material = "" 
		self.number = 0.0 
		self.divergent = False 
		self.downstream_edge = 0.0 
		self.thickness = 0.0 
		self.position = rt_mounting_position()
		self.block_type = rt_ion_block_type()
		self.data = polyset()

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['name'] = self.name
		data['description'] = self.description
		data['material'] = self.material
		data['number'] = self.number
		data['divergent'] = self.divergent
		data['downstream_edge'] = self.downstream_edge
		data['thickness'] = self.thickness
		data['position'] = self.position.expand_data()
		data['block_type'] = self.block_type.expand_data()
		data['data'] = self.data.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'position':
					self.position.from_json(v)
				elif k == 'block_type':
					self.block_type.from_json(v)
				elif k == 'data':
					self.data.from_json(v)
				else:
					setattr(self, k, v)

class rt_ion_block_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# APERTURE
		# SHIELDING

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class rt_ion_rangecompensator(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['name'] = self.name
		data['number'] = self.number
		data['material'] = self.material
		data['divergent'] = self.divergent
		data['mounting_position'] = self.mounting_position.expand_data()
		data['downstream_edge'] = self.downstream_edge
		data['column_offset'] = self.column_offset
		data['relative_stopping_power'] = self.relative_stopping_power
		data['position'] = self.position
		data['pixelSpacing'] = self.pixelSpacing
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
		# PATIENT_SIDE
		# SOURCE_SIDE
		# DOUBLE_SIDED

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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.setup_number = 0.0 
		self.position = patient_position_type()
		self.setup_description = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['setup_number'] = self.setup_number
		data['position'] = self.position.expand_data()
		data['setup_description'] = self.setup_description
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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['plan_date'] = self.plan_date
		data['name'] = self.name
		data['description'] = self.description
		data['label'] = self.label
		data['uid'] = self.uid
		data['geometry'] = self.geometry
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		data['patient_data'] = self.patient_data.expand_data()
		data['study'] = self.study.expand_data()
		dos = []
		for x in self.dose:
			s = rt_dose_reference()
			s.from_json(x)
			dos.append(s.expand_data())
		data['dose'] = dos
		fraction = []
		for x in self.fractions:
			s = rt_fraction()
			s.from_json(x)
			fraction.append(s.expand_data())
		data['fractions'] = fraction
		ref_bea = []
		for x in self.ref_beam:
			s = rt_ref_beam()
			s.from_json(x)
			ref_bea.append(s.expand_data())
		data['ref_beam'] = ref_bea
		tolerance_tabl = []
		for x in self.tolerance_table:
			s = rt_tolerance_table()
			s.from_json(x)
			tolerance_tabl.append(s.expand_data())
		data['tolerance_table'] = tolerance_tabl
		patient_setup = []
		for x in self.patient_setups:
			s = rt_patient_setup()
			s.from_json(x)
			patient_setup.append(s.expand_data())
		data['patient_setups'] = patient_setup
		beam = []
		for x in self.beams:
			s = rt_ion_beam()
			s.from_json(x)
			beam.append(s.expand_data())
		data['beams'] = beam
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_data':
					self.patient_data.from_json(v)
				elif k == 'study':
					self.study.from_json(v)
				else:
					setattr(self, k, v)

class rt_radiation_type(object):

	#Initialize
	def __init__(self):
		self.name = ""

		# Acceptable enum strings for name:
		# PROTON
		# PHOTON
		# ELECTRON
		# NEUTRON

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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.beam_dose = 0.0 
		self.beam_number = 0.0 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['beam_dose'] = self.beam_dose
		data['beam_number'] = self.beam_number
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_snout(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.id = "" 
		self.accessoryCode = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['id'] = self.id
		data['accessoryCode'] = self.accessoryCode
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_structure(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['name'] = self.name
		data['description'] = self.description
		data['number'] = self.number
		data['color'] = self.color.expand_data()
		data['type'] = self.type.expand_data()
		data['point'] = self.point
		data['volume'] = self.volume.expand_data()
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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['name'] = self.name
		data['description'] = self.description
		structure = []
		for x in self.structures:
			s = rt_structure()
			s.from_json(x)
			structure.append(s.expand_data())
		data['structures'] = structure
		data['patient_position'] = self.patient_position.expand_data()
		contour_image_sequenc = []
		for x in self.contour_image_sequence:
			s = dicom_item()
			s.from_json(x)
			contour_image_sequenc.append(s.expand_data())
		data['contour_image_sequence'] = contour_image_sequenc
		data['frame_of_ref_uid'] = self.frame_of_ref_uid
		data['study'] = self.study.expand_data()
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				if k == 'patient_position':
					self.patient_position.from_json(v)
				elif k == 'study':
					self.study.from_json(v)
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
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
		self.series_uid = "" 
		self.elements = [] 
		self.sequences = [] 
		self.study_date = "" 
		self.description = "" 
		self.physician_name = "" 
		self.id = "" 
		self.accession_number = "" 

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['study_date'] = self.study_date
		data['description'] = self.description
		data['physician_name'] = self.physician_name
		data['id'] = self.id
		data['accession_number'] = self.accession_number
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class rt_tolerance_table(object):

	#Initialize
	def __init__(self):
		self.class_uid = "" 
		self.instance_uid = "" 
		self.ref_class_uid = "" 
		self.ref_instance_uid = "" 
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

	def expand_data(self):
		data = {}
		data['class_uid'] = self.class_uid
		data['instance_uid'] = self.instance_uid
		data['ref_class_uid'] = self.ref_class_uid
		data['ref_instance_uid'] = self.ref_instance_uid
		data['series_uid'] = self.series_uid
		element = []
		for x in self.elements:
			s = dicom_element()
			s.from_json(x)
			element.append(s.expand_data())
		data['elements'] = element
		sequence = []
		for x in self.sequences:
			s = dicom_sequence()
			s.from_json(x)
			sequence.append(s.expand_data())
		data['sequences'] = sequence
		data['number'] = self.number
		data['gantry_angle'] = self.gantry_angle
		data['beam_limiting_angle'] = self.beam_limiting_angle
		data['patient_support_angle'] = self.patient_support_angle
		data['table_top_vert_position'] = self.table_top_vert_position
		data['table_top_long_position'] = self.table_top_long_position
		data['table_top_lat_position'] = self.table_top_lat_position
		data['label'] = self.label
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
		# difference
		# xor

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
		self.view_axis = 0.0 

	def expand_data(self):
		data = {}
		data['view_axis'] = self.view_axis
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class sliced_3d_structure_set_view_state(object):

	#Initialize
	def __init__(self):
		self.view_axis = 0.0 

	def expand_data(self):
		data = {}
		data['view_axis'] = self.view_axis
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class sliced_3d_structure_view_state(object):

	#Initialize
	def __init__(self):
		self.view_axis = 0.0 

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

class sobp_calculation_layer(object):

	#Initialize
	def __init__(self):
		self.depth_dose_curve = interpolated_function()
		self.initial_range = 0.0 
		self.initial_sigma = 0.0 
		self.weight = 0.0 
		self.sad = 0.0 
		self.pdd_shift = 0.0 

	def expand_data(self):
		data = {}
		data['depth_dose_curve'] = self.depth_dose_curve.expand_data()
		data['initial_range'] = self.initial_range
		data['initial_sigma'] = self.initial_sigma
		data['weight'] = self.weight
		data['sad'] = self.sad
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
		self.energy = 0.0 
		self.position = [] 

	def expand_data(self):
		data = {}
		data['energy'] = self.energy
		data['position'] = self.position
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
		self.n_samples = 0.0 

	def expand_data(self):
		data = {}
		data['n_samples'] = self.n_samples
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
		self.position = 0.0 
		self.thickness = 0.0 
		self.region = polyset()

	def expand_data(self):
		data = {}
		data['position'] = self.position
		data['thickness'] = self.thickness
		data['region'] = self.region.expand_data()
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
		# task_completed
		# value_produced
		# task_canceled

	def expand_data(self):
		return self.name

	def from_json(self, jdict):
		if hasattr(jdict, 'items'):
			for k, v in jdict.items():
				if hasattr(self,k):
					setattr(self, k, v)
		else:
			self.name = jdict;

class triangle_mesh(object):

	#Initialize
	def __init__(self):
		blob = blob_type()
		self.vertices = blob.toStr()
		blob = blob_type()
		self.faces = blob.toStr()

	def expand_data(self):
		data = {}
		data['vertices'] = parse_bytes_3d(base64.b64decode(self.vertices['blob']))
		data['faces'] = parse_bytes_3i(base64.b64decode(self.faces['blob']))
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class triangle_mesh_with_normals(object):

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

	def expand_data(self):
		data = {}
		data['vertex_positions'] = parse_bytes_3d(base64.b64decode(self.vertex_positions['blob']))
		data['vertex_normals'] = parse_bytes_3d(base64.b64decode(self.vertex_normals['blob']))
		data['face_position_indices'] = parse_bytes_3i(base64.b64decode(self.face_position_indices['blob']))
		data['face_normal_indices'] = parse_bytes_3i(base64.b64decode(self.face_normal_indices['blob']))
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
		# halfway
		# open

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
		self.pixels = [] 
		self.origin = [] 
		self.axes = [] 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['pixels'] = self.pixels
		data['origin'] = self.origin
		data['axes'] = self.axes
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

class unboxed_image_3d(object):

	#Initialize
	def __init__(self):
		self.size = [] 
		self.pixels = [] 
		self.origin = [] 
		self.axes = [] 

	def expand_data(self):
		data = {}
		data['size'] = self.size
		data['pixels'] = self.pixels
		data['origin'] = self.origin
		data['axes'] = self.axes
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
		self.index = 0.0 
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
		self.energy = 0.0 
		self.position = [] 
		self.fluence = 0.0 

	def expand_data(self):
		data = {}
		data['energy'] = self.energy
		data['position'] = self.position
		data['fluence'] = self.fluence
		return data

	def from_json(self, jdict):
		for k, v in jdict.items():
			if hasattr(self,k):
				setattr(self, k, v)

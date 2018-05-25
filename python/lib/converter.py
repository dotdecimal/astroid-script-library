# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:	Travis DeMint
# Date:		12/15/2015
# Desc:		Provides conversions to images other than doubles


import sys
sys.path.append("lib")
import rt_types as rt_types
import base64


class image_2i(object):
	#Initialize
	def __init__(self):
		self.type_info = rt_types.variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = rt_types.linear_function()
		self.units = "" 
		blob = rt_types.blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = rt_types.parse_bytes_i(base64.b64decode(self.pixels['blob']))
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

class image_3i(object):
	#Initialize
	def __init__(self):
		self.type_info = rt_types.variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = rt_types.linear_function()
		self.units = "" 
		blob = rt_types.blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = rt_types.parse_bytes_i(base64.b64decode(self.pixels['blob']))
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

class image_2u(object):
	#Initialize
	def __init__(self):
		self.type_info = rt_types.variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = rt_types.linear_function()
		self.units = "" 
		blob = rt_types.blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = rt_types.parse_bytes_u(base64.b64decode(self.pixels['blob']))
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

class image_3u(object):
	#Initialize
	def __init__(self):
		self.type_info = rt_types.variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = rt_types.linear_function()
		self.units = "" 
		blob = rt_types.blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = rt_types.parse_bytes_u(base64.b64decode(self.pixels['blob']))
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
		self.type_info = rt_types.variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = rt_types.linear_function()
		self.units = "" 
		blob = rt_types.blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = rt_types.parse_bytes_f(base64.b64decode(self.pixels['blob']))
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
		self.type_info = rt_types.variant_type_info()
		self.size = [] 
		self.origin = [] 
		self.axes = [] 
		self.value_mapping = rt_types.linear_function()
		self.units = "" 
		blob = rt_types.blob_type()
		self.pixels = blob.toStr()

	def expand_data(self):
		data = {}
		data['type_info'] = self.type_info.expand_data()
		data['size'] = self.size
		data['origin'] = self.origin
		data['axes'] = self.axes
		data['value_mapping'] = self.value_mapping.expand_data()
		data['units'] = self.units
		data['pixels'] = rt_types.parse_bytes_f(base64.b64decode(self.pixels['blob']))
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
# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:    Travis DeMint & Daniel Patenaude
# Date:        08/27/2018
# Desc:        Provides access to type usage for all types
# Dosimetry Version:        2.1.1-2

from collections import OrderedDict
import base64
import struct as st
import sys

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

def parse_byte_us(buf, offset=0):
    tmp = st.unpack_from('H',buf,offset)
    return tmp[0]

def parse_byte_u(buf, offset=0):
    tmp = st.unpack_from('I',buf,offset)
    return tmp[0]

def parse_byte_i(buf, offset=0):
    tmp = st.unpack_from('i',buf,offset)
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

class adaptive_grid(object):

    #Initialize
    def __init__(self):
        self.bounds = box_3d()
        blob = blob_type()
        self.voxels = blob.toStr()
        blob = blob_type()
        self.volumes = blob.toStr()
        self.extents = box_3d()

    def expand_data(self):
        data = {}
        data['bounds'] = self.bounds.expand_data()
        adaptivegridvoxel = adaptive_grid_voxel()
        data['voxels'] = parse_array(adaptivegridvoxel, base64.b64decode(self.voxels['blob']))
        data['volumes'] = parse_bytes_u(base64.b64decode(self.volumes['blob']))
        data['extents'] = self.extents.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'bounds':
                    self.bounds.from_json(v)
                elif k == 'extents':
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
        self.surface_count = 0
        self.index = 0
        self.volume_offset = 0
        self.inside_count = 0

    def parse_self(self, buf, offset):
        self.index = parse_byte_ul(buf, offset)
        self.surface_count = parse_byte_us(buf, offset + 8)
        self.volume_offset = parse_byte_u(buf, offset + 10)
        self.inside_count = parse_byte_us(buf, offset + 14)

        return self.expand_data()

    def get_offset(self):
        return 16

    def expand_data(self):
        data = {}
        data['surface_count'] = self.surface_count
        data['index'] = self.index
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
        self.mill_radius = 0.0
        self.corner_planes = []
        self.overrides = []
        self.targets = []
        self.centerlines = []
        self.organs = []
        self.target_margin = 0.0
        self.half_planes = []

    def expand_data(self):
        data = {}
        data['downstream_edge'] = self.downstream_edge
        data['mill_radius'] = self.mill_radius
        corner_plane = []
        for x in self.corner_planes:
            s = aperture_corner_plane()
            s.from_json(x)
            corner_plane.append(s.expand_data())
        data['corner_planes'] = corner_plane
        override = []
        for x in self.overrides:
            s = aperture_manual_override()
            s.from_json(x)
            override.append(s.expand_data())
        data['overrides'] = override
        target = []
        for x in self.targets:
            s = triangle_mesh()
            s.from_json(x)
            target.append(s.expand_data())
        data['targets'] = target
        centerline = []
        for x in self.centerlines:
            s = aperture_centerline()
            s.from_json(x)
            centerline.append(s.expand_data())
        data['centerlines'] = centerline
        organ = []
        for x in self.organs:
            s = aperture_organ()
            s.from_json(x)
            organ.append(s.expand_data())
        data['organs'] = organ
        data['target_margin'] = self.target_margin
        half_plane = []
        for x in self.half_planes:
            s = aperture_half_plane()
            s.from_json(x)
            half_plane.append(s.expand_data())
        data['half_planes'] = half_plane
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
        self.margin = 0.0
        self.structure = triangle_mesh()
        self.occlude_by_target = False

    def expand_data(self):
        data = {}
        data['margin'] = self.margin
        data['structure'] = self.structure.expand_data()
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

class api_array_info(object):

    #Initialize
    def __init__(self):
        self.size = 0
        self.element_schema = api_type_info()

    def expand_data(self):
        data = {}
        data['size'] = self.size
        data['element_schema'] = self.element_schema.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'element_schema':
                    self.element_schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_blob_type(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_boolean_type(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_datetime_type(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_dynamic_type(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_enum_info(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_enum_value_info(object):

    #Initialize
    def __init__(self):
        self.description = ""

    def expand_data(self):
        data = {}
        data['description'] = self.description
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_float_type(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_function_info(object):

    #Initialize
    def __init__(self):
        self.execution_class = ""
        self.schema = api_type_info()
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['execution_class'] = self.execution_class
        data['schema'] = self.schema.expand_data()
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_function_parameter_info(object):

    #Initialize
    def __init__(self):
        self.schema = api_type_info()
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['schema'] = self.schema.expand_data()
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_function_result_info(object):

    #Initialize
    def __init__(self):
        self.schema = api_type_info()
        self.description = ""

    def expand_data(self):
        data = {}
        data['schema'] = self.schema.expand_data()
        data['description'] = self.description
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_function_type_info(object):

    #Initialize
    def __init__(self):
        self.returns = api_function_result_info()
        self.parameters = []

    def expand_data(self):
        data = {}
        data['returns'] = self.returns.expand_data()
        parameter = []
        for x in self.parameters:
            s = api_function_parameter_info()
            s.from_json(x)
            parameter.append(s.expand_data())
        data['parameters'] = parameter
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'returns':
                    self.returns.from_json(v)
                else:
                    setattr(self, k, v)

class api_function_upgrade_type_info(object):

    #Initialize
    def __init__(self):
        self.function = ""
        self.version = ""
        self.type = ""

    def expand_data(self):
        data = {}
        data['function'] = self.function
        data['version'] = self.version
        data['type'] = self.type
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_integer_type(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_map_info(object):

    #Initialize
    def __init__(self):
        self.key_schema = api_type_info()
        self.value_schema = api_type_info()

    def expand_data(self):
        data = {}
        data['key_schema'] = self.key_schema.expand_data()
        data['value_schema'] = self.value_schema.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'key_schema':
                    self.key_schema.from_json(v)
                elif k == 'value_schema':
                    self.value_schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_named_type_implementation_info(object):

    #Initialize
    def __init__(self):
        self.upgrade = upgrade_type()
        self.schema = api_type_info()
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['upgrade'] = self.upgrade.expand_data()
        data['schema'] = self.schema.expand_data()
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'upgrade':
                    self.upgrade.from_json(v)
                elif k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_named_type_info(object):

    #Initialize
    def __init__(self):
        self.schema = api_type_info()
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['schema'] = self.schema.expand_data()
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_named_type_reference(object):

    #Initialize
    def __init__(self):
        self.app = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['app'] = self.app
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_nil_type(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_record_info(object):

    #Initialize
    def __init__(self):
        self.schema = api_record_named_type_schema()

    def expand_data(self):
        data = {}
        data['schema'] = self.schema.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_record_named_type_info(object):

    #Initialize
    def __init__(self):
        self.app = ""
        self.account = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['app'] = self.app
        data['account'] = self.account
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_record_named_type_schema(object):

    #Initialize
    def __init__(self):
        self.named_type = api_record_named_type_info()

    def expand_data(self):
        data = {}
        data['named_type'] = self.named_type.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'named_type':
                    self.named_type.from_json(v)
                else:
                    setattr(self, k, v)

class api_record_type_info(object):

    #Initialize
    def __init__(self):
        self.schema = api_type_info()

    def expand_data(self):
        data = {}
        data['schema'] = self.schema.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_string_type(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_structure_field_info(object):

    #Initialize
    def __init__(self):
        self.omissible = False
        self.schema = api_type_info()
        self.description = ""

    def expand_data(self):
        data = {}
        data['omissible'] = self.omissible
        data['schema'] = self.schema.expand_data()
        data['description'] = self.description
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_structure_info(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_type_info(object):

    #Initialize
    def __init__(self):
        self.datetime_type = api_datetime_type.toStr()
        self.boolean_type = api_boolean_type.toStr()
        self.dynamic_type = api_dynamic_type.toStr()
        self.record_type = api_record_info.toStr()
        self.union_type = api_union_info.toStr()
        self.nil_type = api_nil_type.toStr()
        self.function_type = api_function_type_info.toStr()
        self.reference_type = api_type_info.toStr()
        self.optional_type = api_type_info.toStr()
        self.float_type = api_float_type.toStr()
        self.integer_type = api_integer_type.toStr()
        self.structure_type = api_structure_info.toStr()
        self.string_type = api_string_type.toStr()
        self.blob_type = api_blob_type.toStr()
        self.enum_type = api_enum_info.toStr()
        self.named_type = api_named_type_reference.toStr()
        self.array_type = api_array_info.toStr()
        self.map_type = api_map_info.toStr()

class api_union_info(object):

    #Initialize
    def __init__(self):
        data = {}

    def expand_data(self):
        data = {}
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class api_union_member_info(object):

    #Initialize
    def __init__(self):
        self.schema = api_type_info()
        self.description = ""

    def expand_data(self):
        data = {}
        data['schema'] = self.schema.expand_data()
        data['description'] = self.description
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class api_upgrade_function_info(object):

    #Initialize
    def __init__(self):
        self.function = ""
        self.version = ""
        self.type = ""

    def expand_data(self):
        data = {}
        data['function'] = self.function
        data['version'] = self.version
        data['type'] = self.type
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class approval_status(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # rejected
        # approved
        # unapproved

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
        # multiplication
        # subtraction
        # division
        # addition

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

class beam_model(object):

    #Initialize
    def __init__(self):
        self.data = radiation_machine_data()
        self.name = ""

    def expand_data(self):
        data = {}
        data['data'] = self.data.expand_data()
        data['name'] = self.name
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
        self.geometry = beam_geometry()
        self.range = 0.0
        self.beam_index = 0
        self.field = box_2d()
        self.ssd = 0.0
        self.bixel_grid = regular_grid_2d()

    def expand_data(self):
        data = {}
        data['geometry'] = self.geometry.expand_data()
        data['range'] = self.range
        data['beam_index'] = self.beam_index
        data['field'] = self.field.expand_data()
        data['ssd'] = self.ssd
        data['bixel_grid'] = self.bixel_grid.expand_data()
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
        blob = blob_type()
        self.counts = blob.toStr()
        self.bounds = box_3d()
        blob = blob_type()
        self.offsets = blob.toStr()
        blob = blob_type()
        self.bins = blob.toStr()
        self.grid_size = []

    def expand_data(self):
        data = {}
        data['counts'] = parse_bytes_u(base64.b64decode(self.counts['blob']))
        data['bounds'] = self.bounds.expand_data()
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
        self.alphabeta = 0.0
        self.gamma50 = 0.0
        self.cutoff = 0.0
        self.d50 = 0.0
        self.a = 0.0

    def expand_data(self):
        data = {}
        data['alphabeta'] = self.alphabeta
        data['gamma50'] = self.gamma50
        data['cutoff'] = self.cutoff
        data['d50'] = self.d50
        data['a'] = self.a
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

class calculation_array_request(object):

    #Initialize
    def __init__(self):
        self.item_schema = api_type_info()
        self.items = []

    def expand_data(self):
        data = {}
        data['item_schema'] = self.item_schema.expand_data()
        item = []
        for x in self.items:
            s = calculation_request()
            s.from_json(x)
            item.append(s.expand_data())
        data['items'] = item
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'item_schema':
                    self.item_schema.from_json(v)
                else:
                    setattr(self, k, v)

class calculation_object_request(object):

    #Initialize
    def __init__(self):
        data = {}
        self.schema = api_type_info()

    def expand_data(self):
        data = {}
        data['schema'] = self.schema.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'schema':
                    self.schema.from_json(v)
                else:
                    setattr(self, k, v)

class calculation_property_request(object):

    #Initialize
    def __init__(self):
        self.object = calculation_request()
        self.schema = api_type_info()
        self.field = calculation_request()

    def expand_data(self):
        data = {}
        data['object'] = self.object.expand_data()
        data['schema'] = self.schema.expand_data()
        data['field'] = self.field.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'object':
                    self.object.from_json(v)
                elif k == 'schema':
                    self.schema.from_json(v)
                elif k == 'field':
                    self.field.from_json(v)
                else:
                    setattr(self, k, v)

class calculation_request(object):

    #Initialize
    def __init__(self):
        self.function = function_application.toStr()
        self.variable = ""
        self.object = calculation_object_request.toStr()
        self.property = calculation_property_request.toStr()
        self.reference = ""
        self.array = calculation_array_request.toStr()
        self.meta = meta_calculation_request.toStr()
        self.let = let_calculation_request.toStr()

class channel_type(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # uint16
        # uint32
        # int16
        # int64
        # int8
        # int32
        # float
        # double
        # uint8
        # uint64

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

class context_based_calculation_request(object):

    #Initialize
    def __init__(self):
        self.context_id = ""
        self.request = rgba8()

    def expand_data(self):
        data = {}
        data['context_id'] = self.context_id
        data['request'] = self.request.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class ct_image(object):

    #Initialize
    def __init__(self):
        self.image_set = ct_image_set.toStr()
        self.image_slices = []

class ct_image_data(object):

    #Initialize
    def __init__(self):
        self.pixel_ref = ""
        self.pixel = pixel_blob.toStr()
        self.img = image_2d.toStr()

class ct_image_set(object):

    #Initialize
    def __init__(self):
        self.image = image_3d()
        self.frame_of_ref_uid = ""
        self.study_data = dicom_study()
        self.equipment_data = dicom_equipment()
        self.position_reference_indicator = ""
        self.patient_data = patient()
        self.sop_data = dicom_sop_common()
        self.series = dicom_general_series()

    def expand_data(self):
        data = {}
        data['image'] = self.image.expand_data()
        data['frame_of_ref_uid'] = self.frame_of_ref_uid
        data['study_data'] = self.study_data.expand_data()
        data['equipment_data'] = self.equipment_data.expand_data()
        data['position_reference_indicator'] = self.position_reference_indicator
        data['patient_data'] = self.patient_data.expand_data()
        data['sop_data'] = self.sop_data.expand_data()
        data['series'] = self.series.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'image':
                    self.image.from_json(v)
                elif k == 'study_data':
                    self.study_data.from_json(v)
                elif k == 'equipment_data':
                    self.equipment_data.from_json(v)
                elif k == 'patient_data':
                    self.patient_data.from_json(v)
                elif k == 'sop_data':
                    self.sop_data.from_json(v)
                elif k == 'series':
                    self.series.from_json(v)
                else:
                    setattr(self, k, v)

class ct_image_slice(object):

    #Initialize
    def __init__(self):
        self.frame_of_ref_uid = ""
        self.study_data = dicom_study()
        self.equipment_data = dicom_equipment()
        self.position_reference_indicator = ""
        self.sop_data = dicom_sop_common()
        self.patient_data = patient()
        self.referenced_ids = []
        self.series = dicom_general_series()
        self.slice = ct_image_slice_content()

    def expand_data(self):
        data = {}
        data['frame_of_ref_uid'] = self.frame_of_ref_uid
        data['study_data'] = self.study_data.expand_data()
        data['equipment_data'] = self.equipment_data.expand_data()
        data['position_reference_indicator'] = self.position_reference_indicator
        data['sop_data'] = self.sop_data.expand_data()
        data['patient_data'] = self.patient_data.expand_data()
        referenced_id = []
        for x in self.referenced_ids:
            s = ref_dicom_item()
            s.from_json(x)
            referenced_id.append(s.expand_data())
        data['referenced_ids'] = referenced_id
        data['series'] = self.series.expand_data()
        data['slice'] = self.slice.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'study_data':
                    self.study_data.from_json(v)
                elif k == 'equipment_data':
                    self.equipment_data.from_json(v)
                elif k == 'sop_data':
                    self.sop_data.from_json(v)
                elif k == 'patient_data':
                    self.patient_data.from_json(v)
                elif k == 'series':
                    self.series.from_json(v)
                elif k == 'slice':
                    self.slice.from_json(v)
                else:
                    setattr(self, k, v)

class ct_image_slice_content(object):

    #Initialize
    def __init__(self):
        self.axis = 0
        self.image_position = []
        self.content = ct_image_slice_data()
        self.thickness = 0.0
        self.image_orientation = []
        self.samples_per_pixel = 0
        self.position = 0.0
        self.pixel_spacing = []
        self.instance_number = 0
        self.pixel_rep = 0
        self.photometric_interpretation = ""

    def expand_data(self):
        data = {}
        data['axis'] = self.axis
        data['image_position'] = self.image_position
        data['content'] = self.content.expand_data()
        data['thickness'] = self.thickness
        data['image_orientation'] = self.image_orientation
        data['samples_per_pixel'] = self.samples_per_pixel
        data['position'] = self.position
        data['pixel_spacing'] = self.pixel_spacing
        data['instance_number'] = self.instance_number
        data['pixel_rep'] = self.pixel_rep
        data['photometric_interpretation'] = self.photometric_interpretation
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
        self.high_bit = 0
        self.bits_allocated = 0
        self.img = ct_image_data()
        self.bits_stored = 0
        self.cols = 0
        self.rows = 0
        self.rescale_intercept = 0.0
        self.rescale_slope = 0.0
        self.kvp = 0.0

    def expand_data(self):
        data = {}
        data['high_bit'] = self.high_bit
        data['bits_allocated'] = self.bits_allocated
        data['img'] = self.img.expand_data()
        data['bits_stored'] = self.bits_stored
        data['cols'] = self.cols
        data['rows'] = self.rows
        data['rescale_intercept'] = self.rescale_intercept
        data['rescale_slope'] = self.rescale_slope
        data['kvp'] = self.kvp
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'img':
                    self.img.from_json(v)
                else:
                    setattr(self, k, v)

class degrader_geometry(object):

    #Initialize
    def __init__(self):
        self.shape = degrader_shape()
        self.scale_factor = 0.0
        self.downstream_edge = 0.0
        self.thickness_units = ""

    def expand_data(self):
        data = {}
        data['shape'] = self.shape.expand_data()
        data['scale_factor'] = self.scale_factor
        data['downstream_edge'] = self.downstream_edge
        data['thickness_units'] = self.thickness_units
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
        self.rc = rc_geometry.toStr()
        self.shifter = shifter_geometry.toStr()
        self.block = block_geometry.toStr()

class department(object):

    #Initialize
    def __init__(self):
        data = {}
        data = {}
        data = {}
        data = {}
        data = {}
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class device_mounting_info(object):

    #Initialize
    def __init__(self):
        self.mounting_side = mounting_position_side()
        self.position = 0.0

    def expand_data(self):
        data = {}
        data['mounting_side'] = self.mounting_side.expand_data()
        data['position'] = self.position
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'mounting_side':
                    self.mounting_side.from_json(v)
                else:
                    setattr(self, k, v)

class dicom_equipment(object):

    #Initialize
    def __init__(self):
        self.manufacturer = ""
        self.institution_name = ""

    def expand_data(self):
        data = {}
        data['manufacturer'] = self.manufacturer
        data['institution_name'] = self.institution_name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class dicom_file(object):

    #Initialize
    def __init__(self):
        self.frame_of_ref_uid = ""
        self.study_data = dicom_study()
        self.equipment_data = dicom_equipment()
        self.position_reference_indicator = ""
        self.patient_data = patient()
        self.sop_data = dicom_sop_common()

    def expand_data(self):
        data = {}
        data['frame_of_ref_uid'] = self.frame_of_ref_uid
        data['study_data'] = self.study_data.expand_data()
        data['equipment_data'] = self.equipment_data.expand_data()
        data['position_reference_indicator'] = self.position_reference_indicator
        data['patient_data'] = self.patient_data.expand_data()
        data['sop_data'] = self.sop_data.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'study_data':
                    self.study_data.from_json(v)
                elif k == 'equipment_data':
                    self.equipment_data.from_json(v)
                elif k == 'patient_data':
                    self.patient_data.from_json(v)
                elif k == 'sop_data':
                    self.sop_data.from_json(v)
                else:
                    setattr(self, k, v)

class dicom_general_series(object):

    #Initialize
    def __init__(self):
        self.patient_position = patient_position_type()
        self.instance_uid = ""
        self.modality = dicom_modality()
        self.number = 0
        self.description = ""

    def expand_data(self):
        data = {}
        data['patient_position'] = self.patient_position.expand_data()
        data['instance_uid'] = self.instance_uid
        data['modality'] = self.modality.expand_data()
        data['number'] = self.number
        data['description'] = self.description
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'patient_position':
                    self.patient_position.from_json(v)
                elif k == 'modality':
                    self.modality.from_json(v)
                else:
                    setattr(self, k, v)

class dicom_metadata(object):

    #Initialize
    def __init__(self):
        self.creation_date = ""
        self.modality = dicom_modality()
        self.patient_data = patient()
        self.series_uid = ""

    def expand_data(self):
        data = {}
        data['creation_date'] = self.creation_date
        data['modality'] = self.modality.expand_data()
        data['patient_data'] = self.patient_data.expand_data()
        data['series_uid'] = self.series_uid
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'modality':
                    self.modality.from_json(v)
                elif k == 'patient_data':
                    self.patient_data.from_json(v)
                else:
                    setattr(self, k, v)

class dicom_modality(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # ct
        # rtplan
        # rtstruct
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
        self.plan = rt_ion_plan.toStr()
        self.ct_image = ct_image.toStr()
        self.structure_set = rt_structure_set.toStr()
        self.dose = rt_dose.toStr()

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

class dicom_rt_series(object):

    #Initialize
    def __init__(self):
        self.modality = dicom_modality()
        self.number = 0
        self.description = ""
        self.instance_uid = ""

    def expand_data(self):
        data = {}
        data['modality'] = self.modality.expand_data()
        data['number'] = self.number
        data['description'] = self.description
        data['instance_uid'] = self.instance_uid
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'modality':
                    self.modality.from_json(v)
                else:
                    setattr(self, k, v)

class dicom_sop_common(object):

    #Initialize
    def __init__(self):
        self.class_uid = ""
        self.specific_char_set = ""
        self.instance_uid = ""

    def expand_data(self):
        data = {}
        data['class_uid'] = self.class_uid
        data['specific_char_set'] = self.specific_char_set
        data['instance_uid'] = self.instance_uid
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class dicom_study(object):

    #Initialize
    def __init__(self):
        self.accession_number = ""
        self.instance_uid = ""
        self.physician_name = ""
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['accession_number'] = self.accession_number
        data['instance_uid'] = self.instance_uid
        data['physician_name'] = self.physician_name
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class dij_entry(object):

    #Initialize
    def __init__(self):
        self.beamlet_index = 0
        self.dose = 0.0

    def parse_self(self, buf, offset):
        self.beamlet_index = parse_byte_u(buf, offset)
        self.dose = parse_byte_f(buf, offset + 4)
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
        data = {}
        self.n_points = 0
        self.n_beamlets = 0

    def expand_data(self):
        data = {}
        data['n_points'] = self.n_points
        data['n_beamlets'] = self.n_beamlets
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class display_state(object):

    #Initialize
    def __init__(self):
        self.focused_view = ""
        self.controls_expanded = False
        self.selected_composition = ""

    def expand_data(self):
        data = {}
        data['focused_view'] = self.focused_view
        data['controls_expanded'] = self.controls_expanded
        data['selected_composition'] = self.selected_composition
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class divergent_grid(object):

    #Initialize
    def __init__(self):
        self.isUniform = False
        self.source_dist = []
        blob = blob_type()
        self.data = blob.toStr()
        self.grid = regular_grid_2d()
        self.cax_length = 0.0
        blob = blob_type()
        self.rays = blob.toStr()
        self.z_position = 0.0

    def expand_data(self):
        data = {}
        data['isUniform'] = self.isUniform
        data['source_dist'] = self.source_dist
        data['data'] = parse_bytes_not_defined(base64.b64decode(self.data['blob']))
        data['grid'] = self.grid.expand_data()
        data['cax_length'] = self.cax_length
        data['rays'] = parse_bytes_not_defined(base64.b64decode(self.rays['blob']))
        data['z_position'] = self.z_position
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
        self.function = dose_objective()
        self.bound = 0.0

    def expand_data(self):
        data = {}
        data['function'] = self.function.expand_data()
        data['bound'] = self.bound
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'function':
                    self.function.from_json(v)
                else:
                    setattr(self, k, v)

class dose_objective(object):

    #Initialize
    def __init__(self):
        self.minimize_mean_squared_underdose = parameterized_dose_objective.toStr()
        self.maximize_min = simple_dose_objective.toStr()
        self.maximize_lower_cvar = parameterized_dose_objective.toStr()
        self.minimize_robust_cvar = robust_cvar_objective.toStr()
        self.minimize_eud_target = parameterized_dose_objective.toStr()
        self.minimize_mean_underdose = parameterized_dose_objective.toStr()
        self.minimize_weighted_sum = weighted_sum_objective.toStr()
        self.maximize_mean = simple_dose_objective.toStr()
        self.minimize_mean = simple_dose_objective.toStr()
        self.minimize_mean_squared_error = parameterized_dose_objective.toStr()
        self.minimize_robust_worst_case = robust_worst_case_objective.toStr()
        self.minimize_upper_cvar = parameterized_dose_objective.toStr()
        self.minimize_mean_overdose = parameterized_dose_objective.toStr()
        self.minimize_mean_squared_overdose = parameterized_dose_objective.toStr()
        self.minimize_max = simple_dose_objective.toStr()
        self.minimize_eud_normal_tissue = parameterized_dose_objective.toStr()

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
        # effective
        # physical
        # error

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
        self.id = ""
        self.bcm = []
        self.max_mod = 0.0
        self.min_range = 0.0
        self.mod_correction = []
        self.track_length = 0
        self.pristine_peak = irregularly_sampled_function()
        self.sdm = []
        self.name = ""
        self.penumbral_source_size = 0.0
        self.wts1 = 0.0
        self.max_range = 0.0
        self.source_size_on_track = 0.0
        self.steps = []

    def expand_data(self):
        data = {}
        data['id'] = self.id
        data['bcm'] = self.bcm
        data['max_mod'] = self.max_mod
        data['min_range'] = self.min_range
        data['mod_correction'] = self.mod_correction
        data['track_length'] = self.track_length
        data['pristine_peak'] = self.pristine_peak.expand_data()
        data['sdm'] = self.sdm
        data['name'] = self.name
        data['penumbral_source_size'] = self.penumbral_source_size
        data['wts1'] = self.wts1
        data['max_range'] = self.max_range
        data['source_size_on_track'] = self.source_size_on_track
        step = []
        for x in self.steps:
            s = double_scattering_step()
            s.from_json(x)
            step.append(s.expand_data())
        data['steps'] = step
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
        self.sizing = regular_grid_2d()
        self.image_z = 0.0
        self.parameters = []
        self.image_display_options = gray_image_display_options()

    def expand_data(self):
        data = {}
        data['sizing'] = self.sizing.expand_data()
        data['image_z'] = self.image_z
        parameter = []
        for x in self.parameters:
            s = drr_parameters()
            s.from_json(x)
            parameter.append(s.expand_data())
        data['parameters'] = parameter
        data['image_display_options'] = self.image_display_options.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'sizing':
                    self.sizing.from_json(v)
                elif k == 'image_display_options':
                    self.image_display_options.from_json(v)
                else:
                    setattr(self, k, v)

class drr_parameters(object):

    #Initialize
    def __init__(self):
        self.weight = 0.0
        self.max_z = 0.0
        self.min_z = 0.0
        self.max_value = 0.0
        self.min_value = 0.0

    def expand_data(self):
        data = {}
        data['weight'] = self.weight
        data['max_z'] = self.max_z
        data['min_z'] = self.min_z
        data['max_value'] = self.max_value
        data['min_value'] = self.min_value
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class dvh_view_state(object):

    #Initialize
    def __init__(self):
        self.absolute = False

    def expand_data(self):
        data = {}
        data['absolute'] = self.absolute
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class ellipse(object):

    #Initialize
    def __init__(self):
        self.center = []
        self.b = 0.0
        self.a = 0.0

    def expand_data(self):
        data = {}
        data['center'] = self.center
        data['b'] = self.b
        data['a'] = self.a
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class facility(object):

    #Initialize
    def __init__(self):
        data = {}
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['description'] = self.description
        data['name'] = self.name
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

class fixation_device(object):

    #Initialize
    def __init__(self):
        self.label = ""
        self.type = ""
        self.description = ""

    def expand_data(self):
        data = {}
        data['label'] = self.label
        data['type'] = self.type
        data['description'] = self.description
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class function_application(object):

    #Initialize
    def __init__(self):
        self.app = ""
        self.name = ""
        self.account = ""
        self.args = []
        self.level = 0

    def expand_data(self):
        data = {}
        data['app'] = self.app
        data['name'] = self.name
        data['account'] = self.account
        arg = []
        for x in self.args:
            s = calculation_request()
            s.from_json(x)
            arg.append(s.expand_data())
        data['args'] = arg
        data['level'] = self.level
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

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

class hu_rsp_curve(object):

    #Initialize
    def __init__(self):
        self.scan_energy = 0.0
        self.scanner_name = ""
        self.fov_range = min_max()
        self.samples = []

    def expand_data(self):
        data = {}
        data['scan_energy'] = self.scan_energy
        data['scanner_name'] = self.scanner_name
        data['fov_range'] = self.fov_range.expand_data()
        data['samples'] = self.samples
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'fov_range':
                    self.fov_range.from_json(v)
                else:
                    setattr(self, k, v)

class image_1d(object):

    #Initialize
    def __init__(self):
        self.size = []
        self.type_info = variant_type_info()
        self.units = ""
        self.axes = []
        self.origin = []
        blob = blob_type()
        self.pixels = blob.toStr()
        self.value_mapping = linear_function()

    def expand_data(self):
        data = {}
        data['size'] = self.size
        data['type_info'] = self.type_info.expand_data()
        data['units'] = self.units
        data['axes'] = self.axes
        data['origin'] = self.origin
        data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
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
        self.size = []
        self.type_info = variant_type_info()
        self.units = ""
        self.axes = []
        self.origin = []
        blob = blob_type()
        self.pixels = blob.toStr()
        self.value_mapping = linear_function()

    def expand_data(self):
        data = {}
        data['size'] = self.size
        data['type_info'] = self.type_info.expand_data()
        data['units'] = self.units
        data['axes'] = self.axes
        data['origin'] = self.origin
        data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
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
        self.size = []
        self.type_info = variant_type_info()
        self.units = ""
        self.axes = []
        self.origin = []
        blob = blob_type()
        self.pixels = blob.toStr()
        self.value_mapping = linear_function()

    def expand_data(self):
        data = {}
        data['size'] = self.size
        data['type_info'] = self.type_info.expand_data()
        data['units'] = self.units
        data['axes'] = self.axes
        data['origin'] = self.origin
        data['pixels'] = parse_bytes_d(base64.b64decode(self.pixels['blob']))
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
        self.slicing = []
        self.grid = regular_grid_1d()
        self.out_of_plane_info = regular_grid_1d()

    def expand_data(self):
        data = {}
        data['slicing'] = self.slicing
        data['grid'] = self.grid.expand_data()
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
        self.slicing = []
        self.grid = regular_grid_2d()
        self.out_of_plane_info = regular_grid_2d()

    def expand_data(self):
        data = {}
        data['slicing'] = self.slicing
        data['grid'] = self.grid.expand_data()
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
        self.slicing = []
        self.grid = regular_grid_3d()
        self.out_of_plane_info = regular_grid_3d()

    def expand_data(self):
        data = {}
        data['slicing'] = self.slicing
        data['grid'] = self.grid.expand_data()
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
        self.slicing = []
        self.grid = regular_grid_4d()
        self.out_of_plane_info = regular_grid_4d()

    def expand_data(self):
        data = {}
        data['slicing'] = self.slicing
        data['grid'] = self.grid.expand_data()
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
        self.x0 = 0.0
        self.x_spacing = 0.0
        self.outside_domain_policy = outside_domain_policy()
        blob = blob_type()
        self.samples = blob.toStr()

    def expand_data(self):
        data = {}
        data['x0'] = self.x0
        data['x_spacing'] = self.x_spacing
        data['outside_domain_policy'] = self.outside_domain_policy.expand_data()
        functionsample = function_sample()
        data['samples'] = parse_array(functionsample, base64.b64decode(self.samples['blob']))
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

class let_calculation_request(object):

    def __init__(self):
        data = {}

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

class line_stipple_type(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # none
        # dotted
        # dashed
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

class machine_expression(object):

    #Initialize
    def __init__(self):
        self.operation = arithmetic_operation.toStr()
        self.setting = ""

class machine_frame_of_reference(object):

    #Initialize
    def __init__(self):
        self.id = ""
        self.label = ""
        self.tags = []
        self.nested = []
        self.transformation = machine_transformation()

    def expand_data(self):
        data = {}
        data['id'] = self.id
        data['label'] = self.label
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
        data['transformation'] = self.transformation.expand_data()
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
        self.beam = ""
        self.imaging = ""
        self.couch = ""

class machine_geometry(object):

    #Initialize
    def __init__(self):
        self.name = ""
        self.couch_limits = min_max()
        self.gantry_limits = min_max()
        self.frame_of_reference = machine_frame_of_reference()

    def expand_data(self):
        data = {}
        data['name'] = self.name
        data['couch_limits'] = self.couch_limits.expand_data()
        data['gantry_limits'] = self.gantry_limits.expand_data()
        data['frame_of_reference'] = self.frame_of_reference.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'couch_limits':
                    self.couch_limits.from_json(v)
                elif k == 'gantry_limits':
                    self.gantry_limits.from_json(v)
                elif k == 'frame_of_reference':
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
        self.label = ""
        self.units = ""
        self.range = min_max()
        self.precision = 0
        self.description = ""

    def expand_data(self):
        data = {}
        data['id'] = self.id
        data['label'] = self.label
        data['units'] = self.units
        data['range'] = self.range.expand_data()
        data['precision'] = self.precision
        data['description'] = self.description
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
        self.aperture_mount_info = min_max()
        self.field_size = []
        self.extension = min_max()
        self.rc_info = min_max()
        self.shifters = min_max()
        self.physical_size = []
        self.snout_length = 0.0
        self.downstream_device_gap = 0.0
        self.shape = snout_shape()
        self.shifter_mount_info = snout_shape()
        self.name = ""
        self.slabs = snout_shape()

    def expand_data(self):
        data = {}
        data['aperture_mount_info'] = self.aperture_mount_info.expand_data()
        data['field_size'] = self.field_size
        data['extension'] = self.extension.expand_data()
        data['rc_info'] = self.rc_info.expand_data()
        data['shifters'] = self.shifters.expand_data()
        data['physical_size'] = self.physical_size
        data['snout_length'] = self.snout_length
        data['downstream_device_gap'] = self.downstream_device_gap
        data['shape'] = self.shape.expand_data()
        data['shifter_mount_info'] = self.shifter_mount_info.expand_data()
        data['name'] = self.name
        data['slabs'] = self.slabs.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'extension':
                    self.extension.from_json(v)
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

class markup_block(object):

    #Initialize
    def __init__(self):
        self.text = []
        self.column = []
        self.form = []
        self.bulleted_list = []
        self.empty = ""

class markup_document(object):

    #Initialize
    def __init__(self):
        self.content = markup_block()

    def expand_data(self):
        data = {}
        data['content'] = self.content.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'content':
                    self.content.from_json(v)
                else:
                    setattr(self, k, v)

class markup_form_row(object):

    #Initialize
    def __init__(self):
        self.label = ""
        self.value = markup_block()

    def expand_data(self):
        data = {}
        data['label'] = self.label
        data['value'] = self.value.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'value':
                    self.value.from_json(v)
                else:
                    setattr(self, k, v)

class mco_navigation_objective(object):

    #Initialize
    def __init__(self):
        self.range = min_max()
        self.is_maximization = False

    def expand_data(self):
        data = {}
        data['range'] = self.range.expand_data()
        data['is_maximization'] = self.is_maximization
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

class meta_calculation_request(object):

    #Initialize
    def __init__(self):
        self.generator = calculation_request()
        self.schema = api_type_info()

    def expand_data(self):
        data = {}
        data['generator'] = self.generator.expand_data()
        data['schema'] = self.schema.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'generator':
                    self.generator.from_json(v)
                elif k == 'schema':
                    self.schema.from_json(v)
                else:
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

class mlc_aperture_params(object):

    #Initialize
    def __init__(self):
        self.leaf_width = 0.0
        self.is_per_layer = False
        self.leaf_direction_angle = 0.0

    def expand_data(self):
        data = {}
        data['leaf_width'] = self.leaf_width
        data['is_per_layer'] = self.is_per_layer
        data['leaf_direction_angle'] = self.leaf_direction_angle
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class mounting_position_side(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # source_side
        # patient_side

    def expand_data(self):
        return self.name

    def from_json(self, jdict):
        if hasattr(jdict, 'items'):
            for k, v in jdict.items():
                if hasattr(self,k):
                    setattr(self, k, v)
        else:
            self.name = jdict;

class multiple_source_view(object):

    #Initialize
    def __init__(self):
        self.up = []
        self.center = []
        self.display_surface = box_2d()
        self.distance = []
        self.direction = []

    def expand_data(self):
        data = {}
        data['up'] = self.up
        data['center'] = self.center
        data['display_surface'] = self.display_surface.expand_data()
        data['distance'] = self.distance
        data['direction'] = self.direction
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
        self.position = []
        self.color = rgb8()

    def expand_data(self):
        data = {}
        data['label'] = self.label
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

class nurb_surface(object):

    #Initialize
    def __init__(self):
        self.box = box_2d()
        self.order = []
        self.weights = []
        self.heights = []
        self.knots = []
        self.point_counts = []

    def expand_data(self):
        data = {}
        data['box'] = self.box.expand_data()
        data['order'] = self.order
        data['weights'] = self.weights
        data['heights'] = self.heights
        data['knots'] = self.knots
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

class parameterized_dose_objective(object):

    #Initialize
    def __init__(self):
        self.beams = []
        self.voxels = []
        self.parameter = 0.0

    def expand_data(self):
        data = {}
        data['beams'] = self.beams
        voxel = []
        for x in self.voxels:
            s = weighted_grid_index()
            s.from_json(x)
            voxel.append(s.expand_data())
        data['voxels'] = voxel
        data['parameter'] = self.parameter
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class patient(object):

    #Initialize
    def __init__(self):
        self.ethnic_group = ""
        self.id = ""
        self.birth_date = ""
        self.sex = patient_sex()
        self.comments = ""
        self.name = person_name()

    def expand_data(self):
        data = {}
        data['ethnic_group'] = self.ethnic_group
        data['id'] = self.id
        data['birth_date'] = self.birth_date
        data['sex'] = self.sex.expand_data()
        data['comments'] = self.comments
        data['name'] = self.name.expand_data()
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
        # hfp
        # ffs
        # ffdl
        # ffdr
        # hfdl
        # hfs
        # hfdr
        # ffp

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
        # m
        # f

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
        self.energy = 0.0
        self.r80 = 0.0
        self.r90 = 0.0

    def expand_data(self):
        data = {}
        data['energy'] = self.energy
        data['r80'] = self.r80
        data['r90'] = self.r90
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
        # constant
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
        self.deliverable_energies = []
        self.halo_sigma_sq_function = quadratic_function()
        self.modeled_energies = []
        self.aperture_sad = []
        self.source_rotation_function = linear_function()
        self.sad = []

    def expand_data(self):
        data = {}
        deliverable_energie = []
        for x in self.deliverable_energies:
            s = pbs_deliverable_energy()
            s.from_json(x)
            deliverable_energie.append(s.expand_data())
        data['deliverable_energies'] = deliverable_energie
        data['halo_sigma_sq_function'] = self.halo_sigma_sq_function.expand_data()
        modeled_energie = []
        for x in self.modeled_energies:
            s = pbs_modeled_energy()
            s.from_json(x)
            modeled_energie.append(s.expand_data())
        data['modeled_energies'] = modeled_energie
        data['aperture_sad'] = self.aperture_sad
        data['source_rotation_function'] = self.source_rotation_function.expand_data()
        data['sad'] = self.sad
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
        self.sigma = pbs_optical_sigma()
        self.energy = 0.0
        self.w80 = 0.0
        self.r100 = 0.0
        self.pristine_peak = irregularly_sampled_function()
        self.r90 = 0.0

    def expand_data(self):
        data = {}
        data['sigma'] = self.sigma.expand_data()
        data['energy'] = self.energy
        data['w80'] = self.w80
        data['r100'] = self.r100
        data['pristine_peak'] = self.pristine_peak.expand_data()
        data['r90'] = self.r90
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
        self.sigma = pbs_optical_sigma()
        self.energy = 0.0
        self.flixels = []
        self.pristine_peak = interpolated_function()
        self.r90 = 0.0
        self.flixel_rotation = 0.0

    def expand_data(self):
        data = {}
        data['sigma'] = self.sigma.expand_data()
        data['energy'] = self.energy
        flixel = []
        for x in self.flixels:
            s = projected_isocentric_vector()
            s.from_json(x)
            flixel.append(s.expand_data())
        data['flixels'] = flixel
        data['pristine_peak'] = self.pristine_peak.expand_data()
        data['r90'] = self.r90
        data['flixel_rotation'] = self.flixel_rotation
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
        self.spot_tune_id = 0
        self.spots = []
        self.num_spot_positions = 0
        self.spot_size = []
        self.num_paintings = 0

    def expand_data(self):
        data = {}
        data['spot_tune_id'] = self.spot_tune_id
        spot = []
        for x in self.spots:
            s = weighted_spot()
            s.from_json(x)
            spot.append(s.expand_data())
        data['spots'] = spot
        data['num_spot_positions'] = self.num_spot_positions
        data['spot_size'] = self.spot_size
        data['num_paintings'] = self.num_paintings
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class person_name(object):

    #Initialize
    def __init__(self):
        self.given_name = ""
        self.suffix = ""
        self.middle_name = ""
        self.family_name = ""
        self.prefix = ""

    def expand_data(self):
        data = {}
        data['given_name'] = self.given_name
        data['suffix'] = self.suffix
        data['middle_name'] = self.middle_name
        data['family_name'] = self.family_name
        data['prefix'] = self.prefix
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
        self.line_type = line_stipple_type()
        self.size = 0.0
        self.line_thickness = 0.0

    def expand_data(self):
        data = {}
        data['line_type'] = self.line_type.expand_data()
        data['size'] = self.size
        data['line_thickness'] = self.line_thickness
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'line_type':
                    self.line_type.from_json(v)
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
        self.snout_names = []
        self.mode_type = ""
        self.optional_devices = []
        self.required_devices = []
        self.radiation_type = rt_radiation_type()
        self.name = ""

    def expand_data(self):
        data = {}
        data['mode_type'] = self.mode_type
        optional_device = []
        for x in self.optional_devices:
            s = proton_device_type()
            s.from_json(x)
            optional_device.append(s.expand_data())
        data['optional_devices'] = optional_device
        required_device = []
        for x in self.required_devices:
            s = proton_device_type()
            s.from_json(x)
            required_device.append(s.expand_data())
        data['required_devices'] = required_device
        data['radiation_type'] = self.radiation_type.expand_data()
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'radiation_type':
                    self.radiation_type.from_json(v)
                else:
                    setattr(self, k, v)

class range_analysis_context(object):

    #Initialize
    def __init__(self):
        self.sad = []
        self.patient_image = image_3d()
        self.beam_to_image = []
        self.image_to_beam = []
        self.degraders = []

    def expand_data(self):
        data = {}
        data['sad'] = self.sad
        data['patient_image'] = self.patient_image.expand_data()
        data['beam_to_image'] = self.beam_to_image
        data['image_to_beam'] = self.image_to_beam
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
        self.material_ref = ""
        self.thickness = min_max()
        self.extents = box_2d()

    def expand_data(self):
        data = {}
        data['material_ref'] = self.material_ref
        data['thickness'] = self.thickness.expand_data()
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
        self.n_points = 0
        self.offset = 0

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
        self.iteration_count = 0
        self.smear_weight = 0.0
        self.patch_distal_dose = 0.0
        self.target_inner_border = 0.0
        self.shift_direction = 0
        self.dose_grid = nurb_surface()
        self.smear_span = 0
        self.current_dose = nurb_surface()

    def expand_data(self):
        data = {}
        data['target_distal_dose'] = self.target_distal_dose
        data['iteration_count'] = self.iteration_count
        data['smear_weight'] = self.smear_weight
        data['patch_distal_dose'] = self.patch_distal_dose
        data['target_inner_border'] = self.target_inner_border
        data['shift_direction'] = self.shift_direction
        data['dose_grid'] = self.dose_grid.expand_data()
        data['smear_span'] = self.smear_span
        data['current_dose'] = self.current_dose.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class ref_dicom_item(object):

    #Initialize
    def __init__(self):
        self.ref_instance_uid = ""
        self.ref_class_uid = ""

    def expand_data(self):
        data = {}
        data['ref_instance_uid'] = self.ref_instance_uid
        data['ref_class_uid'] = self.ref_class_uid
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class regular_grid_1d(object):

    #Initialize
    def __init__(self):
        self.n_points = []
        self.spacing = []
        self.p0 = []

    def expand_data(self):
        data = {}
        data['n_points'] = self.n_points
        data['spacing'] = self.spacing
        data['p0'] = self.p0
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class regular_grid_2d(object):

    #Initialize
    def __init__(self):
        self.n_points = []
        self.spacing = []
        self.p0 = []

    def expand_data(self):
        data = {}
        data['n_points'] = self.n_points
        data['spacing'] = self.spacing
        data['p0'] = self.p0
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class regular_grid_3d(object):

    #Initialize
    def __init__(self):
        self.n_points = []
        self.spacing = []
        self.p0 = []

    def expand_data(self):
        data = {}
        data['n_points'] = self.n_points
        data['spacing'] = self.spacing
        data['p0'] = self.p0
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class regular_grid_4d(object):

    #Initialize
    def __init__(self):
        self.n_points = []
        self.spacing = []
        self.p0 = []

    def expand_data(self):
        data = {}
        data['n_points'] = self.n_points
        data['spacing'] = self.spacing
        data['p0'] = self.p0
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
        self.outside_domain_policy = outside_domain_policy()
        self.samples = []

    def expand_data(self):
        data = {}
        data['x0'] = self.x0
        data['x_spacing'] = self.x_spacing
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

class rgb8(object):

    #Initialize
    def __init__(self):
        self.b = 0
        self.g = 0
        self.r = 0

    def expand_data(self):
        data = {}
        data['b'] = self.b
        data['g'] = self.g
        data['r'] = self.r
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class rgba8(object):

    #Initialize
    def __init__(self):
        self.b = 0
        self.g = 0
        self.a = 0
        self.r = 0

    def expand_data(self):
        data = {}
        data['b'] = self.b
        data['g'] = self.g
        data['a'] = self.a
        data['r'] = self.r
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class robust_cvar_objective(object):

    #Initialize
    def __init__(self):
        self.objectives = []
        self.alpha = 0.0

    def expand_data(self):
        data = {}
        objective = []
        for x in self.objectives:
            s = dose_objective()
            s.from_json(x)
            objective.append(s.expand_data())
        data['objectives'] = objective
        data['alpha'] = self.alpha
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class robust_worst_case_objective(object):

    #Initialize
    def __init__(self):
        self.objectives = []

    def expand_data(self):
        data = {}
        objective = []
        for x in self.objectives:
            s = dose_objective()
            s.from_json(x)
            objective.append(s.expand_data())
        data['objectives'] = objective
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class room_imaging_parameters(object):

    #Initialize
    def __init__(self):
        self.imaging_sad = []
        self.source_to_panel = []

    def expand_data(self):
        data = {}
        data['imaging_sad'] = self.imaging_sad
        data['source_to_panel'] = self.source_to_panel
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class rt_approval(object):

    #Initialize
    def __init__(self):
        self.approval = approval_status()
        self.approval_time = {}
        self.approval_name = ""

    def expand_data(self):
        data = {}
        data['approval'] = self.approval.expand_data()
        data['approval_name'] = self.approval_name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'approval':
                    self.approval.from_json(v)
                else:
                    setattr(self, k, v)

class rt_contour(object):

    #Initialize
    def __init__(self):
        self.region = polyset()
        self.position = 0.0

    def expand_data(self):
        data = {}
        data['region'] = self.region.expand_data()
        data['position'] = self.position
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'region':
                    self.region.from_json(v)
                else:
                    setattr(self, k, v)

class rt_control_point(object):

    #Initialize
    def __init__(self):
        self.meterset_rate = 0.0
        self.gantry_pitch_angle = 0.0
        self.layer = pbs_spot_layer()
        self.table_top_pitch_angle = 0.0
        self.surface_entry_point = []
        self.gantry_rotation_direction = ""
        self.nominal_beam_energy = 0.0
        self.isocenter_position = []
        self.spot_scan_tune = ""
        self.number = 0
        self.nominal_beam_energy_unit = ""
        self.table_top_roll_angle = 0.0
        self.source_to_surface_distance = 0.0
        self.gantry_angle = 0.0
        self.table_top_roll_direction = ""
        self.patient_support_angle = 0.0
        self.gantry_pitch_direction = ""
        self.table_top_pitch_direction = ""
        self.beam_limiting_device_angle = 0.0
        self.beam_limiting_direction = ""
        self.snout_position = 0.0
        self.patient_support_direction = ""
        self.meterset_weight = 0.0

    def expand_data(self):
        data = {}
        data['meterset_rate'] = self.meterset_rate
        data['gantry_pitch_angle'] = self.gantry_pitch_angle
        data['layer'] = self.layer.expand_data()
        data['table_top_pitch_angle'] = self.table_top_pitch_angle
        data['surface_entry_point'] = self.surface_entry_point
        data['gantry_rotation_direction'] = self.gantry_rotation_direction
        data['nominal_beam_energy'] = self.nominal_beam_energy
        data['isocenter_position'] = self.isocenter_position
        data['spot_scan_tune'] = self.spot_scan_tune
        data['number'] = self.number
        data['nominal_beam_energy_unit'] = self.nominal_beam_energy_unit
        data['table_top_roll_angle'] = self.table_top_roll_angle
        data['source_to_surface_distance'] = self.source_to_surface_distance
        data['gantry_angle'] = self.gantry_angle
        data['table_top_roll_direction'] = self.table_top_roll_direction
        data['patient_support_angle'] = self.patient_support_angle
        data['gantry_pitch_direction'] = self.gantry_pitch_direction
        data['table_top_pitch_direction'] = self.table_top_pitch_direction
        data['beam_limiting_device_angle'] = self.beam_limiting_device_angle
        data['beam_limiting_direction'] = self.beam_limiting_direction
        data['snout_position'] = self.snout_position
        data['patient_support_direction'] = self.patient_support_direction
        data['meterset_weight'] = self.meterset_weight
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
        self.series = dicom_rt_series()
        self.study_data = dicom_study()
        self.position_reference_indicator = ""
        self.ref_plan_data = ref_dicom_item()
        self.patient_data = patient()
        self.ref_fraction_number = 0
        self.type = dose_type()
        self.frame_of_ref_uid = ""
        self.dose = rt_image_data_3d()
        self.summation_type = dose_summation_type()
        self.equipment_data = dicom_equipment()
        self.ref_beam_number = 0
        self.sop_data = dicom_sop_common()

    def expand_data(self):
        data = {}
        data['series'] = self.series.expand_data()
        data['study_data'] = self.study_data.expand_data()
        data['position_reference_indicator'] = self.position_reference_indicator
        data['ref_plan_data'] = self.ref_plan_data.expand_data()
        data['patient_data'] = self.patient_data.expand_data()
        data['ref_fraction_number'] = self.ref_fraction_number
        data['type'] = self.type.expand_data()
        data['frame_of_ref_uid'] = self.frame_of_ref_uid
        data['dose'] = self.dose.expand_data()
        data['summation_type'] = self.summation_type.expand_data()
        data['equipment_data'] = self.equipment_data.expand_data()
        data['ref_beam_number'] = self.ref_beam_number
        data['sop_data'] = self.sop_data.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'series':
                    self.series.from_json(v)
                elif k == 'study_data':
                    self.study_data.from_json(v)
                elif k == 'ref_plan_data':
                    self.ref_plan_data.from_json(v)
                elif k == 'patient_data':
                    self.patient_data.from_json(v)
                elif k == 'type':
                    self.type.from_json(v)
                elif k == 'dose':
                    self.dose.from_json(v)
                elif k == 'summation_type':
                    self.summation_type.from_json(v)
                elif k == 'equipment_data':
                    self.equipment_data.from_json(v)
                elif k == 'sop_data':
                    self.sop_data.from_json(v)
                else:
                    setattr(self, k, v)

class rt_dose_reference(object):

    #Initialize
    def __init__(self):
        self.delivery_max_dose = 0.0
        self.point_coordinates = []
        self.dose_type = ""
        self.target_underdose_vol_fraction = 0.0
        self.description = ""
        self.uid = ""
        self.ref_roi_number = 0
        self.target_max_dose = 0.0
        self.number = 0
        self.target_min_dose = 0.0
        self.target_rx_dose = 0.0
        self.structure_type = ""

    def expand_data(self):
        data = {}
        data['delivery_max_dose'] = self.delivery_max_dose
        data['point_coordinates'] = self.point_coordinates
        data['dose_type'] = self.dose_type
        data['target_underdose_vol_fraction'] = self.target_underdose_vol_fraction
        data['description'] = self.description
        data['uid'] = self.uid
        data['ref_roi_number'] = self.ref_roi_number
        data['target_max_dose'] = self.target_max_dose
        data['number'] = self.number
        data['target_min_dose'] = self.target_min_dose
        data['target_rx_dose'] = self.target_rx_dose
        data['structure_type'] = self.structure_type
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class rt_fraction(object):

    #Initialize
    def __init__(self):
        self.dose_ref_nums = []
        self.fractions_per_day = 0
        self.fraction_pattern_length = 0
        self.number_planned_fractions = 0
        self.number = 0
        self.ref_beams = []
        self.description = ""
        self.fraction_pattern = ""

    def expand_data(self):
        data = {}
        data['dose_ref_nums'] = self.dose_ref_nums
        data['fractions_per_day'] = self.fractions_per_day
        data['fraction_pattern_length'] = self.fraction_pattern_length
        data['number_planned_fractions'] = self.number_planned_fractions
        data['number'] = self.number
        ref_beam = []
        for x in self.ref_beams:
            s = rt_ref_beam()
            s.from_json(x)
            ref_beam.append(s.expand_data())
        data['ref_beams'] = ref_beam
        data['description'] = self.description
        data['fraction_pattern'] = self.fraction_pattern
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class rt_general_accessory(object):

    #Initialize
    def __init__(self):
        self.id = ""
        self.number = 0
        self.accessory_code = ""
        self.description = ""

    def expand_data(self):
        data = {}
        data['id'] = self.id
        data['number'] = self.number
        data['accessory_code'] = self.accessory_code
        data['description'] = self.description
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class rt_image_data_2d(object):

    #Initialize
    def __init__(self):
        self.instance_number = 0
        self.photometric_interpretation = ""
        self.img_data = image_2d()
        self.image_orientation = []

    def expand_data(self):
        data = {}
        data['instance_number'] = self.instance_number
        data['photometric_interpretation'] = self.photometric_interpretation
        data['img_data'] = self.img_data.expand_data()
        data['image_orientation'] = self.image_orientation
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'img_data':
                    self.img_data.from_json(v)
                else:
                    setattr(self, k, v)

class rt_image_data_3d(object):

    #Initialize
    def __init__(self):
        self.instance_number = 0
        self.photometric_interpretation = ""
        self.img_data = image_3d()
        self.image_orientation = []

    def expand_data(self):
        data = {}
        data['instance_number'] = self.instance_number
        data['photometric_interpretation'] = self.photometric_interpretation
        data['img_data'] = self.img_data.expand_data()
        data['image_orientation'] = self.image_orientation
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'img_data':
                    self.img_data.from_json(v)
                else:
                    setattr(self, k, v)

class rt_ion_beam(object):

    #Initialize
    def __init__(self):
        self.beam_scan_mode = rt_ion_beam_scan_mode()
        self.treatment_delivery_type = ""
        self.description = ""
        self.general_accessories = []
        self.primary_dosimeter_unit = ""
        self.machine_manufacturer_name = ""
        self.beam_type = rt_ion_beam_type()
        self.treatment_machine = ""
        self.radiation_type = rt_radiation_type()
        self.block = rt_radiation_type()
        self.beam_number = 0
        self.machine_model_name = ""
        self.final_meterset_weight = 0.0
        self.name = ""
        self.shifters = []
        self.control_points = []
        self.referenced_patient_setup = 0
        self.patient_support_type = ""
        self.referenced_tolerance_table = 0
        self.compensators = []
        self.snout = rt_snout()
        self.virtual_sad = []

    def expand_data(self):
        data = {}
        data['beam_scan_mode'] = self.beam_scan_mode.expand_data()
        data['treatment_delivery_type'] = self.treatment_delivery_type
        data['description'] = self.description
        general_accessorie = []
        for x in self.general_accessories:
            s = rt_general_accessory()
            s.from_json(x)
            general_accessorie.append(s.expand_data())
        data['general_accessories'] = general_accessorie
        data['primary_dosimeter_unit'] = self.primary_dosimeter_unit
        data['machine_manufacturer_name'] = self.machine_manufacturer_name
        data['beam_type'] = self.beam_type.expand_data()
        data['treatment_machine'] = self.treatment_machine
        data['radiation_type'] = self.radiation_type.expand_data()
        data['block'] = self.block.expand_data()
        data['beam_number'] = self.beam_number
        data['machine_model_name'] = self.machine_model_name
        data['final_meterset_weight'] = self.final_meterset_weight
        data['name'] = self.name
        shifter = []
        for x in self.shifters:
            s = rt_ion_range_shifter()
            s.from_json(x)
            shifter.append(s.expand_data())
        data['shifters'] = shifter
        control_point = []
        for x in self.control_points:
            s = rt_control_point()
            s.from_json(x)
            control_point.append(s.expand_data())
        data['control_points'] = control_point
        data['referenced_patient_setup'] = self.referenced_patient_setup
        data['patient_support_type'] = self.patient_support_type
        data['referenced_tolerance_table'] = self.referenced_tolerance_table
        compensator = []
        for x in self.compensators:
            s = rt_ion_rangecompensator()
            s.from_json(x)
            compensator.append(s.expand_data())
        data['compensators'] = compensator
        data['snout'] = self.snout.expand_data()
        data['virtual_sad'] = self.virtual_sad
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'beam_scan_mode':
                    self.beam_scan_mode.from_json(v)
                elif k == 'beam_type':
                    self.beam_type.from_json(v)
                elif k == 'radiation_type':
                    self.radiation_type.from_json(v)
                elif k == 'snout':
                    self.snout.from_json(v)
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
        # dynamic
        # static

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
        self.divergent = False
        self.material = ""
        self.downstream_edge = 0.0
        self.data = polyset()
        self.block_type = rt_ion_block_type()
        self.number = 0
        self.position = rt_mounting_position()
        self.thickness = 0.0
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['divergent'] = self.divergent
        data['material'] = self.material
        data['downstream_edge'] = self.downstream_edge
        data['data'] = self.data.expand_data()
        data['block_type'] = self.block_type.expand_data()
        data['number'] = self.number
        data['position'] = self.position.expand_data()
        data['thickness'] = self.thickness
        data['description'] = self.description
        data['name'] = self.name
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

class rt_ion_plan(object):

    #Initialize
    def __init__(self):
        self.label = ""
        self.frame_of_ref_uid = ""
        self.ref_ss_data = ref_dicom_item()
        self.series = dicom_rt_series()
        self.fractions = []
        self.prescriptions = []
        self.tolerance_tables = []
        self.patient_data = patient()
        self.calibration_date = ""
        self.description = ""
        self.name = ""
        self.geometry = ""
        self.instance_number = 0
        self.patient_setups = []
        self.study_data = dicom_study()
        self.equipment_data = dicom_equipment()
        self.position_reference_indicator = ""
        self.beams = []
        self.sop_data = dicom_sop_common()
        self.approval_info = rt_approval()

    def expand_data(self):
        data = {}
        data['label'] = self.label
        data['frame_of_ref_uid'] = self.frame_of_ref_uid
        data['ref_ss_data'] = self.ref_ss_data.expand_data()
        data['series'] = self.series.expand_data()
        fraction = []
        for x in self.fractions:
            s = rt_fraction()
            s.from_json(x)
            fraction.append(s.expand_data())
        data['fractions'] = fraction
        prescription = []
        for x in self.prescriptions:
            s = rt_dose_reference()
            s.from_json(x)
            prescription.append(s.expand_data())
        data['prescriptions'] = prescription
        tolerance_table = []
        for x in self.tolerance_tables:
            s = rt_tolerance_table()
            s.from_json(x)
            tolerance_table.append(s.expand_data())
        data['tolerance_tables'] = tolerance_table
        data['patient_data'] = self.patient_data.expand_data()
        data['calibration_date'] = self.calibration_date
        data['description'] = self.description
        data['name'] = self.name
        data['geometry'] = self.geometry
        data['instance_number'] = self.instance_number
        patient_setup = []
        for x in self.patient_setups:
            s = rt_patient_setup()
            s.from_json(x)
            patient_setup.append(s.expand_data())
        data['patient_setups'] = patient_setup
        data['study_data'] = self.study_data.expand_data()
        data['equipment_data'] = self.equipment_data.expand_data()
        data['position_reference_indicator'] = self.position_reference_indicator
        beam = []
        for x in self.beams:
            s = rt_ion_beam()
            s.from_json(x)
            beam.append(s.expand_data())
        data['beams'] = beam
        data['sop_data'] = self.sop_data.expand_data()
        data['approval_info'] = self.approval_info.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'ref_ss_data':
                    self.ref_ss_data.from_json(v)
                elif k == 'series':
                    self.series.from_json(v)
                elif k == 'patient_data':
                    self.patient_data.from_json(v)
                elif k == 'study_data':
                    self.study_data.from_json(v)
                elif k == 'equipment_data':
                    self.equipment_data.from_json(v)
                elif k == 'sop_data':
                    self.sop_data.from_json(v)
                elif k == 'approval_info':
                    self.approval_info.from_json(v)
                else:
                    setattr(self, k, v)

class rt_ion_range_shifter(object):

    #Initialize
    def __init__(self):
        self.id = ""
        self.number = 0
        self.type = rt_range_shifter_type()
        self.accessory_code = ""

    def expand_data(self):
        data = {}
        data['id'] = self.id
        data['number'] = self.number
        data['type'] = self.type.expand_data()
        data['accessory_code'] = self.accessory_code
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
        self.divergent = False
        self.material = ""
        self.downstream_edge = 0.0
        self.data = image_2d()
        self.relative_stopping_power = 0.0
        self.number = 0
        self.column_offset = 0.0
        self.mounting_position = rt_mounting_position()
        self.position = []
        self.pixel_spacing = []
        self.name = ""

    def expand_data(self):
        data = {}
        data['divergent'] = self.divergent
        data['material'] = self.material
        data['downstream_edge'] = self.downstream_edge
        data['data'] = self.data.expand_data()
        data['relative_stopping_power'] = self.relative_stopping_power
        data['number'] = self.number
        data['column_offset'] = self.column_offset
        data['mounting_position'] = self.mounting_position.expand_data()
        data['position'] = self.position
        data['pixel_spacing'] = self.pixel_spacing
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'data':
                    self.data.from_json(v)
                elif k == 'mounting_position':
                    self.mounting_position.from_json(v)
                else:
                    setattr(self, k, v)

class rt_mounting_position(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # double_sided
        # source_side
        # patient_side

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
        self.fixation_devices = []
        self.table_top_long_setup_dis = 0.0
        self.setup_technique = ""
        self.setup_number = 0
        self.position = patient_position_type()
        self.table_top_vert_setup_dis = 0.0
        self.table_top_lateral_setup_dis = 0.0
        self.setup_label = ""

    def expand_data(self):
        data = {}
        fixation_device = []
        for x in self.fixation_devices:
            s = fixation_device()
            s.from_json(x)
            fixation_device.append(s.expand_data())
        data['fixation_devices'] = fixation_device
        data['table_top_long_setup_dis'] = self.table_top_long_setup_dis
        data['setup_technique'] = self.setup_technique
        data['setup_number'] = self.setup_number
        data['position'] = self.position.expand_data()
        data['table_top_vert_setup_dis'] = self.table_top_vert_setup_dis
        data['table_top_lateral_setup_dis'] = self.table_top_lateral_setup_dis
        data['setup_label'] = self.setup_label
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'position':
                    self.position.from_json(v)
                else:
                    setattr(self, k, v)

class rt_radiation_type(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # proton
        # neutron
        # electron
        # photon

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
        self.beam_number = 0
        self.beam_meterset = 0.0
        self.dose_specification_point = []

    def expand_data(self):
        data = {}
        data['beam_dose'] = self.beam_dose
        data['beam_number'] = self.beam_number
        data['beam_meterset'] = self.beam_meterset
        data['dose_specification_point'] = self.dose_specification_point
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class rt_roi_geometry(object):

    #Initialize
    def __init__(self):
        self.point = []
        self.slices = []

class rt_roi_type(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # dose_region
        # cavity
        # organ
        # external
        # gtv
        # fixation
        # support
        # avoidance
        # isocenter
        # ptv
        # contrast_agent
        # bolus
        # ctv
        # irrad_volume
        # registration
        # treated_volume
        # control
        # marker

    def expand_data(self):
        return self.name

    def from_json(self, jdict):
        if hasattr(jdict, 'items'):
            for k, v in jdict.items():
                if hasattr(self,k):
                    setattr(self, k, v)
        else:
            self.name = jdict;

class rt_snout(object):

    #Initialize
    def __init__(self):
        self.id = ""
        self.accessory_code = ""

    def expand_data(self):
        data = {}
        data['id'] = self.id
        data['accessory_code'] = self.accessory_code
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class rt_structure(object):

    #Initialize
    def __init__(self):
        self.geometry = rt_roi_geometry()
        self.number = 0
        self.ref_frame_of_reference_uid = ""
        self.roi_type = rt_roi_geometry()
        self.color = rgb8()
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['geometry'] = self.geometry.expand_data()
        data['number'] = self.number
        data['ref_frame_of_reference_uid'] = self.ref_frame_of_reference_uid
        data['roi_type'] = self.roi_type.expand_data()
        data['color'] = self.color.expand_data()
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'geometry':
                    self.geometry.from_json(v)
                elif k == 'color':
                    self.color.from_json(v)
                else:
                    setattr(self, k, v)

class rt_structure_list(object):

    #Initialize
    def __init__(self):
        self.structure_list = []
        self.ref_structure_list = []

class rt_structure_set(object):

    #Initialize
    def __init__(self):
        self.label = ""
        self.frame_of_ref_uid = ""
        self.study_data = dicom_study()
        self.equipment_data = dicom_equipment()
        self.patient_data = patient()
        self.structures = rt_structure_list()
        self.series = dicom_rt_series()
        self.description = ""
        self.name = ""
        self.ref_image_series_uid = ""
        self.contour_image_sequence = []
        self.position_reference_indicator = ""
        self.sop_data = dicom_sop_common()
        self.approval_info = rt_approval()

    def expand_data(self):
        data = {}
        data['label'] = self.label
        data['frame_of_ref_uid'] = self.frame_of_ref_uid
        data['study_data'] = self.study_data.expand_data()
        data['equipment_data'] = self.equipment_data.expand_data()
        data['patient_data'] = self.patient_data.expand_data()
        data['structures'] = self.structures.expand_data()
        data['series'] = self.series.expand_data()
        data['description'] = self.description
        data['name'] = self.name
        data['ref_image_series_uid'] = self.ref_image_series_uid
        contour_image_sequenc = []
        for x in self.contour_image_sequence:
            s = ref_dicom_item()
            s.from_json(x)
            contour_image_sequenc.append(s.expand_data())
        data['contour_image_sequence'] = contour_image_sequenc
        data['position_reference_indicator'] = self.position_reference_indicator
        data['sop_data'] = self.sop_data.expand_data()
        data['approval_info'] = self.approval_info.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'study_data':
                    self.study_data.from_json(v)
                elif k == 'equipment_data':
                    self.equipment_data.from_json(v)
                elif k == 'patient_data':
                    self.patient_data.from_json(v)
                elif k == 'structures':
                    self.structures.from_json(v)
                elif k == 'series':
                    self.series.from_json(v)
                elif k == 'sop_data':
                    self.sop_data.from_json(v)
                elif k == 'approval_info':
                    self.approval_info.from_json(v)
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
        self.ct = ct_image()
        self.accession_number = ""
        self.doses = []
        self.instance_uid = ""
        self.physician_name = ""
        self.structure_set = rt_structure_set()
        self.plan = rt_ion_plan()
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['ct'] = self.ct.expand_data()
        data['accession_number'] = self.accession_number
        dose = []
        for x in self.doses:
            s = rt_dose()
            s.from_json(x)
            dose.append(s.expand_data())
        data['doses'] = dose
        data['instance_uid'] = self.instance_uid
        data['physician_name'] = self.physician_name
        data['structure_set'] = self.structure_set.expand_data()
        data['plan'] = self.plan.expand_data()
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'ct':
                    self.ct.from_json(v)
                elif k == 'structure_set':
                    self.structure_set.from_json(v)
                elif k == 'plan':
                    self.plan.from_json(v)
                else:
                    setattr(self, k, v)

class rt_tolerance_table(object):

    #Initialize
    def __init__(self):
        self.label = ""
        self.table_top_lat_position_tol = 0.0
        self.table_top_long_position_tol = 0.0
        self.table_top_vert_position_tol = 0.0
        self.snout_position_tol = 0.0
        self.beam_limiting_angle_tol = 0.0
        self.patient_support_angle_tol = 0.0
        self.table_top_roll_tol = 0.0
        data = {}
        self.gantry_angle_tol = 0.0
        self.number = 0
        self.table_top_pitch_tol = 0.0

    def expand_data(self):
        data = {}
        data['label'] = self.label
        data['table_top_lat_position_tol'] = self.table_top_lat_position_tol
        data['table_top_long_position_tol'] = self.table_top_long_position_tol
        data['table_top_vert_position_tol'] = self.table_top_vert_position_tol
        data['snout_position_tol'] = self.snout_position_tol
        data['beam_limiting_angle_tol'] = self.beam_limiting_angle_tol
        data['patient_support_angle_tol'] = self.patient_support_angle_tol
        data['table_top_roll_tol'] = self.table_top_roll_tol
        data['gantry_angle_tol'] = self.gantry_angle_tol
        data['number'] = self.number
        data['table_top_pitch_tol'] = self.table_top_pitch_tol
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
        # difference
        # xor
        # intersection

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

class simple_dose_objective(object):

    #Initialize
    def __init__(self):
        self.beams = []
        self.voxels = []

    def expand_data(self):
        data = {}
        data['beams'] = self.beams
        voxel = []
        for x in self.voxels:
            s = weighted_grid_index()
            s.from_json(x)
            voxel.append(s.expand_data())
        data['voxels'] = voxel
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
        self.minimum_mill_radius = 0.0
        self.extents = box_2d()

    def expand_data(self):
        data = {}
        inf = []
        for x in self.info:
            s = slab_info()
            s.from_json(x)
            inf.append(s.expand_data())
        data['info'] = inf
        data['minimum_mill_radius'] = self.minimum_mill_radius
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

class sliced_3d_view_state(object):

    #Initialize
    def __init__(self):
        self.slice_positions = []
        self.show_hu_overlays = False

    def expand_data(self):
        data = {}
        data['slice_positions'] = self.slice_positions
        data['show_hu_overlays'] = self.show_hu_overlays
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
        self.depth_dose_curve = interpolated_function()
        self.pdd_shift = 0.0
        self.initial_range = 0.0
        self.weight = 0.0
        self.sad = 0.0
        self.initial_sigma = 0.0

    def expand_data(self):
        data = {}
        data['depth_dose_curve'] = self.depth_dose_curve.expand_data()
        data['pdd_shift'] = self.pdd_shift
        data['initial_range'] = self.initial_range
        data['weight'] = self.weight
        data['sad'] = self.sad
        data['initial_sigma'] = self.initial_sigma
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
        self.show_slice_highlight = False
        self.fill = spatial_region_fill_options()
        self.outline = spatial_region_outline_options()
        self.render_mode = structure_render_mode()

    def expand_data(self):
        data = {}
        data['show_slice_highlight'] = self.show_slice_highlight
        data['fill'] = self.fill.expand_data()
        data['outline'] = self.outline.expand_data()
        data['render_mode'] = self.render_mode.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'fill':
                    self.fill.from_json(v)
                elif k == 'outline':
                    self.outline.from_json(v)
                elif k == 'render_mode':
                    self.render_mode.from_json(v)
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
        self.opacity = 0.0
        self.width = 0.0
        self.type = line_stipple_type()

    def expand_data(self):
        data = {}
        data['opacity'] = self.opacity
        data['width'] = self.width
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
        self.max_element_index = 0
        self.mean = 0.0
        self.max = 0.0
        self.min = 0.0
        self.n_samples = 0.0

    def expand_data(self):
        data = {}
        data['max_element_index'] = self.max_element_index
        data['mean'] = self.mean
        data['max'] = self.max
        data['min'] = self.min
        data['n_samples'] = self.n_samples
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class structure_geometry(object):

    #Initialize
    def __init__(self):
        self.master_slice_list = []
        data = {}

    def expand_data(self):
        data = {}
        master_slice_lis = []
        for x in self.master_slice_list:
            s = slice_description()
            s.from_json(x)
            master_slice_lis.append(s.expand_data())
        data['master_slice_list'] = master_slice_lis
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

class structure_render_mode(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # contours
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

class styled_text_fragment(object):

    #Initialize
    def __init__(self):
        self.text = ""
        self.style = ""

    def expand_data(self):
        data = {}
        data['text'] = self.text
        data['style'] = self.style
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class treatment_machine(object):

    #Initialize
    def __init__(self):
        self.location = ""
        self.serial = ""
        data = {}
        self.settings = []
        self.manufacturer = ""
        data = {}
        self.description = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['location'] = self.location
        data['serial'] = self.serial
        setting = []
        for x in self.settings:
            s = machine_setting()
            s.from_json(x)
            setting.append(s.expand_data())
        data['settings'] = setting
        data['manufacturer'] = self.manufacturer
        data['description'] = self.description
        data['name'] = self.name
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class treatment_room(object):

    #Initialize
    def __init__(self):
        self.snout_names = []
        data = {}
        self.mlc_parameters = polyset()
        self.imaging_parameters = polyset()
        self.machine_geometry_name = ""
        self.name = ""

    def expand_data(self):
        data = {}
        data['mlc_parameters'] = self.mlc_parameters.expand_data()
        data['imaging_parameters'] = self.imaging_parameters.expand_data()
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
        self.face_normal_indices = blob.toStr()
        blob = blob_type()
        self.face_position_indices = blob.toStr()
        blob = blob_type()
        self.vertex_positions = blob.toStr()
        blob = blob_type()
        self.vertex_normals = blob.toStr()

    def expand_data(self):
        data = {}
        data['face_normal_indices'] = parse_bytes_3i(base64.b64decode(self.face_normal_indices['blob']))
        data['face_position_indices'] = parse_bytes_3i(base64.b64decode(self.face_position_indices['blob']))
        data['vertex_positions'] = parse_bytes_3d(base64.b64decode(self.vertex_positions['blob']))
        data['vertex_normals'] = parse_bytes_3d(base64.b64decode(self.vertex_normals['blob']))
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class unboxed_image_2d(object):

    #Initialize
    def __init__(self):
        self.origin = []
        self.size = []
        self.pixels = []
        self.axes = []

    def expand_data(self):
        data = {}
        data['origin'] = self.origin
        data['size'] = self.size
        data['pixels'] = self.pixels
        data['axes'] = self.axes
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class unboxed_image_3d(object):

    #Initialize
    def __init__(self):
        self.origin = []
        self.size = []
        self.pixels = []
        self.axes = []

    def expand_data(self):
        data = {}
        data['origin'] = self.origin
        data['size'] = self.size
        data['pixels'] = self.pixels
        data['axes'] = self.axes
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

class upgrade_type(object):

    #Initialize
    def __init__(self):
        self.name = ""

        # Acceptable enum strings for name:
        # function
        # none

    def expand_data(self):
        return self.name

    def from_json(self, jdict):
        if hasattr(jdict, 'items'):
            for k, v in jdict.items():
                if hasattr(self,k):
                    setattr(self, k, v)
        else:
            self.name = jdict;

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

class weighted_dose_objective(object):

    #Initialize
    def __init__(self):
        self.weight = 0.0
        self.objective = dose_objective()

    def expand_data(self):
        data = {}
        data['weight'] = self.weight
        data['objective'] = self.objective.expand_data()
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                if k == 'objective':
                    self.objective.from_json(v)
                else:
                    setattr(self, k, v)

class weighted_grid_index(object):

    #Initialize
    def __init__(self):
        self.weight = 0.0
        self.index = 0

    def expand_data(self):
        data = {}
        data['weight'] = self.weight
        data['index'] = self.index
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

class weighted_sum_objective(object):

    #Initialize
    def __init__(self):
        self.objectives = []

    def expand_data(self):
        data = {}
        objective = []
        for x in self.objectives:
            s = weighted_dose_objective()
            s.from_json(x)
            objective.append(s.expand_data())
        data['objectives'] = objective
        return data

    def from_json(self, jdict):
        for k, v in jdict.items():
            if hasattr(self,k):
                setattr(self, k, v)

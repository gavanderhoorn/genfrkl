# Copyright 2015 TU Delft Robotics Institute
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: G.A. vd. Hoorn - TU Delft Robotics Institute
#

import genmsg.msgs
from . import karel
from . import msg_mapping



ROS_TO_KAREL_TYPE_MAP = {
    'byte'    : 'BYTE',
    'char'    : 'BYTE',
    'bool'    : 'BOOLEAN',
    'uint8'   : 'BYTE',
    'int8'    : 'BYTE',
    'uint16'  : 'SHORT',
    'int16'   : 'SHORT',
    'uint32'  : 'INTEGER',
    'int32'   : 'INTEGER',
    #'uint64' : 'uint64',
    #'int64'  : 'int64',
    'float32' : 'REAL',
    'float64' : 'REAL',
    #'string'  : 'STRING',
    #'time'    : 'ros_time_t',
    #'duration': 'ros_dur_t',
}


SM_HEADER='sm_hdr'
SM_HEADER_FULLNAME='simple_msgs/sm_hdr'


class NotImplementedException(Exception):
    pass


class NoKarelTypeMappingPossible(Exception):
    pass


class NoAssignedMessageIdException(Exception):
    pass


def ros_type_to_sm_id(pkg, _type, search_path, mapping_dict):
    """
    Tries to lookup the Simple Message Assigned Identifier for the given ROS
    message type. Official Assigned IDs are documented in REP-I0004. Users
    can supply mappings to IDs outside of the official set by providing yaml
    files that contain msg (MD5 -> SM ID) pairs.

    :param pkg: name of ROS package of current message, ``str``
    :param _type: ROS message type, ``str``
    :param search_path: dictionary mapping message namespaces to a directory locations, ``{str:str}``
    :param mapping_dict: nested dictionary mapping pkg names to dicts containing (md5sum, id) pairs
    :returns: Simple Message Assigned Identifier for the given ROS type, ``int``
    :raises: :exc:`NoAssignedMessageIdException` If the given type has no registered mapping
    """
    # make sure we lookup mapping for base type
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)
    if genmsg.msgs.is_builtin(base_type):
        raise ValueError("Only non built-ins can have SM assigned IDs ('%s' is a ROS built-in)" % (base_type))

    #print "-- mapping: '%s'" % (base_type)

    # TODO: handle special case (u)int64: ROS built-in, but not supported

    # handle special case: simple message header
    if SM_HEADER in base_type:
        return SM_HEADER

    # calculate MD5 for passed type
    # TODO: should we re-use msg_context of msg we are generating for?
    msg_context = genmsg.msg_loader.MsgContext.create_default()
    # TODO: will this work with services?
    spec = genmsg.msg_loader.load_msg_by_type(msg_context, base_type, search_path)
    genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    md5sum = genmsg.gentools.compute_md5(msg_context, spec)

    return msg_mapping.map_md5_to_sm_id(mapping_dict, md5sum)


def map_builtin_to_karel(_type):
    """
    :param _type: Name of a ROS data type, ``str``
    :returns: Name of corresponding Karel primitive type (if possible), ``str``
    :raises: :exc:`NoKarelTypeMappingPossible` If there is no mapping possible
    """
    try:
        return ROS_TO_KAREL_TYPE_MAP[_type]
    except KeyError:
        raise NoKarelTypeMappingPossible(
            'ROS built-in \'%s\' not supported right now' % _type)


def maps_to_karel_primitive(ros_type):
  """
  Note: this method also returns False for types that are currently
  not supported. (u)int64 is one such type.

  :param ros_type: Name of a ROS data type, ``str``
  :returns: ``True`` if the type can be mapped to a primitive Karel type, ``bool``
  """
  return ros_type in ROS_TO_KAREL_TYPE_MAP


def group_fields(spec):
    """ function walks the list of parsed fields and creates groups
    of fields that may be processed in a single READ / WRITE statement.

    In essence, this groups subsequent primitive fields with each other,
    while putting each non-primitive field in its own group (as they
    require the use of 'special' deserialisation functions).

    Arrays are considered non-primitive, for reasons of readability and
    error reporting (overly long READ / WRITE statements will make it hard to
    correctly identify the source of errors).

    :param spec: `MsgSpec` instance, ``MsgSpec``
    :returns: `Field` instances in a list of lists, ``[[genmsg.msgs.Field]]``
    """
    field_groups = []
    field_group = []

    for field in spec.parsed_fields():
        is_primitive = maps_to_karel_primitive(field.base_type)
        is_array = field.is_array

        # every field that is either an array or a non-primitive should end
        # up in its own group
        if (not is_primitive) or is_array:
            if len(field_group) > 0:
                field_groups.append(field_group)
            field_group = []
            field_groups.append([field])

        # all other fields are added to the current group
        else:
            field_group.append(field)

    # make sure to store last group as well, if it contains anything
    if len(field_group) > 0:
        field_groups.append(field_group)

    return field_groups


def fmt_sm_libname(sm_id):
    # TODO: ugly, rework
    if SM_HEADER == sm_id:
        return 'lib' + SM_HEADER
    return 'lib' + fmt_sm_name(sm_id)


def fmt_sm_name(sm_id):
    # TODO: ugly, rework
    if SM_HEADER == sm_id:
        return SM_HEADER
    return 'sm%04X' % sm_id


def fmt_sm_type(sm_id):
    return fmt_sm_name(sm_id) + '_t'


def calculate_msg_length(spec):
    # TODO: implement
    return 0

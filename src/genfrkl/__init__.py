#!/usr/bin/env python
""""""
import genmsg.msgs


MSG_TYPE_TO_KL_TYPE = {
    'byte': 'BYTE',
    'char': 'BYTE',
    'bool': 'BOOLEAN',
    'uint8': 'BYTE',
    'int8': 'BYTE',
    'uint16': 'SHORT',
    'int16': 'SHORT',
    'uint32': 'INTEGER',
    'int32': 'INTEGER',
    #'uint64': 'uint64',
    #'int64': 'int64',
    'float32': 'REAL',
    'float64': 'REAL',
    'string': 'STRING',
    #'time': 'ros.Time',
    #'duration': 'ros.Duration'
}


MSG_TYPE_TO_KL_ZERO_VALUE = {
    'bool': 'FALSE',
    'byte': '0',
    'char': '0',
    'uint8': '0',
    'int8': '0',
    'uint16': '0',
    'int16': '0',
    'uint32': '0',
    'int32': '0',
    #'uint64': '0',
    #'int64': '0',
    'float32': '0.0',
    'float64': '0.0',
    'string': '\'\'',
    #'time': 'ros.Time{}',
    #'duration': 'ros.Duration{}'
}


def msg_type_to_kl(package_context, _type):
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)
    if genmsg.msgs.is_builtin(base_type):
        if base_type not in MSG_TYPE_TO_KL_TYPE.keys():
            raise Exception('ROS type  \'%s\' not supported right now' % base_type)
        kl_type = MSG_TYPE_TO_KL_TYPE[base_type]
    elif len(base_type.split('/')) == 1:
        kl_type = base_type
    else:
        pkg = base_type.split('/')[0]
        msg = base_type.split('/')[1]
        if package_context == pkg:
            kl_type = msg
        else:
            # TODO: hack: type is always type of message, karel does not
            #       support namespacing
            kl_type = msg

    if is_array:
        if array_len is None:
            raise Exception('Variable size arrays not supported right now (\'%s\'' % base_type)
        else:
            # TODO: hack, this should be moved to template?
            return 'ARRAY[{0}] OF {1}'.format(array_len, kl_type)
    else:
        return kl_type


def is_primitive_kl_type(_type):
    #print "-- is_primitive_kl_type: got '%s'" % _type
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)
    # check against ROS msg types
    return base_type in ['byte', 'int8', 'int16', 'int32',
                    'char', 'uint8', 'uint16', 'uint32',
                    'float32', 'float64', 'bool']


def msg_type_to_zero_value(package_context, _type):
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)
    if genmsg.msgs.is_builtin(base_type):
        return MSG_TYPE_TO_KL_ZERO_VALUE[base_type]

    raise Exception("Cannot determine zero value for type '%s'" % _type)



def karel_str_quote(msg_str):
    return msg_str.replace('"', '\'')


def msg_has_sm_header(spec):
    """ Determines whether the message has a field of type rp_hdr_t
    """
    for field in spec.parsed_fields():
        if 'rp_hdr_t' in field.type:
            return True
    return False


def calculate_msg_length(spec):
    len = 0
    # we know header length
    if msg_has_sm_header(spec):
        len += (4 * 3)
    
    return len


def map_complex_type_to_routine_prefix(package_context, _type):
    # assumption: 'rp000A_t'
    # output: 'rp000A'
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)

    assert (not genmsg.msgs.is_builtin(base_type))

    #print "-- map_complex_type_to_routine_prefix: got '%s' ('%s')" % (_type, base_type)

    if 'rp_hdr_t' in _type:
        return 'rp_hdr'

    return 'some_prefix_todo'



def msg_to_simple_message_type(spec):
    # assume there is a constant in the message spec that we use
    for constant in spec.constants:
        if constant.name == 'MSG_TYPE':
            return constant.val
    raise Exception("Msg spec for '%s' missing required MSG_TYPE constant" % spec.short_name)


def has_arrays(spec):
    """ Determines whether the message has any fields that are arrays
    """
    for field in spec.parsed_fields():
        if field.is_array:
            return True
    return False

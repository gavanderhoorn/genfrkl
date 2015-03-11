#!/usr/bin/env python
""""""
import genmsg.msgs


MSG_TYPE_TO_KL_TYPE = {
    'byte'   : 'BYTE',
    'char'   : 'BYTE',
    'bool'   : 'BOOLEAN',
    'uint8'  : 'BYTE',
    'int8'   : 'BYTE',
    'uint16' : 'SHORT',
    'int16'  : 'SHORT',
    'uint32' : 'INTEGER',
    'int32'  : 'INTEGER',
    #'uint64' : 'uint64',
    #'int64'  : 'int64',
    'float32': 'REAL',
    'float64': 'REAL',
    'string' : 'STRING',
    #'time': 'ros.Time',            # ros_tim_t? Karel struct?
    #'duration': 'ros.Duration'     # ros_dur_t? Karel struct?
}


MSG_TYPE_TO_KL_ZERO_VALUE = {
    'bool'   : 'FALSE',
    'byte'   : '0',
    'char'   : '0',
    'uint8'  : '0',
    'int8'   : '0',
    'uint16' : '0',
    'int16'  : '0',
    'uint32' : '0',
    'int32'  : '0',
    #'uint64' : '0',
    #'int64'  : '0',
    'float32': '0.0',
    'float64': '0.0',
    'string' : '\'\'',
    #'time': 'ros.Time{}',
    #'duration': 'ros.Duration{}'
}







# from 'KAREL Reference Manual Rev. C', table 2-6: Reserved Word List
KL_RESERVED_WORDS = [
    'ABORT', 'ABOUT', 'ABS', 'AFTER', 'ALONG', 'ALSO', 'AND', 'ARRAY',
    'ARRAY_LEN', 'AT', 'ATTACH', 'AWAY', 'AXIS', 'BEFORE', 'BEGIN', 'BOOLEAN',
    'BY', 'BYNAME', 'BYTE', 'CAM_SETUP', 'CANCEL', 'CASE', 'CLOSE', 'CMOS',
    'COMMAND', 'COMMON_ASSOC', 'CONDITION', 'CONFIG', 'CONNECT', 'CONST',
    'CONTINUE', 'COORDINATED', 'CR', 'DELAY', 'DISABLE', 'DISCONNECT', 'DIV',
    'DO', 'DOWNTO', 'DRAM', 'ELSE', 'ENABLE', 'END', 'END', 'ENDCONDITION',
    'ENDFOR', 'ENDIF', 'ENDMOVE', 'ENDSELECT', 'ENDSTRUCTURE', 'ENDUSING',
    'ENDWHILE', 'ERROR', 'EVAL', 'EVENT', 'FILE', 'FOR', 'FROM', 'GET_VAR',
    'GO', 'GOTO', 'GROUP', 'GROUP_ASSOC', 'HAND', 'HOLD', 'IF', 'IN',
    'INDEPENDENT', 'INTEGER', 'JOINTPOS', 'JOINTPOS1', 'JOINTPOS2',
    'JOINTPOS3', 'JOINTPOS4', 'JOINTPOS5', 'JOINTPOS6', 'JOINTPOS7',
    'JOINTPOS8', 'JOINTPOS9', 'MOD', 'MODEL', 'MOVE', 'NEAR', 'NOABORT',
    'NODE', 'NODEDATA', 'NOMESSAGE', 'NOPAUSE', 'NOT', 'NOWAIT', 'OF', 'OPEN',
    'OR', 'PATH', 'PATHHEADER', 'PAUSE', 'POSITION', 'POWERUP', 'PROGRAM',
    'PULSE', 'PURGE', 'READ', 'REAL', 'RELATIVE', 'RELAX', 'RELEASE',
    'REPEAT', 'RESTORE', 'RESUME', 'RETURN', 'ROUTINE', 'SELECT', 'SEMAPHORE',
    'SET_VAR', 'SHORT', 'SIGNAL', 'STOP', 'STRING', 'STRUCTURE', 'THEN',
    'TIME', 'TIMER', 'TO', 'TPENABLE', 'TYPE', 'UNHOLD', 'UNINIT', 'UNPAUSE',
    'UNTIL', 'USING', 'VAR', 'VECTOR', 'VIA', 'VIS_PROCESS', 'WAIT', 'WHEN',
    'WHILE', 'WITH', 'WRITE', 'XYZWPR', 'XYZWPREXT']


# from 'KAREL Reference Manual Rev. C'
KL_PREDEFINED_IDENTS = [
    # table 2-7: Predefined Identifier and Value Summary
    'TRUE', 'FALSE', 'ON', 'OFF', 'MAXINT', 'MININT',
    # cont'd
    'RSWORLD', 'AESWORLD', 'WRISTJOINT', 'JOINT', 'LINEAR', 'STRAIGHT',
    'CIRCULAR', 'FINE', 'COARSE', 'NOSETTLE', 'NODECEL', 'VARDECEL',
    # table 2-8: Port and File Predefined Identifier Summary
    'DIN', 'DOUT', 'GIN', 'GOUT', 'AIN', 'AOUT', 'TPIN', 'TPOUT', 'RDI',
    'RDO', 'OPIN', 'OPOUT', 'WDI', 'WDOUT', 'UIN', 'UOUT', 'LDI', 'LDO',
    'FLG', 'MRK',
    # cont'd
    'LAI', 'LAO', 'TPDISPLAY', 'TPERROR', 'TPPROMPT', 'TPFUNC', 'TPSTATUS',
    'INPUT', 'OUTPUT', 'CRTERROR', 'CRTFUNC', 'CRTSTATUS', 'CRTPROMPT',
    'VIS_MONITOR'
]


KL_TYPE_SZ = {
    'BYTE'    : 1,
    'SHORT'   : 2,
    'INTEGER' : 4,
    'REAL'    : 4,
    'BOOLEAN' : 4,
}


# TODO: make 'sm_hdr' map to 'sm_hdr_t' as a Karel type. Perhaps treat it like a built-in?
#  or rework msg to krl type mapping entirely

SM_HEADER_LIBNAME = 'sm_hdr'
SM_HEADER_NAME = 'sm_hdr_t'
SM_HEADER_TYPE = 'sm_hdr_t'


class NotImplementedException(Exception):
    pass



def msg_type_to_kl(package_context, _type):
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)

    # 'byte'
    if genmsg.msgs.is_builtin(base_type):
        if base_type not in MSG_TYPE_TO_KL_TYPE.keys():
            raise NotImplementedException('ROS type  \'%s\' not supported right now' % base_type)
        kl_type = MSG_TYPE_TO_KL_TYPE[base_type]

    # 'Byte'
    elif len(base_type.split('/')) == 1:
        kl_type = base_type

    # 'std_msgs/Byte'
    else:
        pkg = base_type.split('/')[0]
        msg = base_type.split('/')[1]
        if package_context == pkg:
            kl_type = 'sm%s' % msg.upper()
        else:
            # TODO: hack: type is always type of message, karel does not
            #       support namespacing
            # TODO: this should do the same trick as map_complex_type_to_routine_prefix()
            kl_type = 'sm%s' % msg.upper()

    if is_array:
        if array_len is None:
            raise NotImplementedException('Variable sized arrays not supported right now (\'%s\'' % base_type)
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


def is_legal_kl_ident(ident):
    # TODO: expand checks. See KAREL RefMan, 2.1.4: User-Defined Identifiers
    return (len(ident) <= 12) and not is_reserved_karel(ident)


def is_reserved_karel(ident):
    return (ident.upper() in KL_RESERVED_WORDS
        or ident.upper() in KL_PREDEFINED_IDENTS)


def karel_str_quote(msg_str):
    return msg_str.replace('"', '\'')


def msg_has_sm_header(spec):
    """ Determines whether the message has a field of type sm_hdr_t
    """
    for field in spec.parsed_fields():
        if SM_HEADER_NAME in field.type:
            return True
    return False


def calculate_msg_length(spec):
    return get_type_len(spec.parsed_fields())


def load_id_mapper_file(fname):
    from yaml import load
    with open(fname, 'r') as f:
        doc = load(f)
    return doc['data']


from genmsg.msg_loader import load_msg_by_type

def get_type_len(fields):
    ret_len = 0

    for field in fields:
        # get karel type
        (base_type, is_array, array_len) = genmsg.msgs.parse_type(field.type)
        sub_total = 0

        if len(base_type.split('/')) > 1:
            # type (msg) from other package
            # TODO: load msg from other package, recursively call
            #       method on that msg
            if SM_HEADER_NAME in base_type:
                sub_total += (3 * 4)
            else:
                # TODO: implement loading other msg types
                # perhaps use spec.depends? and load_msg_depends(), load_msg_by_type()?
                # same trick as map_complex_type_to_routine_prefix()
                #return 4
                raise NotImplementedException("%s" % base_type)
        else:
            kl_type = MSG_TYPE_TO_KL_TYPE[base_type]
            sub_total = KL_TYPE_SZ[kl_type]
            if is_array and array_len is not None:
                sub_total *= array_len

        ret_len += sub_total

    return ret_len


def needs_swap(package_context, _type):
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)
    return base_type in ['int16', 'int32', 'uint16', 'uint32', 'float32', 'float64', 'bool']


def get_swap_func(package_context, _type):
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)

    assert (base_type in ['int16', 'int32', 'uint16', 'uint32', 'float32', 'float64', 'bool']), "No SWAP function for type '%s'" % base_type

    if base_type in ['int16', 'uint16']:
        return 'SWAP_SHORT'
    elif base_type in ['int32', 'uint32', 'bool']:
        return 'SWAP_INT'
    elif base_type in ['float32', 'float64']:
        return 'SWAP_REAL'
    else:
        # impossible
        raise Exception("No SWAP function for type '%s'" % base_type)


def map_complex_type_to_routine_prefix(package_context, _type):
    # assumption: 'sm000A_t'
    # output: 'sm000A'
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)

    assert (not genmsg.msgs.is_builtin(base_type)), "'%s' is a built-in, cannot map" % base_type

    if SM_HEADER_NAME in _type:
        return SM_HEADER_LIBNAME

    # idea:
    #  - load msg for _type
    #  - calculate md5sum for msg
    #  - use md5 to retrieve assigned id
    #  - prefix 'sm' and return
    #sm_id_data = load_id_mapper_file('sm_assigned_ids.yaml')

    return 'smXXXX'


def has_arrays(spec):
    """ Determines whether the message has any fields that are arrays
    """
    for field in spec.parsed_fields():
        if field.is_array:
            return True
    return False


def get_array_len(_type):
    """ Returns the length of an array
    """
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(_type)
    assert (is_array), "Only array fields have an array length"
    return array_len


def group_fields(spec):
    """ function walks the list of parsed fields and creates groups
    of fields that may be processed in a single READ / WRITE statement.

    In essence, this groups subsequent primitive fields with each other,
    while putting each non-primitive field in its own group (as they
    require the use of 'special' deserialisation functions).

    Arrays are considered non-primitive, for reasons of readability and
    error reporting (overly long READ / WRITE statements will make it hard to
    correctly identify the source of errors).
    """
    field_groups = []
    field_group = []

    for field in spec.parsed_fields():
        # readability
        is_primitive = is_primitive_kl_type(field.type)
        is_array  = field.is_array

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

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
    'WHILE', 'WITH', 'WRITE', 'XYZWPR', 'XYZWPREXT'
]


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


PRIMITIVE_TYPES = ['BYTE', 'SHORT', 'INTEGER', 'REAL', 'BOOLEAN']#, 'STRING']


# from 'KAREL Operation Manual', Section 3.2.7
# and 'KAREL Reference Manual Rev. C', Section 7.9, Table 7-17
# TODO: for now, -1 means: no intrinsic length, but calculated
PRIMITIVE_TYPE_SZ = dict(zip(PRIMITIVE_TYPES, [1, 2, 4, 4, 4]))#, -1]))


ZERO_VALUES = dict(zip(PRIMITIVE_TYPES, ['0', '0', '0', '0.0', 'FALSE']))#, "''"]))


def is_primitive_type(_type):
    """
    :param _type: Name of a data type, ``str``
    :returns: ``True`` if the type is a primitive (or built-in) Karel type, ``bool``
    """
    return _type.upper() in PRIMITIVE_TYPES


def primitive_zero_value(_type):
    return ZERO_VALUES[_type.upper()]


def is_legal_ident(ident):
    """
    Performs some minimal checking to make sure that the given identifier
    is legal in Karel sources.

    Note: this only checks what is not already checked by genmsg.

    :param ident: Name of an identifier, ``str``
    :returns: ``True`` if the name is a legal identifier in Karel, ``bool``
    """
    # TODO: expand checks. See KAREL RefMan, 2.1.4: User-Defined Identifiers
    legal_len = (len(ident) > 0) and (not is_too_long(ident))
    rsvd_word = is_reserved_word(ident)
    return legal_len and not rsvd_word


def is_too_long(ident):
    if not isinstance(ident, str):
        raise ValueError('Identifier names can only be strings')
    return (len(ident) > 12)


def is_reserved_word(ident):
    """
    :param ident: Name of an identifier, ``str``
    :returns: ``True`` if the name is a reserved word in Karel, ``bool``
    """
    return (ident.upper() in KL_RESERVED_WORDS
            or ident.upper() in KL_PREDEFINED_IDENTS)


def quote_str(_str):
    """
    TODO: fix this. Can a string even contain embedded quotes in karel?

    :param _str: A string, ``str``
    :returns: The given string, properly quoted for inclusion in Karel source files, ``str``
    """
    return _str.replace('"', "'")


def get_type_sz(_type):
    """
    :param _type: Name of a Karel data type, ``str``
    :returns: Size of the type, in bytes, ``int``
    """
    return PRIMITIVE_TYPE_SZ[_type.upper()]


def has_swap_function(_type):
    """
    :param _type: Name of a Karel data type, ``str``
    :returns: ``True`` if the type has a defined SWAP function, ``bool``
    """
    return _type.upper() in ['SHORT', 'INTEGER', 'REAL']


def get_swap_function(_type):
    """
    :param _type: Name of a Karel data type, ``str``
    :returns: Byte swap function for given data type, if it exists, ``bool``
    :raises: :exc:``ValueError`` If type has no swap function defined
    """
    if has_swap_function(_type):
        return {
            'SHORT' : 'SWAP_SHORT',
            'INTEGER' : 'SWAP_INT',
            'REAL' : 'SWAP_REAL'
        }[_type.upper()]
    raise ValueError("No SWAP function defined for type '%s'" % _type)

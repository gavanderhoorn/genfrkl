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

def has_arrays(spec):
    """
    :param spec: `MsgSpec` instance, ``MsgSpec``
    :returns: ``True`` if the given spec has any fields that are arrays, ``bool``
    """
    for field in spec.parsed_fields():
        if field.is_array:
            return True
    return False


def abbr(ident, max_len=12):
    """
    Returns an abbreviated version of 'ident'.

    TODO: extend this. Use abbreviation db.

    :param ident: name of identifier, ``str``
    :param max_len: maximum allowed length for identifier, ``int``
    :returns: abbreviated version of the given identifier, ``str``
    """
    return ident[:max_len]

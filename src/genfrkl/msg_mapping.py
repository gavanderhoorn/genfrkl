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

def map_md5_to_sm_id(mapping_dict, md5sum):
    """
    Will try to map the given 'md5sum' to a Simple Message assigned Identifier.

    Mapping dict is assumed to have the following structure:

    {
      "PKG_NAME" : 
      {
        'MD5SUM' : SM_ASSIGNED_ID,
        ...
      },
      ...
    }

    :param mapping_dict: dictionary containing mapping info, ``{str:{str:int}}``
    :param md5sum: MD5 of message type to map, ``str``
    :returns: Simple Message assigned ID if type could be mapped, ``int``
    :raises: :exc:``ValueError`` If type could not be mapped (ie: md5 could not be found)
    """
    for pkg, sums in mapping_dict.iteritems():
        if md5sum in sums:
            return sums[md5sum]

    # in real version, throw here
    raise ValueError("Cannot map '%s' to SM assigned ID. No match. Are all "
        "pkgs with mapping yamls on the ROS_PACKAGE_PATH?" % (md5sum))

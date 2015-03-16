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

class MappedType(object):
  def __init__(self, src_type, tgt_type, tgt_type_pfx=None, sm_id=None):
    self.src_type = src_type
    self.tgt_type = tgt_type
    self.tgt_type_pfx = tgt_type_pfx
    self.sm_id = sm_id

  def __str__(self):
    return "(%s; %s; %s; %s)" % (self.src_type, self.tgt_type,
        self.tgt_type_pfx, self.sm_id)


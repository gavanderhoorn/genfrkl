#!/usr/bin/env python
#
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

#
# Stand alone tool to calculate MD5 sum of a ROS msg file.
#

import os
import sys
import genmsg.command_line
import genmsg



if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser("[options] <msg file>")
    parser.add_option("-p", dest='package',
                      help="ros package the generated msg/srv files belongs to")
    parser.add_option("-I", dest='includepath',
                      help="include path to search for messages",
                      action="append")

    (options, argv) = parser.parse_args(sys.argv)

    if( not options.package):
        parser.print_help()
        exit(-1)


    if len(argv) > 1:
        package_name = options.package
        include_path = options.includepath
        input_file = argv[1]

        # setup context and msg spec
        msg_context = genmsg.msg_loader.MsgContext.create_default()
        full_type_name = genmsg.gentools.compute_full_type_name(package_name, os.path.basename(input_file))

        if input_file.endswith(".msg"):
            spec = genmsg.msg_loader.load_msg_from_file(msg_context, input_file, full_type_name)
        elif input_file.endswith(".srv"):
            spec = genmsg.msg_loader.load_srv_from_file(msg_context, input_file, full_type_name)
        else:
            assert False, "Uknown file extension for %s"%input_file

        search_path = genmsg.command_line.includepath_to_dict(include_path)
        genmsg.msg_loader.load_depends(msg_context, spec, search_path)

        # calc md5
        md5sum = genmsg.gentools.compute_md5(msg_context, spec)

        sys.stdout.write(md5sum + '\n')

    else:
        parser.print_help()
        exit(-1)

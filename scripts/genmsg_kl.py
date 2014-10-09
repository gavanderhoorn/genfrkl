#!/usr/bin/env python


"""
ROS message source code generation for Fanuc Karel

Converts ROS .msg files in a package into Karel source code implementations.
"""

import sys
import genmsg.template_tools

msg_template_map = {
                    'msg.th.template' : '@NAME@.th.kl',
                    'msg.h.template' : '@NAME@.h.kl',
                    'msg.kl.template': '@NAME@.kl',
                   }
srv_template_map = {}

if __name__ == "__main__":
    genmsg.template_tools.generate_from_command_line_options(sys.argv,
                                                             msg_template_map,
                                                             srv_template_map)

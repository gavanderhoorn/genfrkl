#!/usr/bin/env python


"""
ROS message source code generation for Fanuc Karel

Converts ROS .msg files in a package into Karel source code implementations.
"""

import sys
import os
import genmsg.template_tools
import genmsg


# default map
msg_template_map = {
                    'msg.th.template' : '@NAME@.th.kl',
                    'msg.h.template' : '@NAME@.h.kl',
                    'msg.kl.template': '@NAME@.kl',
                   }

srv_template_map = {}


def get_md5_for_msg(input_file, package_name, include_path):
    # setup
    msg_context = genmsg.msg_loader.MsgContext.create_default()
    full_type_name = genmsg.gentools.compute_full_type_name(package_name, os.path.basename(input_file))
    spec = genmsg.msg_loader.load_msg_from_file(msg_context, input_file, full_type_name)
    search_path = genmsg.command_line.includepath_to_dict(include_path)
    genmsg.msg_loader.load_depends(msg_context, spec, search_path)

    # calc md5
    md5sum = genmsg.gentools.compute_md5(msg_context, spec)
    return md5sum


def map_md5_to_sm_id(sm_ids_file, md5sum):
    import genfrkl
    sm_id_data = genfrkl.load_id_mapper_file(sm_ids_file)
    return sm_id_data[md5sum]


def gen_msg_template_map(sm_assigned_id):
    return {
        #'msg.th.template' : os.path.join('include', 'libsm%04X.th.kl' % sm_assigned_id),
        #'msg.h.template'  : os.path.join('include', 'libsm%04X.h.kl' % sm_assigned_id),
        'msg.th.template' : 'libsm%04X.th.kl' % sm_assigned_id,
        'msg.h.template'  : 'libsm%04X.h.kl' % sm_assigned_id,
        'msg.kl.template' : 'libsm%04X.kl' % sm_assigned_id,
    }


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser("[options] <srv file>")
    parser.add_option("-p", dest='package',
                      help="ros package the generated msg/srv files belongs to")
    parser.add_option("-o", dest='outdir',
                      help="directory in which to place output files")
    parser.add_option("-I", dest='includepath',
                      help="include path to search for messages",
                      action="append")
    parser.add_option("-m", dest='module',
                      help="write the module file",
                      action='store_true', default=False)
    parser.add_option("-e", dest='emdir',
                      help="directory containing template files",
                      default=sys.path[0])
    parser.add_option("-l", dest='assigned_ids_yaml',
                      help="File containing MD5 to Simple Message ID mappings",
                      default='sm_assigned_ids.yaml')

    (options, argv) = parser.parse_args(sys.argv)

    if( not options.package or not options.outdir or not options.emdir or not options.assigned_ids_yaml):
        parser.print_help()
        exit(-1)


    if len(argv) > 1:
        # use md5 for msg to retrieve SM assigned ID, use that to construct template map
        md5sum = get_md5_for_msg(argv[1], options.package, options.includepath)
        sm_id = map_md5_to_sm_id(options.assigned_ids_yaml, md5sum)

        msg_template_dict = gen_msg_template_map(sm_id)
        srv_template_dict = srv_template_map

        genmsg.template_tools.generate_from_file(argv[1], options.package, options.outdir, options.emdir, options.includepath, msg_template_dict, srv_template_dict)

    else:
        parser.print_help()
        exit(-1)

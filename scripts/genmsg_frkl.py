#!/usr/bin/env python


"""
ROS message source code generation for Fanuc Karel

Converts ROS .msg files in a package into Karel source code implementations.
"""

import sys
import os

import genmsg
import genmsg.command_line
import genmsg.gentools
import genmsg.msgs
import genmsg.msg_loader
import genmsg.template_tools


# default maps
msg_template_map = {
    'msg.th.template' : '@NAME@.th.kl',
    'msg.h.template'  : '@NAME@.h.kl',
    'msg.kl.template' : '@NAME@.kl',
}

srv_template_map = {
    'srv.th.template' : '@NAME@.th.kl',
    'srv.h.template'  : '@NAME@.h.kl',
    'srv.kl.template' : '@NAME@.kl',
}


def _generate_srv_from_file(input_file, output_dir, template_dir, search_path, package_name, srv_template_dict, msg_template_dict):
    # Read MsgSpec from .srv.file
    msg_context = genmsg.msg_loader.MsgContext.create_default()
    full_type_name = genmsg.gentools.compute_full_type_name(package_name, os.path.basename(input_file))
    spec = genmsg.msg_loader.load_srv_from_file(msg_context, input_file, full_type_name)
    # Load the dependencies
    genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    # Generate the language dependent srv file
    genmsg.template_tools._generate_from_spec(input_file,
                        output_dir,
                        template_dir,
                        msg_context,
                        spec,  # contains both .request and .response
                        srv_template_dict,
                        search_path)


# 'override' just this single method in template_tools
genmsg.template_tools._generate_srv_from_file = _generate_srv_from_file


def get_md5_for_msg(input_file, package_name, include_path):
    # setup
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
    return md5sum


def map_md5_to_sm_id(sm_ids_file, md5sum):
    import genfrkl
    sm_id_data = genfrkl.load_id_mapper_file(sm_ids_file)
    return sm_id_data[md5sum]


def gen_msg_template_map(sm_assigned_id):
    for k, v in msg_template_map.iteritems():
        msg_template_map[k] = v.replace('@NAME@', 'libsm%04X' % sm_assigned_id)
    return msg_template_map


def gen_srv_template_map(sm_assigned_id):
    for k, v in srv_template_map.iteritems():
        srv_template_map[k] = v.replace('@NAME@', 'libsm%04X' % sm_assigned_id)
    return srv_template_map


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

    if(not options.package or not options.outdir or not options.emdir or not options.assigned_ids_yaml):
        parser.print_help()
        exit(-1)


    if len(argv) > 1:
        input_file = argv[1]

        # use md5 for msg to retrieve SM assigned ID, use that to construct template map
        md5sum = get_md5_for_msg(input_file, options.package, options.includepath)
        sm_id = map_md5_to_sm_id(options.assigned_ids_yaml, md5sum)

        msg_template_dict = gen_msg_template_map(sm_id)
        srv_template_dict = gen_srv_template_map(sm_id)

        genmsg.template_tools.generate_from_file(input_file, options.package, options.outdir, options.emdir, options.includepath, msg_template_dict, srv_template_dict)

    else:
        parser.print_help()
        exit(-1)

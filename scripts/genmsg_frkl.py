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
# ROS message source code generation for Fanuc Karel.
#
# Converts ROS .msg files in a package into Karel source code implementations.
#

import em
import os
import sys
import yaml

import genmsg
import genmsg.command_line
import genmsg.gentools
import genmsg.msg_loader
import genmsg.msgs
import genmsg.srvs
import genmsg.template_tools

import rospkg

import genfrkl
import genfrkl.field_info



msg_template_map = {
    'msg.th.template' : '@NAME@.th.kl',
    'msg.h.template'  : '@NAME@.h.kl',
    'msg.kl.template' : '@NAME@.kl'
}

srv_template_map = {
    'srv.th.template' : '@NAME@.th.kl',
    'srv.h.template'  : '@NAME@.h.kl',
    'srv.kl.template' : '@NAME@.kl'
}



# global here. Not nice, but this way _generate_from_spec(..) can access it
# after we populate it from the yamls in main()
_mapping_dict = {}


def _map_types(spec, search_path, mapping_dict):
    """
    Maps each ROS message type in 'spec' onto the corresponding Karel type.

    If the ROS type would be a primitive (or built-in) Karel type, this is easy.
    For ROS types that are complex (ie: entire ROS messages), this needs a
    mapping based on some unique property of the type. In this case we use the
    MD5 of the ROS message (as that is already easily available, and any change
    to the ROS message type should result in either the inability to map, or in
    a new ID being returned).

    :param spec: :class:`MsgSpec` to map all message types for.
    :param search_path: dictionary mapping message namespaces to a directory locations, ``{str:str}``
    :param mapping_dict: nested dictionary mapping pkg names to dicts containing (md5sum, id) pairs
    :returns: dictionary mapping ROS (non-built-in) message types to Karel message types, ``{str:FieldInfo}``
    """
    mapped_types = {}

    for field in spec.parsed_fields():
      if genfrkl.maps_to_karel_primitive(field.base_type):
        tgt_type = genfrkl.map_builtin_to_karel(field.base_type)
        mapped_types[field.base_type] = genfrkl.field_info.MappedType(field.base_type, tgt_type)

      else:
        tgt_type_id  = genfrkl.ros_type_to_sm_id(spec.package, field.base_type, search_path, mapping_dict)
        tgt_type     = genfrkl.fmt_sm_type(tgt_type_id)
        tgt_type_pfx = genfrkl.fmt_sm_name(tgt_type_id)
        mapped_types[field.base_type] = genfrkl.field_info.MappedType(field.base_type, tgt_type, tgt_type_pfx, tgt_type_id)

    return mapped_types


"""
We 'override' this method here, then inject it into template_tools.

This version adds some additional <key, value> pairs to the EmPy globals
dictionary needed by the Karel templates.

In particular, we add the mapping dictionary which contains for each
message type used in 'spec' the corresponding Simple Message Assigned ID
and type info, and 

See the method def in genmsg.template_tools for the original documentation of
_generate_from_spec(..).
"""
def _generate_from_spec(input_file, output_dir, template_dir, msg_context, spec, template_map, search_path):
    md5sum = genmsg.gentools.compute_md5(msg_context, spec)

    # precompute msg definition once
    if isinstance(spec, genmsg.msgs.MsgSpec):
        msg_definition = genmsg.gentools.compute_full_text(msg_context, spec)

    # map all non-built-in ROS types to their Simple Message Assigned IDs
    if isinstance(spec, genmsg.msgs.MsgSpec):
        mapped_types = _map_types(spec, search_path, _mapping_dict)
    elif isinstance(spec, genmsg.srvs.SrvSpec):
        mapped_types = _map_types(spec.request, search_path, _mapping_dict)
        mapped_types.update(_map_types(spec.response, search_path, _mapping_dict))

    # map spec we are generating for currently
    # note that we don't use genfrkl.ros_type_to_sm_id(..) here, as we
    # already have the md5sum of the message spec we are generating for
    spec_tgt_type_id = genfrkl.msg_mapping.map_md5_to_sm_id(_mapping_dict, md5sum)

    kl_smname        = genfrkl.fmt_sm_name(spec_tgt_type_id)
    kl_structname    = genfrkl.fmt_sm_type(spec_tgt_type_id)
    kl_libname       = genfrkl.fmt_sm_libname(spec_tgt_type_id)
    msg_id_hex       = '%04X' % spec_tgt_type_id

    #print "DEBUG: spec_tgt_type_id: %d" % spec_tgt_type_id

    # Loop over all files to generate
    for template_file_name, output_file_name in template_map.items():
        template_file = os.path.join(template_dir, template_file_name)
        output_file = os.path.join(output_dir, output_file_name.replace("@NAME@", spec.short_name))

        #print "generate_from_template %s %s %s" % (input_file, template_file, output_file)

        ofile = open(output_file, 'w') #todo try

        # Set dictionary for the generator interpreter
        g = {
            "file_name_in": input_file,
            "spec": spec,
            "md5sum": md5sum,
            "search_path": search_path,
            "msg_context": msg_context
        }
        if isinstance(spec, genmsg.msgs.MsgSpec):
            g['msg_definition'] = msg_definition

        # add Simple Message data
        g["mapped_types"] = mapped_types
        g["kl_smname"] = kl_smname
        g["kl_structname"] = kl_structname
        g["kl_libname"] = kl_libname
        g["msg_id_hex"] = msg_id_hex
        g["mapped_msg_type"] = spec_tgt_type_id

        # todo, reuse interpreter
        interpreter = em.Interpreter(output=ofile, globals=g, options={em.RAW_OPT:True,em.BUFFERED_OPT:True})
        if not os.path.isfile(template_file):
            ofile.close()
            os.remove(output_file)
            raise RuntimeError("Template file %s not found in template dir %s" % (template_file_name, template_dir))
        interpreter.file(open(template_file)) #todo try
        interpreter.shutdown()

genmsg.template_tools._generate_from_spec = _generate_from_spec


"""
We 'override' this method here, then inject it into template_tools.

Simple Message services are different from ROS services in that they do not use
a pair of messages, but a single message. The 'comm_type' field is set to either
a 'svc request' or 'svc reply' to indicate to a receiver that an incoming msg is
actually a service.

In order to be able to generate Karel sources for this, we call
'_generate_from_spec()' just once, giving it the complete srv spec, containing
both the request and response parts.
"""
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

genmsg.template_tools._generate_srv_from_file = _generate_srv_from_file


MAPPING_EXPORT_KEY='simple_msgs'
MAPPING_EXPORT_ATTR='mappings'

def collect_mapping_file_paths(search_path=None, export_key=MAPPING_EXPORT_KEY, export_attr=MAPPING_EXPORT_ATTR):
    rp = rospkg.RosPack(ros_paths=search_path)
    # TODO: this returns all pkgs on the pkg path, maybe not too efficient
    pkgs = rp.list()

    path_dict = {}
    for pkg in pkgs:
        # TODO: if faster: first check for non-empty exports section, then retrieve
        mapping_exports = rp.get_manifest(pkg).get_export(export_key, export_attr)
        # TODO: do we need to fixup paths on Windows (forward slashes to double bw)?
        if len(mapping_exports) > 0:
            path_dict[pkg] = mapping_exports

    return path_dict


def load_mapping_yamls(path_dict):
    mapping_dict = {}
    for pkg, paths in path_dict.iteritems():
        for path in paths:
            try:
                with open(path, 'r') as f:
                    doc = yaml.safe_load(f)
                    for k in doc:
                        if isinstance(doc[k], dict):
                            if k in mapping_dict:
                                mapping_dict[k].update(doc[k])
                            else:
                                mapping_dict[k] = doc[k]
            except Exception, e:
                sys.stderr.write("Couldn't load mapping file '%s': %s\n" % (path, e))
    return mapping_dict


# TODO: refactor candidate: method body duplicated in calc_msg_md5.py script
def get_md5_for_msg(input_file, package_name, include_path):
    msg_context = genmsg.msg_loader.MsgContext.create_default()
    full_type_name = genmsg.gentools.compute_full_type_name(package_name, os.path.basename(input_file))

    if input_file.endswith(".msg"):
        spec = genmsg.msg_loader.load_msg_from_file(msg_context, input_file, full_type_name)
    elif input_file.endswith(".srv"):
        spec = genmsg.msg_loader.load_srv_from_file(msg_context, input_file, full_type_name)
    else:
        assert False, "Uknown file extension for %s" % input_file

    search_path = genmsg.command_line.includepath_to_dict(include_path)
    genmsg.msg_loader.load_depends(msg_context, spec, search_path)

    md5sum = genmsg.gentools.compute_md5(msg_context, spec)
    return md5sum


def update_template_map(id, map_dict):
    for k, v in map_dict.iteritems():
        map_dict[k] = v.replace('@NAME@', 'libsm%04X' % id)


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
    parser.add_option("-e", dest='emdir',
                      help="directory containing template files",
                      default=sys.path[0])
    parser.add_option("-l", dest='mapping_path',
                      help="Path to search for Simple Message ID mapping yamls",
                      action="append",
                      default=[])

    (options, argv) = parser.parse_args(sys.argv)

    if(not options.package or not options.outdir or not options.emdir):
        # we don't care whether user has provided us with any mapping_paths,
        # if she hasn't, we simply cannot map, but that will be reported
        # later.
        parser.print_help()
        exit(-1)

    if len(argv) > 1:
        input_file = argv[1]

        # collect mapping yamls
        # TODO: perhaps we should only load yamls in those pkgs that are listed
        #       as build_depends in the manifest of the pkg that contains the
        #       msgs for which we are generating? We'll get these from catkin,
        #       passed to use via the '-I' option.
        # TODO: perhaps first reverse return of get_ros_paths(), to make sure
        #       overlay workspaces can override assigned IDs in yamls that are
        #       loaded later.
        ros_paths = rospkg.get_ros_paths()
        yaml_paths = collect_mapping_file_paths(search_path=ros_paths.extend(options.mapping_path))
        _mapping_dict = load_mapping_yamls(yaml_paths)

        # use md5 for msg to retrieve SM assigned ID, then use that to construct template maps
        md5sum = get_md5_for_msg(input_file, options.package, options.includepath)
        sm_id = genfrkl.msg_mapping.map_md5_to_sm_id(_mapping_dict, md5sum)

        update_template_map(sm_id, msg_template_map)
        update_template_map(sm_id, srv_template_map)

        # generate the sources
        genmsg.template_tools.generate_from_file(input_file, options.package, options.outdir,
            options.emdir, options.includepath, msg_template_map, srv_template_map)

    else:
        parser.print_help()
        exit(-1)

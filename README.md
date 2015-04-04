# genfrkl

ROS Message generator for Fanuc Karel.


## Overview

This package provides a ROS [genmsg][] compatible code generator that is
capable of generating Fanuc Karel source code from ROS [messages][] and
[services][]. It can be used both as part of the build process (and is then
invoked by Catkin), or as a stand-alone utility. Generated Karel sources
implement a ROS-Industrial [simple_message][] compatible binary protocol
(de)serialiser, and can be used with either the generic client nodes in the
ROS-Industrial [industrial_robot_client][] package, or any other compatible
implementation of the protocol (note that client side support for any
custom messages will still need to be manually added to the relevant nodes).


## State, known issues & limitations

 - basic generation of Karel for ROS messages and services working
 - no support for dynamic arrays (lists) on the Karel side
 - identifiers with length > 12 are not supported by Karel. The generator
   will add these to the code, but Roboguide and `ktrans` will error out
   when trying to compile the resulting code
 - no support for ROS string fields yet
 - ROS message and service types can only be translated if a mapping has
   been defined onto a Simple Message Identifier. Mappings for the officially
   registered *Standard Message Set* are supplied. Project-specific or custom
   messages may be mapped onto the *Freely assignable* ranges.
   See [REP-I0004][] for more information.

Please report any additional problems and / or bugs to the Github
[issue tracker][].


## Dependencies

 - Python 2.7.x (probably not compatible with Python 3)
 - [genmsg][]
 - [rospkg][]
 - PyYAML (tested with v3.10)


## Installation

### Linux with ROS

TODO.

### Linux without ROS

TODO.

### Windows

TODO.


## FAQ

 - Do I need a ROS installation to use this?

   No, the generator is a Python-only project with no dependencies on ROS
   other than `genmsg` and `rospkg` which are also Python libraries. All
   dependencies can be installed by using the package manager, `pip` or by
   simply checking out the sources and making sure they are on the
   `PYTHONPATH`.

 - Can this be run on Windows?

   Yes. All dependencies can be installed on Windows and there is no platform
   specific code in any of the execution paths.

   Windows compatibility was one of the main requirements and in fact most of
   the initial development was done under Windows. As Fanuc Roboguide is a
   Windows-only program, I wanted to keep the development overhead as low as
   possible by making sure I wouldn't need an additional Linux machine or VM
   just for running the generator.

 - Can this be used with any ROS message and / or service?

   In principle: yes, but the message or service needs to have been assigned
   a Simple Message `msg_type` Identifier, and that mapping must be made
   available to the generator. Note that no dependency analysis is performed
   by the generator, so if a message `A` requires code for message type `B`
   to be present on the controller, this will not be detected until runtime.

 - Can I use this with something other than simple_message?

   Not in its current state, but the (de)serialisers can be changed to work
   with any binary (or even text-based) protocol. This would require
   (significant) changes to the templates though and it would probably make
   more sense to do this in a separate package.


## Usage

In order to be able to generate [simple_message][] compatible Karel sources,
the generator needs access to a mapping between ROS messages and Simple
Message assigned Identifiers (ID). Those IDs are either assigned by the
ROS-Industrial developers (for the *Standard Set*) or may be picked by users
from the *Freely assignable* range, as documented in [REP-I0004][].
For ROS messages or services that are mapped onto the *Freely assignable*
range, it is the users responsibility to make sure no duplicate assignments
are made, as the (de)serialisers are not equiped to detect nor handle those.

TODO: finish this.

### Examples:

 - In a ROS catkin workspace: just clone the package into the workspace,
   catkin should take care of the rest. Not recommended, as the working
   state of the generator is such that it will probably abort your build.

 - Stand-alone: invoke like:
   ```
   scripts/genmsg_frkl.py -p PKG -I MSG_INCLUDE_PATHs -o OUTPUT_PATH -e scripts -l MAPPING_YAML_PATHs /path/to/PKG/your.msg
   ```
   or:
   ```
   scripts/genmsg_frkl.py -p PKG -I MSG_INCLUDE_PATHs -o OUTPUT_PATH -e scripts -l MAPPING_YAML_PATHs /path/to/PKG/your.srv
   ```

   This should result in several `.kl` files being generated in `OUTPUT_PATH`.


[genmsg]: https://github.com/ros/genmsg
[messages]: http://wiki.ros.org/msg
[services]: http://wiki.ros.org/srv
[simple_message]: http://wiki.ros.org/simple_message
[industrial_robot_client]: http://wiki.ros.org/industrial_robot_client
[REP-I0004]: https://github.com/ros-industrial/rep/blob/master/rep-I0004.rst
[rospkg]: http://wiki.ros.org/rospkg
[issue tracker]: https://github.com/gavanderhoorn/genfrkl/issues

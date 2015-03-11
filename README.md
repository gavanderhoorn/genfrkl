# genfrkl

ROS Message generator for Fanuc Karel.

Not really meant as a general purpose message generator, but for use
with [simple_message][].

Current state:

 - basic generation of Karel for ROS msgs and srvs working
 - no support for dynamic arrays (lists)
 - no support for identifiers with length > 12
 - no (proper) support for string fields
 - only works with ROS msgs that have been assigned a simple_message
   message identifier (see [REP-I0004][])


## Usage

 - In a ROS catkin workspace: just clone the package into the workspace,
   catkin should take care of the rest. Not recommended, as the working
   state of the generator is such that it will probably abort your build.

 - Stand-alone: invoke like:
   ```
   scripts/genmsg_frkl.py -p PKG -IMSG_INCLUDE_PATHS -o OUTPUT_PATH -e scripts /path/to/PKG/your.msg
   ```
   or:
   ```
   scripts/genmsg_frkl.py -p PKG -IMSG_INCLUDE_PATHS -o OUTPUT_PATH -e scripts /path/to/PKG/your.srv
   ```

   This should result in several `.kl` files being generated in `OUTPUT_PATH`.


[simple_message]: http://wiki.ros.org/simple_message
[REP-I0004]: https://github.com/ros-industrial/rep/blob/master/rep-I0004.rst

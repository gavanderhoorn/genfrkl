# genfrkl

ROS Message generator for Fanuc Karel.

Not really meant as a general purpose message generator, but for use
with [simple_message][].

Current state:

 - basic generation of Karel for ROS msgs working
 - no support for dynamic arrays (lists)
 - no support for identifiers with length > 12
 - no (proper) support for string fields
 - only works with ROS msgs that have been assigned a simple_message
   message identifier (see [REP-I0004][])


[simple_message]: http://wiki.ros.org/simple_message
[REP-I0004]: https://github.com/ros-industrial/rep/blob/master/rep-I0004.rst

# Todo

 - style: pass 'this' arg to all 'methods' (avoid confusion with 'lower case
   constants')
 - work around identifier name length limit (can't go and change all
   existing msg defs)
 - make `x_len()` work for dynamically sized messages:
   - return `> 0` for statically defined messages (no dynamic arrays fi)
   - return `-1` for dynamically sized messages (then have `x_read()` return
     the nr of additional bytes it needs if it can't completely deserialise
     a message from the current buffer)
 - make `x_read()` capable of reading messages in multiple passes (see comment
   about `x_len()`. Use a (small) internal state machine to keep track of what
   has been deserialised already)
 - add support for variable length arrays
 - remove code duplication in '_wrte' and '_read' routine templates.
 - do something with STRING\[n\] (KAREL) and char\[\] (ROS) arrays?
 - use yaml id db for generation of header include statements
 - load yaml id db using pkg resource api:
   - load one yaml id db for each msg pkg on include path?
 - do something about mess in service templates


# In progress

 - implement additional routines:
   - `x_tstr()`
   - `x_len()`
   - `x_sread()`
   - `x_swrte()`
 - provide ros msg -> simple msg assigned id as yaml file on command line
   - allow multiple mapping files to be provided: this way the 'freely assignable'
     range can be exploited: users can provide their own mapping file
 - add support for services:
   - add service bits to genmsg_frkl.py
   - create srv template files
   - make genfrkl output only a single KL file for services (use asymmetric
     READ / WRITE)
   - avoid duplication in generator code
 - check for illegal declarations (ie: arrays with 0 length)?


# Done

 - add array helper vars only when necessary (there are arrays in msg)
 - optimise generated READ/WRITE statements:
   - group primitive READs/WRITEs
   - unroll array READs/WRITEs
 - rename output files according to mapped type (`librpNNNN`)
 - add license
 - enforce identifier name length limit (12 characters)
 - filter reserved words (ON / OFF, OPEN, etc)
 - create stand-alone tool to calculate MD5 of ROS msg / srv files
 - add Simple Message assigned message type to `msg_type` mapping function


# Wontfix

 - inject 'rp_hdr_t hdr' into msgs that don't have a header (typically that
   would be with 'normal' ROS msgs)  ---> DON'T do this: cannot re-use those
   types in composite msgs otherwise (embedded headers?)

# Todo

  - rename output files according to mapped type (`librpNNNN`)
  - add license
  - enforce identifier name length limit (12 characters)
  - add Simple Message assigned message type to `msg_type` mapping function
  - make `x_len()` work for dynamically sized messages:
    - return `> 0` for statically defined messages (no dynamic arrays fi)
    - return `-1` for dynamically sized messages (then have `x_read()` return
      the nr of additional bytes it needs if it can't completely deserialise
      a message from the current buffer)
  - make `x_read()` capable of reading messages in multiple passes (see comment
    about `x_len()`. Use a (small) internal state machine to keep track of what
    has been deserialised already)
  - implement `x_tstr()`, `x_len()`, `x_sread()` and `x_swrte()`
  - optimise generated READ/WRITE statements:
X   - group primitive READs/WRITEs
    - unroll array READs/WRITEs
  - add support for variable length arrays
  - add array helper vars only when necessary (there are arrays in msg)
  - remove code duplication in '_wrte' and '_read' routine templates.

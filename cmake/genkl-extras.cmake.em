@[if DEVELSPACE]@
# bin and template dir variables in develspace
set(GENKL_BIN "@(CMAKE_CURRENT_SOURCE_DIR)/scripts/genmsg_kl.py")
set(GENKL_TEMPLATE_DIR "@(CMAKE_CURRENT_SOURCE_DIR)/scripts")
@[else]@
# bin and template dir variables in installspace
set(GENKL_BIN "${genkl_DIR}/../../../@(CATKIN_PACKAGE_BIN_DESTINATION)/genmsg_kl.py")
set(GENKL_TEMPLATE_DIR "${genkl_DIR}/..")
@[end if]@

# Generate .msg->(.th,.h,).kl for Fanuc Karel
# The generated files should all be added ALL_GEN_OUTPUT_FILES_kl
macro(_generate_msg_kl ARG_PKG ARG_MSG ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)

  # FIXME: put generated code in source space for now
  set(GEN_OUTPUT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/kl/${ARG_PKG}")

  #file(MAKE_DIRECTORY ${ARG_GEN_OUTPUT_DIR})
  file(MAKE_DIRECTORY ${GEN_OUTPUT_DIR})

  #Create input and output filenames
  get_filename_component(MSG_NAME ${ARG_MSG} NAME)
  get_filename_component(MSG_SHORT_NAME ${ARG_MSG} NAME_WE)

  # should probably expand this to include all three generated files
  set(MSG_GENERATED_NAME ${MSG_SHORT_NAME}.kl)
  #set(GEN_OUTPUT_FILE ${ARG_GEN_OUTPUT_DIR}/${MSG_GENERATED_NAME})
  set(GEN_OUTPUT_FILE ${GEN_OUTPUT_DIR}/${MSG_GENERATED_NAME})

  assert(CATKIN_ENV)
  add_custom_command(OUTPUT ${GEN_OUTPUT_FILE}
    DEPENDS ${GENKL_BIN} ${ARG_MSG} ${ARG_MSG_DEPS} "${GENKL_TEMPLATE_DIR}/msg.h.template"
      "${GENKL_TEMPLATE_DIR}/msg.th.template" "${GENKL_TEMPLATE_DIR}/msg.kl.template" ${ARGN}
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENKL_BIN} ${ARG_MSG}
    ${ARG_IFLAGS}
    -p ${ARG_PKG}
    -o ${GEN_OUTPUT_DIR} #-o ${ARG_GEN_OUTPUT_DIR}
    -e ${GENKL_TEMPLATE_DIR}
    COMMENT "Generating Fanuc Karel code for ${ARG_PKG}/${MSG_NAME}"
    )
  list(APPEND ALL_GEN_OUTPUT_FILES_kl ${GEN_OUTPUT_FILE})
endmacro()

macro(_generate_srv_kl ARG_PKG ARG_SRV ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  # services not supported right now
endmacro()

macro(_generate_module_kl)
  # them macros, they do nothing
endmacro()

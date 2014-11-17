@[if DEVELSPACE]@
# bin and template dir variables in develspace
set(GENFRKL_BIN "@(CMAKE_CURRENT_SOURCE_DIR)/scripts/genmsg_frkl.py")
set(GENFRKL_TEMPLATE_DIR "@(CMAKE_CURRENT_SOURCE_DIR)/scripts")
@[else]@
# bin and template dir variables in installspace
set(GENFRKL_BIN "${genfrkl_DIR}/../../../@(CATKIN_PACKAGE_BIN_DESTINATION)/genmsg_frkl.py")
set(GENFRKL_TEMPLATE_DIR "${genfrkl_DIR}/..")
@[end if]@

# Generate .msg->(.th,.h,).kl for Fanuc Karel
# The generated files should all be added to ALL_GEN_OUTPUT_FILES_frkl
macro(_generate_msg_frkl ARG_PKG ARG_MSG ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)

  # FIXME: put generated code in source space for now
  set(GEN_OUTPUT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/frkl/${ARG_PKG}")

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
    DEPENDS ${GENFRKL_BIN} ${ARG_MSG} ${ARG_MSG_DEPS} "${GENFRKL_TEMPLATE_DIR}/msg.h.template"
      "${GENFRKL_TEMPLATE_DIR}/msg.th.template" "${GENFRKL_TEMPLATE_DIR}/msg.kl.template" ${ARGN}
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENFRKL_BIN} ${ARG_MSG}
    ${ARG_IFLAGS}
    -p ${ARG_PKG}
    -o ${GEN_OUTPUT_DIR} #-o ${ARG_GEN_OUTPUT_DIR}
    -e ${GENFRKL_TEMPLATE_DIR}
    COMMENT "Generating Fanuc Karel code for ${ARG_PKG}/${MSG_NAME}"
    )
  list(APPEND ALL_GEN_OUTPUT_FILES_frkl ${GEN_OUTPUT_FILE})
endmacro()

macro(_generate_srv_frkl ARG_PKG ARG_SRV ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  # services not supported right now
endmacro()

macro(_generate_module_frkl)
  # them macros, they do nothing
endmacro()

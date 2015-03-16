cmake_minimum_required(VERSION 2.8.3)
project(genfrkl)
find_package(catkin REQUIRED COMPONENTS genmsg)

catkin_package(
  CATKIN_DEPENDS genmsg
  CFG_EXTRAS genfrkl-extras.cmake
)

add_subdirectory(scripts)

file(WRITE ${CATKIN_DEVEL_PREFIX}/${GENMSG_LANGS_DESTINATION}/genfrkl "Fanuc Karel")
install(FILES ${CATKIN_DEVEL_PREFIX}/${GENMSG_LANGS_DESTINATION}/genfrkl
  DESTINATION ${GENMSG_LANGS_DESTINATION})

catkin_python_setup()

if(CATKIN_ENABLE_TESTING)
  catkin_add_nosetests(test)
endif()

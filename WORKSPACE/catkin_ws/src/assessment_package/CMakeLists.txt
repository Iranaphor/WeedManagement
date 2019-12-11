cmake_minimum_required(VERSION 2.8.3)
project(assessment_package)


find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  rospy
  rostest
  std_msgs
  topological_navigation
  uol_cmp9767m_base
  roscpp
  rospy
  message_generation
)
add_message_files(
  FILES
  WeedList.msg
)
generate_messages(
  DEPENDENCIES
  std_msgs
)


catkin_package(
	CATKIN_DEPENDS message_runtime
)


include_directories( ${catkin_INCLUDE_DIRS} )
install(PROGRAMS
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
foreach (dir launch models config maps)
    install(DIRECTORY ${dir}/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)



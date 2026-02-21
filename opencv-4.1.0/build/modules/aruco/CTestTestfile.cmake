# CMake generated Testfile for 
# Source directory: /home/yun/opencv_contrib-4.1.0/modules/aruco
# Build directory: /home/yun/opencv-4.1.0/build/modules/aruco
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_aruco "/home/yun/opencv-4.1.0/build/bin/opencv_test_aruco" "--gtest_output=xml:opencv_test_aruco.xml")
set_tests_properties(opencv_test_aruco PROPERTIES  LABELS "Extra;opencv_aruco;Accuracy" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/cmake/OpenCVUtils.cmake;1547;add_test;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1282;ocv_add_test_from_target;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1069;ocv_add_accuracy_tests;/home/yun/opencv_contrib-4.1.0/modules/aruco/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv_contrib-4.1.0/modules/aruco/CMakeLists.txt;0;")

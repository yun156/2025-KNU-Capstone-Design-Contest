# CMake generated Testfile for 
# Source directory: /home/yun/opencv_contrib-4.1.0/modules/img_hash
# Build directory: /home/yun/opencv-4.1.0/build/modules/img_hash
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_img_hash "/home/yun/opencv-4.1.0/build/bin/opencv_test_img_hash" "--gtest_output=xml:opencv_test_img_hash.xml")
set_tests_properties(opencv_test_img_hash PROPERTIES  LABELS "Extra;opencv_img_hash;Accuracy" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/cmake/OpenCVUtils.cmake;1547;add_test;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1282;ocv_add_test_from_target;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1069;ocv_add_accuracy_tests;/home/yun/opencv_contrib-4.1.0/modules/img_hash/CMakeLists.txt;3;ocv_define_module;/home/yun/opencv_contrib-4.1.0/modules/img_hash/CMakeLists.txt;0;")

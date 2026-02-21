# CMake generated Testfile for 
# Source directory: /home/yun/opencv_contrib-4.8.1/modules/bgsegm
# Build directory: /home/yun/opencv-4.8.1/build/modules/bgsegm
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_bgsegm "/home/yun/opencv-4.8.1/build/bin/opencv_test_bgsegm" "--gtest_output=xml:opencv_test_bgsegm.xml")
set_tests_properties(opencv_test_bgsegm PROPERTIES  LABELS "Extra;opencv_bgsegm;Accuracy" WORKING_DIRECTORY "/home/yun/opencv-4.8.1/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/yun/opencv-4.8.1/cmake/OpenCVUtils.cmake;1763;add_test;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1375;ocv_add_test_from_target;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1133;ocv_add_accuracy_tests;/home/yun/opencv_contrib-4.8.1/modules/bgsegm/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv_contrib-4.8.1/modules/bgsegm/CMakeLists.txt;0;")

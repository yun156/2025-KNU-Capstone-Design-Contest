# CMake generated Testfile for 
# Source directory: /home/yun/opencv-4.1.0/build/opencv_contrib-4.8.1/modules/quality
# Build directory: /home/yun/opencv-4.1.0/build/opencv-4.8.1/build/modules/quality
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_quality "/home/yun/opencv-4.1.0/build/opencv-4.8.1/build/bin/opencv_test_quality" "--gtest_output=xml:opencv_test_quality.xml")
set_tests_properties(opencv_test_quality PROPERTIES  LABELS "Extra;opencv_quality;Accuracy" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/opencv-4.8.1/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/build/opencv-4.8.1/cmake/OpenCVUtils.cmake;1763;add_test;/home/yun/opencv-4.1.0/build/opencv-4.8.1/cmake/OpenCVModule.cmake;1375;ocv_add_test_from_target;/home/yun/opencv-4.1.0/build/opencv-4.8.1/cmake/OpenCVModule.cmake;1133;ocv_add_accuracy_tests;/home/yun/opencv-4.1.0/build/opencv_contrib-4.8.1/modules/quality/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv-4.1.0/build/opencv_contrib-4.8.1/modules/quality/CMakeLists.txt;0;")

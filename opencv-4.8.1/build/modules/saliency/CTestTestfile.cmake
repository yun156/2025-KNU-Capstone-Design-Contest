# CMake generated Testfile for 
# Source directory: /home/yun/opencv_contrib-4.8.1/modules/saliency
# Build directory: /home/yun/opencv-4.8.1/build/modules/saliency
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_saliency "/home/yun/opencv-4.8.1/build/bin/opencv_test_saliency" "--gtest_output=xml:opencv_test_saliency.xml")
set_tests_properties(opencv_test_saliency PROPERTIES  LABELS "Extra;opencv_saliency;Accuracy" WORKING_DIRECTORY "/home/yun/opencv-4.8.1/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/yun/opencv-4.8.1/cmake/OpenCVUtils.cmake;1763;add_test;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1375;ocv_add_test_from_target;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1133;ocv_add_accuracy_tests;/home/yun/opencv_contrib-4.8.1/modules/saliency/CMakeLists.txt;7;ocv_define_module;/home/yun/opencv_contrib-4.8.1/modules/saliency/CMakeLists.txt;0;")

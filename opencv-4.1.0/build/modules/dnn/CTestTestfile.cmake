# CMake generated Testfile for 
# Source directory: /home/yun/opencv-4.1.0/modules/dnn
# Build directory: /home/yun/opencv-4.1.0/build/modules/dnn
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_dnn "/home/yun/opencv-4.1.0/build/bin/opencv_test_dnn" "--gtest_output=xml:opencv_test_dnn.xml")
set_tests_properties(opencv_test_dnn PROPERTIES  LABELS "Main;opencv_dnn;Accuracy" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/cmake/OpenCVUtils.cmake;1547;add_test;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1282;ocv_add_test_from_target;/home/yun/opencv-4.1.0/modules/dnn/CMakeLists.txt;91;ocv_add_accuracy_tests;/home/yun/opencv-4.1.0/modules/dnn/CMakeLists.txt;0;")
add_test(opencv_perf_dnn "/home/yun/opencv-4.1.0/build/bin/opencv_perf_dnn" "--gtest_output=xml:opencv_perf_dnn.xml")
set_tests_properties(opencv_perf_dnn PROPERTIES  LABELS "Main;opencv_dnn;Performance" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/test-reports/performance" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/cmake/OpenCVUtils.cmake;1547;add_test;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1189;ocv_add_test_from_target;/home/yun/opencv-4.1.0/modules/dnn/CMakeLists.txt;96;ocv_add_perf_tests;/home/yun/opencv-4.1.0/modules/dnn/CMakeLists.txt;0;")
add_test(opencv_sanity_dnn "/home/yun/opencv-4.1.0/build/bin/opencv_perf_dnn" "--gtest_output=xml:opencv_perf_dnn.xml" "--perf_min_samples=1" "--perf_force_samples=1" "--perf_verify_sanity")
set_tests_properties(opencv_sanity_dnn PROPERTIES  LABELS "Main;opencv_dnn;Sanity" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/test-reports/sanity" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/cmake/OpenCVUtils.cmake;1547;add_test;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1190;ocv_add_test_from_target;/home/yun/opencv-4.1.0/modules/dnn/CMakeLists.txt;96;ocv_add_perf_tests;/home/yun/opencv-4.1.0/modules/dnn/CMakeLists.txt;0;")

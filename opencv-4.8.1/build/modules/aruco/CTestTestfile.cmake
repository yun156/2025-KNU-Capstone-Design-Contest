# CMake generated Testfile for 
# Source directory: /home/yun/opencv_contrib-4.8.1/modules/aruco
# Build directory: /home/yun/opencv-4.8.1/build/modules/aruco
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_aruco "/home/yun/opencv-4.8.1/build/bin/opencv_test_aruco" "--gtest_output=xml:opencv_test_aruco.xml")
set_tests_properties(opencv_test_aruco PROPERTIES  LABELS "Extra;opencv_aruco;Accuracy" WORKING_DIRECTORY "/home/yun/opencv-4.8.1/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/yun/opencv-4.8.1/cmake/OpenCVUtils.cmake;1763;add_test;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1375;ocv_add_test_from_target;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1133;ocv_add_accuracy_tests;/home/yun/opencv_contrib-4.8.1/modules/aruco/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv_contrib-4.8.1/modules/aruco/CMakeLists.txt;0;")
add_test(opencv_perf_aruco "/home/yun/opencv-4.8.1/build/bin/opencv_perf_aruco" "--gtest_output=xml:opencv_perf_aruco.xml")
set_tests_properties(opencv_perf_aruco PROPERTIES  LABELS "Extra;opencv_aruco;Performance" WORKING_DIRECTORY "/home/yun/opencv-4.8.1/build/test-reports/performance" _BACKTRACE_TRIPLES "/home/yun/opencv-4.8.1/cmake/OpenCVUtils.cmake;1763;add_test;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1274;ocv_add_test_from_target;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1134;ocv_add_perf_tests;/home/yun/opencv_contrib-4.8.1/modules/aruco/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv_contrib-4.8.1/modules/aruco/CMakeLists.txt;0;")
add_test(opencv_sanity_aruco "/home/yun/opencv-4.8.1/build/bin/opencv_perf_aruco" "--gtest_output=xml:opencv_perf_aruco.xml" "--perf_min_samples=1" "--perf_force_samples=1" "--perf_verify_sanity")
set_tests_properties(opencv_sanity_aruco PROPERTIES  LABELS "Extra;opencv_aruco;Sanity" WORKING_DIRECTORY "/home/yun/opencv-4.8.1/build/test-reports/sanity" _BACKTRACE_TRIPLES "/home/yun/opencv-4.8.1/cmake/OpenCVUtils.cmake;1763;add_test;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1275;ocv_add_test_from_target;/home/yun/opencv-4.8.1/cmake/OpenCVModule.cmake;1134;ocv_add_perf_tests;/home/yun/opencv_contrib-4.8.1/modules/aruco/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv_contrib-4.8.1/modules/aruco/CMakeLists.txt;0;")

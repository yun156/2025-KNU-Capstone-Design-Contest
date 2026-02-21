# CMake generated Testfile for 
# Source directory: /home/yun/opencv-4.1.0/modules/objdetect
# Build directory: /home/yun/opencv-4.1.0/build/modules/objdetect
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_objdetect "/home/yun/opencv-4.1.0/build/bin/opencv_test_objdetect" "--gtest_output=xml:opencv_test_objdetect.xml")
set_tests_properties(opencv_test_objdetect PROPERTIES  LABELS "Main;opencv_objdetect;Accuracy" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/cmake/OpenCVUtils.cmake;1547;add_test;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1282;ocv_add_test_from_target;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1069;ocv_add_accuracy_tests;/home/yun/opencv-4.1.0/modules/objdetect/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv-4.1.0/modules/objdetect/CMakeLists.txt;0;")
add_test(opencv_perf_objdetect "/home/yun/opencv-4.1.0/build/bin/opencv_perf_objdetect" "--gtest_output=xml:opencv_perf_objdetect.xml")
set_tests_properties(opencv_perf_objdetect PROPERTIES  LABELS "Main;opencv_objdetect;Performance" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/test-reports/performance" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/cmake/OpenCVUtils.cmake;1547;add_test;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1189;ocv_add_test_from_target;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1070;ocv_add_perf_tests;/home/yun/opencv-4.1.0/modules/objdetect/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv-4.1.0/modules/objdetect/CMakeLists.txt;0;")
add_test(opencv_sanity_objdetect "/home/yun/opencv-4.1.0/build/bin/opencv_perf_objdetect" "--gtest_output=xml:opencv_perf_objdetect.xml" "--perf_min_samples=1" "--perf_force_samples=1" "--perf_verify_sanity")
set_tests_properties(opencv_sanity_objdetect PROPERTIES  LABELS "Main;opencv_objdetect;Sanity" WORKING_DIRECTORY "/home/yun/opencv-4.1.0/build/test-reports/sanity" _BACKTRACE_TRIPLES "/home/yun/opencv-4.1.0/cmake/OpenCVUtils.cmake;1547;add_test;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1190;ocv_add_test_from_target;/home/yun/opencv-4.1.0/cmake/OpenCVModule.cmake;1070;ocv_add_perf_tests;/home/yun/opencv-4.1.0/modules/objdetect/CMakeLists.txt;2;ocv_define_module;/home/yun/opencv-4.1.0/modules/objdetect/CMakeLists.txt;0;")

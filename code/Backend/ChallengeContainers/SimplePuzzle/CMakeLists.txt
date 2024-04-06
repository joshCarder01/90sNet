cmake_minimum_required(VERSION 3.14)
project(SimplePuzzle VERSION 0.1.0 LANGUAGES C)

add_executable(SimplePuzzle src/simple.c)

find_package(SQLite3 REQUIRED)

include_directories(${SQLite3_INCLUDE_DIRS})
target_link_libraries(SimplePuzzle ${SQLite3_LIBRARIES})

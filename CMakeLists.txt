cmake_minimum_required(VERSION 3.16)
project(rng_bench CXX)

option(RNG_BENCH_ENABLE_MARCH_NATIVE "Enable -march=native" ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Compiler configuration ---
if (MSVC)
    add_compile_options(/O2 /DNOMINMAX /EHsc)
else()
    # For GCC/Clang (Linux, MinGW, etc.)
    add_compile_options(-O3 -std=gnu++20 -march=native -mavx2 -mfma -mbmi2 -fexceptions -frtti -DNOMINMAX)
endif()

add_executable(rng_bench
  src/main.cpp
)

target_include_directories(rng_bench PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/include/competitors
    ${CMAKE_CURRENT_SOURCE_DIR}/include/competitors/sfmt
)

if (WIN32)
  target_link_libraries(rng_bench PRIVATE ws2_32)
endif()

file(GLOB_RECURSE COMPETITOR_C "${CMAKE_CURRENT_SOURCE_DIR}/include/competitors/*.c")
if (COMPETITOR_C)
  target_sources(rng_bench PRIVATE ${COMPETITOR_C})
endif()

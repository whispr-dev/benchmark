# C-SIMD-RNG-Bench

# 

# Portable high-performance SIMD random number generator benchmark suite

# 

# Overview

# 

# This project benchmarks and compares SIMD-enabled RNG engines (your C-SIMD-RNG-Lib) against leading scalar and vector competitors (PCG, xoroshiro, xoshiro, SFMT, SIMDxorshift, EigenRand, and others).

# It produces statistically sound throughput metrics and exports results as CSV for analysis and graphing.

# 

# Key Features

# 

# Cross-platform (Windows / Linux / macOS)

# 

# Runtime ISA detection (SSE2 / AVX2 / AVX-512)

# 

# Multi-threaded benchmarking

# 

# CSV export for Python/Matplotlib post-analysis

# 

# Easily extensible competitor registry

# 

# Requirements

# 

# CMake ≥ 3.16

# 

# C++20 compiler

# 

# Optional: Intel oneAPI (for SVRNG comparison)

# 

# Tested with:

# 

# Windows 11 + MSVC 2022 / MSYS2 MinGW64

# 

# DragonOS Lubuntu (GCC 13+)

# 

# Build

# Windows (PowerShell)

# cmake -S . -B build -G "Ninja" -DCMAKE\_BUILD\_TYPE=Release

# cmake --build build --config Release

# 

# Linux

# cmake -S . -B build -G Ninja -DCMAKE\_BUILD\_TYPE=Release

# cmake --build build --config Release

# 

# 

# The executable will appear at build/rng\_bench\[.exe].

# 

# Usage

# ./rng\_bench \[options]

# 

# 

# Options:

# 

# --total N             total samples per generator (default 1e8)

# --threads T           number of threads

# --seed S              base seed (hex or decimal)

# --csv PATH            path to write CSV results

# --gens LIST           comma-separated list (std\_mt19937,pcg32,xoroshiro128pp,simdxorshift,csimd)

# --csimd-lib PATH      path to your C-SIMD-RNG shared library

# --csimd-algo ID       algorithm id (default 0)

# --csimd-bw BW         bitwidth (1=64-bit)

# 

# 

# Examples:

# 

# ./rng\_bench --total 200000000 --threads 8 \\

# &nbsp; --csv results.csv \\

# &nbsp; --gens std\_mt19937,pcg32,xoroshiro128pp,simdxorshift,csimd \\

# &nbsp; --csimd-lib ./libuniversal\_rng.so --csimd-algo 0 --csimd-bw 1

# 

# 

# Windows PowerShell:

# 

# .\\build\\rng\_bench.exe --total 200000000 --threads 8 `

# &nbsp; --csv results.csv `

# &nbsp; --gens std\_mt19937,pcg32,xoroshiro128pp,simdxorshift,csimd `

# &nbsp; --csimd-lib "C:\\GitHub\\C-SIMD-RNG-Lib\\lib\_files\\mingw\_shared\\universal\_rng.dll"

# 

# Output

# 

# The tool prints a formatted table:

# 

# generator          u64 ops/s      f64 ops/s      mean(f64)   var(f64)    chi2(bytes)  threads

# ----------------------------------------------------------------------------------------------

# std\_mt19937        42.30 M/s      40.89 M/s      0.499857    0.083251    0.73         8

# pcg32              92.15 M/s      89.40 M/s      0.500120    0.083333    1.04         8

# xoroshiro128pp     155.21 M/s     152.78 M/s     0.500023    0.083320    0.95         8

# simdxorshift       655.20 M/s     642.01 M/s     0.500001    0.083333    0.98         8

# csimd\_universal    10432.80 M/s   10410.35 M/s   0.500002    0.083333    1.01         8

# 

# 

# If --csv is specified, results are saved with:

# 

# generator,u64\_ops\_per\_s,f64\_ops\_per\_s,mean\_f64,var\_f64,chi2\_bytes,threads,total\_u64,total\_f64

# 

# Adding New Competitors

# 

# Place competitor source in include/competitors/

# 

# Create an adapter header with:

# 

# uint64\_t next\_u64();

# double next\_double();

# 

# 

# Add #include and entry in main.cpp if (wants("name")) block.

# 

# Rebuild and rerun.

# 

# Post-Analysis

# 

# Use analysis/analyze-results.py to generate plots:

# 

# cd analysis

# python3 analyze-results.py

# 

# 

# It creates:

# 

# plots/throughput-batch100000000-64bit.png

# 

# plots/scaling-64bit.png

# 

# results-agg/summary-agg.csv

# 

# License

# 

# MIT (for your benchmarker).

# Competitor libraries retain their own respective licenses.

# 

# Citation

# 

# If publishing results, cite Daniel Lemire’s SIMDxorshift and Intel oneMKL VSL for context.

# Acknowledge that your library extends the SIMD RNG concept to a general-purpose, runtime-adaptive implementation.


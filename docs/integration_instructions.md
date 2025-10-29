# Integration and Build Instructions (Platform-specific)

This file contains step-by-step instructions for building and running the benchmarker with UA RNG v1.7 across your platforms (WinMSVC, MSYS2, Linux, macOS).

## Pre-reqs
- CMake >= 3.16
- Ninja recommended
- MSVC (Visual Studio 2022) for WinMSVC
- MSYS2 (mingw64) for WinMSYS2
- GCC/Clang for Linux / macOS
- Python3 for post-analysis scripts (matplotlib)

Place the UA RNG v1.7 folder in a stable path; we assume:
`D:/code/Universal-Architecture-RNG-Lib/v1.7` (Windows) or `~/code/Universal-Architecture-RNG-Lib/v1.7` (Linux).

---
## 1) Using the distributed headers + shared libs (recommended)
No need to recompile UA lib: use prebuilt shared libs in the `lib/<platform>/` folders.

### Windows MSVC (native)
1. Build the benchmarker:
   ```powershell
   cd D:/code/rng-bench
   cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
   cmake --build build --config Release
   ```
2. Run:
   ```powershell
   .\build\rng_bench.exe --total 200000000 --threads 8 --csv results.csv --gens std_mt19937,pcg32,xoroshiro128pp,simdxorshift,csimd --csimd-lib "D:/code/Universal-Architecture-RNG-Lib/v1.7/win_msvc/ua_rng-1.7/lib/universal_rng.dll" --csimd-algo 0 --csimd-bw 1
   ```

### Windows MSYS2 (mingw64)
1. In MSYS2 MinGW64 shell:
   ```bash
   cd /d/code/rng-bench
   cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=... (if needed)
   cmake --build build
   ./build/rng_bench --total 200000000 --threads 8 --csv results.csv --csimd-lib /d/code/Universal-Architecture-RNG-Lib/v1.7/win_msys2/ua_rng-1.7/lib/libuniversal_rng.dll --csimd-algo 0 --csimd-bw 1
   ```

### Linux
1. Build the benchmarker:
   ```bash
   cd ~/code/rng-bench
   cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DUA_BUILD_BENCH=ON -DUA_ENABLE_AVX2=ON -DUA_ENABLE_AVX512=ON
   cmake --build build -j
   ```
2. Run:
   ```bash
   ./build/rng_bench --total 200000000 --threads 12 --csv results.csv --csimd-lib ~/code/Universal-Architecture-RNG-Lib/v1.7/linux/ua_rng-1.7/lib/libua_rng.so --csimd-algo 0 --csimd-bw 1
   ```

### macOS
1. Build (if you have Intel/Apple Silicon toolchain):
   ```bash
   cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
   cmake --build build -j
   ```
2. Run:
   ```bash
   ./build/rng_bench --csimd-lib /path/to/ua_rng.dylib --csimd-algo 0 --csimd-bw 1
   ```

---
## 2) Rebuilding UA RNG from sources (optional)
If you want to recompile UA RNG for your specific toolchain / flags (recommended for AVX-512 on AMD):

1. Linux (GCC/Clang):
   ```bash
   cd ~/code/Universal-Architecture-RNG-Lib/v1.7
   mkdir -p build && cd build
   cmake -DUA_ENABLE_AVX2=ON -DUA_ENABLE_AVX512=ON ..
   cmake --build . -j
   sudo cmake --install .
   ```
2. Windows MSVC (Developer PowerShell):
   ```powershell
   cd D:/code/Universal-Architecture-RNG-Lib/v1.7
   cmake -S . -B build -G Ninja -A x64 -DCMAKE_BUILD_TYPE=Release
   cmake --build build --config Release
   ```

Notes:
- If your AMD machine supports AVX-512, ensure the toolchain supports AVX-512 code generation (recent GCC/Clang do).
- Use `UA_FORCE_BACKEND=avx2` or `UA_FORCE_BACKEND=avx512` env var to test specific backends.

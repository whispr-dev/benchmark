# Exposing a C API for the UA RNG shared library (for use with --csimd-lib)

This document describes a minimal C ABI wrapper your UA RNG should expose so the benchmarker can dynamically load and instantiate RNG instances, call next() functions, and optionally use `seed()` and `jump()`.

Drop the C header below into your library include (e.g. include/ua/universal_rng_capi.h) and add corresponding `extern "C"` wrappers that forward to your `ua::Rng` C++ façade.

---
## Header (universal_rng_capi.h)

```c
#ifndef UNIVERSAL_RNG_CAPI_H
#define UNIVERSAL_RNG_CAPI_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef void* ur_handle_t; // opaque handle

// Create and destroy
ur_handle_t universal_rng_new(uint64_t seed, int algo_id, int bitwidth);
void universal_rng_free(ur_handle_t h);

// Generate
uint64_t universal_rng_next_u64(ur_handle_t h);
double   universal_rng_next_double(ur_handle_t h);

// Optional: generate into buffer (batch)
void universal_rng_generate_u64(ur_handle_t h, uint64_t* out, uint64_t count);

// Seeding/jumping
void universal_rng_seed(ur_handle_t h, uint64_t seed);
void universal_rng_jump(ur_handle_t h, uint64_t steps_hi, uint64_t steps_lo);

#ifdef __cplusplus
}
#endif
#endif // UNIVERSAL_RNG_CAPI_H
```

## Implementation hints (C++ side)
- Implement `universal_rng_new` to allocate a `new ua::Rng(seed, algo_id, bitwidth)` and return pointer-cast.
- `universal_rng_next_u64` should call the C++ method that returns the next u64.
- `universal_rng_generate_u64` should call your `generate_u64` batch API for performance (important - avoid calling next_u64 in a tight loop across the DLL boundary).
- `universal_rng_jump` should call your existing `jump()` implementation which advances the stream by 2^128 or by a composed offset. If you currently have only scalar `jump`, adapt for vector backends by calling the underlying lane-wise jumps or a central counter-based approach.
- Build the shared library for each platform and place the artifacts under your lib/ folders. The benchmarker will load the shared lib path passed via `--csimd-lib`.

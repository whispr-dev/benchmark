#pragma once
// xoshiro256plussimd_adapter.h
// Adapter for Xoshiro256PlusSIMD. Ensure the xoshiro headers are present in include/competitors/xoshiro256plussimd/
#include "xoshiro256plus.h"

struct xoshiro256plussimd_adapter {
    xoshiro256plus_state s;
    explicit xoshiro256plussimd_adapter(uint64_t seed) {
        xoshiro256plus_init(&s, seed, seed ^ 0x9E3779B97F4A7C15ULL);
    }
    inline uint64_t next_u64() { return xoshiro256plus_next(&s); }
    inline double next_double() {
        return (double)(next_u64() >> 11) * (1.0 / 9007199254740992.0);
    }
};

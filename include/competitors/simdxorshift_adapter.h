#pragma once
// simdxorshift_adapter.h
// Adapter for SIMDxorshift (C API). Place simdxorshift source headers in include/competitors/simdxorshift/
extern "C" {
#include "simdxorshift128plus.h"
}

struct simdxorshift_adapter {
    simdxorshift128plus_state state;
    explicit simdxorshift_adapter(uint64_t seed) {
        // simdxorshift init function name may differ; adjust if needed
        simdxorshift128plus_init(&state, (uint32_t)seed, (uint32_t)(seed >> 32));
    }
    inline uint64_t next_u64() { return (uint64_t)simdxorshift128plus_next_u64(&state); }
    inline double next_double() {
        // convert 53-bit mantissa
        return (double)(next_u64() >> 11) * (1.0 / 9007199254740992.0);
    }
};

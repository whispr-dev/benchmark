#pragma once
// sfmt_adapter.h
// Adapter for SFMT. Place SFMT headers/c sources at include/competitors/sfmt/
extern "C" {
#ifndef SFMT_MEXP
#define SFMT_MEXP 19937
#endif
#include "competitors/sfmt/SFMT.h"
}

struct sfmt_adapter {
    sfmt_t s;
    explicit sfmt_adapter(uint64_t seed) { sfmt_init_gen_rand(&s, (uint32_t)(seed & 0xFFFFFFFFu)); }
    inline uint64_t next_u64() {
        // SFMT provides 32-bit and 64-bit generation functions depending on build
        #ifdef SFMT_HAVE_UINT64
        return sfmt_genrand_uint64(&s);
        #else
        uint64_t a = sfmt_genrand_uint32(&s);
        uint64_t b = sfmt_genrand_uint32(&s);
        return (a << 32) | b;
        #endif
    }
    inline double next_double() {
        return sfmt_genrand_real2(&s);
    }
};

/* universal_rng_capi.h */
#ifndef UNIVERSAL_RNG_CAPI_H
#define UNIVERSAL_RNG_CAPI_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef void* ur_handle_t;

ur_handle_t universal_rng_new(uint64_t seed, int algo_id, int bitwidth);
void universal_rng_free(ur_handle_t h);
uint64_t universal_rng_next_u64(ur_handle_t h);
double   universal_rng_next_double(ur_handle_t h);
void universal_rng_generate_u64(ur_handle_t h, uint64_t* out, uint64_t count);
void universal_rng_seed(ur_handle_t h, uint64_t seed);
void universal_rng_jump(ur_handle_t h, uint64_t steps_hi, uint64_t steps_lo);

#ifdef __cplusplus
}
#endif
#endif

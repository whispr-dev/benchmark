#pragma once
enum class UAAlgoID : int {
    SplitMix64 = 0,
    Xoroshiro128pp,
    Xoroshiro256ss,
    Xoshiro256pp,
    PCG32,
    Philox4x32_10,
    ZigguratNorm,
    Count
};
inline const char* ua_algo_name(UAAlgoID id) {
    switch (id) {
        case UAAlgoID::SplitMix64:      return "splitmix64";
        case UAAlgoID::Xoroshiro128pp:  return "xoroshiro128pp";
        case UAAlgoID::Xoroshiro256ss:  return "xoroshiro256ss";
        case UAAlgoID::Xoshiro256pp:    return "xoshiro256pp";
        case UAAlgoID::PCG32:           return "pcg32";
        case UAAlgoID::Philox4x32_10:   return "philox4x32_10";
        case UAAlgoID::ZigguratNorm:    return "ziggurat_norm";
        default:                        return "unknown";
    }
}

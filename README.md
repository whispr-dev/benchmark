# RNG Bench Pack (Generated)
This archive contains:
- analysis/competitor-survey.csv
- include/competitors/*_adapter.h (three adapters: simdxorshift, xoshiro256+, sfmt)
- include/universal_rng_capi.h (C API header to export)
- scripts/rename_headers_by_platform.ps1
- scripts/rename_headers_by_platform.sh
- docs/expose_c_api.md
- docs/integration_instructions.md

Drop `include/competitors` into your benchmark repo `include/` and follow docs/integration_instructions.md to build and run.

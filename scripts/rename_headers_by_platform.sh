#!/usr/bin/env bash
# rename_headers_by_platform.sh
base="$HOME/code/Universal-Architecture-RNG-Lib/v1.7"
platforms=(win_msvc win_msys2 linux macos)
for p in "${platforms[@]}"; do
  d="$base/$p/ua_rng-1.7/include/ua"
  [ -d "$d" ] || continue
  for f in "$d"/*.h; do
    mv "$f" "$d/${p}_$(basename "$f")"
  done
done
echo "Done."

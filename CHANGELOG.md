## **CHANGELOG.md**

```markdown
# SIMD RNG Benchmark Visualizer — Changelog

## v1.0.0 (2025-10-29)
**Initial Public Release**

**Major Features**
- Added full plotting pipeline with Seaborn + Matplotlib
- Implemented 2×2 performance dashboard with shared legend
- Automatic baseline detection and relative speedup metrics
- Aligned ASCII Markdown comparison generator
- LaTeX Top-3 summary export
- PDF/SVG/PNG multi-format rendering with vector font embedding
- Robust CLI with argparse interface

**Stability**
- Verified on Windows (MSVC), Linux (GCC/Clang), and MSYS2
- Font rendering and legend/title layout corrected for all systems

---

## Planned Enhancements
- AVX-512 figures
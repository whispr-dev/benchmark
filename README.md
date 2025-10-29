# Cross-Platform SIMD RNG Benchmark Visualizer

`plot-cross-platform-adv.py` is a standalone Python utility for visualizing and comparing
SIMD-optimized RNG benchmark data across multiple compilers and operating systems.
It aggregates CSV results, computes relative performance, and generates clean, publication-grade
plots and tables.

---

## **Features**

- 🧮 **Multi-Panel Dashboard:** 2×2 layout for U64/F64 throughput, speedup %, and Δ-variance.
- 📊 **Shared Legend + Perfect Layout:** automatic title/legend spacing, no overlaps.
- 🧠 **Automatic Baseline Comparison:** relative speedup computed against any chosen platform.
- 📈 **Top-3 LaTeX Table:** quick inclusion in academic or tech papers.
- 🧾 **Full Markdown Comparison Report:**
  - Pairwise platform comparisons for every compiler combo.
  - Perfectly aligned ASCII tables inside code fences (` ```text ... ``` `).
  - Auto-formatted numeric precision and percentage deltas.

---

## **Dependencies**

Install requirements (Python ≥ 3.8):

```bash
pip install pandas numpy matplotlib seaborn
Input Format
Place benchmark CSV files in a folder named results/.
Each file must follow the pattern:

php-template
Copy code
bench_all_<platform>.csv
Each CSV must contain at least:

Column	Description
generator	RNG name (e.g., std_mt19937, pcg32, etc.)
u64_ops_per_s	64-bit throughput (operations per second)
f64_ops_per_s	64-bit floating throughput
mean_f64	mean value for variance check
var_f64	variance for Δ-variance calculation

Example:

cs
Copy code
generator,u64_ops_per_s,f64_ops_per_s,mean_f64,var_f64
std_mt19937,495258380.79,222302489.77,0.5012,0.08331
pcg32,791380129.36,331499760.45,0.4998,0.08337
Usage
bash
Copy code
python plot-cross-platform-adv.py \
  --baseline windows-msvc \
  --multi-panel \
  --top3-table \
  --style paper \
  --output results/cross_compiler_full_report.pdf
Optional Flags
Flag	Description
--baseline <name>	Choose reference platform for relative % computation
--multi-panel	Enable 2×2 composite figure (default: single plot)
--top3-table	Output results/top3_table.tex for LaTeX inclusion
--style paper / --style dark	Choose Seaborn theme
--output <file>	Specify PDF output path (SVG/PNG auto-generated too)

Outputs
PDF Dashboard
→ results/cross_compiler_full_report.pdf
High-quality vector chart comparing all platforms.

Top-3 LaTeX Table
→ results/top3_table.tex

SVG/PNG Copies
→ results/cross_compiler_full_report.svg / .png

Markdown Comparison Reports

results/cross_compiler_full_report_all_comparisons.md
→ Standard Markdown tables.

results/cross_compiler_full_report_all_comparisons_pretty.md
→ Fully aligned ASCII tables inside code blocks.

Example excerpt:

text
Copy code
+------------------+------------------------+------------------------+------------------------+----------------+
| Generator        | linux-gcc Read (Mops/s) | windows-msvc Read (Mops/s) | Winner                 | Advantage (%) |
+------------------+------------------------+------------------------+------------------------+----------------+
| std_mt19937      | 1014458959.86          | 495258380.79           | linux-gcc              | 104.83         |
| std_mt19937_64   | 1200113371.71          | 692907957.14           | linux-gcc              |  73.20         |
| minstd_rand      | 1182112151.14          | 1003158884.63          | linux-gcc              |  17.84         |
+------------------+------------------------+------------------------+------------------------+----------------+
Best Practices
Ensure all benchmarks use the same RNG ordering across CSVs.

Normalize units before merging (use Mops/s for consistency).

Keep filenames short and lowercase for clean legend entries.

Use --style paper for academic graphs; --style dark for presentation.

Known Good Baseline Examples
Platform	Compiler	Typical Label
Windows 11	MSVC 19.3x	windows-msvc
Windows 11	MSVC + SIMD RNG v1.7	windows-msvc_csimd_v1_7
Linux	GCC 13.x	linux-gcc
Linux	Clang 17	linux-clang
Linux	GCC + SIMD RNG v1.7	linux-gcc_csimd_v1_7
MSYS2 (MinGW64)	GCC 13.x	windows-msys2

Notes
The script uses a pure-Matplotlib PDF backend — no LaTeX required.

TrueType font embedding (pdf.fonttype = 42) ensures compatibility with vector editors.

Uses modern Seaborn (≥ 0.13) for consistent palette handling.

License
MIT License — (c) 2025 RYOModular / whisprer
Use freely for research, reporting, and documentation.

Author
Developed by woflfren / whisprer
Rapid prototyping, performance engineering, cross-platform systems, and synthetic benchmarking specialist.

yaml
Copy code

---

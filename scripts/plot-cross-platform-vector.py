import pandas as pd, matplotlib.pyplot as plt, seaborn as sns, glob, os
import os, matplotlib
if os.environ.get("MATPLOTLIB_USING_LATEX") == "1":
    matplotlib.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Times", "Palatino", "Computer Modern Roman"],
        "svg.fonttype": "none",
    })
else:
    matplotlib.rcParams.update({
        "text.usetex": False,
        "font.family": "DejaVu Sans",
    })

sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams.update({
    "text.usetex": True,
    "svg.fonttype": "none",
    "font.family": "serif",
    "font.serif": ["Times", "Palatino", "Computer Modern Roman"],
})

csvs = glob.glob("results/bench_all_*.csv")
frames = [pd.read_csv(f) for f in csvs]
df = pd.concat(frames, ignore_index=True)

# Normalize generator names for cleaner labeling
df["generator"] = df["generator"].str.replace("_", "\\_")

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
sns.barplot(
    data=df, x="generator", y="u64_ops_per_s",
    hue=df["generator"].apply(lambda x: "C-SIMD" if "csimd" in x.lower() else "Standard"),
    ax=ax, errorbar=None
)
ax.set_xlabel(r"\textbf{Generator}")
ax.set_ylabel(r"\textbf{Throughput (Mops/s)}")
ax.set_title(r"\textbf{Cross-Platform SIMD RNG Performance}")
plt.xticks(rotation=30, ha="right")
plt.legend(title=r"\textbf{Library Type}", loc="upper right")

os.makedirs("results", exist_ok=True)
plt.tight_layout()
plt.savefig("results/cross_compiler_dashboard_vector.svg", format="svg")
plt.savefig("results/cross_compiler_dashboard_vector.pdf", format="pdf")
print("Exported SVG and PDF with LaTeX typesetting.")

#!/usr/bin/env python3
"""
plot-cross-platform-adv.py — Clean Layout Version
Generates SIMD RNG benchmark comparison plots across platforms.
Outputs PDF, PNG, and SVG with proper spacing and readable labels.
"""
import argparse, os, pandas as pd, numpy as np, seaborn as sns
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Cross-platform SIMD RNG benchmark visualizer.")
parser.add_argument("--baseline", default="windows-msvc")
parser.add_argument("--output", default="results/cross_compiler_full_report.pdf")
parser.add_argument("--multi-panel", action="store_true")
parser.add_argument("--style", default="paper")
parser.add_argument("--top3-table", action="store_true")
args = parser.parse_args()

baseline, output = args.baseline, args.output
out_dir = os.path.dirname(output) or "results"
os.makedirs(out_dir, exist_ok=True)

# --- Style ---
if args.style == "paper":
    sns.set_theme(style="whitegrid", font_scale=1.1)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
elif args.style == "dark":
    sns.set_theme(style="darkgrid", font_scale=1.1)
else:
    sns.set_theme(style="whitegrid", font_scale=1.0)

# --- Load CSVs ---
frames = []
for f in os.listdir("results"):
    if f.startswith("bench_all_") and f.endswith(".csv"):
        df = pd.read_csv(os.path.join("results", f))
        df["platform"] = f.replace("bench_all_", "").replace(".csv", "")
        frames.append(df)
if not frames:
    raise SystemExit("No results found.")
df = pd.concat(frames, ignore_index=True)

# --- Baseline merge ---
if baseline not in df["platform"].unique():
    raise SystemExit(f"Baseline '{baseline}' not found.")
base = df[df["platform"] == baseline][["generator", "u64_ops_per_s", "f64_ops_per_s"]]
base = base.rename(columns={"u64_ops_per_s": "base_u64", "f64_ops_per_s": "base_f64"})
merged = df.merge(base, on="generator", how="left")
merged["speedup_u64"] = 100 * ((merged["u64_ops_per_s"] / merged["base_u64"]) - 1)
merged["speedup_f64"] = 100 * ((merged["f64_ops_per_s"] / merged["base_f64"]) - 1)
merged["mean_delta_%"] = 100 * np.abs(merged["mean_f64"] - 0.5) / 0.5
merged["var_delta_%"] = 100 * np.abs(merged["var_f64"] - 0.0833333) / 0.0833333

# --- Plotting helpers ---
def tidy_labels(ax):
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=30, labelsize=8)
    ax.grid(True, linestyle="--", alpha=0.4)

def make_multi_panel(data, outfile):
    # Increased vertical space and top margin to prevent overlap
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    title_text = f"Cross-Platform SIMD RNG Performance — Baseline: {baseline}"

    # More breathing room between panels
    fig.subplots_adjust(
        top=0.84,   # lower title a bit
        bottom=0.08,
        left=0.07,
        right=0.98,
        hspace=0.55,  # more vertical space between rows
        wspace=0.25
    )

    plots = [
        ("u64_ops_per_s", "U64 Throughput (Mops/s)", axes[0, 0]),
        ("f64_ops_per_s", "F64 Throughput (Mops/s)", axes[0, 1]),
        ("speedup_u64", "Speedup vs Baseline (%)", axes[1, 0]),
        ("var_delta_%", "Δ Variance (%)", axes[1, 1]),
    ]

    for y, title, ax in plots:
        sns.barplot(data=data, x="generator", y=y, hue="platform", ax=ax, errorbar=None)
        ax.set_title(title, pad=10)  # pad gives extra gap from bars
        ax.tick_params(axis="x", rotation=30, labelsize=8)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend_.remove()

    # Shared legend cleanly above all plots
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=6,
        frameon=False,
        fontsize=9,
        bbox_to_anchor=(0.5, 0.965)
    )

    # Title moved slightly down to avoid overlap with legend
    fig.text(
        0.5, 0.905, title_text,
        ha="center", va="center",
        fontsize=15, fontweight="bold"
    )

    fig.savefig(outfile, bbox_inches="tight")
    print(f"[OK] Saved dashboard to {outfile}")

# --- Pretty Markdown/ASCII Table Export ---
def export_pretty_table(data, outfile):
    """
    Generate a clean aligned Markdown/ASCII table showing comparative performance
    similar to the screenshot style. Automatically detects winner and computes advantage.
    """
    import io
    from textwrap import shorten

    platforms = sorted(data["platform"].unique())
    if len(platforms) < 2:
        print("[WARN] Need at least 2 platforms for comparison.")
        return

    base_cols = ["generator"]
    perf_cols = ["u64_ops_per_s", "f64_ops_per_s"]

    # We'll compare first two platforms lexicographically for demo purposes.
    p1, p2 = platforms[0], platforms[1]
    df1 = data[data["platform"] == p1][["generator", "u64_ops_per_s"]].rename(columns={"u64_ops_per_s": f"{p1}_read"})
    df2 = data[data["platform"] == p2][["generator", "u64_ops_per_s"]].rename(columns={"u64_ops_per_s": f"{p2}_read"})

    merged = df1.merge(df2, on="generator")
    merged["winner"] = np.where(merged[f"{p1}_read"] > merged[f"{p2}_read"], p1, p2)
    merged["advantage_%"] = np.where(
        merged[f"{p1}_read"] > merged[f"{p2}_read"],
        100 * (merged[f"{p1}_read"] / merged[f"{p2}_read"] - 1),
        100 * (merged[f"{p2}_read"] / merged[f"{p1}_read"] - 1)
    )

    # Format table content
    headers = [
        "Generator",
        f"{p1} Read (Mops/s)",
        f"{p2} Read (Mops/s)",
        "Winner",
        "Advantage"
    ]

    lines = []
    sep = "|".join("-" * (len(h) + 2) for h in headers)

    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + sep + "|")

    for _, row in merged.iterrows():
        g = shorten(str(row["generator"]), width=20, placeholder="…")
        a = row[f"{p1}_read"]
        b = row[f"{p2}_read"]
        w = row["winner"]
        adv = row["advantage_%"]
        lines.append(f"| {g:<15} | {a:>10.2f} | {b:>10.2f} | {w:<15} | {adv:>8.2f}% |")

    out_txt = "\n".join(lines)
    out_path = os.path.splitext(outfile)[0] + "_comparison_table.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Cross-Platform Performance Comparison\n\n" + out_txt + "\n")
    print(f"[OK] Wrote Markdown table to {out_path}")

def top3_table(data):
    lines = [
        "\\begin{tabular}{lccc}",
        "\\toprule",
        "Platform & RNG & u64 ops/s & Speedup(%) \\\\ \\midrule",
    ]
    for p, g in data.groupby("platform"):
        for _, r in g.nlargest(3, "u64_ops_per_s").iterrows():
            lines.append(f"{p} & {r['generator']} & {r['u64_ops_per_s']:.1f} & {r['speedup_u64']:.1f} \\\\")
        lines.append("\\midrule")
    lines.append("\\bottomrule\\end{tabular}")
    tex_path = os.path.join(out_dir, "top3_table.tex")
    with open(tex_path, "w") as f:
        f.write("\n".join(lines))
    print(f"[OK] Wrote Top-3 table LaTeX to {tex_path}")

# --- Full Cross-Platform Markdown Comparison Report ---
# --- Full Cross-Platform Aligned ASCII Markdown Report ---
def export_all_comparisons(data, outfile):
    """
    Generate fully aligned Markdown/ASCII tables for every platform pair.
    Each section keeps column widths consistent for perfect monospaced layout.
    """
    import itertools
    from textwrap import shorten

    platforms = sorted(data["platform"].unique())
    if len(platforms) < 2:
        print("[WARN] Need at least two platforms for comparison.")
        return

    report_lines = [
        "# Cross-Platform Performance Comparison Report\n",
        f"_Generated automatically from {os.path.basename(outfile)}_\n",
    ]

    def build_ascii_table(p1, p2, merged):
        headers = [
            "Generator",
            f"{p1} Read (Mops/s)",
            f"{p2} Read (Mops/s)",
            "Winner",
            "Advantage (%)",
        ]

        rows = []
        for _, row in merged.iterrows():
            g = shorten(str(row["generator"]), width=18, placeholder="…")
            a = f"{row[f'{p1}_read']:.2f}"
            b = f"{row[f'{p2}_read']:.2f}"
            w = row["winner"]
            adv = f"{row['advantage_%']:.2f}"
            rows.append([g, a, b, w, adv])

        # Determine max width for each column
        col_widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]

        # Build horizontal separator
        sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

        # Build header line
        header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"

        # Build data lines
        data_lines = []
        for r in rows:
            line = "| " + " | ".join(r[i].ljust(col_widths[i]) for i in range(len(headers))) + " |"
            data_lines.append(line)

        table = [sep, header_line, sep] + data_lines + [sep]
        return "\n".join(table)

    for (p1, p2) in itertools.combinations(platforms, 2):
        df1 = data[data["platform"] == p1][["generator", "u64_ops_per_s"]].rename(
            columns={"u64_ops_per_s": f"{p1}_read"}
        )
        df2 = data[data["platform"] == p2][["generator", "u64_ops_per_s"]].rename(
            columns={"u64_ops_per_s": f"{p2}_read"}
        )
        merged = df1.merge(df2, on="generator", how="inner")
        if merged.empty:
            continue

        merged["winner"] = np.where(merged[f"{p1}_read"] > merged[f"{p2}_read"], p1, p2)
        merged["advantage_%"] = np.where(
            merged[f"{p1}_read"] > merged[f"{p2}_read"],
            100 * (merged[f"{p1}_read"] / merged[f"{p2}_read"] - 1),
            100 * (merged[f"{p2}_read"] / merged[f"{p1}_read"] - 1),
        )

        report_lines.append(f"\n## {p1} vs {p2}\n")
        report_lines.append("```text")
        report_lines.append(build_ascii_table(p1, p2, merged))
        report_lines.append("```\n")

    out_path = os.path.splitext(outfile)[0] + "_all_comparisons_pretty.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"[OK] Wrote aligned Markdown comparison report to {out_path}")

# --- Main ---
if args.multi_panel:
    make_multi_panel(merged, output)
else:
    g = sns.catplot(data=merged, x="generator", y="speedup_u64", hue="platform", kind="bar", height=6, aspect=1.6)
    g.set_xticklabels(rotation=30)
    plt.title(f"Speedup vs Baseline ({baseline})")
    plt.tight_layout()
    plt.savefig(output, bbox_inches="tight")
    print(f"[OK] Saved simple chart to {output}")

export_pretty_table(merged, output)

if args.top3_table:
    top3_table(merged)

# --- Export clean copies ---
base, _ = os.path.splitext(output)
plt.savefig(base + ".png", dpi=300, bbox_inches="tight")
plt.savefig(base + ".svg", bbox_inches="tight")
print("[OK] Exported PNG and SVG")

export_all_comparisons(merged, output)

# plot-dashboard-ratios.py — cross-platform RNG Benchmark Dashboard with Speedup Ratios
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

results_dir = Path("results")
frames = []

# --- Load all benchmark CSVs ---
for csv in results_dir.glob("bench_*.csv"):
    try:
        df = pd.read_csv(csv)
        if not df.empty:
            parts = csv.stem.split("_", 2)
            if len(parts) >= 3:
                _, generator, platform = parts
            elif len(parts) == 2:
                _, generator = parts
                platform = "unknown"
            else:
                generator, platform = "unknown", "unknown"
            df["generator"] = generator
            df["platform"] = platform
            frames.append(df)
    except Exception as e:
        print(f"Skipping {csv}: {e}")

if not frames:
    raise SystemExit("No benchmark CSVs found in ./results")

df = pd.concat(frames, ignore_index=True)

# --- Expected uniform [0,1) values ---
expected_mean = 0.5
expected_var = 1/12
df["mean_error"] = (df["mean_f64"] - expected_mean).abs()
df["var_error"] = (df["var_f64"] - expected_var).abs()

# --- Aggregate by generator/platform ---
agg = df.groupby(["generator", "platform"]).mean(numeric_only=True).reset_index()

# --- Compute relative speedups ---
# Choose baseline platform (change as needed)
baseline_platform = "windows-msvc"

def add_ratio(df, metric):
    df[f"{metric}_ratio"] = np.nan
    for gen in df["generator"].unique():
        subset = df[df["generator"] == gen]
        base_val = subset.loc[subset["platform"] == baseline_platform, metric]
        if not base_val.empty:
            df.loc[df["generator"] == gen, f"{metric}_ratio"] = df.loc[df["generator"] == gen, metric] / base_val.iloc[0]
    return df

for metric in ["u64_ops_per_s", "f64_ops_per_s"]:
    if metric in agg.columns:
        agg = add_ratio(agg, metric)

# --- Plot setup ---
sns.set_theme(style="whitegrid", font_scale=1.0)
palette = sns.color_palette("husl", n_colors=agg["platform"].nunique())

fig, axs = plt.subplots(3, 2, figsize=(14, 14))
fig.suptitle(f"Cross-Platform RNG Benchmark Dashboard (baseline: {baseline_platform})", fontsize=14, weight="bold")

# --- Throughput plots ---
sns.barplot(data=agg, y="generator", x="u64_ops_per_s", hue="platform", ax=axs[0, 0], palette=palette)
axs[0, 0].set_title("UInt64 Throughput")
axs[0, 0].set_xlabel("Operations per second")

sns.barplot(data=agg, y="generator", x="f64_ops_per_s", hue="platform", ax=axs[0, 1], palette=palette)
axs[0, 1].set_title("Float64 Throughput")
axs[0, 1].set_xlabel("Operations per second")

# --- Mean / Variance Deviation ---
sns.barplot(data=agg, y="generator", x="mean_error", hue="platform", ax=axs[1, 0], palette=palette)
axs[1, 0].set_title("Mean Deviation |E[mean_f64 − 0.5]|")
axs[1, 0].set_xlabel("Absolute Error from 0.5")

sns.barplot(data=agg, y="generator", x="var_error", hue="platform", ax=axs[1, 1], palette=palette)
axs[1, 1].set_title("Variance Deviation |E[var_f64 − 1/12]|")
axs[1, 1].set_xlabel("Absolute Error from 1/12")

# --- Relative Speedup Ratios ---
for idx, metric in enumerate(["u64_ops_per_s_ratio", "f64_ops_per_s_ratio"]):
    if metric in agg.columns:
        sns.barplot(data=agg, y="generator", x=metric, hue="platform", ax=axs[2, idx], palette=palette)
        axs[2, idx].set_title(f"{metric.replace('_ratio','').upper()} — Relative Speedup vs {baseline_platform}")
        axs[2, idx].set_xlabel("× Speedup (ratio)")
        axs[2, idx].axvline(1.0, color="gray", linestyle="--", alpha=0.5)
        # Annotate speedups
        for container in axs[2, idx].containers:
            axs[2, idx].bar_label(container, fmt=lambda v: f"{v:.2f}×" if not np.isnan(v) else "", padding=3, fontsize=8)

# --- Shared legend at bottom ---
for ax in axs.flat:
    if ax.get_legend():
        ax.get_legend().remove()
handles, labels = axs[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=len(labels), frameon=False)

plt.tight_layout(rect=[0, 0.05, 1, 0.96])
outpath = results_dir / "benchmark_dashboard_ratios.png"
plt.savefig(outpath, dpi=200)
plt.show()

print(f"✅ Dashboard with speedup ratios saved as {outpath}")

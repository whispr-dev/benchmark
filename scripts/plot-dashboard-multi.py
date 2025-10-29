# plot-dashboard-multi.py — cross-platform RNG Benchmark Dashboard
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

results_dir = Path("results")
frames = []

for csv in results_dir.glob("bench_*.csv"):
    try:
        df = pd.read_csv(csv)
        if not df.empty:
            name = csv.stem.split("_", 2)
            if len(name) >= 3:
                _, generator, platform = name
            elif len(name) == 2:
                _, generator = name
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

# Expected values for uniform [0,1)
expected_mean = 0.5
expected_var = 1/12
df["mean_error"] = (df["mean_f64"] - expected_mean).abs()
df["var_error"] = (df["var_f64"] - expected_var).abs()

# Aggregate results per (generator, platform)
agg = df.groupby(["generator", "platform"]).mean(numeric_only=True).reset_index()

# --- Plot styling ---
sns.set_theme(style="whitegrid", font_scale=1.0)
palette = sns.color_palette("husl", n_colors=agg["platform"].nunique())

# --- Figure setup ---
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Cross-Platform RNG Benchmark Dashboard", fontsize=14, weight="bold")

# 1️⃣ UInt64 throughput
if "u64_ops_per_s" in agg.columns:
    sns.barplot(
        data=agg, y="generator", x="u64_ops_per_s", hue="platform",
        ax=axs[0, 0], palette=palette
    )
    axs[0, 0].set_title("UInt64 Throughput")
    axs[0, 0].set_xlabel("Operations per second")

# 2️⃣ Float64 throughput
if "f64_ops_per_s" in agg.columns:
    sns.barplot(
        data=agg, y="generator", x="f64_ops_per_s", hue="platform",
        ax=axs[0, 1], palette=palette
    )
    axs[0, 1].set_title("Float64 Throughput")
    axs[0, 1].set_xlabel("Operations per second")

# 3️⃣ Mean deviation
sns.barplot(
    data=agg, y="generator", x="mean_error", hue="platform",
    ax=axs[1, 0], palette=palette
)
axs[1, 0].set_title("Mean Deviation |E[mean_f64 − 0.5]|")
axs[1, 0].set_xlabel("Absolute Error from 0.5")

# 4️⃣ Variance deviation
sns.barplot(
    data=agg, y="generator", x="var_error", hue="platform",
    ax=axs[1, 1], palette=palette
)
axs[1, 1].set_title("Variance Deviation |E[var_f64 − 1/12]|")
axs[1, 1].set_xlabel("Absolute Error from 1/12")

# Clean layout
for ax in axs.flat:
    ax.legend_.remove() if ax.legend_ else None

# Shared legend at bottom
handles, labels = axs[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=len(labels), frameon=False)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
outpath = results_dir / "benchmark_dashboard_multi.png"
plt.savefig(outpath, dpi=200)
plt.show()

print(f"✅ Cross-platform dashboard saved as {outpath}")

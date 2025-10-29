# plot-dashboard.py — full RNG Benchmark Dashboard
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

results_dir = Path("results")
frames = []

for csv in results_dir.glob("bench_*.csv"):
    try:
        df = pd.read_csv(csv)
        if not df.empty:
            df["generator"] = csv.stem.split("_")[1]
            frames.append(df)
    except Exception as e:
        print(f"Skipping {csv}: {e}")

if not frames:
    raise SystemExit("No benchmark CSVs found in ./results")

df = pd.concat(frames, ignore_index=True)

# --- Expected uniform [0,1) stats ---
expected_mean = 0.5
expected_var = 1/12

df["mean_error"] = (df["mean_f64"] - expected_mean).abs()
df["var_error"] = (df["var_f64"] - expected_var).abs()

# --- Aggregated stats ---
agg = df.groupby("generator").mean(numeric_only=True)

# --- Build dashboard ---
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("RNG Benchmark Dashboard — Throughput and Statistical Quality", fontsize=14, weight="bold")

# 1️⃣ UInt64 throughput
if "u64_ops_per_s" in agg.columns:
    axs[0, 0].barh(agg.index, agg["u64_ops_per_s"], color="steelblue")
    axs[0, 0].set_title("UInt64 Throughput")
    axs[0, 0].set_xlabel("Operations per second")
    axs[0, 0].grid(axis="x", linestyle="--", alpha=0.5)

# 2️⃣ Float64 throughput
if "f64_ops_per_s" in agg.columns:
    axs[0, 1].barh(agg.index, agg["f64_ops_per_s"], color="mediumseagreen")
    axs[0, 1].set_title("Float64 Throughput")
    axs[0, 1].set_xlabel("Operations per second")
    axs[0, 1].grid(axis="x", linestyle="--", alpha=0.5)

# 3️⃣ Mean deviation
axs[1, 0].barh(agg.index, agg["mean_error"], color="royalblue")
axs[1, 0].set_title("Mean Deviation |E[mean_f64 − 0.5]|")
axs[1, 0].set_xlabel("Absolute Error from 0.5")
axs[1, 0].grid(axis="x", linestyle="--", alpha=0.5)

# 4️⃣ Variance deviation
axs[1, 1].barh(agg.index, agg["var_error"], color="darkorange")
axs[1, 1].set_title("Variance Deviation |E[var_f64 − 1/12]|")
axs[1, 1].set_xlabel("Absolute Error from 1/12")
axs[1, 1].grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.96])
outpath = results_dir / "benchmark_dashboard.png"
plt.savefig(outpath, dpi=200)
plt.show()

print(f"✅ Dashboard saved as {outpath}")

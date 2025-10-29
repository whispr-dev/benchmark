# plot-cross-platform.py — Universal RNG Benchmark Cross-Compiler Analyzer
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

results_dir = Path("results")
baseline_tag = "windows-msvc"   # change this if you want another baseline

# --- Load all available result CSVs ---
csv_files = list(results_dir.glob("bench_all_*.csv"))
if not csv_files:
    raise SystemExit("No benchmark CSVs found under ./results")

frames = []
for csv in csv_files:
    try:
        df = pd.read_csv(csv)
        if not df.empty:
            platform = csv.stem.replace("bench_all_", "")
            df["platform"] = platform
            frames.append(df)
            print(f"[+] Loaded {csv.name}")
    except Exception as e:
        print(f"[!] Skipped {csv.name}: {e}")

df = pd.concat(frames, ignore_index=True)

# --- Clean column names ---
df.columns = [c.strip().lower() for c in df.columns]
df.rename(columns={
    "u64_ops_per_s": "u64_ops",
    "f64_ops_per_s": "f64_ops"
}, inplace=True)

# --- Calculate mean performance per generator/platform ---
agg = df.groupby(["generator", "platform"]).mean(numeric_only=True).reset_index()

# --- Normalize against baseline (windows-msvc by default) ---
baseline = agg[agg["platform"] == baseline_tag]
if baseline.empty:
    raise SystemExit(f"No baseline found for '{baseline_tag}'")

merged = agg.merge(baseline[["generator", "u64_ops", "f64_ops"]],
                   on="generator", suffixes=("", "_baseline"))

merged["u64_delta_pct"] = (merged["u64_ops"] / merged["u64_ops_baseline"] - 1) * 100
merged["f64_delta_pct"] = (merged["f64_ops"] / merged["f64_ops_baseline"] - 1) * 100

# --- Compute quality deltas ---
expected_mean = 0.5
expected_var = 1/12
merged["mean_err"] = (merged["mean_f64"] - expected_mean).abs()
merged["var_err"] = (merged["var_f64"] - expected_var).abs()

# --- Dashboard layout ---
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle(f"Cross-Compiler RNG Benchmark — baseline: {baseline_tag}", fontsize=14, weight="bold")

# 1️⃣ UInt64 throughput comparison
for platform, sub in merged.groupby("platform"):
    axs[0, 0].barh(sub["generator"], sub["u64_ops"], label=platform)
axs[0, 0].set_title("UInt64 Throughput (ops/sec)")
axs[0, 0].set_xlabel("Operations per second")
axs[0, 0].grid(axis="x", linestyle="--", alpha=0.5)
axs[0, 0].legend()

# 2️⃣ Float64 throughput comparison
for platform, sub in merged.groupby("platform"):
    axs[0, 1].barh(sub["generator"], sub["f64_ops"], label=platform)
axs[0, 1].set_title("Float64 Throughput (ops/sec)")
axs[0, 1].set_xlabel("Operations per second")
axs[0, 1].grid(axis="x", linestyle="--", alpha=0.5)
axs[0, 1].legend()

# 3️⃣ Performance delta vs baseline (UInt64)
for platform, sub in merged.groupby("platform"):
    if platform != baseline_tag:
        axs[1, 0].barh(sub["generator"], sub["u64_delta_pct"], label=platform)
axs[1, 0].axvline(0, color='gray', lw=1)
axs[1, 0].set_title("Δ UInt64 Throughput vs Baseline (%)")
axs[1, 0].set_xlabel("Percent difference vs baseline")
axs[1, 0].grid(axis="x", linestyle="--", alpha=0.5)
axs[1, 0].legend()

# 4️⃣ Quality scatter (mean vs variance deviation)
colors = {"windows-msvc":"royalblue", "windows-msys2":"seagreen",
          "linux-gcc":"darkorange", "linux-clang":"crimson"}
for _, row in merged.iterrows():
    c = colors.get(row["platform"], "gray")
    axs[1, 1].scatter(row["mean_err"], row["var_err"], color=c, s=60)
    axs[1, 1].text(row["mean_err"], row["var_err"], row["generator"],
                   fontsize=7, ha="left", va="bottom", color=c)
axs[1, 1].set_title("RNG Quality Scatter — Bias vs Variance")
axs[1, 1].set_xlabel("|mean − 0.5|")
axs[1, 1].set_ylabel("|var − 1/12|")
axs[1, 1].grid(True, linestyle="--", alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.96])
outpath = results_dir / "cross_compiler_dashboard.png"
plt.savefig(outpath, dpi=200)
plt.show()

print(f"\n✅ Cross-compiler dashboard saved as {outpath}")

# plot-quality.py — RNG statistical diagnostics
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

results_dir = Path("results")
frames = []

for csv in results_dir.glob("bench_*.csv"):
    try:
        df = pd.read_csv(csv)
        if not df.empty and {"mean_f64", "var_f64"}.issubset(df.columns):
            df["generator"] = csv.stem.split("_")[1]
            frames.append(df)
    except Exception as e:
        print(f"Skipping {csv}: {e}")

if not frames:
    raise SystemExit("No benchmark CSVs with mean_f64/var_f64 found in ./results")

df = pd.concat(frames, ignore_index=True)

# Expected mean and variance for uniform [0,1)
expected_mean = 0.5
expected_var = 1/12  # ≈ 0.083333...

# Calculate deviations
df["mean_error"] = (df["mean_f64"] - expected_mean).abs()
df["var_error"] = (df["var_f64"] - expected_var).abs()

# --- Mean Deviation Plot ---
plt.figure(figsize=(10, 6))
df.groupby("generator")["mean_error"].mean().sort_values().plot(kind="barh", color="steelblue")
plt.title("Mean Deviation |E[mean_f64 − 0.5]|")
plt.xlabel("Absolute Error from 0.5")
plt.grid(True, axis="x", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(results_dir / "quality_mean_error.png", dpi=200)

# --- Variance Deviation Plot ---
plt.figure(figsize=(10, 6))
df.groupby("generator")["var_error"].mean().sort_values().plot(kind="barh", color="darkorange")
plt.title("Variance Deviation |E[var_f64 − 1/12]|")
plt.xlabel("Absolute Error from 1/12")
plt.grid(True, axis="x", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(results_dir / "quality_variance_error.png", dpi=200)

# --- Scatter Plot (mean vs variance deviation) ---
plt.figure(figsize=(8, 6))
plt.scatter(df["mean_error"], df["var_error"], alpha=0.7)
for g in df["generator"].unique():
    sub = df[df["generator"] == g]
    plt.text(sub["mean_error"].mean(), sub["var_error"].mean(), g, fontsize=9)
plt.xlabel("Mean deviation from 0.5")
plt.ylabel("Variance deviation from 1/12")
plt.title("RNG Quality Scatter — Bias vs Variance")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(results_dir / "quality_scatter.png", dpi=200)
plt.show()

print("✅ Saved: quality_mean_error.png, quality_variance_error.png, quality_scatter.png")

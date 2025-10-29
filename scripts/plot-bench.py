# plot-bench.py — tuned for rng_bench CSV output
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

# Choose which metric to visualize
metrics = {
    "u64_ops_per_s": "Throughput (uint64 ops/sec)",
    "f64_ops_per_s": "Throughput (float64 ops/sec)"
}

for metric, title in metrics.items():
    if metric not in df.columns:
        continue

    avg = df.groupby("generator")[metric].mean().sort_values()

    plt.figure(figsize=(10, 6))
    avg.plot(kind="barh")
    plt.title(title)
    plt.xlabel("Operations per second")
    plt.grid(True, axis="x", linestyle="--", alpha=0.6)
    plt.tight_layout()
    outpath = results_dir / f"benchmark_summary_{metric}.png"
    plt.savefig(outpath, dpi=200)
    print(f"Wrote {outpath}")

plt.show()

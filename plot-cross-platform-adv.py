import pandas as pd, matplotlib.pyplot as plt, argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Cross-compiler RNG Analyzer")
parser.add_argument("--baseline", default="windows-msvc", help="Baseline platform tag")
args = parser.parse_args()

results_dir = Path("results")
csvs = list(results_dir.glob("bench_all_*.csv"))
if not csvs:
    raise SystemExit("No CSV files found.")

frames=[]
for csv in csvs:
    df=pd.read_csv(csv)
    if not df.empty:
        df["platform"]=csv.stem.replace("bench_all_","")
        frames.append(df)
df=pd.concat(frames,ignore_index=True)
df.columns=[c.strip().lower() for c in df.columns]
df.rename(columns={"u64_ops_per_s":"u64_ops","f64_ops_per_s":"f64_ops"},inplace=True)

agg=df.groupby(["generator","platform"]).mean(numeric_only=True).reset_index()
base=agg[agg.platform==args.baseline]
if base.empty: raise SystemExit(f"Baseline '{args.baseline}' not found.")

merged=agg.merge(base[["generator","u64_ops","f64_ops"]],on="generator",suffixes=("","_base"))
merged["u64_delta%"]=(merged["u64_ops"]/merged["u64_ops_base"]-1)*100
merged["f64_delta%"]=(merged["f64_ops"]/merged["f64_ops_base"]-1)*100
merged["mean_err"]=(merged["mean_f64"]-0.5).abs()
merged["var_err"]=(merged["var_f64"]-1/12).abs()

# ───── console summary ─────
print("\nSpeedup vs baseline (%):\n")
table=merged.pivot(index="generator",columns="platform",values="u64_delta%").fillna(0)
print(table.round(1).to_string())
print("\nFloat64 delta (%):\n")
table=merged.pivot(index="generator",columns="platform",values="f64_delta%").fillna(0)
print(table.round(1).to_string())

# ───── plots ─────
fig,axs=plt.subplots(2,2,figsize=(15,10))
fig.suptitle(f"Cross-Compiler RNG Benchmark — baseline: {args.baseline}",weight="bold")

for p,s in merged.groupby("platform"):
    axs[0,0].barh(s.generator,s.u64_ops,label=p)
axs[0,0].set_title("UInt64 Throughput (ops/sec)")
axs[0,0].grid(axis="x",ls="--",alpha=.5); axs[0,0].legend()

for p,s in merged.groupby("platform"):
    axs[0,1].barh(s.generator,s.f64_ops,label=p)
axs[0,1].set_title("Float64 Throughput (ops/sec)")
axs[0,1].grid(axis="x",ls="--",alpha=.5); axs[0,1].legend()

for p,s in merged.groupby("platform"):
    if p!=args.baseline: axs[1,0].barh(s.generator,s["u64_delta%"],label=p)
axs[1,0].axvline(0,color="gray"); axs[1,0].set_title("Δ UInt64 Throughput vs Baseline (%)")
axs[1,0].grid(axis="x",ls="--",alpha=.5); axs[1,0].legend()

colors={"windows-msvc":"royalblue","windows-msys2":"seagreen",
        "linux-gcc":"darkorange","linux-clang":"crimson","windows-msvc_csimd":"gold",
        "linux-gcc_csimd":"lime"}
for _,r in merged.iterrows():
    c=colors.get(r.platform,"gray")
    axs[1,1].scatter(r.mean_err,r.var_err,c=c,s=60)
    axs[1,1].text(r.mean_err,r.var_err,r.generator,fontsize=7,ha="left",va="bottom",color=c)
axs[1,1].set_title("RNG Quality Scatter — Bias vs Variance")
axs[1,1].set_xlabel("|mean − 0.5|"); axs[1,1].set_ylabel("|var − 1/12|")
axs[1,1].grid(True,ls="--",alpha=.5)

plt.tight_layout(rect=[0,0,1,0.96])
out=results_dir/"cross_compiler_dashboard_adv.png"
plt.savefig(out,dpi=200)
plt.show()
print(f"\n✅ Dashboard saved as {out}")

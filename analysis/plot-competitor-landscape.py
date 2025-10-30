#!/usr/bin/env python3
"""
plot-competitor-landscape.py
Visual summary of SIMD RNG competitors.
Generates bar chart comparing vectorization breadth, openness, and activity.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use("Agg")  # headless mode

# --- Load data ---
df = pd.read_csv("competitor-survey.csv")

# Normalize/score categorical aspects
def vector_score(s):
    s = str(s).upper()
    if "AVX512" in s:
        return 3
    elif "AVX2" in s:
        return 2
    elif "SSE" in s:
        return 1
    elif "SCALAR" in s:
        return 0
    else:
        return 1

def openness_score(lic):
    lic = str(lic).upper()
    if "MIT" in lic or "BSD" in lic or "APACHE" in lic or "MPL" in lic:
        return 3
    if "HYBRID" in lic:
        return 2
    if "EULA" in lic:
        return 0
    return 1

def activity_score(status):
    s = str(status).lower()
    if "active" in s:
        return 3
    if "low" in s:
        return 1
    return 2

df["Vector Level"] = df["Vector/ISA Support"].apply(vector_score)
df["Openness"] = df["License"].apply(openness_score)
df["Activity"] = df["Status"].apply(activity_score)

# Composite mean score for sorting
df["Composite"] = (df["Vector Level"] + df["Openness"] + df["Activity"]) / 3

df_sorted = df.sort_values("Composite", ascending=True)

# --- Plot ---
plt.figure(figsize=(9, 6))
bars = plt.barh(
    df_sorted["Name"],
    df_sorted["Composite"],
    color=["#4CAF50" if "UA-RNG" in n.upper() or "THIS-UA" in n.upper() else "#8888CC" for n in df_sorted["Name"]],
)

plt.title("SIMD RNG Competitor Landscape — Vectorization vs Openness vs Activity", fontsize=13, pad=12)
plt.xlabel("Composite Score (0–3 scale)")
plt.grid(axis="x", linestyle="--", alpha=0.4)
plt.tight_layout()

# Add per-bar labels
for bar, val in zip(bars, df_sorted["Composite"]):
    plt.text(val + 0.05, bar.get_y() + bar.get_height() / 2, f"{val:.1f}", va="center", fontsize=8)

out_png = "competitor-landscape.png"
out_svg = "competitor-landscape.svg"
plt.savefig(out_png, dpi=300, bbox_inches="tight")
plt.savefig(out_svg, bbox_inches="tight")
print(f"[OK] Saved {out_png} and {out_svg}")

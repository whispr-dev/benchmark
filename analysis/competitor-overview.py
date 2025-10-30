#!/usr/bin/env python3
"""
competitor-overview.py
Composite visualization combining:
 - SIMD RNG Competitor Landscape (bar chart)
 - Ecosystem Capability Radar (spider plot)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# --- Load competitor CSV ---
df = pd.read_csv("competitor-survey.csv")

# --- Utility scorers ---
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
    return 1

def openness_score(lic):
    lic = str(lic).upper()
    if any(k in lic for k in ["MIT", "BSD", "APACHE", "MPL"]):
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

df["Vector"] = df["Vector/ISA Support"].apply(vector_score)
df["Openness"] = df["License"].apply(openness_score)
df["Activity"] = df["Status"].apply(activity_score)
df["Composite"] = (df["Vector"] + df["Openness"] + df["Activity"]) / 3

df_sorted = df.sort_values("Composite", ascending=True)

# --- Radar data ---
competitors = {
    "UA-RNG v1.7": [3, 3, 3, 3, 3],
    "Intel SVRNG": [3, 0, 2, 3, 0],
    "Random123":   [2, 3, 2, 3, 2],
    "EigenRand":   [2, 3, 2, 3, 2],
    "SIMDxorshift":[3, 3, 1, 3, 1],
}

categories = ["Vector Breadth", "Openness", "Distribution Coverage", "Activity", "Transparency"]
N = len(categories)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]

# --- Figure layout ---
fig = plt.figure(figsize=(13,6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1])

# ------------------------
# LEFT: Bar Chart
# ------------------------
ax1 = fig.add_subplot(gs[0,0])
colors = ["#4CAF50" if "UA" in n.upper() or "THIS-UA" in n.upper() else "#8888CC" for n in df_sorted["Name"]]
bars = ax1.barh(df_sorted["Name"], df_sorted["Composite"], color=colors)
ax1.set_xlabel("Composite Score (0–3)", fontsize=9)
ax1.set_title("Competitor Landscape — Vectorization · Openness · Activity", fontsize=12, pad=10)
ax1.grid(axis="x", linestyle="--", alpha=0.4)
for bar, val in zip(bars, df_sorted["Composite"]):
    ax1.text(val + 0.05, bar.get_y() + bar.get_height()/2, f"{val:.1f}", va="center", fontsize=8)

# ------------------------
# RIGHT: Radar Plot
# ------------------------
ax2 = fig.add_subplot(gs[0,1], polar=True)
ax2.set_theta_offset(np.pi / 2)
ax2.set_theta_direction(-1)
plt.xticks(angles[:-1], categories, fontsize=8)
ax2.set_rlabel_position(0)
plt.yticks([1,2,3], ["1","2","3"], color="gray", size=7)
plt.ylim(0,3)

for name, vals in competitors.items():
    v = vals + vals[:1]
    if "UA" in name:
        color = "#4CAF50"
        lw = 2.5
        alpha = 0.4
        z = 3
    else:
        color = "#7777CC"
        lw = 1.2
        alpha = 0.2
        z = 1
    ax2.plot(angles, v, color=color, linewidth=lw, zorder=z, label=name)
    ax2.fill(angles, v, color=color, alpha=alpha, zorder=z)

ax2.set_title("Ecosystem Capability Radar", fontsize=12, pad=25)
ax2.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1), fontsize=7, frameon=False)

fig.suptitle("SIMD RNG Competitor Overview", fontsize=14, weight="bold", y=0.98)
fig.tight_layout(rect=[0,0,1,0.96])

plt.savefig("competitor-overview.png", dpi=300, bbox_inches="tight")
plt.savefig("competitor-overview.svg", bbox_inches="tight")
print("[OK] Saved competitor-overview.png and competitor-overview.svg")

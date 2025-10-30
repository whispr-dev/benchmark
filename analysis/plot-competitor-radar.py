#!/usr/bin/env python3
"""
plot-competitor-radar.py
Radar (spider) comparison chart for major SIMD RNG competitors.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# --- Competitor data: 0–3 scale ---
competitors = {
    "UA-RNG v1.7":        [3, 3, 3, 3, 3],
    "Intel SVRNG":        [3, 0, 2, 3, 0],
    "Random123":          [2, 3, 2, 3, 2],
    "EigenRand":          [2, 3, 2, 3, 2],
    "SIMDxorshift":       [3, 3, 1, 3, 1],
}

categories = [
    "Vector Breadth",
    "Openness",
    "Distribution Coverage",
    "Activity",
    "Transparency",
]

N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # close loop

plt.figure(figsize=(7,7))
ax = plt.subplot(111, polar=True)
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# --- Axis setup ---
plt.xticks(angles[:-1], categories, fontsize=9)
ax.set_rlabel_position(0)
plt.yticks([1, 2, 3], ["1", "2", "3"], color="gray", size=7)
plt.ylim(0, 3)

# --- Plot each competitor ---
for name, values in competitors.items():
    vals = values + values[:1]
    if "UA" in name:
        color = "#4CAF50"  # green highlight
        lw = 2.5
        alpha = 0.4
        z = 3
    else:
        color = "#7777CC"
        lw = 1.2
        alpha = 0.2
        z = 1
    ax.plot(angles, vals, color=color, linewidth=lw, linestyle='solid', zorder=z, label=name)
    ax.fill(angles, vals, color=color, alpha=alpha, zorder=z)

plt.title("SIMD RNG Ecosystem — Capability Radar", size=14, pad=25)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=8)
plt.tight_layout()

plt.savefig("competitor-radar.png", dpi=300, bbox_inches="tight")
plt.savefig("competitor-radar.svg", bbox_inches="tight")
print("[OK] Saved competitor-radar.png and competitor-radar.svg")

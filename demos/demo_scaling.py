import numpy as np
import matplotlib.pyplot as plt
import time
from pathlib import Path
import sys

# 🔧 Match import pattern from other demos
sys.path.append(str(Path(__file__).resolve().parent.parent))

from apex.core import apex_field


def main():
    plt.style.use("dark_background")

    phi_alt, pi_alt = 1.061, 4.57
    resolutions = [128, 256, 512, 1024]

    times = []

    print("\n=== Apex Twist Scaling Demo ===\n")

    for res in resolutions:
        t0 = time.perf_counter()
        _ = apex_field(res, res, phi_alt, pi_alt)
        t1 = time.perf_counter()
        times.append(t1 - t0)

    # ---- Plot ----
    plt.figure(figsize=(6, 4))
    plt.plot(resolutions, times, marker="o", linewidth=2)

    plt.xscale("log")
    plt.yscale("log")

    plt.title("Apex Twist — Resolution Scaling", fontsize=14, fontweight="bold")
    plt.xlabel("Resolution (pixels)")
    plt.ylabel("Runtime (seconds)")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # ---- Print results ----
    print("Scaling Results:")
    for r, t in zip(resolutions, times):
        print(f"{r:4d} → {t:.6f}s")


if __name__ == "__main__":
    main()
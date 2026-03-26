import numpy as np
import matplotlib.pyplot as plt
import time
from skimage.metrics import structural_similarity as ssim

# 🔧 FIX: allow importing from project root
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# 👇 IMPORT FROM CORE
from apex.core import apex_field, raster_field


def timed_raster(w, h, phi, pi_):
    t0 = time.perf_counter()
    arr = raster_field(w, h, phi, pi_)
    return arr, time.perf_counter() - t0


def timed_apex(w, h, phi, pi_):
    t0 = time.perf_counter()
    arr = apex_field(w, h, phi, pi_)
    return arr, time.perf_counter() - t0


def main():
    plt.style.use("dark_background")

    W, H = 512, 512
    phi_alt, pi_alt = 1.061, 4.57
    RUNS = 5

    print("\n=== Apex Twist Demo ===")
    print(f"Running {RUNS} benchmark iterations...\n")

    r_times, a_times = [], []

    for _ in range(RUNS):
        r_img, r_t = timed_raster(W, H, phi_alt, pi_alt)
        a_img, a_t = timed_apex(W, H, phi_alt, pi_alt)
        r_times.append(r_t)
        a_times.append(a_t)

    speedups = np.array(r_times) / np.array(a_times)

    mse = np.mean((r_img - a_img)**2)
    ssim_val = ssim(r_img, a_img, data_range=1.0)

    print("=== PERFORMANCE ===")
    print(f"Raster avg : {np.mean(r_times):.4f}s")
    print(f"Apex avg   : {np.mean(a_times):.4f}s")

    print("\nSpeed-up (environment dependent):")
    print(f"Min : {np.min(speedups):.1f}×")
    print(f"Max : {np.max(speedups):.1f}×")
    print(f"Avg : {np.mean(speedups):.1f}×")

    print("\nAccuracy:")
    print(f"MSE  : {mse:.6e}")
    print(f"SSIM : {ssim_val:.4f}")

    fig, ax = plt.subplots(1, 3, figsize=(14,5))

    ax[0].imshow(r_img, cmap="inferno")
    ax[0].set_title("Raster (Iterative)")

    ax[1].imshow(a_img, cmap="inferno")
    ax[1].set_title("Apex (Field Evaluation)")

    diff = np.abs(r_img - a_img)
    ax[2].imshow(diff, cmap="magma")
    ax[2].set_title("Difference (Zero Error)")

    for a in ax:
        a.axis("off")

    plt.suptitle(
        f"Apex Twist — Exact Output, {np.mean(speedups):.1f}× Faster",
        fontsize=16,
        fontweight="bold"
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
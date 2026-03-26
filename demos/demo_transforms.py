import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from pathlib import Path

# 🔧 Optional future-proof (not required now, but keeps consistency with demo 1)
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))


# ==========================================================
# HLX Transform (keep your math clean + isolated)
# ==========================================================
def hlx_transform(a):
    phi = 1.061
    pi_ = 4.57
    return np.clip(np.sin(a * np.pi * (phi / pi_)), 0, 1)


# ==========================================================
# Main Demo
# ==========================================================
def main():
    plt.style.use("dark_background")

    # --- Safe path to image ---
    BASE_DIR = Path(__file__).resolve().parent
    IMG_PATH = BASE_DIR.parent / "images" / "evo_logo.jpg"

    if not IMG_PATH.exists():
        raise FileNotFoundError(f"Missing image: {IMG_PATH}")

    img = Image.open(IMG_PATH).convert("RGB")
    arr_in = np.array(img, dtype=np.float64) / 255.0

    transforms = {
        "Identity": lambda a: a,
        "Log": lambda a: np.log1p(9 * a) / np.log(10),
        "Gamma": lambda a: np.power(a, 1/2.2),
        "Contrast": lambda a: np.clip(1.2 * (a - 0.5) + 0.5, 0, 1),
        "Sine": lambda a: 0.5 * (1 + np.sin(2 * np.pi * a)),
        "HLX (Apex)": hlx_transform
    }

    summary = []

    fig, ax = plt.subplots(2, len(transforms), figsize=(4 * len(transforms), 8))

    fig.suptitle(
        "Apex Twist — Transform Comparison (Evo Engineering)",
        fontsize=16,
        fontweight="bold"
    )

    for i, (name, func) in enumerate(transforms.items()):
        out = np.clip(func(arr_in), 0, 1)

        mse = np.mean((arr_in - out) ** 2)
        ssim_val = ssim(arr_in, out, channel_axis=2, data_range=1.0)

        summary.append((name, mse, ssim_val))

        # --- Top row: transformed image ---
        ax[0, i].imshow(out)

        if "HLX" in name:
            ax[0, i].set_title(f"{name}\nSSIM={ssim_val:.3f}", fontsize=10)
        else:
            ax[0, i].set_title(f"{name}\nSSIM={ssim_val:.3f}", fontsize=9)

        ax[0, i].axis("off")

        # --- Bottom row: difference map ---
        err = np.mean(np.abs(arr_in - out), axis=2)
        ax[1, i].imshow(err, cmap="inferno")
        ax[1, i].set_title("Difference Map", fontsize=9)
        ax[1, i].axis("off")

    plt.tight_layout()
    plt.show()

    # --- Terminal summary ---
    print("\n=== Transform Comparison ===")
    for name, mse, ssim_val in summary:
        print(f"{name:15s}  MSE={mse:.6e}  SSIM={ssim_val:.4f}")


# ==========================================================
# Entry Point
# ==========================================================
if __name__ == "__main__":
    main()
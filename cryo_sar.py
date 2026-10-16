"""
CryoSAR SAR-based analysis of Arctic sea ice.
"""

import rasterio
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter


def load_sar(file_path):
    """Load Sentinel-1 SAR image."""
    with rasterio.open(file_path) as src:
        print(f"Image: {src.width}x{src.height}, Bands: {src.count}")
        band = src.read(1).astype(np.float32)
    return band


def to_db(band):
    """Convert backscatter to dB."""
    return 10 * np.log10(band + 1e-10)


def filter_speckle(band_db, size=3):
    """Apply 3x3 mean filter to reduce speckle noise."""
    return uniform_filter(band_db, size=size)


def classify_sea_ice(band_db):
    classification = np.zeros_like(band_db, dtype=np.uint8)
    classification[(band_db >= -30) & (band_db < -20)] = 0  # open water
    classification[(band_db >= -20) & (band_db < -12)] = 1  # new ice
    classification[(band_db >= -12) & (band_db < -6)] = 2   # first-year ice
    classification[(band_db >= -6) & (band_db <= 0)] = 3    # multi-year ice
    return classification


def plot_results(raw, db, filtered, classification):
    """Plot all results in one figure."""
    fig, axes = plt.subplots(1, 4, figsize=(22, 6))

    axes[0].imshow(raw, cmap="gray")
    axes[0].set_title("Raw Backscatter")
    axes[0].axis("off")

    axes[1].imshow(db, cmap="gray", vmin=-25, vmax=0)
    axes[1].set_title("dB Converted")
    axes[1].axis("off")

    axes[2].imshow(filtered, cmap="gray", vmin=-25, vmax=0)
    axes[2].set_title("Speckle Filtered")
    axes[2].axis("off")

    im = axes[3].imshow(classification, cmap="viridis")
    axes[3].set_title("Sea Ice Classification")
    axes[3].axis("off")
    plt.colorbar(im, ax=axes[3], label="Class")

    plt.tight_layout()
    plt.savefig("cryo_sar_output.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Saved: cryo_sar_output.png")


if __name__ == "__main__":
    FILE_PATH = "path/to/your/sentinel1.tif"
    print("Loading SAR image...")
    raw = load_sar(FILE_PATH)
    print("Converting to dB...")
    db = to_db(raw)
    print("Filtering speckle...")
    filtered = filter_speckle(db)
    print("Classifying sea ice...")
    classification = classify_sea_ice(filtered)
    print("Plotting results...")
    plot_results(raw, db, filtered, classification)
    print("Done!")
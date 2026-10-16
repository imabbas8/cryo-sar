"""
CryoSAR
"""

import rasterio
import numpy as np
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter


def load_sar(file_path, scale_factor=4):
    """
    Load Sentinel-1 SAR image with downsampling to save memory.

    Args:
        file_path: Path to SAR .tif file
        scale_factor: Downsample factor (4 = 1/4 size, 8 = 1/8 size)
    """
    with rasterio.open(file_path) as src:
        print(f"Original image: {src.width}x{src.height}, Bands: {src.count}")
        new_height = src.height // scale_factor
        new_width = src.width // scale_factor

        band = src.read(
            1,
            out_shape=(new_height, new_width),
            resampling=rasterio.enums.Resampling.average,
        ).astype(np.float32)

        print(f"Downsampled to: {new_width}x{new_height}")

    return band


def to_db(band):
    return 10 * np.log10(band + 1e-10)


def filter_speckle(band_db, size=3):
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
    print("Saved: cryo_sar_output.png")


if __name__ == "__main__":
    FILE_PATH = (
        "data/S1C_IW_GRDH_1SDV_20261016T005057_20261016T005122_009903_013BEF_EB5E_COG.SAFE"
        "/measurement/s1c-iw-grd-vh-20261016t005057-20261016t005122-009903-013bef-002-cog.tiff"
    )

    SCALE_FACTOR = 8

    print("Loading SAR image...")
    raw = load_sar(FILE_PATH, scale_factor=SCALE_FACTOR)

    print("Converting to dB...")
    db = to_db(raw)

    print("Filtering speckle...")
    filtered = filter_speckle(db)

    print("Classifying sea ice...")
    classification = classify_sea_ice(filtered)

    print("Plotting results...")
    plot_results(raw, db, filtered, classification)

    print("Done!")
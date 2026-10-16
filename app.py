import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from cryo_sar import load_sar, to_db, filter_speckle, classify_sea_ice

st.set_page_config(page_title="CryoSAR", page_icon="❄️", layout="wide")

st.title("❄️ CryoSAR")
st.markdown("SAR-based analysis of Arctic sea ice using Sentinel-1 imagery.")

uploaded = st.file_uploader("Upload Sentinel-1 .tif file", type=["tif", "tiff"])

if uploaded:
    with open("temp.tif", "wb") as f:
        f.write(uploaded.getbuffer())

    with st.spinner("Processing..."):
        raw = load_sar("temp.tif")
        db = to_db(raw)
        filtered = filter_speckle(db)
        classification = classify_sea_ice(filtered)

    st.success("Processing complete!")

    fig, axes = plt.subplots(1, 4, figsize=(22, 6))

    axes[0].imshow(raw, cmap="gray")
    axes[0].set_title("Raw")
    axes[0].axis("off")

    axes[1].imshow(db, cmap="gray", vmin=-25, vmax=0)
    axes[1].set_title("dB")
    axes[1].axis("off")

    axes[2].imshow(filtered, cmap="gray", vmin=-25, vmax=0)
    axes[2].set_title("Filtered")
    axes[2].axis("off")

    im = axes[3].imshow(classification, cmap="viridis")
    axes[3].set_title("Classification")
    axes[3].axis("off")
    plt.colorbar(im, ax=axes[3])

    st.pyplot(fig)

    st.subheader("Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Min (dB)", f"{filtered.min():.2f}")
    col2.metric("Mean (dB)", f"{filtered.mean():.2f}")
    col3.metric("Max (dB)", f"{filtered.max():.2f}")

    st.subheader("Classification Legend")
    st.write("0 = Open Water | 1 = New Ice | 2 = First-Year Ice | 3 = Multi-Year Ice")
else:
    st.info("Upload a Sentinel-1 .tif file to begin.")
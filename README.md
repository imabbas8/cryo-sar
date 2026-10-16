# ❄️ CryoSAR

**SAR-based analysis of Arctic sea ice using Sentinel-1 imagery.**

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- Load Sentinel-1 GRD products (.tif)
- Downsample large images for memory efficiency
- Convert backscatter to dB scale
- Apply speckle filtering (3x3 mean)
- Classify sea ice types using data-driven percentiles
- Generate 4-panel visualizations
- Interactive Streamlit dashboard

## Installation

```bash
git clone https://github.com/imabbas8/cryo-sar.git
cd cryo-sar
pip install -r requirements.txt

![CryoSAR Output](cryo_sar_output.png)

_Four-panel visualization of Sentinel-1 SAR imagery over the Canadian Arctic:
(a) raw backscatter, (b) dB-converted, (c) speckle-filtered, and
(d) sea ice classification._
```

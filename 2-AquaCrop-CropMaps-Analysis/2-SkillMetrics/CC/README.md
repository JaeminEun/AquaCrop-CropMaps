# AquaCrop Wrapper Evaluation: Skill Metrics against CGLS

This module evaluates the output of AquaCrop wrapper simulations by comparing model results (e.g. Canopy Cover) to reference satellite observations from the Copernicus Global Land Service (CGLS). Metrics are computed spatially and aggregated to fit the resolution of the AquaCrop grid cell.

---

## 🔍 What It Does

- Compares **simulated daily time series** from AquaCrop to:
  - **FCOVER** (CGLS): for evaluating **Canopy Cover (CC)**
  - **DMP** (Dry Matter Productivity): optional for evaluating **Biomass**
- Computes **standard skill metrics**:
  - Pearson correlation coefficient (R)
  - Bias
  - Root Mean Square Deviation (RMSD)
  - Unbiased RMSD (ubRMSD)

Each script processes a different metric independently using parallel processing.

---

## 📂 Scripts Overview

| Script | Metric | Description |
|--------|--------|-------------|
| `1-Mz_CC_R.py` | Pearson R | Correlation between simulated and observed CGLS FCOVER |
| `2-Mz_CC_Bias.py` | Bias | Mean difference between AquaCrop and CGLS FCOVER |
| `3-Mz_CC_RMSD.py` | RMSD | Total deviation, (computed from bias)|
| `4-Mz_CC_ubRMSD.py` | ubRMSD | Unbiased deviation |

> 🔁 All scripts use the same spatial matching logic and can be **adapted to evaluate other variables like Biomass** by modifying the variable references inside the `calculate_metrics` function.

---

## 🗺 Data Sources

- **AquaCrop output**: NetCDF files from wrapper simulations.
- **CGLS FCOVER**: Two separate files covering 2018–2022.
- **CGLS DMP**: Used optionally to evaluate biomass.
- **Crop calendar (SOS/EOS)**: WorldCereal TIFFs used to mask non-growing season periods.

---

## ⚙️ How It Works

1. Each AquaCrop grid cell is matched with nearby 300m CGLS pixels using a crop mask (maize = 85).
2. Daily time series are extracted and interpolated as needed.
3. Masking is applied based on WorldCereal's SOS/EOS.
4. Final metrics are aggregated and saved as NetCDF maps.

---

## 🖥 Execution Notes

- Each script uses **Python multiprocessing** across 36 cores.
- Datasets are expected to be in pre-defined paths (update these if needed).
- Output files are named like `MapCorrelationMz_CC.nc`, `MapBiasMz_CC.nc`, etc.

---

## 🧪 Adapting to Biomass Evaluation

To evaluate **Biomass** instead of Canopy Cover:
- Change the variables `x_Mz_CC` and `y_Mz_CC` to use `'Biomass'` and `'CGLS_DMP'`.
- Adjust scaling or unit conversions as needed (`Biomass.diff() * 1000` is often used to approximate daily increments).
- All metrics scripts follow the same interface and logic — so modifications are minimal.

---

## 📌 Requirements

- `xarray`, `numpy`, `pandas`, `GDAL` (via CropCalFunctions), `netCDF4`, `Pillow`, `matplotlib`
- Datasets must be available in the correct directory structure.

---

## 📁 Outputs

Each script will produce a spatial NetCDF dataset (one per metric), usable for plotting or further statistical aggregation.

---

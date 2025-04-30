# AquaCrop Evaluation Pipeline

This portion of the repository includes tools for evaluating AquaCrop simulations against satellite-based observations, primarily from the **Copernicus Global Land Service (CGLS)**. It contains preprocessing routines, spatial matching logic, metric computation, and final visualization scripts.

---

## 📁 Directory Overview

```plaintext
1-CGLS_preprocess/   # Preprocessing Copernicus FCOVER/DMP data for evaluation
2-CropMaps/          # Crop-specific masking using multi-year remote sensing maps
3-SkillMetrics/      # Compute R, Bias, RMSD, ubRMSD between AquaCrop and CGLS
4-Figures/           # Boxplots, maps, and time series comparing model to observations
```

---

## 1️⃣ CGLS Preprocessing

Scripts and shell commands to process **CGLS FCOVER/DMP data**:
- Download via API (`CGLS_catalogue_and_download_demo.py`)
- Subset using NCO (`ncks_subsetFCOVER.sh`)
- Combine into time-aware NetCDF files (`ncecat`, `ExtractTime.py`, `ncap2`)
- Add units and chunk for efficiency

---

## 2️⃣ Crop Map Masking

Combines **EUCROPMAP (2018/2022)** and **WorldCereal (2021)** to:
- Identify **stable crop locations** for maize, spring/winter cereals
- Create intersection masks to reduce noise from crop rotation
- Resample to match CGLS 300m resolution
- Output used for spatial evaluation of AquaCrop outputs

---

## 3️⃣ Skill Metric Computation

Evaluates AquaCrop's **daily outputs** against satellite data:
- FCOVER → for Canopy Cover (CC)
- DMP → for Biomass (optional)

Four metrics computed:
- Pearson R
- Bias
- RMSD
- ubRMSD

Each script operates independently and outputs spatial NetCDF metric maps.

---

## 4️⃣ Visualization and Comparison

Scripts to produce evaluation figures:
- **Boxplots**: Aggregate performance across scenarios
- **Maps**: Spatial distribution of correlation or error
- **Diff Maps**: Compare setups (e.g., Calendar vs GDD)
- **Time Series**: Daily crop dynamics, grid-cell matched

Outputs are publication-ready `.png` figures summarizing model performance vs. CGLS.

---

## ⚙️ Requirements

- Python: `numpy`, `xarray`, `pandas`, `matplotlib`, `seaborn`, `netCDF4`, `Pillow`
- Shell: NCO tools (`ncks`, `ncecat`, `ncap2`, `ncatted`)
- Some parts use `Basemap` for mapping

---




# AquaCrop vs. CGLS Evaluation Toolkit

This repository contains a set of Python scripts developed to compare crop growth simulations from the **AquaCrop** model with observational datasets from **Copernicus Global Land Service (CGLS)**. The analysis focuses on evaluating model performance for both generic and maize-specific crop setups under different calibration scenarios (Calendar-based and GDD-based).

## 📂 Repository Structure

- `1-Boxplots.py`  
  Generates summary **boxplots** of correlation, bias, RMSD, and ubRMSD metrics for **Biomass** and **Canopy Cover (CC)** across four AquaCrop model setups:
  - Generic Calendar
  - Generic GDD
  - Maize Calendar
  - Maize GDD  
  Output: `Boxplots.png`

- `2-MapCompare.py`  
  Creates **spatial maps of correlation coefficients** for Canopy Cover (CC) to visualize how well each setup correlates with CGLS CC data. Includes:
  - Color-coded maps for each configuration
  - Summary statistics (mean, std) embedded per map  
  Output: `CC_R_Comparison.png`

- `3-DiffMap.py`  
  Produces **difference maps** between GDD and Calendar setups for both generic and maize crops, visualizing where GDD calibration improves or worsens correlation with observed data.  
  Output: `CorrelationDiff.png`

- `4-TimeSeries.py`  
  Performs **time-series comparisons** of daily **Biomass accumulation** and **Canopy Cover (CC)**:
  - AquaCrop outputs vs. aggregated CGLS DMP and FCOVER signals
  - Merges observational data with AquaCrop outputs at the grid-cell level
  - Visualizes daily dynamics and biomass growth phases  
  Output: `BiomassComparison.png`, `CC_Comparison.png`

## 🛰 Data Sources

- **AquaCrop Model Outputs**: Simulated crop development under different calibration and crop-specific scenarios.
- **CGLS DMP & FCOVER**: 300m observational products used for benchmarking model performance.
- **UnionResample300m.tif**: Used to align the model domain with satellite observations.

## 🛠 Dependencies

All scripts are built with standard Python libraries for scientific computing and geospatial analysis:

```bash
numpy
pandas
xarray
matplotlib
seaborn
PIL
netCDF4
Basemap (mpl_toolkits.basemap)
```

Some scripts also rely on internal project-specific functions like `ac_columns`, `ac_skiprows`, and `extract_doy_from_tiff`.

## 📈 Outputs Summary

Each script outputs a high-resolution `.png` image that can be used directly in reports or publications. The visualizations collectively highlight spatial, temporal, and statistical differences between modeling configurations and observed crop dynamics.

## ✍ Author

Developed by **Jaemin Eun** as part of a crop modeling evaluation framework.

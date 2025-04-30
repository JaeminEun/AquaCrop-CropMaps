<div style="float: right; text-align: right; margin-top: -80px;">
  <img src="https://github.com/user-attachments/assets/26282e47-c12c-4077-b605-96096071e9c4" alt="KU Leuven logo" width="200"/><br/>
</div>

# Enhancing AquaCrop Simulations with Crop Maps and Calendars: A Continental-Scale Modelling Approach for Europe

## AquaCrop Setup

## Data for AquaCrop with crop maps and calendars
1. Crop maps: Maize, Spring Wheat, and Winter Wheat locations combined for 2018, 2021, and 2022 from ESA WorldCereal 
([Van Tricht et al., 2023](https://doi.org/10.5194/essd-15-5491-2023)) and EUCROPMAP 
([d'Andrimont et al., 2021](https://doi.org/10.1016/j.rse.2021.112708)).
2. Crop calendars ([Franch et al., 2022](https://doi.org/10.1080/15481603.2022.2079273))
3. CLI climate files: Climate characteristics derived from MERRA-2 ([NASA GMAO](https://doi.org/10.5067/VJAFPLI1CSIV)) implemented
from spatial AquaCrop processing following [de Roos et al., 2021](https://doi.org/10.5194/gmd-14-7309-2021) and 
[Busschaert et al., 2022](https://doi.org/10.5194/hess-26-3731-2022).
4. SOL soil files: Soil characteristics derived from HWSD v1.2 ([Fischer et al., 2008](https://doi.org/10.1002/2014MS000330)) 
with soil hydraulic properties linked to mineral soil texture and organic matter
via pedo-transfer functions described in [de Lannoy et al., 2014](https://doi.org/10.1002/2014MS000330).
5. CRO files: Crop parameters derived from default AquaCrop crop files ([Raes et al., 2017](http://www.fao.org/nr/water/aquacrop.html))
and calibrated across Europe following processes similarly described in "Vincent's Paper".

## Data Structure (HPC)
There are 3 main data sources that are housed in the following path:`/staging/leuven/stg_00024/OUTPUT/jaemine/Data`
1. climate: Contains climate files (.CLI) and dependencies (.ETo, .PLU, .Tnx) for the European domain for years 2018-2022.  
2. Copernicus_DMP_300m: For validation of biomass (the processing is documented in more detail in the "Analysis" portion of this repository).
3. Copernicus_FCOVER_300m: For validation of canopy cover (the processing is documented in more detail in the "Analysis" portion of this repository).
4. CropMaps: Contains assets used to create the 300-m crop maps used to match the resolution of the Copernicus (CGLS) evaluation data. Assets include processed binaries (seperated by crop type) for each map source, resampled maps, and csv files of grid locations (row, col) containing the specified crop types.
5. soil: Contains soil files (.SOL) specific to each grid location for the European domain.

---

# AquaCrop Simulation Framework

This repository contains a full pipeline for preparing, running, and post-processing **AquaCrop** simulations at scale, using remote sensing and climate data as inputs.

## 📦 Repository Structure

```plaintext
Inputs/         # Create AquaCrop-compatible .CLI, .CRO, and .SOL input files
Wrapper/        # Generate PRM files and run AquaCrop in parallel across a grid
Postprocessing/ # Convert AquaCrop output files to NetCDF for analysis
```

---

## 1️⃣ Inputs: Climate, Crop, and Soil File Generation

These scripts create the necessary input files for AquaCrop:

- **`.CLI` files**: Generated from MERRA-2 climate data for each grid cell, including `.Tnx`, `.PLU`, `.ETo`, and `.CO2` references.
- **`.CRO` files**: Built from satellite-derived GDD phenology data, assigning unique crop stages per cell.
- **`.SOL` files**: Created using dominant soil texture data from HWSD, assigning one of 12 soil profiles per grid cell.

Each file is written with AquaCrop's naming conventions (e.g., `307_317.SOL`) and only where valid land and soil data exist.

---

## 2️⃣ Wrapper: Batch Simulation and PRM File Management

This module automates:

- **PRM file creation**: For each grid cell and crop type, generating AquaCrop project management files with proper configurations.
- **Parallel execution**: Runs AquaCrop simulations using Python's `multiprocessing`, optionally integrated with SLURM for HPC.

Supports multiple crop strategies (e.g., Gen-GDD, Mz-Cal, Mz-GDD), some of which depend on per-cell `.CRO` files or dynamic SOS timing from WorldCereal.

---

## 3️⃣ Postprocessing: Export to NetCDF

After simulations complete, this script:

- Extracts selected daily output variables (e.g., `Biomass`, `CC`) from AquaCrop’s `.OUT` files.
- Combines them into a single compressed **NetCDF4** file across all grid cells and time steps.
- Converts AquaCrop’s grid system to georeferenced `lat/lon` coordinates at 0.05° resolution.

This improves data accessibility for visualization, large-scale analysis, or climate impact assessments.

---

## 🚀 Usage Overview

1. Prepare input files in the `Inputs/` folder
2. Run the wrapper scripts per crop scenario in `Wrapper/`
3. Execute the NetCDF export from `Postprocessing/` once outputs are available

---

---

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

## ✍ Author

Developed by **Jaemin Eun**, as part of a geospatial modeling pipeline to benchmark crop simulations using earth observation data.





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


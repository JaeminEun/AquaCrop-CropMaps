# AquaCrop Crop File Generator Using GDD Data

This Python script generates AquaCrop-compatible `.CRO` files using growing degree-day (GDD) phenological data derived from satellite observations (VIIRS VNP22C2). It maps each AquaCrop grid cell to a custom crop configuration file using GDD thresholds, writing output files in parallel across a defined spatial grid.

## Overview

- Uses remotely sensed phenology data to calibrate crop development parameters
- Outputs a `.CRO` file per AquaCrop grid cell (e.g., `GDD_123_456.CRO`)
- Includes default crop parameters related to canopy growth, rooting depth, and water productivity
- Skips locations without corresponding `.SOL` soil files
- Parallelized using Python's `multiprocessing` for speed

## Workflow Summary

1. Load crop GDD data and landmask from NetCDF files
2. Loop through a grid of AquaCrop cells
3. For each land cell with valid soil data:
   - Extract median GDD values for crop stages
   - Write an AquaCrop `.CRO` file with parameterized settings

## Usage

### Modify Input Paths

- **Output Directory**:  
  `dir_data` → Where `.CRO` files are saved

- **Input NetCDF Files**:
  - `lis_input_EU.d01.nc` → For LANDMASK
  - `phenology_VNP22C2_GDD_ALL_EU.nc` → For crop GDD stages

- **Soil Directory**:  
  Used to check if a `.SOL` file exists before writing a `.CRO` file

## Output Example

```
GDD-Crop/INPUT/crop/
├── GDD_0_0.CRO
├── GDD_0_1.CRO
├── ...
└── GDD_700_920.CRO
```

Each file contains a full crop configuration using growing degree-day thresholds.

## Performance Notes

- Uses multiprocessing for speed (default: 36 processes)
- Skips grid cells with no matching `.SOL` file
- Median GDD values across multiple years ensure robust phenological parameterization



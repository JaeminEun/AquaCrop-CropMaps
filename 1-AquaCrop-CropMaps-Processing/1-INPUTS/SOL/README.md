# AquaCrop Soil File Generator from HWSD Data

This Python script generates AquaCrop-compatible `.SOL` files based on dominant soil texture data extracted from a NetCDF file. It maps each AquaCrop grid cell to one of 12 predefined soil types and saves a renamed copy of the corresponding `.SOL` file using AquaCrop's grid naming conventions.

## Overview

- Extracts soil texture dominance from a NetCDF file derived from the Harmonized World Soil Database (HWSD)
- Skips masked-out land areas 
- Copies the matching predefined `.SOL` file into the output directory using a `<row>_<col>.SOL` naming pattern

This script was adapted by Jaemin Eun based on input data created by Dr. Shannon De Roos.

## Workflow Summary

1. Load soil texture and landmask data from a NetCDF file.
2. Loop through a defined range of AquaCrop grid cells.
3. For each land cell:
   - Determine the dominant soil type.
   - Copy the corresponding `.SOL` template file (e.g. `TEXT_0.SOL` to `TEXT_11.SOL`).
   - Rename and store it based on grid coordinates.

## Usage

### Set Parameters in the Script

- **Grid Range**:
  Modify the grid boundaries with `row_start`, `row_end`, `col_start`, `col_end`.

- **Input NetCDF File**:
  Update `netcdf_file` to point to the LIS input containing `TEXTURE` and `LANDMASK`.

- **Template Soil Directory**:
  Ensure `input_dir` contains the 12 predefined `.SOL` files named `TEXT_0.SOL` to `TEXT_11.SOL`.

- **Output Directory**:
  Set `soil_dir` to the desired path for saving the grid-based `.SOL` files.

### Example Output

```
soil/
├── 0_0.SOL
├── 0_1.SOL
├── ...
└── 700_920.SOL
```

Each file corresponds to a grid cell with land presence and contains AquaCrop-compatible soil parameters.

## Notes

- Soil texture type `13` is skipped by design.
- Ensure the 12 `.SOL` template files exist before running the script.
- The script assumes the `TEXTURE` variable in the NetCDF file has the shape `[soil_class, row, col]`.



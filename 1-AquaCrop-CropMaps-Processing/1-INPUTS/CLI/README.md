
# MERRA-2 to AquaCrop Climate File Generator

This Python script converts MERRA-2 climate forcing data into AquaCrop-compatible `.CLI` files. It was originally developed by Dr. Shannon De Roos and has been adapted by Jaemin Eun to ingest individual MERRA-2 NetCDF files rather than LIS SURFACEMODEL output.

## Overview

AquaCrop requires daily climate input files for:
- Minimum and maximum temperature (`.Tnx`)
- Precipitation (`.PLU`)
- Reference evapotranspiration (`.ETo`)
- A `.CLI` file pointing to the above components and a CO₂ file

This script automates the generation of these files for a given AquaCrop grid cell, identified by its `lat_id` and `lon_id` from a reference grid.

## Features

- Converts daily MERRA-2 NetCDF files into AquaCrop format
- Uses AquaCrop grid structure from LIS SURFACEMODEL NetCDF to extract lat/lon coordinates
- Outputs `.Tnx`, `.PLU`, `.ETo`, and `.CLI` files into organized subdirectories
- Designed for batch processing using looped grid IDs

## Usage

### 1. Set Input Parameters

- `lat_id`, `lon_id`: Indexes identifying the AquaCrop grid cell
- `base_dir`: Output directory where AquaCrop input files will be saved
- MERRA-2 and LIS NetCDF paths are hardcoded but can be modified

### 2. Example: Run for a Single Cell

```python
lat_id = 317
lon_id = 307
base_dir = '/your/output/directory'
write_CLI_LIS(lat_id, lon_id, base_dir)
```

### 3. Batch Process Over a Range

```python
row_start = 317
row_end = 317
col_start = 307
col_end = 307

for lat_id in range(row_start, row_end + 1):
    for lon_id in range(col_start, col_end + 1):
        write_CLI_LIS(lat_id, lon_id, base_dir)
```

## Directory Structure

Each output subdirectory is named using the pattern `<lat_id>_<lon_id>_<start_year>_<end_year>`. Inside, the following files will be created:

- `*.Tnx` – daily min/max temperature
- `*.PLU` – daily precipitation
- `*.ETo` – daily evapotranspiration
- `*.CLI` – AquaCrop input control file

## File Format Assumptions

- MERRA-2 files are daily and follow the pattern `MERRA2_AC_YYYYMMDD.nc`
- Temperature, precipitation, and evapotranspiration variables are named:
  - `TMIN`, `TMAX`, `PREC`, and `ETo`
- AquaCrop reference grid is based on:
  `/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/SURFACEMODEL_tchunk.nc`

## Output Example

```
317_307_2022_2022/
├── 317_307.Tnx
├── 317_307.PLU
├── 317_307.ETo
└── 317_307.CLI
```
## Notes

- The script currently only supports climate data for the year 2022.
- Be sure the MERRA-2 data for the full year exists before running.



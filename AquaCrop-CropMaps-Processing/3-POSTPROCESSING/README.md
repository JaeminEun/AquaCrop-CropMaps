# AquaCrop Post-Processing: NetCDF Export Tool

This module converts AquaCrop's daily `.OUT` output files into a single compressed and structured **NetCDF** file. It allows for selective export of specific variables across all spatial grid cells, resulting in significantly more efficient data storage and retrieval for large-scale analyses.

---

## 🧭 Purpose

- Consolidate distributed AquaCrop output files into a **single NetCDF file**.
- Allow the **selection of key variables** (e.g., `Biomass`, `CC`, etc.) to reduce file size.
- Improve **read and write performance** for post-simulation analysis and visualization.

---

## ⚙️ How It Works

The core script is [`vars_ACout_to_netCDF.py`](./vars_ACout_to_netCDF.py):

1. Loops over all AquaCrop output folders.
2. Reads the daily `PRMday.OUT` file from each grid cell.
3. Extracts only user-specified variables.
4. Writes them into a structured `NetCDF4` file (`dimensions`: time × lat × lon).

### Coordinate system

The geospatial references are defined using `COORD_AC.py`, which maps AquaCrop's internal row/column system to real-world latitudes and longitudes at **0.05° resolution**.

---

## 🗂 Required Files and Modules

| File | Description |
|------|-------------|
| `vars_ACout_to_netCDF.py` | Main conversion script |
| `acout_filestructure.py` | Helps interpret AquaCrop output file structure |
| `COORD_AC.py` | Spatial referencing for grid-to-lat/lon conversion |
| `Mz-OUT-nc.slurm` | SLURM job script to run the export on HPC |

---

## 🧪 Example Output

The script outputs a file like:

```
Mz-GDD_2020Fert_2018-2022.nc
```

This file contains:
- Daily data from 2018 to 2022
- Variables: `Biomass`, `CC` (customizable)
- Dimensions: `time × latitude × longitude`

---

## 🖥 Running with SLURM (Recommended)

The job can be submitted with the following SLURM script:

```bash
#!/bin/bash
#SBATCH -t hh:mm:ss
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH -A lp_ees_swm_ls_002 (your vsc credit account)
#SBATCH --cluster=genius
#SBATCH -o run_log.txt
#SBATCH -e error_out.txt
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=YOUR.EMAIL@kuleuven.be

module load Python/3.10.4
source ~/envs/aquacrop_env/bin/activate

python vars_ACout_to_netCDF.py
```

Submit the job:

```bash
sbatch Mz-OUT-nc.slurm
```

---

## 📝 Customization

You can modify the following in `vars_ACout_to_netCDF.py`:

```python
vars = ['Biomass', 'CC']        # Output variables to include
years = [2018, 2022]            # Time span
run_name = 'Mz-GDD_2020Fert'    # Used in naming output file
```

---

## 📌 Notes

- Handles leap years and AquaCrop quirks (e.g. -9.9 placeholders).
- Invalid/missing files are skipped with error logging.
- Designed to be used after wrapper simulations have finished.

---


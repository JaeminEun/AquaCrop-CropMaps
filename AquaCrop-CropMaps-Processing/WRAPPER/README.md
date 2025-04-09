# AquaCrop Wrapper (Multi-Crop Setup)

This repository provides a streamlined, script-based approach to running the AquaCrop model across multiple grid cells with crop-specific parameterization. It is designed to automate the preparation of AquaCrop's Project Management (PRM) files and execute simulations in parallel using Python multiprocessing.

---

## 🌱 Overview

The AquaCrop wrapper consists of two key script types for each crop configuration:

- **PRM script**: Prepares AquaCrop input (`.PRM`) files for a given grid cell.
- **Exec script**: Handles parallelized execution across all cells, generating simulation outputs for a specified time period.

Each crop type is stored in its own configuration with custom PRM logic depending on modeling needs.

---

## 📁 Folder Structure (per crop)

Each crop type has its own set of scripts and input folders:

```
/<Crop-Type>/
│
├── AC_exec_<Crop-Type>.py   # Main script to execute AquaCrop in parallel
├── AC_PRM_<Crop-Type>.py    # Script to generate AquaCrop PRM files
├── INPUT/                   # Input files: crop, climate, soil, management
└── OUTPUT/                  # Outputs saved per grid cell
```

---

## 🌾 Crop Configurations

| Crop Type | Crop File Setup | Cropping Period | Special Notes |
|-----------|------------------|------------------|----------------|
| **Gen-Cal** | Shared | Fixed: Jan 1–Dec 31 | Simple baseline |
| **Gen-GDD** | **Unique per grid cell** | Fixed annually | Each grid has its own `.CRO` file |
| **Mz-Cal** | Shared | **SOS from WorldCereal** + offset | WorldCereal start-of-season (SOS) integrated |
| **Mz-GDD** | Shared | **SOS from WorldCereal** + offset | Uses GDD dynamics but not unique `.CRO` |

Offset: A buffer of 24 days is added to align the AquaCrop emergence window with WorldCereal Crop Calendar definitions.

---

## ⚙️ Running the Wrapper

To run a configuration locally:

```bash
python AC_exec_<Crop-Type>.py
```

Each script uses 36 cores by default via Python’s `multiprocessing.Pool`.

---

## 🖥 Running with SLURM (Recommended for HPC)

It is **strongly recommended** to submit the wrapper as a SLURM job to:
- Utilize all requested cores efficiently.
- Keep the job running even after logging out.
- Avoid losing progress on long runs.

Example SLURM script: `AC_exec.slurm`

```bash
#!/bin/bash
#SBATCH --job-name=AC_Run
#SBATCH --output=AC_Run.out
#SBATCH --error=AC_Run.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=36
#SBATCH --time=12:00:00
#SBATCH --mem=64G

module load Python/3.10.4  # Adjust based on your environment
source ~/envs/aquacrop_env/bin/activate  # Activate your virtual environment

python AC_exec_Mz-GDD.py  # Replace with the target script
```

To submit:

```bash
sbatch AC_exec.slurm
```

> ✅ This will run the AquaCrop wrapper using 36 CPU cores.  
> 🔁 Even if your SSH session ends, the job continues until completion or timeout.

---

## 📌 Notes

- PRM scripts require valid `.SOL` (soil) files to proceed.
- WorldCereal SOS TIFFs must be accessible and correctly formatted.
- Ensure that for `Gen-GDD`, the per-cell `.CRO` files are generated beforehand.

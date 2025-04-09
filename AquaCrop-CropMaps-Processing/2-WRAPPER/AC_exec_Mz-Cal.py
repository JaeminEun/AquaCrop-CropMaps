# Jaemin Eun

import os
import shutil
import pandas as pd
import numpy as np
from multiprocessing import Pool
from AC_PRM import run_ac_pro_yrs
import subprocess
import time

def main():
    # Read row and column values from the CSV file
    csv_path = '/data/leuven/361/vsc36151/data-jeun/AquaCrop/Continent_EU/AC_Grids_w_maize.csv'
    data = pd.read_csv(csv_path)

    # Ensure the CSV has 'row' and 'col' columns
    if not {'row', 'col'}.issubset(data.columns):
        raise ValueError("CSV file must contain 'row' and 'col' columns.")
    
    skip_coords = {(400, 51), (423, 877)}  # Rows and columns to skip

    # Prepare arguments, filtering out skipped coordinates
    args = [
        (row, col) 
        for row, col in zip(data['row'], data['col']) 
        if (row, col) not in skip_coords
    ]

    # Create pool for parallel processing
    with Pool(36) as p:  # Define the number of cores for parallelization
        p.map(wrapper, args)  # Perform actual parallelization

def wrapper(coords):
    row, col = coords

    # Filenames and directories
    input_dir = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/AdjustWC/INPUT/'
    dir_out = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/AdjustWC/OUTPUT/'
    dir_soil = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/soil/'
    dir_cli = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/climate/'
    dir_crop = input_dir + 'crop/'
    dir_suppl = input_dir + 'suppl_input/'

    start_year = 2018
    end_year = 2022

    fname = f"{row}_{col}"
    pa = os.path.join(dir_out, fname)
    PRM = os.path.join(pa, 'LIST', f"{fname}.PRM")

    if os.path.exists(os.path.join(dir_soil, f"{fname}.SOL")):
        if os.path.exists(pa):
            print(f"Skipping {row}, {col} - output directory already exists", flush=True)
            return

        print(f"======== Processing {row}, {col} ========", flush=True)

        os.makedirs(pa)
        os.chdir(pa)

        shutil.copytree(input_dir + 'SIMUL', os.path.join(pa, 'SIMUL'))
        os.makedirs(os.path.join(pa, 'OUTP'))
        os.makedirs(os.path.join(pa, 'LIST'))
        with open(os.path.join(pa, 'LIST', 'ListProjects.txt'), 'a') as file:
            file.write(f"{fname}.PRM\n")

        AC_loc = '/data/leuven/361/vsc36151/data-jeun/FORTRAN/AquaCrop-main/src/aquacrop'
        os.symlink(AC_loc, os.path.join(pa, 'aquacrop'))

        run_ac_pro_yrs(row, col, dir_out, dir_soil, dir_cli, dir_crop, dir_suppl, start_year, end_year)

        try:
            start_time = time.time()
            subprocess.run([os.path.join(pa, 'aquacrop')], timeout=30, check=True)
            elapsed_time = time.time() - start_time
            print(f"Completed {row}, {col} in {elapsed_time:.2f} seconds", flush=True)
        except subprocess.TimeoutExpired:
            print(f"Timeout for {row}, {col}. Cleaning up...", flush=True)
            shutil.rmtree(pa)  # Remove directory and contents
            return
        except subprocess.CalledProcessError as e:
            print(f"Error for {row}, {col}: {e}", flush=True)
            shutil.rmtree(pa)  # Cleanup on error
            return

        shutil.copyfile(PRM, os.path.join(pa, f"{fname}.PRM"))
        shutil.rmtree(os.path.join(pa, 'SIMUL'))
        shutil.rmtree(os.path.join(pa, 'LIST'))
        os.unlink(os.path.join(pa, 'aquacrop'))
        os.remove(os.path.join(pa, 'OUTP', 'AllDone.OUT'))
        os.remove(os.path.join(pa, 'OUTP', 'ListProjectsLoaded.OUT'))

main()



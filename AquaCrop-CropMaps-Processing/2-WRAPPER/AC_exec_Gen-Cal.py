# !/usr/bin/env python
import os
import shutil
import numpy as np
from multiprocessing import Pool
from AC_PRM import run_ac_pro_yrs

''' --------------------------------------------------------------------------------------------------------------------------
Executable for AquaCrop, the regional version. With multiprocessing it can be run on the max available cores on a single node.
@ Shannon de Roos 2020: original author, for AquaCropV6.1
@ Louise Busschaert 2023: simplified and adapted for AquaCropV7 and higher
----------------------------------------------------------------------------------------------------------------------------'''


# ------------------------ parallel processing python ------------------------------------------------------------------------

def main():
    # MAKE SURE TO DOUBLE CHECK ROW COL EXTENT!!!
    row_start = int(0)
    row_end = int(700)
    col_start = int(0)
    col_end = int(920)
    args = list()
    for row in np.arange(row_start, row_end + 1):
        for col in np.arange(col_start,col_end + 1):
            args.append((col, row))

    p = Pool(36)            # For paralelization: define number of cores.
                            # If not (1 process): p = Pool(1)
    p.map(wrapper, args)    #performs actual parallelization


def wrapper(coords):  # wraps all functions into one list of functions

    col, row = coords

    #filenames and directories
    input_dir =  '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/INPUT/'
    dir_out = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/OUTPUT/'
    dir_soil = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/soil/'
    dir_cli = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/climate/'
    dir_crop = input_dir + 'crop/'
    dir_suppl = input_dir + 'suppl_input/'

    start_year = 2018
    end_year = 2022

    fname = str(row) + '_' + str(col)
    pa = dir_out  + fname + '/'
    PRM = pa + 'LIST/' + fname + '.PRM'


    if os.path.exists(dir_soil + fname+'.SOL'): # To run only for pixel
                                                # with available soil file
        print('=========', row, col, '=========', flush=True)

        # Make new local directory for each gridcell
        os.mkdir(pa)
        os.chdir(pa)

        # Place Aquacrop directories SIMUL and LIST in local directory
        shutil.copytree(input_dir + 'SIMUL', pa + 'SIMUL')
        os.mkdir(pa + 'OUTP')
        os.mkdir(pa + 'LIST')
        with open(pa + 'LIST/ListProjects.txt', 'a') as file:
            file.write(fname + '.PRM\n')

        # Link Aquacrop model to current directory
        AC_loc =  '/data/leuven/361/vsc36151/data-jeun/FORTRAN/AquaCrop-main/src/aquacrop'
        os.symlink(AC_loc, pa + 'aquacrop')

        # Prepare PRM file
        run_ac_pro_yrs(row, col,
                       dir_out, dir_soil, dir_cli, dir_crop, dir_suppl,
                       start_year, end_year)
        # Run the executable
        os.system(pa + 'aquacrop')

        #remove extra files and directories: only save PRM and output file
        # Comment in case of debugging to look into the files
        shutil.copyfile(PRM, pa + fname + '.PRM')
        shutil.rmtree(pa + 'SIMUL')
        shutil.rmtree(pa + 'LIST')
        os.unlink(pa + 'aquacrop')
        os.remove(pa + 'OUTP/AllDone.OUT')
        os.remove(pa + 'OUTP/ListProjectsLoaded.OUT')

main()

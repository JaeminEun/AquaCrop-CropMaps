#!/bin/bash
#SBATCH -t 23:59:59
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH -A lp_ees_swm_ls_002
#SBATCH --cluster=wice
#SBATCH -o run_log.txt
#SBATCH -e error_out.txt
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=jaemin.eun@kuleuven.be


source /data/leuven/317/vsc31786/miniconda/bin/activate /data/leuven/361/vsc36151/envs/vsc-hpc-env


cd /staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/ncOUT
python vars_ACout_to_netCDF.py
wait


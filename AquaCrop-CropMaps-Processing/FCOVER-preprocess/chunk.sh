#!/bin/bash
module load NCO/5.0.1-foss-2021a

fileIN="FILE.nc" # Change to your filename
fileOUT="${fileIN%.nc}_tchunk.nc"
timesteps=512  # Set chunk size for the time dimension

ncks -4 -L 4 --cnk_dmn time,$timesteps --cnk_dmn lat,1 --cnk_dmn lon,1 $fileIN $fileOUT

echo "Output file created: $fileOUT"


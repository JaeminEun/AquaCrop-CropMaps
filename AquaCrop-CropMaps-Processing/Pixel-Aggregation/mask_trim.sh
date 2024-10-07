#!/bin/bash

# -----------------------------------------------------------------------------
# Script: mask_trim.sh
# Author: Jaemin Eun
# Contact: jaemin.eun@kuleuven.be
# Date Created: 2024-10-07
# Last Modified: 2024-10-07
# Version: 1.0
#
# Description:
# This script removes the rightmost column and the topmost row from a netCDF file.
# The purpose is to match the dimensions of a crop mask to the corresponding
# validation data from the Copernicus Global Land Service (CGLS) products.
#
# Usage:
# ./mask_trim.sh input_file.nc output_file.nc
#
# Requirements:
# - NCO (NetCDF Operators) must be installed on the system.
#    * VSC HPC: module load NCO/5.0.1-foss-2021a
# -----------------------------------------------------------------------------

# Check if input and output filenames are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_file.nc output_file.nc"
    exit 1
fi

# Input and output file names
input_file="$1"
output_file="$2"

# Get the dimensions of the input file
# Here, we extract the 'lat' and 'lon' dimensions to understand the grid size
lat_dim=$(ncdump -h "$input_file" | grep "lat = " | cut -d " " -f 3)
lon_dim=$(ncdump -h "$input_file" | grep "lon = " | cut -d " " -f 3)

# Calculate new dimensions after removing top row and rightmost column
# We subtract 1 from the total dimensions because we want to remove one row and one column
new_lat_dim=$((lat_dim - 1))  # Remove topmost row
new_lon_dim=$((lon_dim - 1))  # Remove rightmost column

# Use ncks to remove the top row and rightmost column
# We are trimming the file to adjust the crop mask dimensions for compatibility with
# the CGLS validation data, ensuring the grids align correctly
ncks -d lat,1,$new_lat_dim -d lon,0,$new_lon_dim "$input_file" -o "$output_file"

# Confirm completion
if [ $? -eq 0 ]; then
    echo "Successfully trimmed the file: $output_file"
else
    echo "Error trimming the file."
fi


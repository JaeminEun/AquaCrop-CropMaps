# Jaemin Eun
# Post-Processing Set-Up

# This script takes soil information derived from the HWSD and processes them into AquaCrop .SOL file formats.
# It selects one of 12 total files that represent a "dominant" soil texture and renames it based on the
# AquaCrop row/col naming conventions. 

from netCDF4 import Dataset
import numpy as np
import shutil
import os

# Defining the grid we want to extract soil information from. 
row_start = 0
row_end = 700
col_start = 0
col_end = 920

# The netcdf file is used to draw the soil texture information from a previous LIS input created by Dr. de Roos.
# From this layer, unnecessary regions are completely masked to make processing more efficient. 
netcdf_file = '/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/lis_input_EU.d01.nc'
nc = Dataset(netcdf_file, 'r')

# Get the Texture and LANDMASK variables
texture_var = nc.variables['TEXTURE']
landmask_var = nc.variables['LANDMASK']

# Path to directory containing soil files, i.e., in TEXT .SOL format.
# THIS SHOULD NOT BE CHANGED, i.e. these files already exist and describe the soil characteristics
input_dir = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/SOL_LIS/' 

# Outputting the individual soil files and renaming them for each grid location.
# This should be changed based on user characteristics.
soil_dir = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/soil/'

# Iterate over the rows and columns of the grid
for row in range(row_start, row_end + 1):
    for col in range(col_start, col_end + 1):
        # Check the value of LANDMASK for the current cell
        landmask_value = landmask_var[row, col]
        
        if landmask_value == 0:
            continue
 
        soil_type_value = texture_var[:, row, col]  # Assuming texture_var is multi-dimensional

        # Find the index location of the largest value
        # Locations can have different soil classes in them, their assigned soil type is based on 
        # which type is most 'dominant' i.e. np.argmax().
        max_index = np.argmax(soil_type_value)

        # Skip if the dominant texture is 13
        if max_index == 13:
            continue

        # Generate the filename for the corresponding soil file
        soil_filename = f'TEXT_{max_index}.SOL'

        # Generate the new filename based on the row and column location
        new_filename = f'{row}_{col}.SOL'

        # Copy the soil file to the output directory and rename it
        shutil.copy(os.path.join(input_dir, soil_filename), os.path.join(soil_dir, new_filename))

# Close the netCDF file
nc.close()




# Jaemin Eun
# Mask CGLS pixels using crop map locations

import xarray as xr
import rasterio
import numpy as np

# Load the CGLS cells netCDF file
# Replace with paths to CGLS FCOVER or DMP files
CGLS_nc = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/Copernicus_DMP_300m/EU_DMP_300m_2018-2022.nc')

# Assuming the variable name in the netCDF is 'DMP' (Can change to FCOVER)
CGLS_cells = CGLS_nc['DMP']

# Load the crop mask TIFF (resampled to match the netCDF grid)
with rasterio.open('/staging/leuven/stg_00024/OUTPUT/jaemine/CropMaps/Maize/MaizeMap_300m_2018-2022.tif') as src:
    crop_mask = src.read(1)  # Read the first band

# Convert crop_mask to a boolean mask (crop locations are set to 85)
crop_mask_bool = crop_mask == 85

# Apply the crop mask to the CGLS cells data (mask non-crop areas)
masked_CGLS_cells = CGLS_cells.where(crop_mask_bool)

# Save the masked CGLS cells data to a new netCDF file
masked_CGLS_cells.to_netcdf('masked_EU_DMP_300m_2018-2022.nc')


# Jaemin Eun
# Convert crop mask tiff to a NetCDF file

import rasterio
import xarray as xr
import numpy as np

# Open the crop mask TIFF
with rasterio.open('/staging/leuven/stg_00024/OUTPUT/jaemine/CropMaps/Maize/MaizeMap_300m_2018-2022.tif') as src:
    crop_mask = src.read(1)  # Read the first band (assuming the crop mask is in a single band)
    crop_mask_transform = src.transform
    crop_mask_crs = src.crs
    crop_mask_meta = src.meta

# Create an xarray DataArray from the crop mask
crop_mask_da = xr.DataArray(
    crop_mask,
    dims=['y', 'x'],
    coords={
        'x': np.arange(crop_mask.shape[1]) * crop_mask_transform[0] + crop_mask_transform[2],
        'y': np.arange(crop_mask.shape[0]) * crop_mask_transform[4] + crop_mask_transform[5]
    },
    attrs={'crs': str(crop_mask_crs)}
)

# Convert the DataArray to a Dataset and save it as netCDF
crop_mask_ds = xr.Dataset({'crop_mask': crop_mask_da})
crop_mask_ds.to_netcdf('crop_mask.nc')

print("Crop mask has been converted to netCDF format.")


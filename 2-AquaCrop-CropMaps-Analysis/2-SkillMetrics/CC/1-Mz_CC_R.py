# Jaemin Eun

import numpy as np
import pandas as pd
from datetime import date, timedelta
import os
import xarray as xr
from scipy import stats
from COORD_AC import mindist
from acout_filestructure import ac_columns, ac_skiprows
import math
from pathlib import Path
import matplotlib
from matplotlib import pyplot as plt
from CropCalFunctions import extract_doy_from_tiff
from AC_Metrics import pearson_r, compute_bias, compute_rmsd, compute_ubrmsd, value_ubrmsd
from PIL import Image
from netCDF4 import Dataset
from multiprocessing import Pool
#import cartopy.crs as ccrs
#import cartopy.feature as cfeature

# Load datasets
GDD_ds = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/climate_merge/resampled_tchunk.nc')
lats = GDD_ds['lat'].values
lons= GDD_ds['lon'].values

AC_out_Mz = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/OUTPUTS/Mz-Output_2018-2022_tchunk.nc')
DMP = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/EU_DMP_300m.nc')
DMP_lats = DMP['lat'].values # NEED TO KEEP THESE VALUES TO CALCULATE VALIDATION WINDOWS!!!
DMP_lons = DMP['lon'].values
FCOVER_1 = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/EU_FCOVER_300m_2018-01-10_to_2020-06-30.nc')
FCOVER_2 = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/EU_FCOVER_300m_2020-07-10_to_2022-11-20.nc')

# Initialize some constants
#row_start = 150
#row_end = 250
#col_start = 150
#col_end = 250

# Load the crop map
tif_path = '/data/leuven/361/vsc36151/VincentShare/UnionResample300mNearest.tif'
tif_image = Image.open(tif_path)
tif_array = np.array(tif_image)

# Read the relevant rows and columns from the CSV file
relevant_coords = pd.read_csv('/data/leuven/361/vsc36151/data-jeun/AquaCrop/Continent_EU/AC_Grids_w_maize.csv')
min_row = relevant_coords['row'].min()
max_row = relevant_coords['row'].max()
min_col = relevant_coords['col'].min()
max_col = relevant_coords['col'].max()

# Define extent based on CSV
lat_min_global = lats[min_row] - (lats[min_row + 1] - lats[min_row]) / 2
lat_max_global = lats[max_row] + (lats[max_row + 1] - lats[max_row]) / 2
lon_min_global = lons[min_col] - (lons[min_col + 1] - lons[min_col]) / 2
lon_max_global = lons[max_col] + (lons[max_col + 1] - lons[max_col]) / 2

lat_indices_global = np.where((DMP_lats >= lat_min_global) & (DMP_lats <= lat_max_global))[0]
lon_indices_global = np.where((DMP_lons >= lon_min_global) & (DMP_lons <= lon_max_global))[0]

netcdf_file = '/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/lis_input_EU.d01.nc'
nc = Dataset(netcdf_file, 'r')

texture_var = nc.variables['TEXTURE']
landmask_var = nc.variables['LANDMASK']

def calculate_metrics(coords):
    row, col = coords
    lat, lon = lats[row], lons[col]
    name = str(row) + '_' + str(col)
    #print(name)

    df_Mz = pd.DataFrame({'time': AC_out_Mz['time'], 'Biomass': AC_out_Mz['Biomass'][:, row, col].values})
    df_Mz['CC'] = AC_out_Mz['CC'][:, row, col].values
    df_Mz['CC'] = df_Mz['CC']/100
    df_Mz = df_Mz.set_index('time')
    df_Mz['B_diff'] = (df_Mz['Biomass'].diff()) * 1000
    df_Mz[df_Mz['B_diff'] < -1] = np.nan

    lat_ac = lats[row]
    lon_ac = lons[col]
    delta_lat_ac = (lats[row + 1] - lat_ac) / 2
    delta_lon_ac = (lons[col + 1] - lon_ac) / 2

    lat_min = lat_ac - delta_lat_ac
    lat_max = lat_ac + delta_lat_ac
    lon_min = lon_ac - delta_lon_ac
    lon_max = lon_ac + delta_lon_ac

    lat_indices = np.where((DMP_lats >= lat_min) & (DMP_lats <= lat_max))[0]
    lon_indices = np.where((DMP_lons >= lon_min) & (DMP_lons <= lon_max))[0]

    contained_cells = []

    for i in lat_indices:
        for j in lon_indices:
            center_lat = DMP_lats[i]
            center_lon = DMP_lons[j]
            if (lat_min <= center_lat <= lat_max) and (lon_min <= center_lon <= lon_max):
                contained_cells.append((i, j))

    #correlation_values_local = np.full((len(lat_indices_global), len(lon_indices_global)), np.nan)
    partial_result = []

    if contained_cells:
        i_start, i_end = min(i for i, _ in contained_cells), max(i for i, _ in contained_cells)
        j_start, j_end = min(j for _, j in contained_cells), max(j for _, j in contained_cells)

        specified_region_values = tif_array[i_start + 1:i_end + 2, j_start:j_end + 1]
        
        dmp_values = DMP['DMP'][:, i_start:i_end + 1, j_start:j_end + 1]
        FCOVER_values_1 = FCOVER_1['FCOVER'][:, i_start:i_end + 1, j_start:j_end + 1]
        FCOVER_values_2 = FCOVER_2['FCOVER'][:, i_start:i_end + 1, j_start:j_end + 1]
        
        mask = specified_region_values == 85

        dmp_filtered = np.where(mask, dmp_values, np.nan)
        fcover_filtered_1 = np.where(mask, FCOVER_values_1, np.nan)
        fcover_filtered_2 = np.where(mask, FCOVER_values_2, np.nan)

        for CGLS_row in range(i_start, i_end + 1):
            for CGLS_col in range(j_start, j_end + 1):
                DMP_CGLS_cell = dmp_filtered[:, CGLS_row - i_start, CGLS_col - j_start]
                CGLS_DMP = pd.DataFrame({'time': DMP['time'], 'CGLS_DMP': DMP_CGLS_cell})
                CGLS_DMP = CGLS_DMP.set_index('time')

                FCOVER_CGLS_cell_1 = fcover_filtered_1[:, CGLS_row - i_start, CGLS_col - j_start]
                FCOVER_CGLS_cell_2 = fcover_filtered_2[:, CGLS_row - i_start, CGLS_col - j_start]

                CGLS_FCOVER_1 = pd.DataFrame({'time': FCOVER_1['time'], 'CGLS_FCOVER': FCOVER_CGLS_cell_1})
                CGLS_FCOVER_1 = CGLS_FCOVER_1.set_index('time')

                CGLS_FCOVER_2 = pd.DataFrame({'time': FCOVER_2['time'], 'CGLS_FCOVER': FCOVER_CGLS_cell_2})
                CGLS_FCOVER_2 = CGLS_FCOVER_2.set_index('time')

                CGLS_FCOVER_ALL = pd.concat([CGLS_FCOVER_1, CGLS_FCOVER_2])

                DMP_daily = pd.DataFrame({'dekad': DMP['time']}, index=CGLS_DMP.index).asfreq('D')
                FCOVER_daily = pd.DataFrame({'dekad': CGLS_FCOVER_ALL.index}, index=CGLS_FCOVER_ALL.index).asfreq('D')
                df_dekad = DMP_daily.bfill(axis='rows')

                df_Mz_m = pd.merge(df_Mz, CGLS_DMP, how='inner', left_index=True, right_index=True)
                df_Mz_m = pd.merge(df_Mz_m, CGLS_FCOVER_ALL, how='inner', left_index=True, right_index=True)
                df_Mz_m = df_Mz_m.dropna()

                # MAIZE - DROPPING WITH ESA WorldCereal CROP CALENDAR SOS-EOS VALUES (CropCalFunctions)
                # Here we retrieve the SOS (Start-of-Season) and EOS (End-of-Season) value from the WorldCereal tif. 
                # We feed it a location (AquaCrop grid) and GDAL extracts the value from that spatial location. 

                SOS_tiff_Path_Mz = '/data/leuven/361/vsc36151/data-jeun/WorldCereal/CropCalendars/M1_SOS_WGS84.tif'
                EOS_tiff_Path_Mz = '/data/leuven/361/vsc36151/data-jeun/WorldCereal/CropCalendars/M1_EOS_WGS84.tif'

                lat_CropCalendar = float(lat) # CropCalFunctions is written with GDAL which requires a "double" type value to run properly.
                lon_CropCalendar = float(lon) # Here, we simply make sure that the values are readable (i.e. float)

                # Save the DOY results in variables 
                Mz_SOS_DOY = extract_doy_from_tiff(SOS_tiff_Path_Mz, lat_CropCalendar, lon_CropCalendar) 
                Mz_EOS_DOY = extract_doy_from_tiff(EOS_tiff_Path_Mz, lat_CropCalendar, lon_CropCalendar)

                Drop_df_Mz_m = df_Mz_m.copy()
                # Convert index to DOY and add as a new column (will drop DOY ranges)
                Drop_df_Mz_m['DOY'] = Drop_df_Mz_m.index.strftime('%j').astype(int)
                mask_Mz = (Drop_df_Mz_m['DOY'] >= Mz_SOS_DOY) & (Drop_df_Mz_m['DOY'] <= Mz_EOS_DOY)
                Drop_df_Mz_m = Drop_df_Mz_m[mask_Mz]

                # Convert the index to datetime to easily extract the year
                Drop_df_Mz_m.index = pd.to_datetime(Drop_df_Mz_m.index, format='%d-%m-%Y')

                # Drop rows where the year is 2019 or 2020
                Drop_df_Mz_m = Drop_df_Mz_m[(Drop_df_Mz_m.index.year != 2019) & (Drop_df_Mz_m.index.year != 2020)]

                Drop_df_Mz_m = Drop_df_Mz_m.dropna(subset=['CGLS_DMP'])

                x_Mz_CC = Drop_df_Mz_m['CC']
                y_Mz_CC = Drop_df_Mz_m['CGLS_FCOVER']

                if len(x_Mz_CC) > 1 and len(y_Mz_CC) > 1:
                    correlation_value = pearson_r(x_Mz_CC, y_Mz_CC)
                    partial_result.append((CGLS_row, CGLS_col, correlation_value))
    return partial_result

def main():
    #args = [(row, col) for row in range(row_start, row_end + 1) for col in range(col_start, col_end + 1)]
    #relevant_coords = pd.read_csv('/data/leuven/361/vsc36151/data-jeun/AquaCrop/Continent_EU/AC_Grid_Mz_NoIT.csv')
    args = list(zip(relevant_coords['row'], relevant_coords['col']))
    with Pool(36) as pool:
        results = pool.map(calculate_metrics, args)

    # Aggregate results
    correlation_values_Mz_CC = np.full((len(lat_indices_global), len(lon_indices_global)), np.nan)
    for partial_result in results:
        if partial_result is not None:
            for (CGLS_row, CGLS_col, correlation_value) in partial_result:
                correlation_values_Mz_CC[CGLS_row - lat_indices_global[0], CGLS_col - lon_indices_global[0]] = correlation_value

    correlation_Mz_CC_da = xr.DataArray(correlation_values_Mz_CC,
                                        coords={'lat': DMP['lat'][lat_indices_global[0]:lat_indices_global[-1] + 1],
                                                'lon': DMP['lon'][lon_indices_global[0]:lon_indices_global[-1] + 1]},
                                        dims=['lat', 'lon'])

    # Maybe double check the 'correlation' label i.e. for things like bias and etc.
    correlation_Mz_CC_ds = xr.Dataset({'correlation': correlation_Mz_CC_da})
    correlation_Mz_CC_ds.to_netcdf('MapCorrelationMz_CC.nc')

if __name__ == "__main__":
    main()


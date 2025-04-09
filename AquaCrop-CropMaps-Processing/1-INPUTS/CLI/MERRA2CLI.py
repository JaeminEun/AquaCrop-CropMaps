# Jaemin Eun
# MERRA-2 to AquaCrop Climate Files

# This script is based off of Dr. Shannon De Roos' work, original file:
# '/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/src/execute_AC/LIS_MERRA_to_ACGUI.py'

# The function can be run on a single cell (i.e. hard code a numeric value for lat_id and lon_id),
# but more usefully, it is designed to be run programmatically in a "for" loop across a range of row and column values.

# 15-05-2024
# The script has been updated to ingest individual MERRA-2 AC files as opposed to the LIS SURFACEMODEL OUTPUT used 
# previously by Dr. Shannon de Roos. 

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import netCDF4 as nc
from netCDF4 import Dataset

def write_CLI_LIS(lat_id, lon_id, base_dir): #base_dir will be the INPUT directory

    start_date = '2022-01-01'
    end_date  = '2022-12-31'

    #name_fil = 'EU_' + str(lat_id) + '_'+ str(lon_id)
    name_fil = str(lat_id) + '_'+ str(lon_id)

    # Create directory based on lat_id and lon_id and the year range
    # The climate directories in the wrapper include a year range, and for now this is the range I want to use so 
    # I have hard coded the values
    start_year = 2022
    end_year = 2022   

    dir_out = os.path.join(base_dir, f'{name_fil}_{start_year}_{end_year}')
    os.makedirs(dir_out, exist_ok=True)  # Create directory if it doesn't exist

    # The LIS SURFACEMODEL output has been processed to the extent and dimensions of the AquaCrop grid we want to run.
    # We are simply using this grid to draw the location (lat, lon) based on the row/col setup of the wrapper.
    AC_Grid = '/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/SURFACEMODEL_tchunk.nc'
    # Open the netCDF file
    AC_LatLon = nc.Dataset(AC_Grid, 'r')

    # Get latitude and longitude variables
    lats_AC = AC_LatLon.variables['lat'][lat_id] #Replace these values with row col for AC loop
    lons_AC = AC_LatLon.variables['lon'][lon_id]

    # Loading in 1 of the MERRA2_AC files to again extract location details. 
    # The climate characteristics will be extracted for each AC row/col based on the larger MERRA-2 grid cells
    # which correspond to this location.
    MERRA2Grid = '/staging/leuven/stg_00024/input/met_forcing/MERRA2_land_forcing/MERRA2_AC/MERRA2_AC_20180101.nc'
    MERRA2_LatLon = nc.Dataset(MERRA2Grid, 'r')

    lats_MERRA2 = MERRA2_LatLon.variables['lat'][:]
    lons_MERRA2 = MERRA2_LatLon.variables['lon'][:]

    MERRA2_lat_index = (abs(lats_MERRA2 - lats_AC)).argmin()
    MERRA2_lon_index = (abs(lons_MERRA2 - lons_AC)).argmin()

    #Create DataFrames for data ouput
    date_s = datetime.strptime(start_date, '%Y-%m-%d').date()
    date_e = datetime.strptime(end_date, '%Y-%m-%d').date()
    TMP = pd.DataFrame(columns=['Tmin','Tmax'], index=pd.date_range(date_s, date_e))
    PLU = pd.DataFrame(columns=['PLU'], index=pd.date_range(date_s, date_e))
    ETo = pd.DataFrame(columns=['ETo'], index=pd.date_range(date_s, date_e))

    # Define the directory containing the NetCDF files
    nc_dir = '/staging/leuven/stg_00024/input/met_forcing/MERRA2_land_forcing/MERRA2_AC/'

    # Loop over each date in the range
    current_date = date_s
    while current_date <= date_e:
        # Construct the filename for the current date
        filename = f'MERRA2_AC_{current_date.strftime("%Y%m%d")}.nc'
        file_path = os.path.join(nc_dir, filename)

        # Check if the file exists
        if os.path.exists(file_path):
            # Open the NetCDF file
            with Dataset(file_path, 'r') as nc:
                # Extract the temperature data (Assuming it's a 2D array, adjust indices if necessary)
                try:
                    # nc['variable'][lat_id, lon_in].data
                    Tmin = nc['TMIN'][MERRA2_lat_index,MERRA2_lon_index].data
                    Tmax = nc['TMAX'][MERRA2_lat_index,MERRA2_lon_index].data
                    PREC = nc['PREC'][MERRA2_lat_index,MERRA2_lon_index].data
                    EVAP = nc['ETo'][MERRA2_lat_index,MERRA2_lon_index].data
                except KeyError:
                    print(f"Variable {var_min_temp} or {var_max_temp} not found in {filename}")
                    continue

                TMP.at[pd.Timestamp(current_date), 'Tmin'] = Tmin
                TMP.at[pd.Timestamp(current_date), 'Tmax'] = Tmax
                PLU.at[pd.Timestamp(current_date), 'PLU'] = PREC
                ETo.at[pd.Timestamp(current_date), 'ETo'] = EVAP
        else:
            print(f"File {file_path} does not exist")
    
        # Move to the next day
        current_date += timedelta(days=1)

    title = name_fil+'- daily data:' + start_date + ' to ' + end_date
    head_date= '\n'.join([title,
    '     ' + str(1)+ '  : Daily records (1=daily, 2=10-daily and 3=monthly data)',
    '     ' + str(date_s.day) + '  : First day of record (1, 11 or 21 for 10-day or 1 for months)',
    '     ' + str(date_s.month) + '  : First month of record',
    '  '+ str(date_s.year) + '  : First year of record (1901 if not linked to a specific year)'
    '\n'])

    hd_tmp ='''Tmin (C)   Tmax (C)
    ======================'''
    head_tmp='\n'.join([head_date, hd_tmp])
    tmp_fn = f'{name_fil}.Tnx'

    hd_prec=''' Total Rain (mm)
    ======================='''
    head_prec='\n'.join([head_date, hd_prec])
    prec_fn = f'{name_fil}.PLU'


    hd_ETo = '''  Average ETo (mm/day)
    ======================='''
    head_ETo = '\n'.join([head_date, hd_ETo])
    eto_fn = f'{name_fil}.ETo'

    #name_dir = 'GDD_AC_input'
    # Delimiter argument spaces output by 5 spaces for .TNX
    np.savetxt(os.path.join(dir_out, tmp_fn), TMP, fmt=('%3.1f', '%3.1f'), comments='', header=head_tmp, delimiter='\t')
    np.savetxt(os.path.join(dir_out, prec_fn), PLU, fmt='%3.1f', comments='', header= head_prec)
    np.savetxt(os.path.join(dir_out, eto_fn), ETo, fmt='%3.1f', comments='', header=head_ETo)

    #np.savetxt(dir_out + tmp_fn, TMP, fmt=('%3.1f', '%3.1f'), comments='', header=head_tmp, delimiter='\t') #Vincent Cal-Search searches for tabs.
    #np.savetxt(dir_out + tmp_fn, TMP, fmt=('%3.1f','%3.1f'), comments='', header= head_tmp, delimiter= '     ')
    #np.savetxt(dir_out  + prec_fn, PLU, fmt='%3.1f', comments='', header= head_prec)
    #np.savetxt(dir_out  + eto_fn, ETo, fmt='%3.1f', comments='', header=head_ETo)
    # Construct the .CLI file:
    climate_filename = os.path.join(dir_out, f'{name_fil}.CLI')
    with open(climate_filename, 'w') as climate_file:
        climate_file.write('\n'.join([
            title,
            ' 6.1   : AquaCrop Version (May 2018)',
            tmp_fn,
            eto_fn,
            prec_fn,
            'MaunaLoa.CO2'
        ]))

    #climate= (open(dir_out  + name_fil+'.CLI', 'w')).write('\n'.join([title,
    #                 ' 6.1   : AquaCrop Version (May 2018)',
    #                 tmp_fn,
    #                 eto_fn,
    #                 prec_fn,
    #                 'MaunaLoa.CO2']))

base_dir = '/data/leuven/361/vsc36151/data-jeun/AquaCrop/Continent_EU/Cli_Med_Brussels/'
#LIS  = Dataset('/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/SURFACEMODEL_tchunk.nc', 'r')
# Running the function programmatically across these ranges of row and column values
row_start = 317
row_end = 317
col_start = 307
col_end = 307

for lat_id in range (row_start, row_end + 1):
   for lon_id in range(col_start, col_end + 1):
      # Call write_CLI_LIS function for each combination of lat_id and lon_id
      write_CLI_LIS(lat_id, lon_id, base_dir)
      


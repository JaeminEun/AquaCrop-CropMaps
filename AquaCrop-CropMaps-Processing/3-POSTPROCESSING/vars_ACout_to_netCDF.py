import numpy as np
from datetime import date, timedelta
from matplotlib import dates
import pandas as pd
import os
from netCDF4 import Dataset
from acout_filestructure import ac_columns, ac_skiprows
from COORD_AC import AC_GEOREF2, mindist
import sys

crds = AC_GEOREF2()  # GEO_reference example

'''
Generates netCDF file from AquaCrop output.
@Louise Busschaert
'''

years = [2018, 2022]
run_name = 'Mz-GDD_2020Fert'  # Name of the netCDF file
vars = [
    'Biomass',
    'CC'
]
newfile = run_name + '_' + str(years[0]) + '-' + str(years[1])

row_start = 0
row_end = 700
rows = np.arange(row_start, row_end + 1)
col_start = 0
col_end = 920
cols = np.arange(col_start, col_end + 1)
dir_out = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/OUTPUT/'
dir_nc = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/'

long_names = {
    'Biomass': 'cummulative biomass production',
    'CC': 'canopy cover'
}
units = {
    'Biomass': 'ton/ha',
    'CC': '-'
}

lats = np.arange(crds.row_to_lat(row_start), crds.row_to_lat(row_end) + crds.step / 2, crds.step)
lons = np.arange(crds.col_to_lon(col_start), crds.col_to_lon(col_end) + crds.step / 2, crds.step)
Dates = np.arange(date(years[0], 1, 1), date(years[1] + 1, 1, 1), timedelta(days=1))
index = pd.DatetimeIndex(Dates)
times = dates.date2num(index.to_pydatetime()).astype('int32')
timeunit = 'days since ' + str(years[0]) + '-01-01 00:00'
times = times - times[0]

dims = (len(vars), len(times), len(lats), len(lons))
ts_data = np.full(dims, np.nan)

for row in rows:
    for col in cols:
        file_id = str(row) + '_' + str(col)
        path = os.path.join(dir_out, file_id, 'OUTP', f'{file_id}PRMday.OUT')

        if not os.path.exists(path):
            print(f"File not found: {path}", flush=True)
            continue

        if os.path.getsize(path) == 0:
            print(f"File is empty: {path}", flush=True)
            continue

        try:
            df = pd.read_csv(
                path, 
                encoding='cp1252',
                delim_whitespace=True, 
                skiprows=ac_skiprows(years[0], years[1]), 
                header=None,
                index_col=False
            ).replace({-9.9: 0, -9.00: 0., -9.000: 0, -900.0: 0})
        except Exception as e:
            print(f"Error reading file {path}: {e}", flush=True)
            continue

        df_len_cols = df.shape[1]
        df.columns = ac_columns(df_len_cols)

        for v, var in enumerate(vars):
            if var in df:
                ts_data[v, :, row, col] = df[var]

with Dataset(os.path.join(dir_nc, f'{newfile}.nc'), 'w', format="NETCDF4") as ds:
    ds.createDimension('lat', len(lats))
    ds.createDimension('lon', len(lons))
    ds.createDimension('time', len(times))

    ds.createVariable('time', 'float', dimensions='time', zlib=True)
    ds.createVariable('lat', 'float', dimensions='lat', zlib=True)
    ds.createVariable('lon', 'float', dimensions='lon', zlib=True)

    for v, var in enumerate(vars):
        ds.createVariable(var, 'float', dimensions=('time', 'lat', 'lon'), zlib=True)
        ds.variables[var][:] = ts_data[v, :, :, :]
        ds.variables[var].setncatts({'long_name': long_names[var], 'unit': units[var]})

    ds.variables['lat'][:] = lats
    ds.variables['lon'][:] = lons
    ds.variables['time'][:] = times
    ds.variables['time'].setncatts({'long_name': 'time', 'units': timeunit})

print('NetCDF file creation completed successfully.', flush=True)


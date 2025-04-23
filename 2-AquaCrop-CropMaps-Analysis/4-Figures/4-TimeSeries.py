# Jaemin Eun

import numpy as np
import pandas as pd
from datetime import date, timedelta
import xarray as xr
from matplotlib import pyplot as plt
from PIL import Image
from acout_filestructure import ac_columns, ac_skiprows
from CropCalFunctions import extract_doy_from_tiff

# Load datasets
GDD_ds = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/SURFACEMODEL_tchunk.nc')
lats = GDD_ds['lat'].values
lons = GDD_ds['lon'].values

DMP = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/Copernicus_DMP_300m/EU_DMP_300m_2018-2022.nc')
DMP_lats = DMP['lat'].values
DMP_lons = DMP['lon'].values

FCOVER_1 = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/Copernicus_FCOVER_300m/EU_FCOVER_300m_2018-01-10_to_2020-06-30.nc')
FCOVER_2 = xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/jaemine/Copernicus_FCOVER_300m/EU_FCOVER_300m_2020-07-10_to_2022-11-20.nc')

# Crop map TIFF
tif_path = '/data/leuven/361/vsc36151/VincentShare/UnionResample300mNearest.tif'
tif_image = Image.open(tif_path)
tif_array = np.array(tif_image)

# Define AquaCrop grid
row_start = 205
row_end = 205
col_start = 411
col_end = 411

# Directory paths
output_dir_GDD = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/OUTPUT/'
output_dir_Cal = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Cal-Crop/OUTPUT/'
output_dir_Mz = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Maize/Fert_2020/OUTPUT/'
output_dir_Mz_GDD = '/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/Mz-GDD/WC_FertCalib/OUTPUT/'

# Iterate over AquaCrop cells
for row in range(row_start, row_end + 1):
    for col in range(col_start, col_end + 1):
        name = f"{row}_{col}"
        lat, lon = lats[row], lons[col]

        # Determine indices for the current AquaCrop grid cell
        lat_indices = np.where((DMP_lats >= lat - 0.5) & (DMP_lats <= lat + 0.5))[0]
        lon_indices = np.where((DMP_lons >= lon - 0.5) & (DMP_lons <= lon + 0.5))[0]

        # Aggregated CGLS signals
        dmp_values = DMP['DMP'][:, lat_indices, lon_indices]
        fcover_values_1 = FCOVER_1['FCOVER'][:, lat_indices, lon_indices]
        fcover_values_2 = FCOVER_2['FCOVER'][:, lat_indices, lon_indices]

        CGLS_DMP_agg = pd.DataFrame({'time': DMP['time'].values, 'CGLS_DMP': np.nanmean(dmp_values, axis=(1, 2))}).set_index('time')
        FCOVER_combined = np.concatenate([np.nanmean(fcover_values_1, axis=(1, 2)), np.nanmean(fcover_values_2, axis=(1, 2))])
        time_combined = np.concatenate([FCOVER_1['time'].values, FCOVER_2['time'].values])
        CGLS_FCOVER_agg = pd.DataFrame({'time': time_combined, 'CGLS_FCOVER': FCOVER_combined}).set_index('time')

        # AquaCrop output files
        f_ac_GDD = f"{output_dir_GDD}{name}/OUTP/{name}PRMday.OUT"
        f_ac_Cal = f"{output_dir_Cal}{name}/OUTP/{name}PRMday.OUT"
        f_ac_Mz = f"{output_dir_Mz}{name}/OUTP/{name}PRMday.OUT"
        f_ac_Mz_GDD = f"{output_dir_Mz_GDD}{name}/OUTP/{name}PRMday.OUT"

        # Load AquaCrop outputs
        AC_out_GDD = pd.read_csv(
            f_ac_GDD,
            encoding='cp1252',
            delim_whitespace=True,
            skiprows=ac_skiprows(2018, 2022),
            header=None,
            index_col=False
        ).replace({-9.9: 0, -9.00: 0., -9.000: 0, -900.0: 0})
        AC_out_Cal = pd.read_csv(
            f_ac_Cal,
            encoding='cp1252',
            delim_whitespace=True,
            skiprows=ac_skiprows(2018, 2022),
            header=None,
            index_col=False
        ).replace({-9.9: 0, -9.00: 0., -9.000: 0, -900.0: 0})
        AC_out_Mz = pd.read_csv(
            f_ac_Mz,
            encoding='cp1252',
            delim_whitespace=True,
            skiprows=ac_skiprows(2018, 2022),
            header=None,
            index_col=False
        ).replace({-9.9: 0, -9.00: 0., -9.000: 0, -900.0: 0})
        AC_out_Mz_GDD = pd.read_csv(
            f_ac_Mz_GDD,
            encoding='cp1252',
            delim_whitespace=True,
            skiprows=ac_skiprows(2018, 2022),
            header=None,
            index_col=False
        ).replace({-9.9: 0, -9.00: 0., -9.000: 0, -900.0: 0})

        # Assign column names
        AC_out_GDD.columns = ac_columns(AC_out_GDD.shape[1])
        AC_out_Cal.columns = ac_columns(AC_out_Cal.shape[1])
        AC_out_Mz.columns = ac_columns(AC_out_Mz.shape[1])
        AC_out_Mz_GDD.columns = ac_columns(AC_out_Mz_GDD.shape[1])

        # Create DataFrames
        def create_df(data):
            return pd.DataFrame({
                'Year': data['Year'],
                'Month': data['Month'],
                'Day': data['Day'],
                'CC': data['CC'] / 100,
                'Biomass': data['Biomass'],
                'WC01': data['WC01']
            })

        df_GDD = create_df(AC_out_GDD)
        df_Cal = create_df(AC_out_Cal)
        df_Mz = create_df(AC_out_Mz)
        df_Mz_GDD = create_df(AC_out_Mz_GDD)

        # Format DataFrames
        for df in [df_Cal, df_GDD, df_Mz, df_Mz_GDD]:
            df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
            df.set_index('Date', inplace=True)
            df['B_diff'] = df['Biomass'].diff() * 1000
            df[df['B_diff'] < -1] = np.nan

        # Merge with aggregated CGLS data
        df_GDD_m = pd.merge(df_GDD, CGLS_DMP_agg, how='inner', left_index=True, right_index=True)
        df_GDD_m = pd.merge(df_GDD_m, CGLS_FCOVER_agg, how='inner', left_index=True, right_index=True)
        df_Cal_m = pd.merge(df_Cal, CGLS_DMP_agg, how='inner', left_index=True, right_index=True)
        df_Cal_m = pd.merge(df_Cal_m, CGLS_FCOVER_agg, how='inner', left_index=True, right_index=True)
        df_Mz_m = pd.merge(df_Mz, CGLS_DMP_agg, how='inner', left_index=True, right_index=True)
        df_Mz_m = pd.merge(df_Mz_m, CGLS_FCOVER_agg, how='inner', left_index=True, right_index=True)
        df_Mz_GDD_m = pd.merge(df_Mz_GDD, CGLS_DMP_agg, how='inner', left_index=True, right_index=True)
        df_Mz_GDD_m = pd.merge(df_Mz_GDD_m, CGLS_FCOVER_agg, how='inner', left_index=True, right_index=True)

        # Plot example for GDD DataFrame
        #plt.figure(figsize=(13, 4))
        ##plt.plot(df_Mz.index, df_Mz['B_diff'], color='gold', marker='.', label = "Maize-Cal")
        ##plt.plot(df_GDD.index, df_GDD['B_diff'], color='darkgreen', marker='.', label="Gen-GDD")
        ##plt.plot(df_Mz_GDD.index, df_Mz_GDD['B_diff'], color='tab:brown', marker='.', label = "Maize-GDD")
        #plt.plot(df_Mz.index, df_Mz['B_diff'], color='gold', label = "Maize-Cal")
        #plt.plot(df_GDD.index, df_GDD['B_diff'], color='darkgreen', label="Gen-GDD")
        #plt.plot(df_Mz_GDD.index, df_Mz_GDD['B_diff'], color='tab:brown', label = "Maize-GDD")
        #plt.plot(df_GDD_m.index, df_GDD_m['CGLS_DMP'], label="Aggregated CGLS DMP", color='lightsalmon')
        #plt.xlabel('Year')
        #plt.ylabel('Daily Biomass (kg ha$^{-1}$ day$^{-1}$)')
        #plt.title(f"Biomass Comparison (AC: {row}_{col})")
        #plt.legend()
        #plt.tight_layout()
        #plt.savefig(f'Biomass_Comparison_{row}_{col}_GDD.jpg', dpi=300)
        #plt.show()

        #plt.figure(figsize=(13, 4))
        ##plt.plot(df_Mz.index, df_Mz['B_diff'], color='gold', marker='.', label = "Maize-Cal")
        ##plt.plot(df_GDD.index, df_GDD['B_diff'], color='darkgreen', marker='.', label="Gen-GDD")
        ##plt.plot(df_Mz_GDD.index, df_Mz_GDD['B_diff'], color='tab:brown', marker='.', label = "Maize-GDD")
        #plt.plot(df_Mz.index, df_Mz['CC'], color='gold', label = "Maize-Cal")
        #plt.plot(df_GDD.index, df_GDD['CC'], color='darkgreen', label="Gen-GDD")
        #plt.plot(df_Mz_GDD.index, df_Mz_GDD['CC'], color='tab:brown',marker='.', label = "Maize-GDD")
        #plt.plot(df_GDD_m.index, df_GDD_m['CGLS_FCOVER'], label="Aggregated CGLS CC", color='lightsalmon')
        #plt.xlabel('Year')
        #plt.ylabel('Daily Biomass (kg ha$^{-1}$ day$^{-1}$)')
        #plt.title(f"Biomass Comparison (AC: {row}_{col})")
        #plt.legend()
        #plt.tight_layout()
        #plt.savefig(f'CC_Comparison_{row}_{col}_GDD.jpg', dpi=300)
        #plt.show()
        # Create a figure and subplots
        fig, axs = plt.subplots(2, 1, figsize=(13, 8), sharex=True)

        # Top: Generic Crops
        axs[0].plot(df_Mz.index, df_Cal['B_diff'], color='grey', label="Gen-Cal")
        axs[0].plot(df_Mz.index, df_GDD['B_diff'], color='darkgreen', label="Gen-GDD")
        #axs[0].plot(df_Mz_GDD.index, df_Mz_GDD['CC'], color='tab:brown', marker='.', label="Gen-GDD")
        axs[0].plot(df_Mz_m.index, df_Mz_m['CGLS_DMP'], label="CGLS DMP", color='lightsalmon')
        axs[0].set_xlabel('Year')
        axs[0].set_ylabel('Daily Biomass (kg ha$^{-1}$ day$^{-1}$)')
        axs[0].set_title("Generic Crop Biomass Comparison (9.57 E, 45.26 N)")
        axs[0].legend(loc='lower right')
        axs[0].grid(True)

        # First subplot: Biomass comparison
        axs[1].plot(df_Mz.index, df_Mz['B_diff'], color='gold', label="Maize-Cal")
        #axs[1].plot(df_GDD.index, df_GDD['B_diff'], color='darkgreen', label="Gen-GDD")
        axs[1].plot(df_Mz_GDD.index, df_Mz_GDD['B_diff'], color='tab:brown', label="Maize-GDD")
        axs[1].plot(df_Mz_m.index, df_Mz_m['CGLS_DMP'], label="CGLS DMP", color='lightsalmon')
        axs[1].set_ylabel('Daily Biomass (kg ha$^{-1}$ day$^{-1}$)')
        axs[1].set_title("Maize Biomass Comparison (9.57 E, 45.26 N)")
        axs[1].legend(loc='lower right')
        axs[1].grid(True)

        # Adjust layout
        plt.tight_layout()
        plt.savefig('BiomassComparison.png', dpi=400)
        plt.show()



#!/usr/bin/env python
import xarray as xr
import numpy as np
from netCDF4 import Dataset
import os
from multiprocessing import Pool

# dir_data is where we want to output the crop files for
dir_data = "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/GDD-Crop/INPUT/crop/"

# Defining the grid we want to extract soil information from.
row_start = 0
row_end = 700
col_start = 0
col_end = 920

netcdf_file = '/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/lis_input_EU.d01.nc'
nc = Dataset(netcdf_file, 'r')
# Get the Texture and LANDMASK variables
texture_var = nc.variables['TEXTURE']
landmask_var = nc.variables['LANDMASK']

# NOTE: Have to open the netcdf to read in the data (later in the function)
GDD_ds = xr.open_dataset("/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/phenology_VNP22C2_GDD_ALL_EU.nc")

def write_CRO_GDD(lat_id, lon_id, dir_data, GDD_ds):
    # Check if the .CRO file already exists
    #Sname = 'GDD_'+ str(lat_id)+ '_'+ str(lon_id) +'.CRO'
    #if os.path.exists(os.path.join(dir_data, Sname)):
    #    print(f"File {Sname} already exists. Skipping...")
    #    return
    '''------------------------------------------CROP PARAMETERS FOR CALIBRATION ---------------------------------'''

    #1.Water balance
    minR = 0.30
    maxR = 0.80
    WP =  17 #C3 crop

    #2.Crop development
    Kc = 1.1
    ageing = 0.1
    CCx = 0.85

    #--------related to CCo ! AquaCrop calculates CCo from Canopy size and plant density. CCo set here to 0.1
    CC_cov = 15.00
    CC_size= 15.00
    density= 666667
    CCo = round((density/10000)*(CC_size/10000),2)

    '''------------------------------------------READ IN GDD INFO--------------------------------------------------------'''

    # lat_id = 174   #122
    # lon_id  = 210   #118

    GDD_CCo= GDD_ds['GDD_onset_CCo'][:,lat_id, lon_id].median().values       #seperate medians or select "median year"?
    GDD_maturity = GDD_ds['GDD_offset_maturity'][:, lat_id, lon_id].median().values
    GDD_senescence =  GDD_ds['GDD_sen_CGC'][:, lat_id, lon_id].median().values
    GDD_maxR = 0.7*GDD_senescence

    GDD_to_50maxCC = GDD_ds['GDD_midGup'][:, lat_id, lon_id].median().values - GDD_CCo
    GDD_to_50declineCC  = GDD_ds['GDD_midsen'][:, lat_id, lon_id].median().values - GDD_senescence
    CGC = np.log((0.5*CCx)/CCo)/GDD_to_50maxCC
    CDC_factor = (((0.5*CCx)/CCx)-1.05)/-0.05
    CDC = (np.log(CDC_factor)*(CCx+2.29))/(3.33*GDD_to_50declineCC)

    if GDD_maturity >0 and GDD_CCo >0:
        '''------------------------------------------CROP--------------------------------------------------------'''

        firstline = 'Generic crop based on GDD days'
        Sname = 'GDD_'+ str(lat_id)+ '_'+ str(lon_id) +'.CRO'
        fid = open(dir_data  + Sname, 'w')

        cro_sow = 0
        mode =0 #0== GDD 1== calendar days
        cro_type = 1
        # write line coinciding with parameter value

        if cro_type == 2:
            type = ': fruit/grain producing crop\n'
        elif cro_type == 3:
            type = ': root tuber producing crop\n'
        elif cro_type == 1:
            type = ': leafy vegetable crop\n'

        if cro_sow == 0:
            sow = ': Crop is transplanted\n'
        elif cro_sow == 1:
            sow = ': Crop is sown\n'

        if mode == 0:
            gdd = ': Determination of crop cycle : by growing degree-days\n'
        elif mode == 1:
            gdd = ': Determination of crop cycle : by calendar days\n'

        fid.write(firstline + '\n')
        fid.write('\t %2.1f\t\t'%7.0   + ': AquaCrop Version (march 2017)\n')
        fid.write('\t %d\t\t'%1        + ': file not protected\n')
        fid.write('\t %d\t\t'%cro_type + type)
        fid.write('\t %d\t\t'%cro_sow  + sow)
        fid.write('\t %d\t\t'%mode     + gdd)
        fid.write('\t %d\t\t'%1        + ': Soil water depletion factors (p) are adjusted by ETo\n')
        fid.write('\t %3.1f\t\t'%5     + ': Base temperature (°C) below which crop development does not progress\n')
        fid.write('\t %4.1f\t\t'%30    + ': Upper temperature (°C) above which crop development no longer increases with an increase in temperature\n')
        fid.write('\t%d\t\t'% GDD_maturity+': Total length of crop cycle in growing degree-days\n')
        fid.write('\t %4.2f\t\t'%0.25  + ': Soil water depletion factor for canopy expansion (p-exp) - Upper threshold\n')
        fid.write('\t %4.2f\t\t'%0.55  + ': Soil water depletion factor for canopy expansion (p-exp) - Lower threshold\n')
        fid.write('\t %3.1f\t\t'%3     + ': Shape factor for water stress coefficient for canopy expansion (0.0 = straight line)\n')
        fid.write('\t %4.2f\t\t'%0.50  + ': Soil water depletion fraction for stomatal control (p - sto) - Upper threshold\n')
        fid.write('\t %3.1f\t\t'%3.0   + ': Shape factor for water stress coefficient for stomatal control (0.0 = straight line)\n')
        fid.write('\t %4.2f\t\t'%0.85  + ': Soil water depletion factor for canopy senescence (p - sen) - Upper threshold\n')
        fid.write('\t %3.1f\t\t'%3.0   + ': Shape factor for water stress coefficient for canopy senescence (0.0 = straight line)\n')
        fid.write('\t %d\t\t'%500      + ': Sum(ETo) during stress period to be exceeded before senescence is triggered\n')
        fid.write('\t %4.2f\t\t'%0.90  + ': Soil water depletion factor for pollination (p - pol) - Upper threshold\n')
        fid.write('\t %d\t\t'%5        + ': Volpct for Anaerobiotic point (* (SAT - [volpct]) at which deficient aeration occurs *)\n')
        fid.write('\t %d\t\t'%50       + ': Soil fertility stress at calibration (pct)\n')
        fid.write('\t %4.2f\t\t'%25.00 + ': Response of decline of canopy cover is not considered\n')
        fid.write('\t %4.2f\t\t'%25.00 + ': Response of decline of canopy cover is not considered\n')
        fid.write('\t %4.2f\t\t'%25.00 + ': Response of decline of canopy cover is not considered\n')
        fid.write('\t %4.2f\t\t'%25.00 + ': Response of decline of canopy cover is not considered\n')
        fid.write('\t %d\t\t'%-9       + ': dummy - Parameter no Longer required\n')
        fid.write('\t %d\t\t'%8        + ': Minimum air temperature below which pollination starts to fail (cold stress) (°C)\n')
        fid.write('\t %d\t\t'%40       + ': Maximum air temperature above which pollination starts to fail (heat stress) (°C)\n')
        fid.write('\t %3.1f\t\t'%10    + ': Minimum growing degrees required for full crop transpiration (°C - day)\n')
        fid.write('\t %d\t\t'%-9       + ': Electrical Conductivity of soil saturation extract at which crop starts to be affected by soil salinity (dS/m)\n')
        fid.write('\t %d\t\t'%-9       + ': Electrical Conductivity of soil saturation extract at which crop can no longer grow (dS/m)\n')
        fid.write('\t %d\t\t'%-9       + ': dummy - Parameter no Longer applicable\n')
        fid.write('\t %d\t\t'%25       + ': Calibrated distortion (%) of CC due to salinity stress (Range: 0 (none) to +100 (very strong))\n')
        fid.write('\t %d\t\t'%100       + ': Calibrated response (%) of stomata stress to ECsw (Range: 0 (none) to +200 (extreme))\n')
        fid.write('\t %4.2f\t\t'%Kc     + ': Crop coefficient when canopy is complete but prior to senescence (Kcb%x)\n')
        fid.write('\t %5.3f\t\t'%ageing + ': Decline of crop coefficient (pct/day) as a result of ageing% nitrogen deficiency% etc.\n')
        fid.write('\t %4.2f\t\t'%minR   + ': Minimum effective rooting depth (m)\n')
        fid.write('\t %4.2f\t\t'%maxR   + ': Maximum effective rooting depth (m)\n')
        fid.write('\t %d\t\t'%15        + ': Shape factor describing root zone expansion\n')
        fid.write('\t %5.3f\t\t'%0.048  + ': Maximum root water extraction (m3water/m3soil.day) in top quarter of root zone\n')
        fid.write('\t %5.3f\t\t'%0.012  + ': Maximum root water extraction (m3water/m3soil.day) in bottom quarter of root zone\n')
        fid.write('\t %d\t\t'%60        + ': Effect of canopy cover in reducing soil evaporation in late season stage\n')
        fid.write('\t %4.2f\t\t'%CC_cov  + ': Soil surface covered by an individual seedling at 90pct emergence (cm2)\n')
        fid.write('\t %4.2f\t\t'%CC_size     + ': Canopy size of individual plant (re-growth) at 1st day (cm2)\n')
        fid.write('\t %d\t\t'%density    + ': Number of plants per hectare\n')
        fid.write('\t %7.6f\t'%0.10368      + ': Canopy growth coefficient (CGC): Increase in canopy cover (fraction soil cover per day)\n')
        fid.write('\t %d\t\t'%-9        + ': Number of years at which CCx declines to 90 % of its value due to self-thinning - Not Applicable\n')
        fid.write('\t %4.2f\t\t'%-9     + ': Shape factor of the decline of CCx over the years due to self-thinning - Not Applicable\n')
        fid.write('\t %d\t\t'%-9        + ': dummy - Parameter no Longer required\n')
        fid.write('\t %4.2f\t\t'%CCx + ': Maximum canopy cover (CCx) in fraction soil cover\n')
        fid.write('\t %7.6f\t'%0.08000 + ': Canopy decline coefficient (CDC): Decrease in canopy cover (in fraction per day)\n')
        fid.write('\t %d\t\t'%2 + ': Calendar Days: from sowing to emergence\n')
        fid.write('\t %d\t\t'%80 + ': Calendar Days: from sowing to maximum rooting depth\n')
        fid.write('\t %d\t\t'%232 + ': Calendar Days: from sowing to start senescence\n')
        fid.write('\t %d\t\t'%360 + ':  Calendar Days: from sowing to maturity (length of crop cycle)\n')
        fid.write('\t %d\t\t'%0 + ': Calendar Days: from sowing to flowering\n')
        fid.write('\t %d\t\t'%0 + ': Length of the flowering stage (days)\n')
        fid.write('\t %d\t\t'%0 + ': Crop determinancy unlinked with flowering\n')
        fid.write('\t %d\t\t'%-9 + ': parameter NO LONGER required\n')
        fid.write('\t %d\t\t'%36 + ': Building up of Harvest Index starting at sowing/transplanting (days)\n')
        fid.write('\t %4.1f\t\t'%WP + ': Water Productivity normalized for ETo and CO2 (WP*) (gram/m2)\n')
        fid.write('\t %d\t\t'%100 + ': Water Productivity normalized for ETo and CO2 during yield formation (as pct WP*)\n')
        fid.write('\t %2.0f\t\t'%50 + ': Crop performance under elevated atmospheric CO2 concentration (%)\n')
        fid.write('\t %2.0f\t\t'%85 + ': Reference Harvest Index (HIo) (pct)\n')
        fid.write('\t %d\t\t'%-9 + ': Possible increase (pct) of HI due to water stress before flowering\n')
        fid.write('\t %3.1f\t\t'%-9.0 + ': No impact on HI of restricted vegetative growth during yield formation \n')
        fid.write('\t %3.1f\t\t'%-9.0+ ': No effect on HI of stomatal closure during yield formation\n')
        fid.write('\t %d\t\t'%-9 + ': Allowable maximum increase (pct) of specified HI\n')
        fid.write('\t %d\t\t'%GDD_CCo + ': GDDays: from transplanting to recovered transplant\n')
        fid.write('\t %d\t\t'%GDD_maxR + ': GDDays: from sowing to maximum rooting depth\n')
        fid.write('\t %d\t\t'%GDD_senescence + ': GDDays: from sowing to start senescence\n')
        fid.write('\t %d\t\t'%GDD_maturity + ': GDDays: from sowing to maturity (length of crop cycle)\n')
        fid.write('\t %d\t\t'%0 + ': GDDays: from sowing to flowering\n')
        fid.write('\t %d\t\t'%0 + ': Length of the flowering stage (growing degree days)\n')
        fid.write('\t %7.6f\t'%CGC + ': CGC for GGDays: Increase in canopy cover (in fraction soil cover per growing-degree day)\n')
        fid.write('\t %7.6f\t'%CDC + ': CDC for GGDays: Decrease in canopy cover (in fraction per growing-degree day)\n')
        fid.write('\t %d\t\t'%140 + ': GDDays: building-up of Harvest Index during yield formation\n')
        fid.write('\t %d\t\t'%10 + ': dry matter content (%) of fresh yield\n')
        fid.write('\t %d\t\t'%0.3 + 'Minimum effective rooting depth (m) in first year - required only in case of regrowth\n')
        fid.write('\t %d\t\t'%0 + ': Crop is transplanted in 1st year - required only in case of regrowth\n')
        fid.write('\t %d\t\t'%0 + ': Transfer of assimilates from above ground parts to root system is NOT considered\n')
        fid.write('\t %d\t\t'%0 + ': Number of days at end of season during which assimilates are stored in root system\n')
        fid.write('\t %d\t\t'%0 + ': Percentage of assimilates transferred to root system at last day of season\n')
        fid.write('\t %d\t\t'%0 + ': Percentage of stored assimilates transferred to above ground parts in next season\n')

        fid.close()

def process_grid_point(grid_point):
    lat_id, lon_id = grid_point
    soil_direc = "/staging/leuven/stg_00024/OUTPUT/jaemine/LIS-Wrapper-GDD/MERRA-Grid/soil/"
    fname = str(lat_id) + '_' + str(lon_id)
    if os.path.exists(soil_direc + fname + '.SOL'):  # To run only for pixel
        write_CRO_GDD(lat_id, lon_id, dir_data, GDD_ds)
    else:
        print('Skip ' + fname)

if __name__ == "__main__":
    # Generate the grid points to process
    grid_points = [(lat_id, lon_id) for lat_id in range(row_start, row_end + 1)
                                    for lon_id in range(col_start, col_end + 1)]
    
    # Use multiprocessing to parallelize the grid processing
    with Pool(processes=36) as pool:
        pool.map(process_grid_point, grid_points)


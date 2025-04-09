#!/usr/bin/env python
import numpy as np
import os
from datetime import datetime
from CropCalFunctions import extract_doy_from_tiff
from datetime import datetime, timedelta
import xarray as xr

'''---------------------------------------------------------------------------------------------------------------------
This script creates a Project Management File as input for AquaCrop, containing the information of CLI, SOL, CRO & MAN.
It has to be executed before AquaCrop is executed.
@ Shannon de Roos 2020: original author, for AquaCropV6.1
@ Louise Busschaert 2023: simplified and adapted for AquaCropV7 and higher
 -----------------------------------------------------------------------------------------------------------------------'''

def run_ac_pro_yrs(row, col, dir_out, DirSoil, DirCli, DirCrop, DirSupfiles, start_year, end_year):
    nan = 'nan'
    locs = str(row) + '_' + str(col)
    Dirsupfiles= '   "' + DirSupfiles + '"\n'
    DirCrop = '   "' + DirCrop + '"\n'
    MANfile = 'SFR30' # or nan
    IRRfile = 'nan' # or nan
    CROfile = 'MaizeCal' # Define crop file
    fname = locs
    fsoil = locs
    Dirnew = dir_out + fname +'/'

    WC_adjustment = 24 #WC SOS is defined as 30 days before emergence. This factor must be subtracted from the AC crop file emergence window.
    
    # For Maize, we want to feed the SOS value into the growing period.
    GDD_ds =  xr.open_dataset('/staging/leuven/stg_00024/OUTPUT/shannondr/GDD/GDD_DATA/datasets/SURFACEMODEL_tchunk.nc')
    lats = GDD_ds['lat'].values
    lons=  GDD_ds['lon'].values
    lat, lon = lats[row], lons[col]

    SOS_tiff_Path_Mz = '/data/leuven/361/vsc36151/data-jeun/WorldCereal/CropCalendars/M1_SOS_WGS84.tif'
    #EOS_tiff_Path_Mz = '/data/leuven/361/vsc36151/data-jeun/WorldCereal/CropCalendars/M1_EOS_WGS84.tif'
    lat_CropCalendar = float(lat) # CropCalFunctions is written with GDAL which requires a "double" type value to run properly.
    lon_CropCalendar = float(lon) # Here, we simply make sure that the values are readable (i.e. float)

    # Save the DOY results in variables 
    Mz_SOS_DOY = extract_doy_from_tiff(SOS_tiff_Path_Mz, lat_CropCalendar, lon_CropCalendar)
    #Mz_EOS_DOY = extract_doy_from_tiff(EOS_tiff_Path_Mz, lat_CropCalendar, lon_CropCalendar)

    # Initializing an empty list to store the dates to pass into the growing period 
    dates_list = []

    for year in range(start_year, end_year + 1):
        # Add days to offset the WorldCereal SOS definition with the crop file "emergence" window.
        adjusted_DOY = Mz_SOS_DOY + WC_adjustment
        # Construct the date string in format 'YYYY-MM-DD'
        date_string = datetime(year, 1, 1) + timedelta(days=Mz_SOS_DOY - 1)
        date_string = date_string.strftime('%Y-%m-%d')
        dates_list.append(date_string)

    if os.path.exists(DirSoil + fsoil + '.SOL'):
        # Only prepares PRM files if the soil file exists
        print(locs, 'Prepare PRM file')

        # Find correct climate file:
        cliname = locs
        #Huge bug we have to fix, there was a hyphen that's supposed to be an underscore 
        Dir_cli = DirCli + cliname + '_' + str(start_year) + '_' + str(end_year) + '/'

        '''------------------------------------------PROJECT FILE-------------------------------------------------------'''

        fid = open(Dirnew + 'LIST/' + fname + '.PRM', 'w')

        #------------------------------years cropping and simulation periods---------------------------------------------------------------#
        # Start at 1 Jan

        years = np.arange(start_year, end_year + 1)
        sim_s = []
        for i in np.arange(len(years)):
            sim_s.append(str(years[i])+'-01-01')

        sim_e = []
        for i in np.arange(len(years)):
            sim_e.append(str(years[i])+'-12-31')

        crop_s = dates_list # Changing the start of the growing period
        crop_e = sim_e


        #--------------------------------------------------file-input--------------------------------------------------------------#
        syears = len(sim_s)

        '''file for each year in successive order'''
        name_cal = [nan] * syears
        name_crop = [CROfile] * syears
        name_irr = [IRRfile] * syears
        name_man = [MANfile] * syears
        name_gwt = [nan] * syears
        name_sw0 = [nan] * syears
        name_off = [nan] * syears
        name_field = [nan] * syears

        #-------------------------------------------------------------------------------------------------------------------------#

        fid.write(locs + ' Project file\n')
        fid.write('\t 7.1\t' + '\t: AquaCrop Version (August 2023)\n')

        #------------------------------convert dates to day numbers---------------------------------------------------------------#
        list = [sim_s[0], sim_e[0], crop_s[0], crop_e[0]]
        day = []
        for i in list:
            strip = datetime.strptime(i, '%Y-%m-%d')
            month = [0, 0, 31, 59.25, 90.25, 120.25, 151.25, 181.25, 212.25, 243.25, 273.25, 304.25, 334.25]
            daynmr = int((strip.year - 1901) * 365.25 + month[strip.month] + strip.day)
            day.append(daynmr)

        SDsim = day[0]          #first day of simulation period
        EDsim = day[1]          #last day of simulation period
        SDcrop = day[2]         #first day of cropping period
        EDcrop = day[3]         #last day of cropping period


        #---------------------------------------write Project file-------------------------------------------------------------------------#
        fid.write('\t 1\n')
        fid.write('\t %d\t'%SDsim + '\t: First day of simulation period  - ' + sim_s[0] + '\n')
        fid.write('\t %d\t'%EDsim + '\t: Last day of simulation period  - ' + sim_e[0] + '\n')
        fid.write('\t %d\t'%SDcrop + '\t: First day of cropping period  - ' + crop_s[0] + '\n')
        fid.write('\t %d\t'%EDcrop + '\t: Last day of cropping period  - ' + crop_e[0] + '\n')

        CLI= ['-- 1. Climate (CLI) file\n',
             '   ' + cliname + '.CLI\n'
             '   ' + '"' + Dir_cli + '"' + '\n'
             '   1.1 Temperature (TNx or TMP) file\n'
             '   ' + cliname + '.Tnx\n'
             '   ' + '"' + Dir_cli + '"' + '\n'
             '   1.2 Reference ET (ETo) file\n'
             '   ' + cliname + '.ETo\n'
             '   ' + '"' + Dir_cli + '"' + '\n'
             '   1.3 Rain (PLU) file\n'
             '   ' + cliname + '.PLU\n'
             '   ' + '"' + Dir_cli + '"' + '\n'
             '   1.4 Atmospheric CO2 concentration (CO2) file\n'
             '   MaunaLoa.CO2\n'
             '   ' + '"' + Dirnew + 'SIMUL/' + '"' + '\n' ]
        fid.writelines(CLI)

        if name_cal[0] == nan:
            calfile = '   (None)\n'
            caldir = '   (None)\n'
        else:
            calfile = '   '+ name_cal[0] + '.CAL\n'
            caldir = Dirsupfiles
        CAL = ['-- 2. Calendar file\n',
              calfile,
              caldir]
        fid.writelines(CAL)

        CROP= ['-- 3. CROP (CRO) file\n',
              '   ' + name_crop[0] + '.CRO\n',
               DirCrop]
        fid.writelines(CROP)

        if name_irr[0] == nan:
            irrfile = '   (None)\n'
            irrdir = '   (None)\n'
        else:
            print('IRR in PRM')
            irrfile = '   ' + name_irr[0] + '.IRR\n'
            irrdir = Dirsupfiles
        IRR = ['-- 4. Irrigation management (IRR) file\n',
              irrfile,
              irrdir]
        fid.writelines(IRR)

        if name_man[0] == nan:
            manfile = '   (None)\n'
            mandir = '   (None)\n'
        else:
            print('MAN in PRM')
            manfile = '   ' + name_man[0] + '.MAN\n'
            mandir = Dirsupfiles
        MAN = ['-- 5. Field management (MAN) file\n',
              manfile,
              mandir]
        fid.writelines(MAN)

        SOL = ['-- 6. Soil profile (SOL) file\n',
              '   ' + fsoil + '.SOL\n',
              '   "' + DirSoil + '"\n']
        fid.writelines(SOL)

        if name_gwt[0] == nan:
            gwtfile = '   (None)\n'
            gwtdir = '   (None)\n'
        else:
            gwtfile = '   '+ name_gwt[0] + '.GWT\n'
            gwtdir = Dirsupfiles
        GWT = ['-- 7. Groundwater table (GWT) file\n',
              gwtfile,
              gwtdir]
        fid.writelines(GWT)

        if name_sw0[0] == nan:
            inifile = '   (None)\n'
            inidir = '   (None)\n'
        else:
            inifile = '   '+ name_sw0[0] + '.SW0\n'
            inidir = Dirsupfiles
        INI = ['-- 8. Initial conditions (SW0) file\n',
              inifile,
              inidir]
        fid.writelines(INI)

        if name_off[0] == nan:
            offfile = '   (None)\n'
            offdir = '   (None)\n'
        else:
            offfile = '   '+ name_off[0] + '.OFF\n'
            offdir = Dirsupfiles
        OFF = ['-- 9. Off-season conditions (OFF) file\n',
              offfile,
              offdir]
        fid.writelines(OFF)

        if name_field[0] == nan:
            fieldfile = '   (None)\n'
            fielddir = '   (None)\n'
        else:
            fieldfile = '   ' + name_field[0] + '.OBS\n'
            fielddir = Dirsupfiles
        FIELD = ['-- 10. Field data (OBS) file\n',
              fieldfile,
              fielddir]
        fid.writelines(FIELD)


        ''' =====================================
        ============= Successive years ==========
        ========================================='''
        if syears > 0:
            for syear in range(syears):
                if syear > 0:
                    n = syear
                    list = [sim_s[n], sim_e[n], crop_s[n], crop_e[n]]
                    day = []
                    for i in list:
                        strip = datetime.strptime(i, '%Y-%m-%d')
                        month = [0, 0, 31, 59.25, 90.25, 120.25, 151.25, 181.25, 212.25, 243.25, 273.25, 304.25, 334.25]
                        daynmr = int((strip.year - 1901) * 365.25 + month[strip.month] + strip.day)
                        day.append(daynmr)

                    SDsim = day[0]      #first day of simulation period
                    EDsim = day[1]      #last day of simulation period'
                    SDcrop = day[2]     #first day of cropping period
                    EDcrop = day[3]     #last day of cropping period


                    simul = ['  1\n',
                    '  %d  '%SDsim + '         : First day of simulation period  - '+sim_s[n]+ '\n',
                    '  %d  '%EDsim + '         : Last day of simulation period  - '+sim_e[n]+ '\n',
                    '  %d  '%SDcrop + '         : First day of cropping period  - '+crop_s[n]+ '\n',
                    '  %d  '%EDcrop + '         : Last day of cropping period  - '+crop_e[n]+ '\n']
                    fid.writelines(simul)
                    fid.writelines(CLI)

                    if name_cal[n] == nan:
                        calfile = '   (None)\n'
                        caldir = '   (None)\n'
                    else:
                        calfile = '   ' + name_cal[n] + '.CAL\n'
                        caldir = '"' + Dirsupfiles + '"'
                    CAL = ['-- 2. Calendar file\n',
                           calfile,
                           caldir]
                    fid.writelines(CAL)

                    CROP = ['-- 3. CROP (CRO) file\n',
                            '   ' + name_crop[n] + '.CRO\n',
                            DirCrop]
                    fid.writelines(CROP)

                    if name_irr[n] == nan:
                        irrfile = '   (None)\n'
                        irrdir = '   (None)\n'
                    else:
                        irrfile = '   ' + name_irr[n] + '.IRR\n'
                        irrdir = Dirsupfiles
                    IRR = ['-- 4. Irrigation management (IRR) file\n',
                           irrfile,
                           irrdir]
                    fid.writelines(IRR)

                    if name_man[n] == nan:
                        manfile = '   (None)\n'
                        mandir = '   (None)\n'
                    else:
                        manfile = '   ' + name_man[n] + '.MAN\n'
                        mandir = Dirsupfiles
                    MAN = ['-- 5. Field management (MAN) file\n',
                           manfile,
                           mandir]
                    fid.writelines(MAN)

                    SOL = ['-- 6. Soil profile (SOL) file\n',
                           '   ' + fsoil + '.SOL\n',
                           '   "' + DirSoil + '"\n']
                    fid.writelines(SOL)

                    if name_gwt[n] == nan:
                        gwtfile = '   (None)\n'
                        gwtdir = '   (None)\n'
                    else:
                        gwtfile = '   ' + name_gwt[n] + '.GWT\n'
                        gwtdir = Dirsupfiles
                    GWT = ['-- 7. Groundwater table (GWT) file\n',
                           gwtfile,
                           gwtdir]
                    fid.writelines(GWT)

                    INI = ['-- 8. Initial conditions (SW0) file\n',
                           '   KeepSWC\n'
                           '   Keep soil water profile of previous run\n']
                    fid.writelines(INI)

                    if name_off[n] == nan:
                        offfile = '   (None)\n'
                        offdir = '   (None)\n'
                    else:
                        offfile = '   ' + name_off[n] + '.OFF\n'
                        offdir = Dirsupfiles
                    OFF = ['-- 9. Off-season conditions (OFF) file\n',
                           offfile,
                           offdir]
                    fid.writelines(OFF)

                    if name_field[n] == nan:
                        fieldfile = '   (None)\n'
                        fielddir = '   (None)\n'
                    else:
                        fieldfile = '   ' + name_field[n] + '.OBS\n'
                        fielddir = Dirsupfiles
                    FIELD = ['-- 10. Field data (OBS) file\n',
                             fieldfile,
                             fielddir]
                    fid.writelines(FIELD)
            fid.writelines('\n')

        fid.close()
    else:
        print('no soil file')
        pass

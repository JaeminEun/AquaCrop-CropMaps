<img src="https://github.com/user-attachments/assets/26282e47-c12c-4077-b605-96096071e9c4" alt="KU Leuven logo" width="200"/>

# CGLS Evaluation Data Proprocessing Steps

FCOVER datasets from the CGLS (Copernicus Global Land Service) do not come with native time records.
The following assets contain a mix of python and shell scripts (utilizing NCO) to subset data to user specified locations
and combining files through date information extracted from the file naming format. The following steps give an overview of the process:

1. Obtain data urls from the Copernicus API 
   - Query data and export url links from dataframe to txt file
   - **Python script: CGLS_catalogue_and_download_demo.py)** 

2. Download data from txt file links:
   - Simple: wget -i links.txt
   - Fast: Concurrent downloads with multiprocessing (script provided: **concurrent_download.py**)
        - Distributes downloads across HPC (36 files i.e. processors downloaded at the same time)

3. Subset spatial domain:
     - FCOVER individual files are for entire globe.
     - Use NCO ncks to subset to Europe (shell script: **ncks_subsetFCOVER.sh**)

4. Combine individual subsetted netcdf files together:
     - "module load NCO/5.0.1-foss-2021a"
     - **"ncecat -u time in\*.nc out.nc"**
         - Combined netcdf now has time dimension but not in date format. Look at the next step to build date info.

5. Build date info:
     - FCOVER does not include timestamps within the NetCDF (DMP does not have this problem)
     - From previous step, the new time dimension is listed sequentially i.e. 1, 2, 3, etc.
     - To build date info, dates are extracted using the individual file names
     - Python script: **ExtractTime.py** (Converts dates to number of days since 01/01/1970)
         - Dates saved as text file
     - NCO Command: **ncap2 -O -s 'time[time]={1,2,3,etc.\*copy_and_paste_dates_from_text_file_here}' out.nc out.nc**

6. Build date units:
     - NCO Command: **ncatted -a units,time,o,c,"days since 1970-01-01 00:00:00"**

7. Chunk NetCDF:
     - Shell script: **chunk.sh**




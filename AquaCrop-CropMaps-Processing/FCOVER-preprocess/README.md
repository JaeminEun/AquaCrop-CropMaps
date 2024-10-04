# FCOVER Proprocessing Steps

FCOVER datasets from the CGLS (Copernicus Global Land Service) do not come with native time records.
The following assets contain a mix of python and shell scripts (utilizing NCO) to subset data to user specified locations
and combining files through date information extracted from the file naming format. The following steps give an overview of the process:

1. Obtain data urls from the Copernicus API 
**Python script: CGLS_catalogue_and_download_demo.py)**
- Query data and export url links from dataframe to txt file
 



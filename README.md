<div style="float: right; text-align: right; margin-top: -80px;">
  <img src="https://github.com/user-attachments/assets/26282e47-c12c-4077-b605-96096071e9c4" alt="KU Leuven logo" width="200"/><br/>
</div>

# Enhancing AquaCrop Simulations with Crop Maps and Calendars: A Continental-Scale Modelling Approach for Europe

## AquaCrop Setup

## Data for AquaCrop with crop maps and calendars
1. Crop maps: Maize, Spring Wheat, and Winter Wheat locations combined for 2018, 2021, and 2022 from ESA WorldCereal 
([Van Tricht et al., 2023](https://doi.org/10.5194/essd-15-5491-2023)) and EUCROPMAP 
([d'Andrimont et al., 2021](https://doi.org/10.1016/j.rse.2021.112708)).
2. Crop calendars ([Franch et al., 2022](https://doi.org/10.1080/15481603.2022.2079273))
3. CLI climate files: Climate characteristics derived from MERRA-2 ([NASA GMAO](https://doi.org/10.5067/VJAFPLI1CSIV)) implemented
from spatial AquaCrop processing following [de Roos et al., 2021](https://doi.org/10.5194/gmd-14-7309-2021) and 
[Busschaert et al., 2022](https://doi.org/10.5194/hess-26-3731-2022).
4. SOL soil files: Soil characteristics derived from HWSD v1.2 ([Fischer et al., 2008](https://doi.org/10.1002/2014MS000330)) 
with soil hydraulic properties linked to mineral soil texture and organic matter
via pedo-transfer functions described in [de Lannoy et al., 2014](https://doi.org/10.1002/2014MS000330).
5. CRO files: Crop parameters derived from default AquaCrop crop files ([Raes et al., 2017](http://www.fao.org/nr/water/aquacrop.html))
and calibrated across Europe following processes similarly described in "Vincent's Paper".

## Data Structure (HPC)
There are 3 main data sources that are housed in the following path:`/staging/leuven/stg_00024/OUTPUT/jaemine/Data`
1. Copernicus_DMP_300m: For validation of biomass (the processing is documented in more detail in the "Analysis" portion of this repository).
2. Copernicus_FCOVER_300m: For validation of canopy cover (the processing is documented in more detail in the "Analysis" portion of this repository).
3. CropMaps: Contains assets used to create the 300-m crop maps used to match the resolution of the Copernicus (CGLS) evaluation data.
- List... 

## Author
Jaemin Eun



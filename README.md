<p style="text-align: right;">
  <img src="https://github.com/user-attachments/assets/26282e47-c12c-4077-b605-96096071e9c4" alt="KU Leuven logo" width="200"/><br/>
  <img src="https://github.com/user-attachments/assets/16f6e334-aa18-4c72-9882-ca82fc49e649" alt="BELSPO" width="200"/>
</p>

# Enhancing AquaCrop Simulations with Crop Maps and Calendars: A Continental-Scale Modelling Approach for Europe

This repository contains the crop map and crop calendar implementation for AquaCrop simulations used in *[Eun et al., 2025]*.

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
and calibrated across Europe following processes similarly described in *([insert Vincent's paper here])*.

## AquaCrop simulation performance analysis
1. Validation metric calculation
2. Spatial boxplots
3. Anomaly correlation

## Data availability 
The data required to produce the AquaCrop set up with crop maps and crop calendars are accesible at the following (*[Insert Zenodo Here]*)

## Version
Version 1.0, October 2024

## Author
Jaemin Eun

## References
*[Insert DOI to article here]*
